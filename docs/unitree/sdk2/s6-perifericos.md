# S6: Periféricos y Actuadores — Manos, Audio, Visión y Control Remoto

## Objetivos

- Acceder a cámaras RGB y de profundidad del B2 vía SDK2
- Controlar el sistema de audio del robot (altavoces, micrófono)
- Programar las manos dextras del H1-2 usando `HandClient`
- Leer el estado del mando a distancia (`wirelesscontroller`)

---

## Periféricos del B2 vs H1-2

| Periférico               | B2                              | H1-2                            |
|--------------------------|---------------------------------|---------------------------------|
| Cámara RGB frontal       | ✅ Intel RealSense D435i         | ✅ Intel RealSense D435i         |
| Cámara de profundidad    | ✅ D435i depth                   | ✅ D435i depth                   |
| LiDAR 3D                 | ✅ Hesai AT128 (128 planos)       | ❌ (IMU + cámera solo)           |
| Audio (altavoz/micro)    | ✅ Buzzer + micro integrado       | ✅ Array de micrófonos           |
| Manos dextras            | ❌ No tiene                      | ✅ Dexterous Hand (5 dedos)      |
| IMU                      | ✅ 6-DoF                         | ✅ 6-DoF                         |
| Mando a distancia        | ✅ Joystick Unitree              | ✅ Joystick Unitree              |
| Batería removible        | ❌ Integrada                     | ✅ Hot-swap                      |

---

## Cámara RGB: acceso via SDK2

El B2 expone la cámara como un publicador DDS. Desde ROS 2 también está disponible en `/camera/image_raw`.

```python title="s6_camara.py"
#!/usr/bin/env python3
"""Captura imágenes de la cámara RGB del B2 / sim_lite."""
import cv2
import numpy as np
import rclpy
from rclpy.node import Node
from sensor_msgs.msg import Image
from cv_bridge import CvBridge

class CameraCapture(Node):
    def __init__(self):
        super().__init__("camera_capture")
        self.bridge = CvBridge()
        self.latest = None
        self.create_subscription(Image, "/camera/image_raw",
                                 self._cb, 10)  # (1)!

    def _cb(self, msg: Image):
        self.latest = self.bridge.imgmsg_to_cv2(msg, "bgr8")

    def save_frame(self, path: str):
        if self.latest is not None:
            cv2.imwrite(path, self.latest)
            self.get_logger().info(f"Guardado: {path}")
            return True
        return False

def main():
    rclpy.init()
    node = CameraCapture()

    # Capturar 3 imágenes a intervalos de 1 s
    for i in range(3):
        rclpy.spin_once(node, timeout_sec=0.2)
        node.save_frame(f"/tmp/frame_{i:02d}.jpg")
        import time; time.sleep(1.0)

    node.destroy_node()
    rclpy.shutdown()
```

1. `/camera/image_raw` — disponible tanto en sim_lite como en el bridge ROS 2 del B2 real

### Cámara de profundidad (solo robot real)

```python
# Tópico de profundidad (requiere bridge ROS 2 activo en el B2)
# /camera/depth/image_rect_raw  → sensor_msgs/Image (16UC1, en mm)
# /camera/depth/points          → sensor_msgs/PointCloud2

from sensor_msgs.msg import PointCloud2
# Procesar con open3d o pcl_ros para nube de puntos 3D
```

---

## Audio: altavoz y pitidos

```python title="s6_audio.py"
#!/usr/bin/env python3
"""Control del sistema de audio del B2."""
import time

# SDK2 real — emitir pitido de aviso
# from unitree_sdk2py.b2.sport_client import SportClient
# sport = SportClient(); sport.Init()
# sport.PlaySound(1)   # 1 = pitido corto, 2 = pitido largo, 3 = alarma

from sdk2_bridge_sim import SDK2Bridge
bridge = SDK2Bridge()
import rclpy; rclpy.init()

# Simular: el bridge simplemente imprime en log
print("Audio: pitido corto (sim)")
bridge.play_sound(1)  # (1)!
time.sleep(0.5)
print("Audio: alarma (sim)")
bridge.play_sound(3)

bridge.destroy()
rclpy.shutdown()
```

1. En robot real: `sport.PlaySound(1)` emite un pitido físico — útil para notificaciones

---

## Manos dextras del H1-2 (HandClient)

!!! info "Solo disponible en H1-2"
    Las Dexterous Hands del H1-2 tienen 5 dedos con 6 DoF cada uno (30 DoF totales). Se controlan via `HandClient` del SDK2 — no disponible para el B2.

```python title="s6_hand_h12.py"
#!/usr/bin/env python3
"""Control de manos dextras del H1-2 via SDK2."""

# NOTA: Este script solo funciona en H1-2 físico.
# Para simulación, ver ros2-b2/s6-simulacion.md.

# Robot real (H1-2):
# from unitree_sdk2py.h1.hand_client import HandClient
# hand = HandClient()
# hand.Init()

# Abrir mano derecha completamente
# hand.SetDexHandPos("right", [0.0] * 6)  # 0.0 = abierto

# Cerrar mano derecha (agarre de potencia)
# GRIP_CLOSED = [1.5, 1.5, 1.5, 1.5, 1.5, 0.8]
# hand.SetDexHandPos("right", GRIP_CLOSED)

# Pinch (pulgar + índice)
# PINCH = [1.5, 1.5, 0.0, 0.0, 0.0, 1.5]
# hand.SetDexHandPos("right", PINCH)

print("HandClient disponible cuando el H1-2 esté en el laboratorio.")
print("Consulta la documentación de SDK2 para los rangos de cada articulación.")
```

### Mapa de articulaciones de la mano (H1-2)

| Índice | Articulación    | Rango (rad) |
|--------|----------------|-------------|
| 0      | Pulgar MCP     | [0, 1.57]   |
| 1      | Índice MCP     | [0, 1.57]   |
| 2      | Medio MCP      | [0, 1.57]   |
| 3      | Anular MCP     | [0, 1.57]   |
| 4      | Meñique MCP    | [0, 1.57]   |
| 5      | Pulgar rotación| [0, 1.57]   |

---

## Mando a distancia (WirelessController)

El B2 y H1-2 publican el estado del joystick Unitree en `rt/wirelesscontroller`:

```python title="s6_joystick.py"
#!/usr/bin/env python3
"""Lee el estado del mando a distancia via SDK2."""
import time
import rclpy
from sdk2_bridge_sim import SDK2Bridge  # (1)!

# Robot real:
# from unitree_sdk2py.core.channel import ChannelFactory, ChannelSubscriber
# from unitree_sdk2py.idl.unitree_go.msg.dds_ import WirelessController_

def main():
    rclpy.init()
    bridge = SDK2Bridge()

    print("Esperando datos del joystick... (Ctrl+C para salir)")
    print(f"{'Botón/Eje':<20} {'Valor':>8}")
    print("-" * 30)
    try:
        while True:
            ctrl = bridge.get_wireless_controller()
            if ctrl:
                import os; os.system("clear")
                print(f"{'Eje LX':<20} {ctrl.lx:>8.3f}")
                print(f"{'Eje LY':<20} {ctrl.ly:>8.3f}")
                print(f"{'Eje RX':<20} {ctrl.rx:>8.3f}")
                print(f"{'Eje RY':<20} {ctrl.ry:>8.3f}")
                print(f"{'Botones (hex)':<20} {ctrl.keys:>8}")
                # Decodificar botones comunes
                if ctrl.keys & 0x0001: print("  → R1 presionado")
                if ctrl.keys & 0x0002: print("  → R2 presionado")
                if ctrl.keys & 0x0008: print("  → SELECT presionado")
            time.sleep(0.05)
    except KeyboardInterrupt:
        pass

    bridge.destroy()
    rclpy.shutdown()
```

1. En robot real el mando envía datos a 100 Hz; en sim_lite se puede simular con teclado

---

## Ejercicios

### Ejercicio 1 — Pipeline de visión
Implementa un nodo que capture frames de `/camera/image_raw`, detecte el color más común en la imagen central (ROI 100×100 px) y publique el nombre del color en un tópico `/detected_color` como `std_msgs/String`.

### Ejercicio 2 — Cámara + movimiento
Combina captura de imágenes con movimiento: el robot avanza, se detiene, captura una imagen, avanza 1 m más, repite 3 veces. Guarda las imágenes con timestamp en el nombre del archivo.

### Ejercicio 3 — Joystick virtual
Modifica `s6_joystick.py` para que el robot se mueva en respuesta a los ejes LX/LY del mando: `LY → vx`, `LX → vyaw`. Limita a ±0.5 m/s y ±1.0 rad/s.

### Ejercicio 4 — (H1-2) Secuencia de gestos
Diseña una secuencia de 5 posiciones de mano (abierto, cerrado, pinch, punto, OK) y anima la transición entre ellas con interpolación lineal a 10 Hz.

### Ejercicio 5 — Detección de obstáculo + audio
Cuando el LiDAR detecte un obstáculo a < 0.5 m, el robot se detiene Y emite 3 pitidos de alerta con `play_sound(1)`. Usa un estado FSM explícito (NAVEGANDO / ALERTA).

---

## Pasa al robot real

!!! info "Cámara RealSense en el B2 físico"
    ```bash
    # Verificar que el driver RealSense está activo en el PC2 del B2
    ros2 topic list | grep camera
    # Debería mostrar: /camera/color/image_raw, /camera/depth/image_rect_raw
    ```

    Para el audio en hardware real, `PlaySound` requiere que el servicio `sport_mode` esté activo. No ejecutes comandos de audio cuando el B2 esté en estado de emergencia.

---

## Referencias

- [Intel RealSense D435i specs](https://www.intelrealsense.com/depth-camera-d435i/)
- [H1-2 Dexterous Hand — Unitree docs](https://support.unitree.com/home/en/developer/H1_2)
- [B2 Industrial — hardware completo](../b2-industrial.md)
