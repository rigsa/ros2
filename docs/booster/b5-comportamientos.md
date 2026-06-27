---
title: "B5: Comportamientos y Servicios"
description: "Activa comportamientos predefinidos del K1 usando servicios ROS 2 /sport/*."
---

# B5: Comportamientos y Servicios

## Servicios disponibles

```bash
ros2 service list | grep sport
# /sport/stand_up
# /sport/stand_down
# /sport/hello
# /sport/stretch
# /sport/dance1
# /sport/dance2
# /sport/recovery_stand
# /sport/balance_stand
# /sport/dock
# /sport/undock
```

Todos son de tipo `std_srvs/Trigger` — no tienen argumentos, solo devuelven éxito/fallo.

## Cliente de servicio

```python
#!/usr/bin/env python3
import rclpy
from rclpy.node import Node
from std_srvs.srv import Trigger

class BehaviorClient(Node):
    def __init__(self):
        super().__init__('behavior_client')

    def call(self, behavior: str) -> bool:
        client = self.create_client(Trigger, f'/sport/{behavior}')
        if not client.wait_for_service(timeout_sec=3.0):
            self.get_logger().error(f'Servicio /sport/{behavior} no disponible')
            return False
        future = client.call_async(Trigger.Request())
        rclpy.spin_until_future_complete(self, future)
        result = future.result()
        self.get_logger().info(f'{behavior}: {result.message}')
        return result.success

def main():
    rclpy.init()
    node = BehaviorClient()
    node.call('hello')      # saludar
    node.call('dance1')     # bailar
    node.call('stand_up')   # ponerse de pie
    rclpy.shutdown()
```

## Tarea

Crea un nodo que active la secuencia: `hello` → esperar 2 s → `dance1` → `recovery_stand`.

---

## Creando tu propio servidor de servicio

Un cliente llama servicios; un servidor los atiende. El mismo tipo `Trigger` puede usarse en ambos lados.

```python
#!/usr/bin/env python3
import rclpy
from rclpy.node import Node
from nav_msgs.msg import Odometry
from std_srvs.srv import Trigger
import math

class RobotStatusServer(Node):
    def __init__(self):
        super().__init__('robot_status_server')
        self._x = 0.0; self._y = 0.0; self._th = 0.0
        self.create_subscription(Odometry, '/odom', self._odom_cb, 10)
        # Registrar el servidor — callback se llama al recibir cada petición
        self.create_service(Trigger, '/robot/status', self._status_cb)
        self.get_logger().info('Servidor /robot/status listo')

    def _odom_cb(self, msg):
        self._x  = msg.pose.pose.position.x
        self._y  = msg.pose.pose.position.y
        q = msg.pose.pose.orientation
        self._th = math.atan2(2*(q.w*q.z + q.x*q.y), 1 - 2*(q.y**2 + q.z**2))

    def _status_cb(self, request, response):
        response.success = True
        response.message = (
            f"x={self._x:.2f} y={self._y:.2f} "
            f"hdg={math.degrees(self._th):.1f}°"
        )
        return response

def main():
    rclpy.init()
    rclpy.spin(RobotStatusServer())
    rclpy.shutdown()
```

```bash
# Terminal 1 — iniciar el servidor
ros2 run booster_b5_behaviors b5_status_server.py

# Terminal 2 — llamarlo desde la línea de comandos
ros2 service call /robot/status std_srvs/srv/Trigger {}

# O desde otro nodo Python
node.call('status')   # usando el BehaviorClient de la primera parte
```

### Diferencia clave: cliente vs. servidor

| | Cliente | Servidor |
|---|---------|---------|
| Crea con | `create_client(Tipo, nombre)` | `create_service(Tipo, nombre, callback)` |
| Inicia la comunicación | Sí — llama `call_async()` | No — espera peticiones |
| Necesita girar | Sí — `spin_until_future_complete` | Sí — `rclpy.spin()` |
| Callback recibe | resultado | `(request, response)` |

## Tarea extendida

Crea un nodo que sirva `/robot/status` y además suscriba `/battery_state`.
Incluye el porcentaje de batería en la respuesta del servicio.
