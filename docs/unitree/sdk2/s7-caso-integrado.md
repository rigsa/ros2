# S7: Caso Integrado — Implementación Práctica Completa

## Objetivos

- Integrar LocoClient, SportClient, cámara y LiDAR en una aplicación autónoma
- Implementar un sistema de patrulla con registro automático usando SDK2 Python
- Aplicar patrones de seguridad: watchdog, estop, límites de velocidad
- Preparar el código para transición directa a robot real

---

## Proyecto: Sistema de Patrulla Autónoma

Desarrollaremos un sistema completo que:

1. Navega hacia 3 puntos de inspección predefinidos (coordenadas relativas)
2. En cada punto: detiene el robot, captura imagen, verifica obstáculo con LiDAR
3. Registra timestamps, posiciones y estados en un archivo de log
4. Tiene un watchdog de seguridad: para si no recibe confirmación cada 5 s

```
┌─────────────────────────────────────────────────────────┐
│                   Sistema de Patrulla                    │
│                                                          │
│  ┌──────────┐    ┌──────────┐    ┌──────────────────┐  │
│  │ LocoClient│    │ LiDAR    │    │ Cámara + Logger   │  │
│  │ .Move()  │    │ /scan    │    │ /camera/image_raw │  │
│  │ .StopMove│    │ obstáculos│    │ → /tmp/patrol/    │  │
│  └────┬─────┘    └────┬─────┘    └────────┬──────────┘  │
│       │               │                   │             │
│  ┌────▼───────────────▼───────────────────▼──────────┐  │
│  │               FSM de Patrulla                      │  │
│  │  INIT → NAVIGATE → INSPECT → LOG → NEXT_POINT     │  │
│  └───────────────────────────────────────────────────┘  │
│       │                                                  │
│  ┌────▼──────────┐                                       │
│  │   Watchdog    │  ← Thread separado, para si silencio │
│  └───────────────┘                                       │
└─────────────────────────────────────────────────────────┘
```

---

## Código completo: patrulla autónoma

```python title="s7_patrol_system.py"
#!/usr/bin/env python3
"""
Sistema de patrulla autónoma — caso integrado SDK2.
Combina: LocoClient, LiDAR, Cámara, Logger y Watchdog.

Simulación: sdk2_bridge_sim + sim_lite unitree_inspection
Robot real: descomenta los imports de unitree_sdk2py
"""
import os, time, threading, logging, json, cv2, math
from dataclasses import dataclass, field, asdict
from datetime import datetime
from pathlib import Path
import numpy as np

import rclpy
from rclpy.node import Node
from sensor_msgs.msg import LaserScan, Image
from nav_msgs.msg import Odometry
from cv_bridge import CvBridge
from sdk2_bridge_sim import LocoClientSim as LocoClient  # (1)!

# Robot real:
# from unitree_sdk2py.core.channel import ChannelFactory
# from unitree_sdk2py.b2.loco_client import LocoClient
# ChannelFactory.Instance().Init(0)

# ── Parámetros ──────────────────────────────────────────────
MAX_SPEED      = 0.4      # m/s  # (2)!
OBSTACLE_DIST  = 0.5      # m — detener si LiDAR < 0.5 m
WATCHDOG_SECS  = 5.0      # s — parar si no hay actividad
OUTPUT_DIR     = Path("/tmp/patrol")
OUTPUT_DIR.mkdir(parents=True, exist_ok=True)

# Puntos de patrulla (dx, dy) relativo a la posición inicial
PATROL_POINTS = [
    ( 2.0,  0.0),   # Estación 1
    ( 2.0,  2.0),   # Estación 2
    ( 0.0,  2.0),   # Estación 3
]

# ── Estado ──────────────────────────────────────────────────
@dataclass
class PatrolState:
    start_pos: tuple = (0.0, 0.0)
    current_pos: tuple = (0.0, 0.0)
    current_yaw: float = 0.0
    min_lidar: float = float('inf')
    latest_image: object = None
    log: list = field(default_factory=list)
    last_active: float = field(default_factory=time.time)
    stop_requested: bool = False

state = PatrolState()

# ── Nodo ROS 2 ──────────────────────────────────────────────
class PatrolNode(Node):
    def __init__(self):
        super().__init__("patrol_system")
        self.bridge = CvBridge()
        self.create_subscription(LaserScan, "/scan", self._scan_cb, 10)
        self.create_subscription(Odometry,  "/odom", self._odom_cb, 10)
        self.create_subscription(Image, "/camera/image_raw", self._img_cb, 10)

    def _scan_cb(self, msg: LaserScan):
        ranges = [r for r in msg.ranges if not (math.isnan(r) or math.isinf(r))]
        state.min_lidar = min(ranges) if ranges else float('inf')

    def _odom_cb(self, msg: Odometry):
        pos = msg.pose.pose.position
        state.current_pos = (pos.x, pos.y)
        q = msg.pose.pose.orientation
        state.current_yaw = math.atan2(
            2*(q.w*q.z + q.x*q.y), 1 - 2*(q.y*q.y + q.z*q.z))

    def _img_cb(self, msg: Image):
        state.latest_image = self.bridge.imgmsg_to_cv2(msg, "bgr8")

# ── Watchdog ─────────────────────────────────────────────────
def watchdog(loco: LocoClient):
    while not state.stop_requested:
        time.sleep(1.0)
        if time.time() - state.last_active > WATCHDOG_SECS:
            print("⚠ WATCHDOG: sin actividad — deteniendo robot")
            loco.StopMove()
            state.stop_requested = True

# ── Funciones de navegación ──────────────────────────────────
def move_to_relative(loco, node, dx, dy, speed=MAX_SPEED, timeout=30.0):
    """Navega a (dx, dy) relativo a start_pos usando odometría."""
    target_x = state.start_pos[0] + dx
    target_y = state.start_pos[1] + dy

    t0 = time.time()
    while time.time() - t0 < timeout:
        rclpy.spin_once(node, timeout_sec=0.05)
        cx, cy = state.current_pos
        dist = math.hypot(target_x - cx, target_y - cy)

        if dist < 0.15:             # Llegamos al punto
            loco.StopMove()
            return True

        if state.min_lidar < OBSTACLE_DIST:  # Obstáculo detectado
            loco.StopMove()
            print(f"  Obstáculo a {state.min_lidar:.2f} m — esperando...")
            time.sleep(1.0)
            continue

        # Control proporcional hacia el objetivo
        angle_to_target = math.atan2(target_y - cy, target_x - cx)
        yaw_error = angle_to_target - state.current_yaw
        # Normalizar a [-π, π]
        while yaw_error > math.pi:  yaw_error -= 2*math.pi
        while yaw_error < -math.pi: yaw_error += 2*math.pi

        vx   = min(speed, dist * 0.5) if abs(yaw_error) < 0.3 else 0.0
        vyaw = max(-1.0, min(1.0, yaw_error * 2.0))
        loco.Move(vx, 0.0, vyaw)
        state.last_active = time.time()

    loco.StopMove()
    return False  # Timeout

def inspect_point(node, point_id: int):
    """Inspeccion en el punto actual: LiDAR + imagen + log."""
    rclpy.spin_once(node, timeout_sec=0.5)

    # Guardar imagen
    img_path = OUTPUT_DIR / f"point_{point_id}_{datetime.now():%H%M%S}.jpg"
    if state.latest_image is not None:
        cv2.imwrite(str(img_path), state.latest_image)

    # Registrar en log
    entry = {
        "point": point_id,
        "time": datetime.now().isoformat(),
        "position": state.current_pos,
        "min_lidar_m": round(state.min_lidar, 3),
        "obstacle_detected": state.min_lidar < OBSTACLE_DIST,
        "image": str(img_path),
    }
    state.log.append(entry)
    print(f"  Punto {point_id}: LiDAR={entry['min_lidar_m']:.2f}m  img={img_path.name}")
    return entry

# ── Main ──────────────────────────────────────────────────────
def main():
    rclpy.init()
    node = PatrolNode()
    loco = LocoClient()
    loco.Init()
    loco.SwitchGait(1)  # Walk

    # Registrar posición inicial
    rclpy.spin_once(node, timeout_sec=0.5)
    state.start_pos = state.current_pos
    print(f"Inicio en {state.start_pos}")

    # Lanzar watchdog en thread separado
    wd = threading.Thread(target=watchdog, args=(loco,), daemon=True)
    wd.start()

    # ── Patrulla ─────────────────────────────────────────────
    for i, (dx, dy) in enumerate(PATROL_POINTS):
        if state.stop_requested:
            break
        print(f"\n→ Navegando al punto {i+1} (Δ={dx:.1f}, {dy:.1f})")
        arrived = move_to_relative(loco, node, dx, dy)
        if arrived:
            entry = inspect_point(node, i+1)

    # ── Volver al inicio ──────────────────────────────────────
    if not state.stop_requested:
        print("\n→ Volviendo al origen")
        move_to_relative(loco, node, 0.0, 0.0)

    loco.StopMove()
    state.stop_requested = True

    # ── Guardar reporte ───────────────────────────────────────
    report_path = OUTPUT_DIR / f"patrol_report_{datetime.now():%Y%m%d_%H%M%S}.json"
    report_path.write_text(json.dumps(state.log, indent=2, ensure_ascii=False))
    print(f"\n✓ Patrulla completada. Reporte: {report_path}")
    print(f"  Puntos inspeccionados: {len(state.log)}")

    node.destroy_node()
    rclpy.shutdown()

if __name__ == '__main__':
    main()
```

1. Swap this single import for `from unitree_sdk2py.b2.loco_client import LocoClient` on real hardware
2. En hardware real limitar a 0.3 m/s hasta validar el comportamiento

---

## Ejercicios

### Ejercicio 1 — Añadir SportClient
Extiende el sistema para que el robot ejecute `hello` (SportClient) al llegar a cada punto de inspección. El saludo debe estar en el estado `INSPECT`.

### Ejercicio 2 — Detección de ArUco en inspección
Integra la detección de marcadores ArUco del módulo U10. Si se detecta un marcador en el punto, incluye su ID en el log JSON. Añade una imagen anotada (con `cv2.aruco.drawDetectedMarkers`).

### Ejercicio 3 — Ruta dinámica
En lugar de coordenadas fijas, lee los puntos de patrulla desde un archivo YAML en tiempo de ejecución. Permite actualizar la ruta sin recompilar.

### Ejercicio 4 — Modo de emergencia completo
Implementa un suscriptor a `/emergency_stop` (`std_msgs/Bool`). Si se publica `True`, el robot para, se sienta (`squat()`), y escribe un log de emergencia. Si se publica `False`, reanuda desde el punto actual.

### Ejercicio 5 — Dashboard en terminal
Añade un thread que imprima un dashboard con `curses` (sin usar `clear`): punto actual, distancia al objetivo, LiDAR mínimo, tiempo transcurrido, y estado de la FSM, actualizando a 2 Hz.

---

## Pasa al robot real

!!! success "Checklist pre-vuelo para B2 físico"
    - [ ] Batería > 40%
    - [ ] Área despejada, radio ≥ 3 m
    - [ ] Operador físicamente presente con mando
    - [ ] Cambia el import: `sdk2_bridge_sim` → `unitree_sdk2py.b2.loco_client`
    - [ ] `MAX_SPEED` ≤ 0.3 m/s para la primera prueba
    - [ ] Verifica `ros2 topic echo /odom` antes de iniciar
    - [ ] Ten `loco.StopMove()` en una terminal separada listo para ejecutar

    El código de este módulo puede ejecutarse en el B2 físico sin ningún otro cambio.

---

## Referencias

- [U9: Rutinas de Inspección (versión ROS 2)](../u9-rutinas-inspeccion.md)
- [U10: Tags ArUco](../u10-aruco.md)
- [SDK2 SportClient](s5-alto-nivel.md)
- [Cola de Robot — Reservar una sesión](../../../robot-queue)
