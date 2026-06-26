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
