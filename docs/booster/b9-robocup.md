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
