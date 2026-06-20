# S4: Interfaces de Hardware — ros2_control, JointState y Sensores

## Objetivos

- Comprender el rol de `ros2_control` en el B2
- Leer y publicar `JointState` del robot desde ROS 2
- Integrar el IMU del B2 como fuente de datos para localización
- Publicar datos de hardware de forma idiomática en ROS 2

---

## ros2_control en el B2

`ros2_control` es el framework estándar de ROS 2 para control de hardware. En el B2, el bridge oficial lo implementa parcialmente:

```
Hardware (B2 PC2)
     │  LowState @ 500 Hz (DDS)
     ▼
unitree_ros2_bridge
     │  /joint_states  (sensor_msgs/JointState)  @ 500 Hz
     │  /imu/data      (sensor_msgs/Imu)          @ 500 Hz
     ▼
ros2_control
  ├── JointStateInterface     → leer q, dq de motores
  ├── CommandInterface        → enviar comandos (solo con HW Controller)
  └── ControllerManager       → gestiona lifecycle de controllers
```

!!! warning "CommandInterface en el B2"
    Escribir en los motores vía `CommandInterface` requiere el `UnitreeHWInterface` (disponible en SDK2 C++). En este módulo nos limitamos a **leer** el estado de articulaciones. El envío de comandos se hace vía `LocoClient` (alto nivel) o `LowCmd` (bajo nivel, solo hardware real).

---

## JointState: leer articulaciones en tiempo real

```python title="s4_joint_monitor.py"
#!/usr/bin/env python3
"""
Monitor de articulaciones via /joint_states.
Muestra posición y velocidad de los 12 motores del B2 en tiempo real.
"""
import rclpy
from rclpy.node import Node
from sensor_msgs.msg import JointState
import math

# Nombres de articulaciones del B2 (orden del bridge)
B2_JOINTS = [
    "FL_hip_joint",   "FL_thigh_joint",  "FL_calf_joint",
    "FR_hip_joint",   "FR_thigh_joint",  "FR_calf_joint",
    "RL_hip_joint",   "RL_thigh_joint",  "RL_calf_joint",
    "RR_hip_joint",   "RR_thigh_joint",  "RR_calf_joint",
]

# Rangos seguros de operación (rad)
JOINT_LIMITS = {
    "hip_joint":   (-1.0, 1.0),
    "thigh_joint": (-1.5, 3.4),
    "calf_joint":  (-2.7, -0.8),
}

class JointMonitor(Node):
    def __init__(self):
        super().__init__("joint_monitor")
        self._latest: JointState | None = None
        self.create_subscription(JointState, "/joint_states", self._cb, 10)
        self.create_timer(0.5, self._print_state)  # 2 Hz para visualización

    def _cb(self, msg: JointState):
        self._latest = msg

    def _print_state(self):
        if self._latest is None:
            self.get_logger().info("Esperando /joint_states...")
            return
        msg = self._latest

        import os; os.system("clear")
        print(f"{'Articulación':<22} {'pos (rad)':>10} {'vel (r/s)':>10} {'estado':>10}")
        print("-" * 58)

        for i, name in enumerate(msg.name):
            if i >= len(msg.position):
                break
            pos = msg.position[i]
            vel = msg.velocity[i] if i < len(msg.velocity) else 0.0

            # Verificar límites
            joint_type = next((k for k in JOINT_LIMITS if k in name), None)
            status = "OK"
            if joint_type:
                lo, hi = JOINT_LIMITS[joint_type]
                if pos < lo or pos > hi:
                    status = "⚠ FUERA"  # (1)!

            print(f"{name:<22} {pos:>10.3f} {vel:>10.3f} {status:>10}")

def main():
    rclpy.init()
    try:
        rclpy.spin(JointMonitor())
    except KeyboardInterrupt:
        pass
    rclpy.shutdown()

if __name__ == "__main__":
    main()
```

1. En robot real, articulaciones fuera de rango indican posible fallo mecánico o configuración incorrecta

---

## IMU: integración y filtrado

El B2 publica datos IMU de 6-DoF en `/imu/data`. Para localización robusta, conviene aplicar un filtro complementario:

```python title="s4_imu_filter.py"
#!/usr/bin/env python3
"""
Filtro complementario simple sobre el IMU del B2.
Fusiona giroscopio + acelerómetro para estimar roll y pitch.
"""
import math
import time
import rclpy
from rclpy.node import Node
from sensor_msgs.msg import Imu
from geometry_msgs.msg import Vector3Stamped

ALPHA = 0.98  # Peso del giroscopio en el filtro complementario

class ImuFilter(Node):
    def __init__(self):
        super().__init__("imu_filter")
        self._roll = 0.0
        self._pitch = 0.0
        self._last_t = None

        self._pub = self.create_publisher(Vector3Stamped, "/b2/rpy_filtered", 10)
        self.create_subscription(Imu, "/imu/data", self._cb, 50)

    def _cb(self, msg: Imu):
        now = self.get_clock().now().nanoseconds * 1e-9
        if self._last_t is None:
            self._last_t = now
            return

        dt = now - self._last_t
        self._last_t = now
        if dt <= 0 or dt > 0.5:  # Ignorar saltos de tiempo
            return

        # Ángulos del acelerómetro
        ax = msg.linear_acceleration.x
        ay = msg.linear_acceleration.y
        az = msg.linear_acceleration.z
        acc_roll  = math.atan2(ay, az)
        acc_pitch = math.atan2(-ax, math.sqrt(ay**2 + az**2))

        # Integración del giroscopio
        gx = msg.angular_velocity.x
        gy = msg.angular_velocity.y
        gyro_roll  = self._roll  + gx * dt
        gyro_pitch = self._pitch + gy * dt

        # Filtro complementario
        self._roll  = ALPHA * gyro_roll  + (1 - ALPHA) * acc_roll
        self._pitch = ALPHA * gyro_pitch + (1 - ALPHA) * acc_pitch

        # Yaw del cuaternión (no hay referencia absoluta en acelerómetro)
        q = msg.orientation
        yaw = math.atan2(2*(q.w*q.z + q.x*q.y), 1 - 2*(q.y*q.y + q.z*q.z))

        out = Vector3Stamped()
        out.header = msg.header
        out.vector.x = math.degrees(self._roll)
        out.vector.y = math.degrees(self._pitch)
        out.vector.z = math.degrees(yaw)
        self._pub.publish(out)


def main():
    rclpy.init()
    rclpy.spin(ImuFilter())
    rclpy.shutdown()

if __name__ == "__main__":
    main()
```

---

## Publicar datos de hardware de forma idiomática

Patrón recomendado para cualquier sensor del B2 en ROS 2:

```python title="s4_patron_sensor.py"
#!/usr/bin/env python3
"""
Patrón para publicar datos de hardware desde SDK2 a ROS 2.
Ilustrado con la batería del B2.
"""
import rclpy
from rclpy.node import Node
from sensor_msgs.msg import BatteryState
from sdk2_bridge_sim import SDK2Bridge  # (1)!

class BatteryPublisher(Node):
    def __init__(self):
        super().__init__("battery_publisher")
        self._bridge = SDK2Bridge()
        self._pub = self.create_publisher(BatteryState, "/b2/battery", 1)
        self.create_timer(5.0, self._publish)  # Batería no cambia rápido

    def _publish(self):
        pct = self._bridge.get_battery_pct()  # 0-100
        msg = BatteryState()
        msg.header.stamp = self.get_clock().now().to_msg()
        msg.percentage = pct / 100.0
        msg.power_supply_status = (
            BatteryState.POWER_SUPPLY_STATUS_DISCHARGING
        )
        self._pub.publish(msg)
        if pct < 20:
            self.get_logger().warn(f"Batería baja: {pct}%")  # (2)!

def main():
    rclpy.init()
    rclpy.spin(BatteryPublisher())
    rclpy.shutdown()

if __name__ == "__main__":
    main()
```

1. En robot real reemplaza con `from unitree_sdk2py.b2.sport_client import SportClient` y lee `sport_state.battery_voltage`
2. En robot real, batería < 20% debe activar protocolo de aterrizaje controlado

---

## Ejercicios

### Ejercicio 1 — Monitor de articulaciones
Lanza `s4_joint_monitor.py` y mueve el robot con `ros2 topic pub /cmd_vel`. ¿Qué articulaciones muestran mayor variación de velocidad durante una traslación frontal vs una rotación?

### Ejercicio 2 — Fusión IMU + Odometría
Suscríbete a `/imu/data` y `/odom` simultáneamente. Calcula el yaw de ambas fuentes y publícalos en `/b2/yaw_comparison` como `Float64MultiArray`. ¿Divergen con el tiempo?

### Ejercicio 3 — Detección de impacto
Monitoriza `linear_acceleration` del IMU. Si la norma del vector supera 15 m/s² (golpe), publica un `String` en `/b2/events` con el texto `"impacto detectado"` y el timestamp.

### Ejercicio 4 — Análisis de simetría de articulaciones
Compara las posiciones de cadera izquierda (FL, RL) vs derecha (FR, RR) mientras el robot camina. ¿Son simétricas? Calcula la asimetría como `|q_left - q_right|` y publícala en un tópico.

### Ejercicio 5 — Estado de batería en RViz
Añade el `BatteryPublisher` a tu launch file y configura un panel de texto en rqt que muestre el porcentaje de batería en tiempo real. Envía una alerta de ROS 2 (`rclpy.logging.get_logger`) cuando baje del 25%.

---

## Pasa al robot real

!!! tip "Verificación de hardware en el B2 físico"
    Antes de mover el robot, ejecuta estos comandos para confirmar que los sensores reportan valores razonables:

    ```bash
    # IMU — verifica que acelerómetro Z ≈ 9.81 m/s² en reposo
    ros2 topic echo /imu/data --field linear_acceleration --once

    # Articulaciones — verifica que no hay valores fuera de rango
    python3 s4_joint_monitor.py
    # Ninguna articulación debe mostrar "⚠ FUERA" en posición de pie estático

    # Batería — verifica > 40% antes de iniciar sesión
    ros2 topic echo /b2/battery --once
    ```

---

## Referencias

- [ros2_control — docs.ros.org](https://control.ros.org/jazzy/)
- [sensor_msgs/JointState — ROS 2 API](https://docs.ros2.org/latest/api/sensor_msgs/msg/JointState.html)
- [S4: LowState — mapa de motores](../sdk2/s4-bajo-nivel.md)
- [B2 Industrial — specs de hardware](../b2-industrial.md)
