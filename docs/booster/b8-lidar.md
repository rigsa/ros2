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
