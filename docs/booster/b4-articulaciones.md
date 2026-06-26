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
