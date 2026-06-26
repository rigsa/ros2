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
