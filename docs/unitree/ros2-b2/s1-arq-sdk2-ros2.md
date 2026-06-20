# S1: Arquitectura SDK2 + ROS 2 — Capas, Bridges y Mapeo de Tópicos

## Objetivos

- Comprender cómo SDK2 (DDS) y ROS 2 coexisten en el B2
- Identificar qué capa usar para cada tipo de tarea
- Mapear los tópicos SDK2 nativos a su equivalente ROS 2
- Configurar el bridge oficial `unitree_ros2` en el PC2

---

## Arquitectura de capas del B2

El B2 tiene dos sistemas de comunicación funcionando simultáneamente:

```
┌──────────────────────────────────────────────────────────┐
│                      Tu aplicación                        │
├──────────────────┬───────────────────────────────────────┤
│   ROS 2 (Jazzy)  │          SDK2 (DDS nativo)            │
│   /cmd_vel       │     rt/api/loco/request               │
│   /odom          │     rt/lowstate                       │
│   /scan          │     rt/wirelesscontroller             │
│   /camera/...    │     rt/sportstate                     │
├──────────────────┴───────────────────────────────────────┤
│              unitree_ros2_bridge                          │
│   (convierte DDS ↔ ROS 2 en tiempo real)                 │
├──────────────────────────────────────────────────────────┤
│         CycloneDDS — transporte común                     │
├──────────────────────────────────────────────────────────┤
│                  PC2 del B2 (Ubuntu)                      │
│              192.168.123.18 — LAN del robot              │
├──────────────────────────────────────────────────────────┤
│           MCU — 12 motores @ 500 Hz                      │
└──────────────────────────────────────────────────────────┘
```

### Cuándo usar cada capa

| Tarea                              | Capa recomendada     | Razón                                   |
|------------------------------------|----------------------|-----------------------------------------|
| Teleop básico / Nav2               | ROS 2 `/cmd_vel`     | Ecosistema estándar                     |
| SLAM, costmaps, planning           | ROS 2 nativo         | nav2, slam_toolbox, rtabmap             |
| Gait switching (kRun, kClimb)      | SDK2 `LocoClient`    | Solo disponible en SDK2                 |
| Lectura de motores a 500 Hz        | SDK2 `LowState`      | Latencia directa, sin bridge            |
| Manos H1-2 (`HandClient`)          | SDK2 puro            | No bridgeado                            |
| Integración rápida de sensors      | ROS 2                | Herramientas (RViz, rosbag, plotjuggler)|
| Producción / robustez de red       | ROS 2 lifecycle      | Gestión de estado de nodos              |

---

## Tópicos SDK2 ↔ ROS 2

El bridge `unitree_ros2` mapea los siguientes canales DDS a tópicos ROS 2:

| Tópico DDS (SDK2)                  | Tópico ROS 2                    | Tipo ROS 2                      | Hz   |
|------------------------------------|----------------------------------|---------------------------------|------|
| `rt/lowstate`                      | `/joint_states`                  | `sensor_msgs/JointState`        | 500  |
| `rt/lowstate` (IMU)                | `/imu/data`                      | `sensor_msgs/Imu`               | 500  |
| `rt/sportstate`                    | `/odom`                          | `nav_msgs/Odometry`             | 50   |
| `rt/sportstate` (pose)             | `/robot_pose`                    | `geometry_msgs/PoseStamped`     | 50   |
| `rt/scan`                          | `/scan`                          | `sensor_msgs/LaserScan`         | 10   |
| `rt/camera/image_raw`              | `/camera/image_raw`              | `sensor_msgs/Image`             | 30   |
| `rt/wirelesscontroller`            | `/wirelesscontroller`            | `unitree_msgs/WirelessController`| 100 |
| `/cmd_vel` (ROS 2)                 | `rt/api/loco/request`            | `geometry_msgs/Twist` → DDS     | —    |

!!! note "Bridge dirección de flujo"
    La mayoría de tópicos fluyen `DDS → ROS 2` (sensores). El único flujo inverso importante es `/cmd_vel → rt/api/loco/request` (comando de velocidad).

---

## Verificar tópicos activos en el PC2

```bash title="En el PC2 del B2 (ssh unitree@192.168.123.18)"
# Ver todos los tópicos publicados por el bridge
ros2 topic list

# Verificar frecuencia del IMU
ros2 topic hz /imu/data

# Ver un mensaje de odometría
ros2 topic echo /odom --once
```

Desde el **sandbox** (con CYCLONEDDS_URI configurado):

```bash title="En el sandbox del estudiante"
# Si el slot de robot está activo y CYCLONEDDS_URI apunta al lab
ros2 topic list | grep -E "odom|scan|joint|imu"
```

---

## Configurar el bridge en el PC2

El bridge `unitree_ros2` debería estar corriendo automáticamente. Si no:

```bash title="En el PC2 del B2"
# Verificar
ps aux | grep ros2

# Iniciar manualmente
cd ~/unitree_ros2
source install/setup.bash
ros2 launch unitree_ros2_bringup b2.launch.py
```

```python title="s1_verificar_bridge.py"
#!/usr/bin/env python3
"""
Verifica que el bridge SDK2↔ROS2 está activo y publicando datos.
Funciona tanto en sim_lite como con el B2 real.
"""
import rclpy
from rclpy.node import Node
from nav_msgs.msg import Odometry
from sensor_msgs.msg import Imu, LaserScan

from sdk2_bridge_sim import SDK2Bridge  # (1)!

# Robot real: no necesitas SDK2Bridge, los tópicos ROS 2 ya están disponibles

class BridgeVerifier(Node):
    def __init__(self):
        super().__init__("bridge_verifier")
        self._odom_ok   = False
        self._imu_ok    = False
        self._lidar_ok  = False

        self.create_subscription(Odometry,  "/odom",     self._odom_cb,  1)
        self.create_subscription(Imu,       "/imu/data", self._imu_cb,   1)
        self.create_subscription(LaserScan, "/scan",     self._scan_cb,  1)

    def _odom_cb(self,  msg): self._odom_ok  = True
    def _imu_cb(self,   msg): self._imu_ok   = True
    def _scan_cb(self,  msg): self._lidar_ok = True

    def status(self) -> dict:
        return {"odom": self._odom_ok, "imu": self._imu_ok, "lidar": self._lidar_ok}

def main():
    rclpy.init()
    node = BridgeVerifier()

    import time
    t0 = time.time()
    while time.time() - t0 < 5.0:
        rclpy.spin_once(node, timeout_sec=0.2)
        s = node.status()
        if all(s.values()):
            break

    s = node.status()
    print("Bridge status:")
    for k, v in s.items():
        icon = "✓" if v else "✗"
        print(f"  {icon} {k:10} {'recibiendo' if v else 'SIN DATOS — verifica el bridge'}")

    node.destroy_node()
    rclpy.shutdown()

if __name__ == "__main__":
    main()
```

1. En el sandbox el bridge sim ya expone `/odom`, `/imu/data` y `/scan` listos para usar

---

## Ejercicios

### Ejercicio 1 — Mapa de tópicos
Ejecuta `ros2 topic list` en el sandbox (sim_lite activo) y clasifica cada tópico en: sensores, comandos, transformaciones (TF) y estado del sistema.

### Ejercicio 2 — Latencia del bridge
Suscríbete a `/imu/data` y mide el `header.stamp` vs el tiempo de recepción. ¿Cuál es la latencia promedio? Compara con el valor esperado en hardware real (~1 ms DDS directo).

### Ejercicio 3 — Inspección del JointState
Suscríbete a `/joint_states` y extrae los nombres de las articulaciones publicadas. Verifica que coinciden con el mapa de 12 motores del B2 del módulo S4.

### Ejercicio 4 — Flujo bidireccional
Publica en `/cmd_vel` desde la terminal mientras monitorizas `/odom`. ¿Cuántos mensajes de odometría se generan por cada comando `Twist`?

### Ejercicio 5 — Reproducibilidad con rosbag
Graba 30 segundos de `/scan`, `/odom` e `/imu/data` con `ros2 bag record`. Verifica que puedes reproducir la secuencia con `ros2 bag play` y que los tópicos aparecen con la misma frecuencia.

---

## Pasa al robot real

!!! success "Verificación inicial con el B2 físico"
    Al activar tu slot de robot real, ejecuta este script para confirmar que el bridge está activo y los datos llegan correctamente antes de enviar cualquier comando de movimiento.

    ```bash
    # Configura el entorno (ya hecho automáticamente si tienes slot activo)
    export CYCLONEDDS_URI='<CycloneDDS><Domain><General>
      <NetworkInterfaceAddress>eth0</NetworkInterfaceAddress>
    </General></Domain></CycloneDDS>'

    python3 s1_verificar_bridge.py
    # Espera ver: ✓ odom, ✓ imu, ✓ lidar
    ```

    Si algún tópico falla: `ssh unitree@192.168.123.18` → `ros2 topic list` para diagnosticar en el PC2 directamente.

---

## Referencias

- [S3: Acceso al PC2](../sdk2/s3-acceso-pc2.md)
- [S4: Interfaces de Bajo Nivel](../sdk2/s4-bajo-nivel.md)
- [Unitree ROS 2 package — GitHub](https://github.com/unitreerobotics/unitree_ros2)
- [CycloneDDS URI configuration](https://cyclonedds.io/docs/cyclonedds/latest/config/)
