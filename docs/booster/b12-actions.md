---
title: "B12: Actions — Tareas de Larga Duración"
description: "Aprende el tercer patrón de comunicación de ROS 2: actions con meta, retroalimentación y resultado."
---

# B12: Actions — Tareas de Larga Duración

## Los tres patrones de comunicación de ROS 2

| Patrón | Cuándo usarlo | Ejemplo K1 |
|--------|--------------|------------|
| **Topic** (pub/sub) | Datos continuos, sin respuesta esperada | `/odom`, `/scan`, `/cmd_vel` |
| **Service** | Operación instantánea con respuesta | `/sport/hello` — ejecutar y listo |
| **Action** | Tarea larga, con progreso y cancelación | "ve a (2, 0)" — puedo ver el avance y cancelar |

Un **Action** tiene tres partes:

```
Cliente → [Goal]      → Servidor   # "ve a (2.0, 0.0)"
Cliente ← [Feedback]  ← Servidor   # "distancia restante: 1.4 m"  (periódico)
Cliente ← [Result]    ← Servidor   # "llegué: posición final (2.01, 0.02)"
```

## La interfaz `GoTo.action`

Las interfaces de action se definen en archivos `.action` con tres secciones separadas por `---`:

```
# Definición en rigsa_ros_booster/action/GoTo.action

# Goal — qué queremos lograr
float64 x
float64 y
---
# Result — qué ocurrió al terminar
bool    success
float64 final_x
float64 final_y
---
# Feedback — progreso periódico mientras se ejecuta
float64 distance_remaining
float64 heading_error
```

```bash
# Compilar el paquete para generar el código Python de la interfaz
colcon build --packages-select rigsa_ros_booster --symlink-install
source install/setup.bash

# Verificar que la interfaz está disponible
ros2 interface show rigsa_ros_booster/action/GoTo
```

## Servidor de acción: navegación con retroalimentación

El servidor recibe la meta, ejecuta la tarea en un callback `execute`, publica
feedback periódicamente y devuelve un resultado.

```python
#!/usr/bin/env python3
import rclpy, math, threading
from rclpy.node import Node
from rclpy.action import ActionServer, CancelResponse, GoalResponse
from rclpy.executors import MultiThreadedExecutor
from nav_msgs.msg import Odometry
from geometry_msgs.msg import TwistStamped
from rigsa_ros_booster.action import GoTo

class NavigateToServer(Node):
    def __init__(self):
        super().__init__('navigate_to_server')
        self._lock = threading.Lock()
        self._x = self._y = self._th = 0.0

        self.create_subscription(Odometry, '/odom', self._odom_cb, 10)
        self._pub = self.create_publisher(TwistStamped, '/cmd_vel', 10)

        self._action_server = ActionServer(
            self, GoTo, '/navigate_to',
            execute_callback=self._execute,
            goal_callback=lambda _: GoalResponse.ACCEPT,
            cancel_callback=lambda _: CancelResponse.ACCEPT,
        )
        self.get_logger().info('Servidor /navigate_to listo')

    def _odom_cb(self, msg):
        with self._lock:
            self._x = msg.pose.pose.position.x
            self._y = msg.pose.pose.position.y
            q = msg.pose.pose.orientation
            self._th = math.atan2(2*(q.w*q.z + q.x*q.y),
                                  1 - 2*(q.y**2 + q.z**2))

    def _execute(self, goal_handle):
        tx, ty = goal_handle.request.x, goal_handle.request.y
        self.get_logger().info(f'Meta recibida: ({tx:.2f}, {ty:.2f})')
        rate = self.create_rate(10)

        while rclpy.ok():
            if goal_handle.is_cancel_requested:
                goal_handle.canceled()
                self._stop()
                return GoTo.Result(success=False,
                                   final_x=self._x, final_y=self._y)

            with self._lock:
                x, y, th = self._x, self._y, self._th

            dx = tx - x;  dy = ty - y
            dist = math.sqrt(dx**2 + dy**2)

            fb = GoTo.Feedback()
            fb.distance_remaining = dist
            fb.heading_error = math.atan2(
                math.sin(math.atan2(dy, dx) - th),
                math.cos(math.atan2(dy, dx) - th))
            goal_handle.publish_feedback(fb)

            if dist < 0.25:
                break

            desired_th = math.atan2(dy, dx)
            angle_err = math.atan2(math.sin(desired_th - th),
                                   math.cos(desired_th - th))
            cmd = TwistStamped()
            cmd.header.stamp = self.get_clock().now().to_msg()
            if abs(angle_err) > 0.2:
                cmd.twist.angular.z = 0.4 * (1 if angle_err > 0 else -1)
            else:
                cmd.twist.linear.x = min(0.2, dist)
            self._pub.publish(cmd)
            rate.sleep()

        self._stop()
        goal_handle.succeed()
        with self._lock:
            fx, fy = self._x, self._y
        return GoTo.Result(success=True, final_x=fx, final_y=fy)

    def _stop(self):
        self._pub.publish(TwistStamped())


def main():
    rclpy.init()
    node = NavigateToServer()
    # MultiThreadedExecutor: necesario para que el servidor pueda
    # procesar callbacks de odom mientras ejecuta una meta
    executor = MultiThreadedExecutor()
    executor.add_node(node)
    executor.spin()
    rclpy.shutdown()
```

!!! note "MultiThreadedExecutor"
    El servidor de acción ejecuta `_execute` en un hilo separado mientras
    `_odom_cb` sigue recibiendo datos. Con `SingleThreadedExecutor` el
    nodo se bloquearía durante la navegación.

## Cliente de acción: enviar metas y escuchar progreso

```python
#!/usr/bin/env python3
import rclpy, math
from rclpy.node import Node
from rclpy.action import ActionClient
from rigsa_ros_booster.action import GoTo

class NavigateToClient(Node):
    def __init__(self):
        super().__init__('navigate_to_client')
        self._client = ActionClient(self, GoTo, '/navigate_to')

    def send_goal(self, x: float, y: float):
        self._client.wait_for_server()
        goal = GoTo.Goal()
        goal.x = x;  goal.y = y
        self.get_logger().info(f'Enviando meta: ({x}, {y})')

        future = self._client.send_goal_async(
            goal,
            feedback_callback=self._on_feedback,
        )
        future.add_done_callback(self._on_accepted)

    def _on_feedback(self, msg):
        d = msg.feedback.distance_remaining
        h = math.degrees(msg.feedback.heading_error)
        self.get_logger().info(f'  dist={d:.2f} m   hdg_err={h:.1f}°')

    def _on_accepted(self, future):
        gh = future.result()
        if not gh.accepted:
            self.get_logger().error('Meta rechazada por el servidor')
            rclpy.shutdown()
            return
        self.get_logger().info('¡Meta aceptada! Esperando resultado...')
        gh.get_result_async().add_done_callback(self._on_result)

    def _on_result(self, future):
        result = future.result().result
        if result.success:
            self.get_logger().info(
                f'¡Llegué! posición final: '
                f'({result.final_x:.2f}, {result.final_y:.2f})')
        else:
            self.get_logger().warn('Navegación cancelada o fallida')
        rclpy.shutdown()


def main():
    rclpy.init()
    node = NavigateToClient()
    node.send_goal(2.0, 0.0)
    rclpy.spin(node)
```

```bash
# Terminal 1 — servidor
ros2 run booster_b12_actions b12_navigate_server.py

# Terminal 2 — cliente
ros2 run booster_b12_actions b12_navigate_client.py

# Ver los goals activos mientras corre
ros2 action list
ros2 action info /navigate_to
```

### Cancelar una meta en progreso

```python
# En el cliente, después de send_goal_async:
import time
time.sleep(2.0)                 # deja avanzar 2 segundos
gh.cancel_goal_async()          # cancela — servidor recibe is_cancel_requested=True
```

## Tarea

Modifica el cliente para que:

1. Envíe **3 waypoints en secuencia**: (1.5, 1.5) → (1.5, −1.5) → (0.0, 0.0).
2. Solo envíe el siguiente waypoint cuando el resultado del anterior sea `success=True`.
3. Al llegar al origen, llame al servicio `/sport/hello` para celebrar.
