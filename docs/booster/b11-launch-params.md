---
title: "B11: Launch Files y Parameters"
description: "Organiza múltiples nodos con launch files y configura su comportamiento con parameters en tiempo de ejecución."
---

# B11: Launch Files y Parameters

## ¿Por qué launch files?

Hasta ahora iniciabas cada nodo con `ros2 run` en una terminal separada:

```bash
# Terminal 1
ros2 run booster_sim_lite booster_sim_lite.py booster_obstacles
# Terminal 2
ros2 run booster_b8_lidar b8_obstacle_avoidance.py
```

Un **launch file** lo hace en un solo comando y permite configurar los nodos desde fuera:

```bash
ros2 launch booster_b11_launch b11_obstacle.launch.py safe_distance:=0.8
```

## Tu primer launch file

Los launch files de ROS 2 son scripts Python en `launch/`:

```python
# launch/b11_obstacle.launch.py
from launch import LaunchDescription
from launch.actions import DeclareLaunchArgument
from launch.substitutions import LaunchConfiguration
from launch_ros.actions import Node

def generate_launch_description():
    safe_dist_arg = DeclareLaunchArgument(
        'safe_distance', default_value='0.6',
        description='Distancia de seguridad en metros'
    )
    speed_arg = DeclareLaunchArgument(
        'linear_speed', default_value='0.15',
        description='Velocidad lineal máxima en m/s'
    )

    avoider_node = Node(
        package='booster_b11_launch',
        executable='b11_parameterized_avoider.py',
        name='obstacle_avoider',
        parameters=[{
            'safe_distance': LaunchConfiguration('safe_distance'),
            'linear_speed':  LaunchConfiguration('linear_speed'),
        }]
    )

    return LaunchDescription([safe_dist_arg, speed_arg, avoider_node])
```

```bash
colcon build --packages-select booster_b11_launch --symlink-install
source install/setup.bash

# Usar valores por defecto
ros2 launch booster_b11_launch b11_obstacle.launch.py

# Cambiar parámetros sin recompilar
ros2 launch booster_b11_launch b11_obstacle.launch.py safe_distance:=0.8 linear_speed:=0.1
```

## Parameters: configuración sin recompilar

Los nodos declaran sus parameters en `__init__` y los leen en cada uso:

```python
#!/usr/bin/env python3
import rclpy, math
from rclpy.node import Node
from sensor_msgs.msg import LaserScan
from geometry_msgs.msg import TwistStamped

class ParameterizedAvoider(Node):
    def __init__(self):
        super().__init__('obstacle_avoider')

        # 1. Declarar con valor por defecto y descripción
        self.declare_parameter('safe_distance', 0.6)
        self.declare_parameter('linear_speed',  0.15)
        self.declare_parameter('turn_speed',    0.5)

        self.create_subscription(LaserScan, '/scan', self.scan_cb, 10)
        self.pub = self.create_publisher(TwistStamped, '/cmd_vel', 10)

    def scan_cb(self, msg):
        # 2. Leer en cada callback — permite cambios en caliente
        safe  = self.get_parameter('safe_distance').value
        speed = self.get_parameter('linear_speed').value
        turn  = self.get_parameter('turn_speed').value

        ranges = msg.ranges
        n = len(ranges)

        def sector(start_deg, end_deg):
            i0 = int((start_deg + 180) / 360 * n)
            i1 = int((end_deg   + 180) / 360 * n)
            vals = [r for r in ranges[i0:i1] if 0.05 < r < msg.range_max]
            return min(vals) if vals else msg.range_max

        front = sector(-30, 30)
        left  = sector( 30, 90)
        right = sector(-90, -30)

        cmd = TwistStamped()
        cmd.header.stamp = self.get_clock().now().to_msg()

        if front < safe:
            cmd.twist.angular.z = turn if left > right else -turn
        else:
            cmd.twist.linear.x = speed

        self.pub.publish(cmd)

def main():
    rclpy.init()
    rclpy.spin(ParameterizedAvoider())
    rclpy.shutdown()
```

### Cambiar un parameter en caliente

```bash
# Mientras el nodo corre, sin reiniciarlo:
ros2 param set /obstacle_avoider safe_distance 1.0

# Ver todos los parameters activos:
ros2 param list /obstacle_avoider
ros2 param get /obstacle_avoider safe_distance
```

### Guardar y cargar parameters desde un archivo YAML

```bash
# Guardar estado actual a un archivo
ros2 param dump /obstacle_avoider > my_params.yaml

# Lanzar con un archivo de parámetros
ros2 run booster_b11_launch b11_parameterized_avoider.py \
    --ros-args --params-file my_params.yaml
```

## Varios nodos en un launch file

```python
# Iniciar sim + nodo en un solo comando:
from launch_ros.actions import Node

def generate_launch_description():
    return LaunchDescription([
        Node(
            package='booster_sim_lite',
            executable='booster_sim_lite.py',
            arguments=['booster_obstacles'],
            name='simulator',
        ),
        Node(
            package='booster_b11_launch',
            executable='b11_parameterized_avoider.py',
            name='avoider',
            parameters=[{'safe_distance': 0.7}],
        ),
    ])
```

## Tarea

1. Crea un launch file que inicie **simultáneamente** el evitador de obstáculos y
   el monitor de odometría de B3.
2. Agrega un parameter `log_interval` al monitor de odometría que controle
   cada cuántos mensajes imprime la posición (por defecto: `10`).
