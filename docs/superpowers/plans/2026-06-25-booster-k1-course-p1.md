# Booster K1 Course Track — Implementation Plan (Part 1 of 2)

> **For agentic workers:** REQUIRED SUB-SKILL: Use superpowers:subagent-driven-development to implement task-by-task.

**Goal:** Add a full standalone Booster K1 humanoid course track (B1–B10) with landing-page chooser, visually rich sim, and a separate Ubuntu 22.04/ROS 2 Humble Docker image.

**Architecture:** New `docs/booster/` tree + `docs/index.md` chooser in `ros2`; new `Dockerfile.booster`, `booster_sim_lite.py`, `course-map-booster.yaml` in `ros2-sandbox`; new `humble-booster` branch in `rigsa_ros`. Orchestrator gains `?track=booster` routing.

**Tech Stack:** MkDocs Material, Python 3.10+, ROS 2 Humble, PyBullet (TinyRenderer, DIRECT mode), pygame, booster_robotics_sdk_python, ultralytics (YOLOv8), FastAPI.

## Global Constraints

- All course prose in Spanish.
- ROS 2 Jazzy = Unitree track; ROS 2 Humble = Booster track. Never mix.
- Sheffield CC BY-SA attributions in `docs/course/README.md:40` and `docs/about/license.md:15` must not be touched.
- `pybullet.stepSimulation()` must never be called in `booster_sim_lite.py`.
- Booster K1 joint names (22 DoF): `head_yaw`, `head_pitch`, `l_shoulder_pitch`, `l_shoulder_roll`, `l_shoulder_yaw`, `l_elbow_pitch`, `r_shoulder_pitch`, `r_shoulder_roll`, `r_shoulder_yaw`, `r_elbow_pitch`, `l_hip_pitch`, `l_hip_roll`, `l_hip_yaw`, `l_knee_pitch`, `l_ankle_pitch`, `l_ankle_roll`, `r_hip_pitch`, `r_hip_roll`, `r_hip_yaw`, `r_knee_pitch`, `r_ankle_pitch`, `r_ankle_roll`.
- K1 camera topics from real robot: `/StereoNetNode/rectified_image` and `/StereoNetNode/stereonet_depth`. Sim publishes to `/camera/image_raw` and `/camera/depth` — bridge remaps on real hardware.
- `SANDBOX_IMAGE_BOOSTER` env var selects the Booster Cloud Run image in the orchestrator.

---

### Task 1: Sheffield Module Code Cleanup

**Files:**
- Modify: `ros2-sandbox/sandbox/course-map.yaml:92,103`
- Modify: `ros2/docs/.pages:7`
- Modify: `ros2/docs/amr/.pages:2`

**Interfaces:** Produces: nothing consumed by later tasks.

- [ ] **Step 1: Fix course-map.yaml display names**

In `ros2-sandbox/sandbox/course-map.yaml`, change lines 92 and 103:
```yaml
# line 92 — was: display_name: "AMR31001 Lab 1: Mobile Robotics"
display_name: "Laboratorio 1: Robótica Móvil"

# line 103 — was: display_name: "AMR31001 Lab 2: Feedback Control"
display_name: "Laboratorio 2: Control Retroalimentado"
```

- [ ] **Step 2: Fix docs/.pages**

In `ros2/docs/.pages`, find the line:
```yaml
  - "AMR31001": amr
```
Change to:
```yaml
  - "Laboratorios AMR": amr
```

- [ ] **Step 3: Fix docs/amr/.pages**

In `ros2/docs/amr/.pages`, find:
```yaml
  - "AMR31001": README.md
```
Change to:
```yaml
  - "Laboratorios de Robótica Móvil": README.md
```

- [ ] **Step 4: Verify no more Sheffield module codes in docs**

```bash
grep -r "AMR31001\|COM31001\|ELE31001" /home/jahir/repos/ros2/docs/ /home/jahir/repos/ros2-sandbox/sandbox/course-map.yaml
```
Expected: no output.

- [ ] **Step 5: Commit**
```bash
cd /home/jahir/repos/ros2 && git add docs/.pages docs/amr/.pages && git commit -m "chore: remove Sheffield module codes from nav"
cd /home/jahir/repos/ros2-sandbox && git add sandbox/course-map.yaml && git commit -m "chore: remove AMR31001 module codes from course map"
```

---

### Task 2: MkDocs Landing Page + Booster Nav Structure

**Files:**
- Modify: `ros2/docs/index.md`
- Create: `ros2/docs/booster/.pages`
- Create: `ros2/docs/booster/README.md`

**Interfaces:** Produces: `docs/booster/` nav root consumed by Tasks 3–4.

- [ ] **Step 1: Replace docs/index.md**

```markdown
---
title: "Inicio"
description: "Elige tu plataforma robótica para comenzar el curso de ROS 2 — RIGSA"
hide:
  - navigation
  - toc
---

# Laboratorio de Robótica con ROS 2

Selecciona la plataforma robótica con la que deseas trabajar:

<div class="grid cards" markdown>

-   :material-dog:{ .lg .middle } **Robots Cuadrúpedos — Unitree**

    ---

    Go2 EDU · AS2 EDU · B2  
    ROS 2 Jazzy · Parts 1–6 + U1–U12

    [:octicons-arrow-right-24: Comenzar](course/README.md)

-   :material-robot:{ .lg .middle } **Robot Humanoide — Booster K1**

    ---

    95 cm · 22 DoF · RoboCup 2025 Campeón  
    ROS 2 Humble · B1–B10

    [:octicons-arrow-right-24: Comenzar](booster/README.md)

</div>
```

- [ ] **Step 2: Create docs/booster/.pages**

```yaml
nav:
  - README.md
  - b1-introduccion.md
  - b2-locomocion.md
  - b3-pubsub.md
  - b4-articulaciones.md
  - b5-comportamientos.md
  - b6-camara.md
  - b7-yolo.md
  - b8-lidar.md
  - b9-robocup.md
  - b10-mision.md
```

- [ ] **Step 3: Create docs/booster/README.md**

```markdown
---
title: "Curso Booster K1 — Introducción"
description: "Curso completo de ROS 2 con el robot humanoide Booster K1. 10 módulos, desde cero hasta misión autónoma."
---

# Curso Booster K1

Aprende ROS 2 usando el **Booster K1** — el robot humanoide de 95 cm que ganó el RoboCup 2025 KidSize.

## Módulos del curso

| Módulo | Tema | Mundo |
|--------|------|-------|
| [B1](b1-introduccion.md) | Hardware y arquitectura | — |
| [B2](b2-locomocion.md) | Locomoción bípeda | `booster_empty` |
| [B3](b3-pubsub.md) | Publishers y Subscribers | `booster_empty` |
| [B4](b4-articulaciones.md) | Articulaciones e IMU | `booster_empty` |
| [B5](b5-comportamientos.md) | Comportamientos y Servicios | `booster_empty` |
| [B6](b6-camara.md) | Cámara RGBD y OpenCV | `booster_obstacles` |
| [B7](b7-yolo.md) | Detección con YOLO | `booster_soccer` |
| [B8](b8-lidar.md) | LiDAR y obstáculos | `booster_obstacles` |
| [B9](b9-robocup.md) | Arquitectura RoboCup | `booster_soccer` |
| [B10](b10-mision.md) | Misión autónoma integrada | `booster_inspection` |

## Requisitos

- Acceso al sandbox (botón **Sandbox** en cada módulo)
- No se requiere experiencia previa con ROS 2

## El patrón bridge

Tu código usa topics ROS 2 estándar. En el sandbox, `booster_sim_lite.py` los simula.
En el robot real, `booster_ros2_bridge.py` traduce al SDK de Booster automáticamente.
**El mismo código funciona en ambos entornos.**
```

- [ ] **Step 4: Verify mkdocs build**
```bash
cd /home/jahir/repos/ros2 && mkdocs build --strict 2>&1 | tail -20
```
Expected: `INFO - Documentation built in N seconds` with no errors.

- [ ] **Step 5: Commit**
```bash
cd /home/jahir/repos/ros2 && git add docs/index.md docs/booster/ && git commit -m "feat: add landing page chooser and booster course nav structure"
```

---

### Task 3: Course Lessons B1–B5

**Files:**
- Create: `ros2/docs/booster/b1-introduccion.md`
- Create: `ros2/docs/booster/b2-locomocion.md`
- Create: `ros2/docs/booster/b3-pubsub.md`
- Create: `ros2/docs/booster/b4-articulaciones.md`
- Create: `ros2/docs/booster/b5-comportamientos.md`

- [ ] **Step 1: Create b1-introduccion.md**

```markdown
---
title: "B1: Introducción al K1 — Hardware y Arquitectura"
description: "Especificaciones del Booster K1, modos de operación, conexión y el patrón bridge para ROS 2."
---

# B1: Introducción al K1

## El robot

| Propiedad | Valor |
|-----------|-------|
| Altura | 95 cm |
| Peso | 19.5 kg |
| Grados de libertad | 22 DoF |
| Velocidad máxima | ~0.4 m/s |
| Cómputo (EDU) | Jetson Orin NX 8GB — 117 TOPS |
| Batería (EDU) | 5 Ah — ~80 min |
| Conectividad | Ethernet, WiFi 6, Bluetooth 5.2 |
| IP por defecto | 192.168.10.102 |

## Modos de operación

El K1 pasa secuencialmente por estos estados al encenderse:

```
DAMP → PREP → WALK → CUSTOM → PROTECT (automático al caer)
```

- **DAMP**: articulaciones pasivas (seguro para maniobrar manualmente)
- **PREP**: posición de pie con control de posición (espera 3 s)
- **WALK**: responde a comandos de locomoción
- **CUSTOM**: control via SDK (requiere fixture de desarrollo)
- **PROTECT**: modo seguro automático al detectar caída

## Los 22 grados de libertad

```
Cabeza (2):    head_yaw, head_pitch
Brazo izq (4): l_shoulder_pitch, l_shoulder_roll, l_shoulder_yaw, l_elbow_pitch
Brazo der (4): r_shoulder_pitch, r_shoulder_roll, r_shoulder_yaw, r_elbow_pitch
Pierna izq (6): l_hip_pitch, l_hip_roll, l_hip_yaw, l_knee_pitch, l_ankle_pitch, l_ankle_roll
Pierna der (6): r_hip_pitch, r_hip_roll, r_hip_yaw, r_knee_pitch, r_ankle_pitch, r_ankle_roll
```

## Arquitectura del sistema

```
┌──────────────────────────────────┐
│         Tu código ROS 2          │
│  /cmd_vel  /odom  /joint_states  │
│  /imu/data  /camera/image_raw    │
│  /scan  /sport/*                 │
└──────────────┬───────────────────┘
               │ topics ROS 2 estándar
   ┌───────────┴───────────┐
   │                       │
┌──▼──────────┐   ┌────────▼──────────────┐
│booster_sim_ │   │ booster_ros2_bridge.py │
│lite.py      │   │ (robot real)           │
│(simulador)  │   │ booster_robotics_sdk   │
└─────────────┘   └───────────┬───────────┘
                               │ SDK FastDDS
                        ┌──────▼──────┐
                        │ Booster K1  │
                        │(hardware)   │
                        └─────────────┘
```

## Conexión al robot real

```bash
# Configurar red: PC en 192.168.10.10 / 255.255.255.0
ssh booster@192.168.10.102   # contraseña: 123456

# Instalar SDK Python
pip install booster_robotics_sdk_python --user

# Verificar conexión
python3 -c "from booster_robotics_sdk_python import RobotClient; print('SDK OK')"
```

!!! info "En el sandbox"
    No necesitas conexión física. El sandbox usa `booster_sim_lite.py`
    que publica los mismos topics que el robot real.
```

- [ ] **Step 2: Create b2-locomocion.md**

```markdown
---
title: "B2: Locomoción Bípeda"
description: "Controla el movimiento omnidireccional del K1 con /cmd_vel TwistStamped."
---

# B2: Locomoción Bípeda

## El K1 es holonómico

A diferencia de un robot de ruedas diferencial, el K1 puede moverse en cualquier dirección
sin girar primero: adelante/atrás, lateral izquierda/derecha, y rotación **simultáneamente**.

```python
from geometry_msgs.msg import TwistStamped

msg = TwistStamped()
msg.twist.linear.x  =  0.2   # adelante (m/s)
msg.twist.linear.y  =  0.1   # lateral izquierda (m/s)  ← nuevo vs. robot diferencial
msg.twist.angular.z = -0.3   # rotación antihoraria (rad/s)
```

## Configuración del sandbox

Abre el sandbox con **"B2: Locomoción Bípeda"**.

- Mundo: `booster_empty`
- Archivo semilla: `b2_walk_square.py` en `~/ros2_ws/src/booster_b2_locomotion/scripts/`

## Ejercicio: caminar en cuadrado

```python
#!/usr/bin/env python3
import rclpy
from rclpy.node import Node
from geometry_msgs.msg import TwistStamped
import time

class WalkSquare(Node):
    def __init__(self):
        super().__init__('walk_square')
        self.pub = self.create_publisher(TwistStamped, '/cmd_vel', 10)

    def move(self, vx=0.0, vy=0.0, wz=0.0, duration=2.0):
        msg = TwistStamped()
        msg.twist.linear.x  = vx
        msg.twist.linear.y  = vy
        msg.twist.angular.z = wz
        end = time.monotonic() + duration
        rate = self.create_rate(20)
        while time.monotonic() < end:
            msg.header.stamp = self.get_clock().now().to_msg()
            self.pub.publish(msg)
            rate.sleep()
        self.pub.publish(TwistStamped())  # detener

    def run(self):
        for _ in range(4):
            self.move(vx=0.2, duration=3.0)   # avanzar
            self.move(wz=1.57, duration=1.0)  # girar 90°

def main():
    rclpy.init()
    node = WalkSquare()
    node.run()
    rclpy.shutdown()

if __name__ == '__main__':
    main()
```

```bash
cd ~/ros2_ws
colcon build --packages-select booster_b2_locomotion --symlink-install
source install/setup.bash
ros2 run booster_b2_locomotion b2_walk_square.py
```

## Tarea: figura en ocho

Modifica el nodo para que el K1 haga una figura en ocho usando `linear.y`.
```

- [ ] **Step 3: Create b3-pubsub.md**

```markdown
---
title: "B3: Publishers y Subscribers"
description: "Fundamentos de pub/sub con ROS 2 usando los topics del K1: /odom e /imu/data."
---

# B3: Publishers y Subscribers

## Topics disponibles

```bash
ros2 topic list
# /cmd_vel        geometry_msgs/TwistStamped
# /odom           nav_msgs/Odometry
# /imu/data       sensor_msgs/Imu
# /joint_states   sensor_msgs/JointState
# /scan           sensor_msgs/LaserScan
# /camera/image_raw  sensor_msgs/Image
# /battery_state  sensor_msgs/BatteryState
```

## Suscribirse a /odom

```python
#!/usr/bin/env python3
import rclpy
from rclpy.node import Node
from nav_msgs.msg import Odometry

class OdomSubscriber(Node):
    def __init__(self):
        super().__init__('odom_subscriber')
        self.create_subscription(Odometry, '/odom', self.callback, 10)

    def callback(self, msg):
        x = msg.pose.pose.position.x
        y = msg.pose.pose.position.y
        self.get_logger().info(f'Posición: x={x:.2f} y={y:.2f}')

def main():
    rclpy.init()
    rclpy.spin(OdomSubscriber())
    rclpy.shutdown()
```

## Suscribirse a /imu/data

```python
from sensor_msgs.msg import Imu

class ImuSubscriber(Node):
    def __init__(self):
        super().__init__('imu_subscriber')
        self.create_subscription(Imu, '/imu/data', self.callback, 10)

    def callback(self, msg):
        ax = msg.linear_acceleration.x
        ay = msg.linear_acceleration.y
        az = msg.linear_acceleration.z
        self.get_logger().info(f'Aceleración: ax={ax:.2f} ay={ay:.2f} az={az:.2f}')
```

## Tarea

Crea un nodo que publique en `/cmd_vel` y a la vez se suscriba a `/odom`.
Detén el robot automáticamente cuando `x > 1.0 m`.
```

- [ ] **Step 4: Create b4-articulaciones.md**

```markdown
---
title: "B4: Articulaciones y Estado del Robot"
description: "Lee /joint_states (22 DoF) e /imu/data para monitorear la postura del K1."
---

# B4: Articulaciones y Estado del Robot

## El topic /joint_states

```bash
ros2 topic echo /joint_states --once
# name: [head_yaw, head_pitch, l_shoulder_pitch, ..., r_ankle_roll]
# position: [0.0, 0.0, -0.1, ...]   # radianes
# velocity: [0.0, 0.0, ...]
# effort:   [0.0, 0.0, ...]
```

22 articulaciones en orden: 2 cabeza, 4 brazo izq, 4 brazo der, 6 pierna izq, 6 pierna der.

## Monitor de articulaciones

```python
#!/usr/bin/env python3
import rclpy
from rclpy.node import Node
from sensor_msgs.msg import JointState

K1_JOINTS = [
    "head_yaw","head_pitch",
    "l_shoulder_pitch","l_shoulder_roll","l_shoulder_yaw","l_elbow_pitch",
    "r_shoulder_pitch","r_shoulder_roll","r_shoulder_yaw","r_elbow_pitch",
    "l_hip_pitch","l_hip_roll","l_hip_yaw","l_knee_pitch","l_ankle_pitch","l_ankle_roll",
    "r_hip_pitch","r_hip_roll","r_hip_yaw","r_knee_pitch","r_ankle_pitch","r_ankle_roll",
]

class JointMonitor(Node):
    def __init__(self):
        super().__init__('joint_monitor')
        self.create_subscription(JointState, '/joint_states', self.callback, 10)

    def callback(self, msg):
        joint_map = dict(zip(msg.name, msg.position))
        l_knee = joint_map.get('l_knee_pitch', 0.0)
        r_knee = joint_map.get('r_knee_pitch', 0.0)
        self.get_logger().info(f'Rodillas: izq={l_knee:.3f} der={r_knee:.3f} rad')
```

## IMU — detectar inclinación

```python
import math
from sensor_msgs.msg import Imu

class TiltMonitor(Node):
    def __init__(self):
        super().__init__('tilt_monitor')
        self.create_subscription(Imu, '/imu/data', self.callback, 10)

    def callback(self, msg):
        # Aceleración gravitacional indica inclinación
        ax = msg.linear_acceleration.x  # inclinación adelante/atrás
        ay = msg.linear_acceleration.y  # inclinación lateral
        tilt = math.sqrt(ax**2 + ay**2)
        if tilt > 2.0:
            self.get_logger().warn(f'¡Robot inclinado! tilt={tilt:.2f} m/s²')
```

## Tarea

Crea un nodo que monitoree `/joint_states` e `/imu/data` simultáneamente
y emita una advertencia si la inclinación supera 5°.
```

- [ ] **Step 5: Create b5-comportamientos.md**

```markdown
---
title: "B5: Comportamientos y Servicios"
description: "Activa comportamientos predefinidos del K1 usando servicios ROS 2 /sport/*."
---

# B5: Comportamientos y Servicios

## Servicios disponibles

```bash
ros2 service list | grep sport
# /sport/stand_up
# /sport/stand_down
# /sport/hello
# /sport/stretch
# /sport/dance1
# /sport/dance2
# /sport/recovery_stand
# /sport/balance_stand
# /sport/dock
# /sport/undock
```

Todos son de tipo `std_srvs/Trigger` — no tienen argumentos, solo devuelven éxito/fallo.

## Cliente de servicio

```python
#!/usr/bin/env python3
import rclpy
from rclpy.node import Node
from std_srvs.srv import Trigger

class BehaviorClient(Node):
    def __init__(self):
        super().__init__('behavior_client')

    def call(self, behavior: str) -> bool:
        client = self.create_client(Trigger, f'/sport/{behavior}')
        if not client.wait_for_service(timeout_sec=3.0):
            self.get_logger().error(f'Servicio /sport/{behavior} no disponible')
            return False
        future = client.call_async(Trigger.Request())
        rclpy.spin_until_future_complete(self, future)
        result = future.result()
        self.get_logger().info(f'{behavior}: {result.message}')
        return result.success

def main():
    rclpy.init()
    node = BehaviorClient()
    node.call('hello')      # saludar
    node.call('dance1')     # bailar
    node.call('stand_up')   # ponerse de pie
    rclpy.shutdown()
```

## Tarea

Crea un nodo que active la secuencia: `hello` → esperar 2 s → `dance1` → `recovery_stand`.
```

- [ ] **Step 6: Verify all files build**
```bash
cd /home/jahir/repos/ros2 && mkdocs build --strict 2>&1 | grep -E "ERROR|WARNING|built in"
```
Expected: `INFO - Documentation built in N seconds`.

- [ ] **Step 7: Commit**
```bash
cd /home/jahir/repos/ros2 && git add docs/booster/b1-introduccion.md docs/booster/b2-locomocion.md docs/booster/b3-pubsub.md docs/booster/b4-articulaciones.md docs/booster/b5-comportamientos.md && git commit -m "feat(booster): add lessons B1-B5"
```

---

### Task 4: Course Lessons B6–B10

**Files:**
- Create: `ros2/docs/booster/b6-camara.md`
- Create: `ros2/docs/booster/b7-yolo.md`
- Create: `ros2/docs/booster/b8-lidar.md`
- Create: `ros2/docs/booster/b9-robocup.md`
- Create: `ros2/docs/booster/b10-mision.md`

- [ ] **Step 1: Create b6-camara.md**

```markdown
---
title: "B6: Cámara RGBD y Visión con OpenCV"
description: "Usa la cámara estéreo del K1 para detección de color y aproximación a objetos."
---

# B6: Cámara RGBD y Visión con OpenCV

## Topics de cámara

```bash
/camera/image_raw    # sensor_msgs/Image — imagen RGB 320×240
/camera/depth        # sensor_msgs/Image — profundidad float32 en metros
```

!!! note "En el robot real"
    Los topics reales son `/StereoNetNode/rectified_image` y `/StereoNetNode/stereonet_depth`.
    El bridge los remapea automáticamente a los nombres del sandbox.

## Convertir imagen ROS a OpenCV

```python
import cv2
import numpy as np
from sensor_msgs.msg import Image

def imgmsg_to_bgr(msg: Image) -> np.ndarray:
    """Convierte sensor_msgs/Image (bgr8) a numpy BGR."""
    return np.frombuffer(msg.data, dtype=np.uint8).reshape(msg.height, msg.width, 3)

def depth_to_array(msg: Image) -> np.ndarray:
    """Convierte imagen de profundidad float32 a numpy array en metros."""
    return np.frombuffer(msg.data, dtype=np.float32).reshape(msg.height, msg.width)
```

## Detección de color

```python
#!/usr/bin/env python3
import rclpy, cv2, numpy as np
from rclpy.node import Node
from sensor_msgs.msg import Image
from geometry_msgs.msg import TwistStamped

class ColorFollower(Node):
    def __init__(self):
        super().__init__('color_follower')
        self.create_subscription(Image, '/camera/image_raw', self.img_cb, 10)
        self.create_subscription(Image, '/camera/depth',     self.dep_cb, 10)
        self.pub = self.create_publisher(TwistStamped, '/cmd_vel', 10)
        self._depth = None

    def dep_cb(self, msg):
        self._depth = np.frombuffer(msg.data, dtype=np.float32).reshape(msg.height, msg.width)

    def img_cb(self, msg):
        bgr = np.frombuffer(msg.data, dtype=np.uint8).reshape(msg.height, msg.width, 3)
        hsv = cv2.cvtColor(bgr, cv2.COLOR_BGR2HSV)
        # Detectar pelota naranja
        mask = cv2.inRange(hsv, (5, 150, 150), (20, 255, 255))
        contours, _ = cv2.findContours(mask, cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_SIMPLE)
        cmd = TwistStamped()
        cmd.header.stamp = self.get_clock().now().to_msg()
        if contours:
            c = max(contours, key=cv2.contourArea)
            M = cv2.moments(c)
            if M['m00'] > 200:
                cx = M['m10'] / M['m00']
                error = (cx - msg.width / 2) / msg.width   # -0.5 a 0.5
                cmd.twist.angular.z = -error * 0.8
                if self._depth is not None:
                    cy = int(M['m01'] / M['m00'])
                    dist = self._depth[int(cy), int(cx)]
                    if dist > 0.6:
                        cmd.twist.linear.x = 0.15
        self.pub.publish(cmd)
```

## Tarea

Modifica el nodo para que el robot se detenga a 0.4 m del objeto detectado.
```

- [ ] **Step 2: Create b7-yolo.md**

```markdown
---
title: "B7: Detección de Objetos con YOLO"
description: "Usa YOLOv8 sobre el feed de cámara del K1 para detectar pelota y personas."
---

# B7: Detección de Objetos con YOLO

## Instalación

YOLOv8 ya está instalado en el sandbox Booster:
```bash
python3 -c "from ultralytics import YOLO; print('YOLO OK')"
```

## Detector básico con YOLOv8

```python
#!/usr/bin/env python3
import rclpy, cv2, numpy as np
from rclpy.node import Node
from sensor_msgs.msg import Image
from ultralytics import YOLO

class YoloDetector(Node):
    def __init__(self):
        super().__init__('yolo_detector')
        self.model = YOLO('yolov8n.pt')   # nano — más rápido
        self.create_subscription(Image, '/camera/image_raw', self.callback, 10)

    def callback(self, msg):
        bgr = np.frombuffer(msg.data, dtype=np.uint8).reshape(msg.height, msg.width, 3)
        results = self.model(bgr, verbose=False)
        for box in results[0].boxes:
            cls  = int(box.cls[0])
            name = self.model.names[cls]
            conf = float(box.conf[0])
            x1, y1, x2, y2 = map(int, box.xyxy[0])
            self.get_logger().info(f'{name} ({conf:.0%})  bbox=({x1},{y1})-({x2},{y2})')
```

## Detección de pelota (clase 32 = sports ball)

```python
BALL_CLASS = 32   # COCO class id for sports ball

def callback(self, msg):
    bgr = np.frombuffer(msg.data, dtype=np.uint8).reshape(msg.height, msg.width, 3)
    results = self.model(bgr, verbose=False, classes=[BALL_CLASS, 0])  # 0=persona
    for box in results[0].boxes:
        name = self.model.names[int(box.cls[0])]
        cx = (box.xyxy[0][0] + box.xyxy[0][2]) / 2
        cy = (box.xyxy[0][1] + box.xyxy[0][3]) / 2
        self.get_logger().info(f'Detectado: {name} en ({cx:.0f},{cy:.0f})')
```

## Tarea

Combina el detector YOLO con el controlador de locomoción de B6 para que el robot
se aproxime a la pelota detectada.
```

- [ ] **Step 3: Create b8-lidar.md**

```markdown
---
title: "B8: LiDAR y Evitación de Obstáculos"
description: "Usa /scan (LaserScan 360°) para navegar evitando obstáculos reactivamente."
---

# B8: LiDAR y Evitación de Obstáculos

## El topic /scan

```bash
ros2 topic echo /scan --once
# angle_min: -3.14159  # -180°
# angle_max:  3.14159  # +180°
# angle_increment: 0.01745  # 1° por rayo
# ranges: [3.5, 3.5, 0.8, 0.8, ...]  # metros; 3.5 = sin obstáculo
```

## Evitación reactiva

```python
#!/usr/bin/env python3
import rclpy, math
from rclpy.node import Node
from sensor_msgs.msg import LaserScan
from geometry_msgs.msg import TwistStamped

class ObstacleAvoider(Node):
    def __init__(self):
        super().__init__('obstacle_avoider')
        self.create_subscription(LaserScan, '/scan', self.scan_cb, 10)
        self.pub = self.create_publisher(TwistStamped, '/cmd_vel', 10)

    def scan_cb(self, msg):
        ranges = msg.ranges
        n = len(ranges)
        safe = 0.6  # metros — distancia de seguridad

        def sector(start_deg, end_deg):
            # Extrae mínima distancia en un sector angular
            i0 = int((start_deg + 180) / 360 * n)
            i1 = int((end_deg   + 180) / 360 * n)
            sector_ranges = [r for r in ranges[i0:i1] if 0.05 < r < msg.range_max]
            return min(sector_ranges) if sector_ranges else msg.range_max

        front = sector(-30, 30)
        left  = sector(30,  90)
        right = sector(-90, -30)

        cmd = TwistStamped()
        cmd.header.stamp = self.get_clock().now().to_msg()

        if front < safe:
            if left > right:
                cmd.twist.angular.z =  0.5   # girar izquierda
            else:
                cmd.twist.angular.z = -0.5   # girar derecha
        else:
            cmd.twist.linear.x = 0.15        # avanzar

        self.pub.publish(cmd)
```

## Tarea

Modifica el nodo para que el robot navegue hasta alcanzar la posición `(2.0, 0.0)`
en odometría, evitando obstáculos en el camino.
```

- [ ] **Step 4: Create b9-robocup.md**

```markdown
---
title: "B9: Arquitectura RoboCup — Vision + Brain"
description: "Estudia la arquitectura del robocup_demo y construye un rastreador de pelota."
---

# B9: Arquitectura RoboCup — Vision + Brain

## La arquitectura del robocup_demo

El sistema `robocup_demo` de Booster tiene tres módulos:

```
vision/ ──── YOLOv8 TensorRT ────► /vision/ball_pos, /vision/field_state
brain/  ──── decisión + estrategia ► /cmd_vel, /sport/kick
game_controller/ ── paquetes árbitro ► /game_controller/state
```

El código está en `/opt/booster/robocup_demo/` — léelo, no lo compiles.

```bash
ls /opt/booster/robocup_demo/
# brain/  game_controller/  scripts/  vision/  config/
cat /opt/booster/robocup_demo/vision/src/vision_node.cpp | head -60
```

## Ejercicio: rastreador de pelota con visión

Combina detección YOLO (B7) con locomoción (B2) para seguir la pelota:

```python
#!/usr/bin/env python3
import rclpy, numpy as np
from rclpy.node import Node
from sensor_msgs.msg import Image
from geometry_msgs.msg import TwistStamped
from ultralytics import YOLO

class BallTracker(Node):
    BALL_CLASS = 32

    def __init__(self):
        super().__init__('ball_tracker')
        self.model = YOLO('yolov8n.pt')
        self.create_subscription(Image, '/camera/image_raw', self.callback, 10)
        self.pub = self.create_publisher(TwistStamped, '/cmd_vel', 10)

    def callback(self, msg):
        bgr = np.frombuffer(msg.data, dtype=np.uint8).reshape(msg.height, msg.width, 3)
        results = self.model(bgr, verbose=False, classes=[self.BALL_CLASS])
        cmd = TwistStamped()
        cmd.header.stamp = self.get_clock().now().to_msg()
        if results[0].boxes:
            box = results[0].boxes[0]
            cx = float((box.xyxy[0][0] + box.xyxy[0][2]) / 2)
            error = (cx - msg.width / 2) / msg.width
            cmd.twist.angular.z = -error * 1.0
            cmd.twist.linear.x  =  0.12
        self.pub.publish(cmd)
```

## Tarea

Agrega un servicio `/sport/dance1` para celebrar cuando el robot llegue a menos de
0.5 m de la pelota (usa el canal de profundidad de B6).
```

- [ ] **Step 5: Create b10-mision.md**

```markdown
---
title: "B10: Misión Autónoma Integrada"
description: "Capstone: integra B2–B9 en una misión completa — caminar, detectar, reportar, regresar."
---

# B10: Misión Autónoma Integrada

## La misión

1. Caminar desde el origen hasta el punto de inspección `(2.0, 0.0)`
2. Detectar y clasificar el objeto más cercano con YOLO
3. Ejecutar comportamiento de reporte (`hello`)
4. Regresar al origen

## Estructura del nodo

```python
#!/usr/bin/env python3
import rclpy, math, numpy as np
from rclpy.node import Node
from nav_msgs.msg import Odometry
from sensor_msgs.msg import Image, LaserScan
from geometry_msgs.msg import TwistStamped
from std_srvs.srv import Trigger
from ultralytics import YOLO
from enum import Enum

class State(Enum):
    NAVIGATE_TO_TARGET = 1
    DETECT_OBJECT      = 2
    REPORT             = 3
    RETURN_HOME        = 4
    DONE               = 5

class AutonomousMission(Node):
    TARGET = (2.0, 0.0)

    def __init__(self):
        super().__init__('autonomous_mission')
        self.model  = YOLO('yolov8n.pt')
        self.state  = State.NAVIGATE_TO_TARGET
        self._x     = 0.0
        self._y     = 0.0
        self._th    = 0.0
        self._front = 3.5
        self._detection = None

        self.pub = self.create_publisher(TwistStamped, '/cmd_vel', 10)
        self.create_subscription(Odometry,  '/odom',              self._odom_cb, 10)
        self.create_subscription(LaserScan, '/scan',              self._scan_cb, 10)
        self.create_subscription(Image,     '/camera/image_raw',  self._img_cb, 10)
        self.create_timer(0.1, self._tick)

    def _odom_cb(self, msg):
        self._x  = msg.pose.pose.position.x
        self._y  = msg.pose.pose.position.y
        q = msg.pose.pose.orientation
        self._th = math.atan2(2*(q.w*q.z + q.x*q.y), 1 - 2*(q.y**2 + q.z**2))

    def _scan_cb(self, msg):
        front = [r for r in msg.ranges[0:30] + msg.ranges[-30:] if 0.05 < r < 3.5]
        self._front = min(front) if front else 3.5

    def _img_cb(self, msg):
        if self.state != State.DETECT_OBJECT:
            return
        bgr = np.frombuffer(msg.data, dtype=np.uint8).reshape(msg.height, msg.width, 3)
        results = self.model(bgr, verbose=False)
        if results[0].boxes:
            self._detection = self.model.names[int(results[0].boxes[0].cls[0])]

    def _navigate_to(self, tx, ty, tolerance=0.25):
        dx = tx - self._x
        dy = ty - self._y
        dist = math.sqrt(dx**2 + dy**2)
        if dist < tolerance:
            return True
        desired_th = math.atan2(dy, dx)
        angle_err  = math.atan2(math.sin(desired_th - self._th),
                                math.cos(desired_th - self._th))
        cmd = TwistStamped()
        cmd.header.stamp = self.get_clock().now().to_msg()
        if abs(angle_err) > 0.2:
            cmd.twist.angular.z = 0.4 * (1 if angle_err > 0 else -1)
        elif self._front > 0.5:
            cmd.twist.linear.x = min(0.2, dist)
        else:
            cmd.twist.angular.z = 0.4
        self.pub.publish(cmd)
        return False

    def _call_sport(self, behavior):
        client = self.create_client(Trigger, f'/sport/{behavior}')
        if client.wait_for_service(timeout_sec=2.0):
            client.call_async(Trigger.Request())

    def _tick(self):
        if self.state == State.NAVIGATE_TO_TARGET:
            if self._navigate_to(*self.TARGET):
                self.get_logger().info('¡Llegué al punto de inspección!')
                self.state = State.DETECT_OBJECT

        elif self.state == State.DETECT_OBJECT:
            if self._detection:
                self.get_logger().info(f'Detectado: {self._detection}')
                self.state = State.REPORT

        elif self.state == State.REPORT:
            self._call_sport('hello')
            self.state = State.RETURN_HOME

        elif self.state == State.RETURN_HOME:
            if self._navigate_to(0.0, 0.0):
                self.get_logger().info('¡Misión completada!')
                self.pub.publish(TwistStamped())
                self.state = State.DONE

def main():
    rclpy.init()
    rclpy.spin(AutonomousMission())
    rclpy.shutdown()
```

## Tarea

Extiende la misión para visitar 3 puntos de inspección antes de regresar,
reportando qué objeto detectó en cada uno.
```

- [ ] **Step 6: Build and verify**
```bash
cd /home/jahir/repos/ros2 && mkdocs build --strict 2>&1 | grep -E "ERROR|built in"
```

- [ ] **Step 7: Commit**
```bash
cd /home/jahir/repos/ros2 && git add docs/booster/b6-camara.md docs/booster/b7-yolo.md docs/booster/b8-lidar.md docs/booster/b9-robocup.md docs/booster/b10-mision.md && git commit -m "feat(booster): add lessons B6-B10"
```

---

*Continues in Part 2: booster_sim_lite.py, Dockerfile.booster, orchestrator routing, rigsa_ros branch.*
