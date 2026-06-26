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
