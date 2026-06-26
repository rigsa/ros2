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
