---
title: "Go2 EDU: Hardware en profundidad"
description: "Análisis completo del hardware del Go2 EDU: motores, sensores, compute, SDK2 de bajo nivel, D1 arm y variantes."
---

# Go2 EDU: Hardware en profundidad

Este documento va más allá del bridge de alto nivel y explora todo lo que el Go2 EDU
expone al desarrollador: cada sensor, cada joint, cada topic DDS y cada llamada de bajo
nivel disponible para investigación.

## Variantes del Go2 y qué incluye cada una

| Característica | Go2 Air | Go2 Pro | Go2-X | Go2 EDU Std | Go2 EDU Plus |
|---|---|---|---|---|---|
| Precio aprox. | $2 590 | $3 799 | $7 600 | $13 000 | $16 000+ |
| SDK / ROS 2 | ✗ | ✗ | ✓ | ✓ | ✓ |
| Compute | CPU básico | CPU básico | Orin NX | Orin Nano 40 TOPS | **Orin NX 100 TOPS** |
| LiDAR | L1 4D | L1 4D | L1 4D | L1 4D + XT16 | L1 4D + upgradeable |
| Batería | 8 000 mAh | 8 000 mAh | 8 000 mAh | 15 000 mAh | 15 000 mAh |
| Carga útil | 3 kg | 3 kg | 5 kg | 5 kg | **8 kg (12 kg límite)** |
| D1 arm (acc.) | ✗ | ✗ | Opcional | Opcional | **✓ Compatible** |

!!! warning "Sin SDK no hay ROS 2"
    El Go2 Air y Pro no dan acceso al SDK. Para el curso (U1-U12) y cualquier
    investigación personalizada **necesitas Go2-X, EDU Standard o EDU Plus**.
    Esto no puede desbloquearse con firmware — es una diferencia de hardware.

## Arquitectura de cómputo

### NVIDIA Jetson Orin NX (EDU Plus, 100 TOPS)

```
CPU: 8-core ARM Cortex-A78AE (64-bit)
GPU: 1024-core NVIDIA Ampere
DLA: 2× Deep Learning Accelerator
RAM: 16 GB LPDDR5
Almacenamiento: 64 GB eMMC + microSD
TOPS: 100 (combinando CPU + GPU + DLA)
```

El Orin NX puede ejecutar:
- Inferencia en tiempo real de modelos ViT / YOLOv8 (GPU)
- SLAM 3D (Point-LIO) a 10 Hz (CPU + DLA)
- Dos nodos ROS 2 + bridge + teleop simultáneos sin saturación

### NVIDIA Jetson Orin Nano (EDU Standard, 40 TOPS)

```
CPU: 6-core ARM Cortex-A78AE
GPU: 1024-core NVIDIA Ampere (escala reducida)
RAM: 8 GB LPDDR5
TOPS: 40
```

Suficiente para el curso completo (U1-U12) y la mayoría de proyectos de investigación.
Insuficiente para inferencia de modelos >1B parámetros en tiempo real.

## Sistema de actuación: 12 motores

El Go2 tiene **4 patas × 3 joints = 12 DOF**:

```
Pelvis
├── Pierna delantera izquierda (FL)
│   ├── FL_hip    (abducción/aducción)
│   ├── FL_thigh  (flexión del muslo)
│   └── FL_calf   (flexión de la pantorrilla)
├── Pierna delantera derecha (FR)
│   ├── FR_hip
│   ├── FR_thigh
│   └── FR_calf
├── Pierna trasera izquierda (RL)
│   ├── RL_hip
│   ├── RL_thigh
│   └── RL_calf
└── Pierna trasera derecha (RR)
    ├── RR_hip
    ├── RR_thigh
    └── RR_calf
```

Cada motor:
- **Torque máximo**: 45 N·m
- **Velocidad**: hasta 21 rad/s
- **Resolución de posición**: ~0.001 rad
- **Control**: posición, velocidad o torque (según modo)

Desde el SDK2 (`LowCmd`), puedes controlar cada joint individualmente:

```python
from unitree_sdk2py.idl.unitree_go.msg.dds_ import LowCmd_

cmd = LowCmd_()
# Joint 0 = FL_hip, 1 = FL_thigh, 2 = FL_calf
# Joint 3 = FR_hip, ...
# Joint 9 = RL_hip, ...
cmd.motor_cmd[1].q   = 0.67   # ángulo target (rad)
cmd.motor_cmd[1].kp  = 60.0   # rigidez proporcional
cmd.motor_cmd[1].kd  = 5.0    # amortiguamiento
cmd.motor_cmd[1].tau = 0.0    # torque feedforward
```

!!! danger "LowCmd requiere 10 ms de ciclo exacto"
    El control de bajo nivel a través de `LowCmd` requiere enviar comandos cada 2–10 ms.
    Si el ciclo se interrumpe más de 100 ms, el robot entra en modo de seguridad y cae.
    Usa el API de `SportClient` (alto nivel) a menos que seas desarrollador de gaits.

## Suite de sensores

### LiDAR L1 — Unitree 4D

El LiDAR L1 es el sensor principal de percepción del Go2:

| Parámetro | Valor |
|---|---|
| Canales | 16 (por rotación) |
| FOV vertical | 90° (−45° a +45°) |
| FOV horizontal | 360° |
| Rango mínimo | 0.05 m |
| Rango máximo | 20 m (típico), 30 m (interior) |
| Frecuencia | 10 Hz |
| Puntos por segundo | ~240 000 |
| Salida | PointCloud2 en `/utlidar/cloud` |
| Precisión | ±2 cm |

```bash
# Ver la nube de puntos en tiempo real
ros2 topic echo /utlidar/cloud --no-arr   # solo metadatos
ros2 topic hz /utlidar/cloud              # frecuencia actual

# Con RViz2
ros2 run rviz2 rviz2
# Fixed Frame: base_link
# Add → PointCloud2 → /utlidar/cloud
```

Para convertir a LaserScan 2D (lo que usa el bridge del curso):

```bash
ros2 run pointcloud_to_laserscan pointcloud_to_laserscan_node \
  --ros-args \
  -p target_frame:=base_scan \
  -p min_height:=0.1 \
  -p max_height:=0.5 \
  -p angle_min:=-3.14159 \
  -p angle_max:=3.14159
```

### Intel RealSense D435i (profundidad + IMU)

| Canal | Topic | Tipo |
|---|---|---|
| RGB | `/camera/color/image_raw` | `sensor_msgs/Image` |
| Profundidad | `/camera/depth/image_rect_raw` | `sensor_msgs/Image` |
| Nube 3D | `/camera/depth/color/points` | `sensor_msgs/PointCloud2` |
| IMU interno | `/camera/imu` | `sensor_msgs/Imu` |

```python
# Usar la cámara de profundidad para estimar distancia a obstáculo frontal
from sensor_msgs.msg import Image
import numpy as np

def depth_cb(self, msg: Image):
    # El D435i publica uint16 en mm
    data = np.frombuffer(msg.data, dtype=np.uint16)
    data = data.reshape(msg.height, msg.width)
    centro = data[msg.height // 2, msg.width // 2]
    dist_m = centro / 1000.0
    self.get_logger().info(f"Distancia frontal: {dist_m:.2f} m")
```

### 5 Cámaras fish-eye estéreo

El Go2 EDU lleva 5 cámaras de ojo de pez (amplio ángulo) que permiten:
- Visión 360° del entorno inmediato
- Estimación de profundidad stereo
- Detección de obstáculos en las patas

Topics (nombres aproximados, varían por firmware):
- `/front_camera/image_raw`
- `/rear_camera/image_raw`
- `/left_camera/image_raw`
- `/right_camera/image_raw`
- `/top_camera/image_raw`

### 4 Sensores de fuerza en las patas

Cada pata tiene un sensor que mide la fuerza de contacto con el suelo:

```python
from unitree_sdk2py.idl.unitree_go.msg.dds_ import LowState_

def lowstate_cb(self, msg: LowState_):
    # foot_force: [FL, FR, RL, RR] en Newtons
    fl_force = msg.foot_force[0]
    fr_force = msg.foot_force[1]
    rl_force = msg.foot_force[2]
    rr_force = msg.foot_force[3]
    
    # Si la fuerza es 0, esa pata está en el aire
    patas_en_suelo = sum(1 for f in msg.foot_force if f > 10.0)
    self.get_logger().info(f"Patas en suelo: {patas_en_suelo}/4")
```

Aplicaciones: detección de terreno irregular, clasificación de superficie, control adaptativo de contacto.

### IMU (dentro del LiDAR L1)

El LiDAR L1 contiene una IMU que publica:

```python
# Via DDS directo:
from unitree_sdk2py.idl.unitree_go.msg.dds_ import LowState_

def state_cb(self, msg: LowState_):
    imu = msg.imu_state
    roll  = imu.rpy[0]   # radianes
    pitch = imu.rpy[1]
    yaw   = imu.rpy[2]
    
    gyro_x = imu.gyroscope[0]   # rad/s
    gyro_y = imu.gyroscope[1]
    gyro_z = imu.gyroscope[2]
    
    acc_x = imu.accelerometer[0]   # m/s²
```

En ROS 2 (a través del bridge): `/imu/data` (si el bridge lo republica).

## Temas DDS — mapa completo

El SDK2 usa Fast DDS sobre la red del robot. Topics disponibles:

| Nombre DDS | Descripción | IDL |
|---|---|---|
| `rt/sportmodestate` | Posición, velocidad, modo de marcha | `SportModeState_` |
| `rt/lf/lowstate` | Estado de joints, IMU, fuerza de patas, batería | `LowState_` |
| `rt/lf/lowcmd` | Comando de joints de bajo nivel | `LowCmd_` |
| `rt/utlidar/cloud` | Nube de puntos del LiDAR L1 | `PointCloud2` |
| `rt/utlidar/imu` | IMU del LiDAR | `IMUState_` |
| `rt/api/sport/request` | Comandos del SportClient | `Request_` |
| `rt/api/sport/response` | Respuestas del SportClient | `Response_` |
| `rt/audio/sdk/tomic` | Audio desde el micrófono del robot | Audio |

### SportModeState — lo que lee el bridge de `/odom`

```python
from unitree_sdk2py.idl.unitree_go.msg.dds_ import SportModeState_

# Campos principales:
msg.position        # [x, y, z] en metros (frame del mundo)
msg.velocity        # [vx, vy, vz] m/s
msg.imu_state.rpy   # [roll, pitch, yaw] radianes
msg.imu_state.gyroscope     # velocidades angulares rad/s
msg.imu_state.accelerometer # aceleración m/s²
msg.foot_position_body      # posición de cada pata relativa al cuerpo
msg.foot_speed_body         # velocidad de cada pata
msg.mode                    # modo de marcha actual
msg.gait_type               # tipo de gait (0=idle, 1=trot, 2=run)
msg.foot_raise_height       # altura de elevación de pata (m)
msg.body_height             # altura del cuerpo sobre el suelo (m)
```

## Modos de marcha y comportamientos

### Gait types disponibles

| ID | Nombre | Descripción |
|---|---|---|
| 0 | Idle | Sin movimiento de patas |
| 1 | Trot | Trote (2 patas en el aire, diagonales) |
| 2 | Running trot | Trote rápido |
| 3 | Climbing | Modo de escalada de escalones |
| 4 | Crawl | Rastro (4 puntos de apoyo siempre) |

### Sport behaviors completos (via SportClient)

| ID | Nombre | Descripción |
|---|---|---|
| 1001 | Damp | Amortiguamiento — robot afloja joints |
| 1002 | BalanceStand | Se para y equilibra en lugar |
| 1003 | StopMove | Para el movimiento |
| 1004 | StandUp | Se levanta desde el suelo |
| 1005 | StandDown | Se sienta |
| 1006 | RecoveryStand | Recuperación si volcó |
| 1007 | Euler(roll, pitch, yaw) | Inclina el cuerpo en ángulos |
| 1008 | Move(vx, vy, vyaw) | Movimiento base |
| 1009 | Sit | Se sienta |
| 1010 | RiseSit | Se levanta desde sentado |
| 1013 | BodyHeight(h) | Cambia altura del cuerpo |
| 1014 | FootRaiseHeight(h) | Cambia altura de elevación de pata |
| 1016 | Hello | Saluda con la pata |
| 1017 | Stretch | Se estira |
| 1022 | Dance1 | Baile 1 |
| 1023 | Dance2 | Baile 2 |
| 1028 | Pose(pitch) | Postura de modelo |
| 1030 | FrontFlip | Voltereta frontal |
| 1031 | FrontJump | Salto frontal |
| 1032 | FrontPounce | Salto sobre objetivo |

Para behaviors parametrizados (Euler, Move, BodyHeight) usa el payload JSON del SportClient:

```python
import json

# Cambiar altura del cuerpo a 0.25 m
data = json.dumps({"data": 0.25})
sport_client.SendApiRequest(1013, data)
```

## Brazo D1 — manipulación embarcada

El [Unitree D1](https://www.unitree.com/d1) es el brazo robótico diseñado para el Go2:

| Característica | Valor |
|---|---|
| DOF | 6 (+ 1 gripper) |
| Alcance | 600 mm |
| Carga máxima | 500 g (extendido) |
| Peso del brazo | 2.5 kg |
| Interfaces | CAN bus o Ethernet |
| SDK | `unitree_arm_sdk` |

El D1 se monta sobre el cuerpo del Go2 EDU (con la plataforma de montaje). El control
se realiza con un SDK separado que se integra con el de locomoción:

```python
from unitree_arm_sdk import ArmClient

arm = ArmClient("d1")
arm.init()

# Mover a posición cartesiana (x, y, z en metros desde la base del brazo)
arm.moveTo(x=0.3, y=0.0, z=0.1)

# Abrir/cerrar gripper (0.0=cerrado, 1.0=abierto)
arm.setGripper(0.8)
```

Para integración con ROS 2:

```bash
# Paquete de la comunidad con interfaz ROS 2 para D1:
git clone https://github.com/unitreerobotics/unitree_arm_ros2.git
```

## Variante Go2-W (con ruedas)

El [Go2-W](https://www.unitree.com/go2w) añade ruedas sobre las patas traseras.
Las patas delanteras siguen siendo articuladas. Esto permite:
- Velocidad aumentada en terreno plano (modo rueda)
- Capacidad de escalar obstáculos (modo pata)
- Transición automática entre modos

La interfaz ROS 2 es idéntica al Go2 estándar — `cmd_vel`, `odom`, `scan`, `/sport/*`.
El SDK añade control de las ruedas pero el bridge del curso funciona sin cambios.

## Red y configuración de entorno

```bash
# 1. Conectar Go2 EDU por Ethernet (IP típica: 192.168.123.161)
# O por WiFi (el Go2 actúa como AP: SSID Unitree_Go2_XXXX)

# 2. Configurar la interfaz de red:
export RMW_IMPLEMENTATION=rmw_cyclonedds_cpp
export UNITREE_WIRED_ETHERNET="eth0"    # o wlan0 para WiFi

# 3. Verificar conectividad
ping 192.168.123.161

# 4. Verificar que el DDS está disponible (requiere unitree_sdk2py)
python3 -c "
from unitree_sdk2py.core.channel import ChannelFactory
ChannelFactory.Instance().Init(0, 'eth0')
print('DDS OK')
"

# 5. Ver topics DDS disponibles
# (no es ros2 topic list — es el bus DDS interno)
from unitree_sdk2py.core.channel import ChannelFactory
```

## Acceso SSH al robot

```bash
# SSH al Jetson Orin integrado
ssh unitree@192.168.123.18    # contraseña: 123

# Desde el Jetson puedes correr el bridge directamente:
python3 ~/unitree_ros2_bridge.py --network_interface eth0
```

## Herramientas de diagnóstico

```bash
# Estado de batería en tiempo real
ros2 topic echo /battery_state

# Verificar odometría (posición del robot)
ros2 topic echo /odom --field pose.pose.position

# Frecuencia del LiDAR
ros2 topic hz /scan     # ~10 Hz esperado
ros2 topic hz /utlidar/cloud  # ~10 Hz en el DDS

# Ver la nube de puntos del LiDAR
ros2 run rviz2 rviz2 &

# Calibrar IMU (necesario una vez por sesión en autonomy_stack_go2)
ros2 run calibrate_imu calibrate_imu
```
