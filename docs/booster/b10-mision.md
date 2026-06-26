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

    DETECT_TIMEOUT = 5.0   # segundos máximos esperando detección YOLO

    def __init__(self):
        super().__init__('autonomous_mission')
        self.model  = YOLO('yolov8n.pt')
        self.state  = State.NAVIGATE_TO_TARGET
        self._x     = 0.0
        self._y     = 0.0
        self._th    = 0.0
        self._front = 3.5
        self._detection = None
        self._detect_t  = 0.0   # timestamp when DETECT_OBJECT started

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
        front = [r for r in msg.ranges[165:195] if 0.05 < r < 3.5]
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
                self._detect_t = self.get_clock().now().nanoseconds * 1e-9
                self.state = State.DETECT_OBJECT

        elif self.state == State.DETECT_OBJECT:
            elapsed = self.get_clock().now().nanoseconds * 1e-9 - self._detect_t
            if self._detection:
                self.get_logger().info(f'Detectado: {self._detection}')
                self.state = State.REPORT
            elif elapsed > self.DETECT_TIMEOUT:
                self.get_logger().warn('Tiempo de detección agotado — nada detectado')
                self._detection = 'desconocido'
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
