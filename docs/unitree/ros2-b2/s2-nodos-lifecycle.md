# S2: Nodos Lifecycle — Gestión de Estado para Drivers de Hardware

## Objetivos

- Comprender el ciclo de vida (lifecycle) de nodos ROS 2 y sus estados
- Implementar un driver de hardware del B2 como nodo lifecycle
- Controlar transiciones de estado desde CLI y desde código
- Integrar la seguridad de hardware en el ciclo de vida del nodo

---

## ¿Por qué lifecycle para drivers de hardware?

Los nodos ROS 2 estándar se conectan y publican inmediatamente al lanzarse. Para drivers de hardware esto es peligroso:

```
Nodo estándar:
  __init__() → conecta → publica → el robot ya se mueve

Nodo lifecycle:
  __init__() → configura → activa → publica (solo si hardware verificado)
```

El modelo lifecycle permite separar:
1. **Construcción** — crear el objeto Python, sin hardware
2. **Configuración** — abrir conexiones, verificar sensores, cargar parámetros
3. **Activación** — comenzar a publicar / suscribirse
4. **Desactivación** — parar publicaciones (el nodo sigue en memoria)
5. **Limpieza** — liberar recursos de hardware
6. **Destrucción** — eliminar el nodo

---

## Diagrama de estados lifecycle

```
         configure()
[Unconfigured] ────────────── [Inactive]
                               │     ↑
                    activate() │     │ deactivate()
                               ↓     │
                            [Active]
                               │
                    cleanup()  │   errorprocess()
[Unconfigured] ◄───────────────┘   ────► [Finalized]
```

| Estado         | Describe                                   | Operaciones de hardware |
|----------------|--------------------------------------------|------------------------|
| `Unconfigured` | Nodo creado, sin recursos                  | Ninguna                |
| `Inactive`     | Recursos asignados, hardware verificado    | Monitoreo pasivo       |
| `Active`       | Publicando / recibiendo comandos           | Todas                  |
| `Finalized`    | Estado terminal (error irrecuperable)      | Ninguna                |

---

## Implementación: driver lifecycle para el B2

```python title="s2_b2_lifecycle_driver.py"
#!/usr/bin/env python3
"""
Driver lifecycle para el B2.
- configure: verifica bridge activo y parámetros de red
- activate:  inicia publicación de estado y suscripción a /cmd_vel
- deactivate: para movimiento y publicaciones

Funciona en sim_lite y en el B2 real sin cambios.
"""
import rclpy
from rclpy.lifecycle import LifecycleNode, TransitionCallbackReturn, State
from rclpy.lifecycle import Publisher
from nav_msgs.msg import Odometry
from geometry_msgs.msg import Twist
from sensor_msgs.msg import LaserScan
from std_msgs.msg import String
import time, threading

from sdk2_bridge_sim import LocoClientSim as LocoClient  # (1)!

# Robot real:
# from unitree_sdk2py.b2.loco_client import LocoClient

class B2LifecycleDriver(LifecycleNode):  # (2)!

    def __init__(self):
        super().__init__("b2_driver")
        self._loco: LocoClient | None = None
        self._status_pub: Publisher | None = None
        self._watchdog_timer = None
        self._last_cmd = time.time()

        # Parámetro: timeout watchdog (s)
        self.declare_parameter("watchdog_timeout", 3.0)
        self.declare_parameter("max_speed", 0.5)

    # ── Transiciones lifecycle ────────────────────────────────

    def on_configure(self, state: State) -> TransitionCallbackReturn:  # (3)!
        """Reserva recursos y verifica conectividad."""
        self.get_logger().info("Configurando driver B2...")
        try:
            self._loco = LocoClient()
            self._loco.Init()
            self._loco.SwitchGait(1)
            self.get_logger().info("LocoClient iniciado correctamente")

            # Publisher de estado (solo reserva, no publica aún)
            self._status_pub = self.create_lifecycle_publisher(
                String, "/b2/driver_status", 10)
            return TransitionCallbackReturn.SUCCESS
        except Exception as e:
            self.get_logger().error(f"Error en configuración: {e}")
            return TransitionCallbackReturn.FAILURE

    def on_activate(self, state: State) -> TransitionCallbackReturn:  # (4)!
        """Activa publicaciones y suscripciones."""
        self.get_logger().info("Activando driver B2...")
        self._status_pub.on_activate(state)

        # Suscripción a comandos de velocidad
        self._cmd_sub = self.create_subscription(
            Twist, "/cmd_vel", self._cmd_vel_cb, 10)

        # Odometría de salida
        self._odom_sub = self.create_subscription(
            Odometry, "/odom", self._odom_cb, 10)

        # Watchdog timer
        timeout = self.get_parameter("watchdog_timeout").value
        self._watchdog_timer = self.create_timer(1.0, self._watchdog_cb)
        self._last_cmd = time.time()

        self._publish_status("active")
        return TransitionCallbackReturn.SUCCESS

    def on_deactivate(self, state: State) -> TransitionCallbackReturn:
        """Para movimiento de forma segura, desactiva publicaciones."""
        self.get_logger().info("Desactivando driver B2 — parando robot")
        if self._loco:
            self._loco.StopMove()
        if self._watchdog_timer:
            self._watchdog_timer.cancel()

        self._status_pub.on_deactivate(state)
        self._publish_status("inactive")
        return TransitionCallbackReturn.SUCCESS

    def on_cleanup(self, state: State) -> TransitionCallbackReturn:
        """Libera recursos de hardware."""
        self.get_logger().info("Limpiando driver B2...")
        if self._loco:
            self._loco.StopMove()
        self._loco = None
        return TransitionCallbackReturn.SUCCESS

    def on_shutdown(self, state: State) -> TransitionCallbackReturn:
        if self._loco:
            self._loco.StopMove()
        return TransitionCallbackReturn.SUCCESS

    # ── Callbacks ─────────────────────────────────────────────

    def _cmd_vel_cb(self, msg: Twist):
        max_speed = self.get_parameter("max_speed").value
        vx   = max(-max_speed, min(max_speed, msg.linear.x))
        vy   = max(-max_speed, min(max_speed, msg.linear.y))
        vyaw = max(-1.5, min(1.5, msg.angular.z))
        self._loco.Move(vx, vy, vyaw)
        self._last_cmd = time.time()

    def _odom_cb(self, msg: Odometry):
        # Procesar odometría si necesario
        pass

    def _watchdog_cb(self):
        """Para el robot si no recibe comandos en 'watchdog_timeout' segundos."""
        timeout = self.get_parameter("watchdog_timeout").value
        if time.time() - self._last_cmd > timeout:
            self.get_logger().warn("Watchdog: sin /cmd_vel — parando robot")
            self._loco.StopMove()

    def _publish_status(self, status: str):
        if self._status_pub and self._status_pub.is_activated:
            msg = String()
            msg.data = status
            self._status_pub.publish(msg)


def main():
    rclpy.init()
    driver = B2LifecycleDriver()
    rclpy.spin(driver)
    driver.destroy_node()
    rclpy.shutdown()

if __name__ == "__main__":
    main()
```

1. `sdk2_bridge_sim` traduce `LocoClient` a `/cmd_vel` ROS 2 del sim_lite
2. `LifecycleNode` en lugar de `Node` — hereda todas las transiciones de estado
3. `on_configure`: se llama al ejecutar `ros2 lifecycle set /b2_driver configure`
4. `on_activate`: solo aquí el robot recibe comandos de verdad

---

## Control del lifecycle desde CLI

```bash title="Terminal — controlar el nodo"
# Lanzar el driver (en estado Unconfigured)
ros2 run tu_paquete s2_b2_lifecycle_driver

# En otra terminal — ver el estado actual
ros2 lifecycle get /b2_driver

# Transiciones
ros2 lifecycle set /b2_driver configure    # → Inactive
ros2 lifecycle set /b2_driver activate     # → Active
ros2 lifecycle set /b2_driver deactivate   # → Inactive (robot para)
ros2 lifecycle set /b2_driver cleanup      # → Unconfigured
```

---

## Orquestar el lifecycle desde código

```python title="s2_lifecycle_manager.py"
#!/usr/bin/env python3
"""Gestiona el ciclo de vida del driver B2 de forma programática."""
import rclpy
from rclpy.node import Node
from lifecycle_msgs.srv import ChangeState, GetState
from lifecycle_msgs.msg import Transition

class LifecycleManager(Node):
    def __init__(self, managed_node: str):
        super().__init__("lifecycle_manager")
        self._change = self.create_client(
            ChangeState, f"/{managed_node}/change_state")
        self._get = self.create_client(
            GetState, f"/{managed_node}/get_state")
        self._change.wait_for_service(timeout_sec=5.0)
        self._get.wait_for_service(timeout_sec=5.0)

    def _transition(self, transition_id: int):
        req = ChangeState.Request()
        req.transition.id = transition_id
        future = self._change.call_async(req)
        rclpy.spin_until_future_complete(self, future, timeout_sec=5.0)
        return future.result().success if future.result() else False

    def configure(self): return self._transition(Transition.TRANSITION_CONFIGURE)
    def activate(self):  return self._transition(Transition.TRANSITION_ACTIVATE)
    def deactivate(self):return self._transition(Transition.TRANSITION_DEACTIVATE)
    def cleanup(self):   return self._transition(Transition.TRANSITION_CLEANUP)

def main():
    rclpy.init()
    mgr = LifecycleManager("b2_driver")

    print("Configurando driver...")
    assert mgr.configure(), "Falló configure"
    import time; time.sleep(0.5)

    print("Activando driver...")
    assert mgr.activate(), "Falló activate"
    print("Driver activo — el robot acepta /cmd_vel ahora")

    time.sleep(10.0)  # Operar el robot por 10 segundos

    print("Desactivando driver...")
    mgr.deactivate()
    mgr.cleanup()
    print("Driver limpio")

    mgr.destroy_node()
    rclpy.shutdown()
```

---

## Ejercicios

### Ejercicio 1 — Transiciones básicas
Lanza `s2_b2_lifecycle_driver.py`. Ejecuta las transiciones `configure → activate → deactivate` desde la CLI y observa los mensajes de log en cada transición. ¿Qué sucede en el simulador cuando el nodo se desactiva?

### Ejercicio 2 — Watchdog en acción
Con el driver activo, envía un comando `/cmd_vel` para mover el robot y luego deja de enviar comandos. Observa cuándo el watchdog para el robot. Modifica el parámetro `watchdog_timeout` a 1.0 s y repite.

### Ejercicio 3 — Parámetro dinámico de velocidad máxima
Modifica `max_speed` en tiempo de ejecución con `ros2 param set /b2_driver max_speed 0.2`. Verifica que el robot no supera esta velocidad publicando en `/cmd_vel` con valores más altos.

### Ejercicio 4 — Estado de fallo
Simula un error en `on_configure` (p.ej. lanza una excepción intencionada). Verifica que el nodo entra en `Finalized` y que el robot no recibe comandos. Añade lógica de reintento (`ErrorProcessing` → `Unconfigured`).

### Ejercicio 5 — Lifecycle launch file
Crea un archivo `launch/b2_driver.launch.py` que lance `s2_b2_lifecycle_driver.py` con un `lifecycle_manager` que automáticamente lo lleve a estado `Active` al iniciar.

---

## Pasa al robot real

!!! warning "Orden de inicio en hardware real"
    En el B2 físico, lanza el driver en este orden:

    1. Verifica `sport_mode` activo: `ps aux | grep sport_mode`
    2. Lanza el driver: `ros2 run tu_paquete s2_b2_lifecycle_driver`
    3. `ros2 lifecycle set /b2_driver configure` — verifica logs ("LocoClient iniciado")
    4. Solo entonces: `ros2 lifecycle set /b2_driver activate`

    Si `on_configure` falla en hardware real, **no ejecutes `activate`**. Investiga la causa antes de continuar.

---

## Referencias

- [ROS 2 Lifecycle Nodes — docs.ros.org](https://docs.ros.org/en/jazzy/Tutorials/Intermediate/Ros2-Launch-Managed-Nodes.html)
- [S5: Interfaces de Alto Nivel — LocoClient](../sdk2/s5-alto-nivel.md)
- [lifecycle_msgs — ROS 2 API](https://docs.ros2.org/foxy/api/lifecycle_msgs/)
