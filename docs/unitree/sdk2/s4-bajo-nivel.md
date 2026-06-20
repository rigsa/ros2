# S4: Interfaces de Bajo Nivel — Control Directo, Mensajes y Librerías

## Objetivos

- Leer estados de motores e IMU desde `LowState` a 500 Hz
- Comprender la estructura de `LowCmd` y su campo `motor_cmd`
- Implementar un monitor de articulaciones con alarmas de rango
- Entender cuándo el control de bajo nivel es necesario vs peligroso

---

## ¿Qué es el control de bajo nivel?

El SDK2 tiene dos niveles de abstracción para controlar el B2:

```
Alto nivel  ──  LocoClient / SportClient  ──  "Muévete 0.5 m/s adelante"
                        │
Bajo nivel  ──  LowCmd / LowState        ──  "Motor 0: τ=2.5 Nm, kp=40, kd=1"
```

El **control de bajo nivel** publica `LowCmd` directamente al controlador de cada motor (12 en el B2). Permite:

- Implementar controladores de posición / impedancia personalizados
- Acceder a datos de sensores a máxima frecuencia (500 Hz)
- Desarrollar algoritmos de contacto y estimación de estado
- Leer corriente, temperatura y torque de cada motor

!!! danger "Úsalo con precaución"
    Publicar en `rt/lowcmd` incorrectamente puede causar caídas del robot o daño mecánico. En este módulo nos limitamos a **leer** LowState y solo publicamos LowCmd en el ejercicio avanzado con el robot en reposo.

---

## Estructura de LowState

```python
# Campos relevantes de LowState (simplificado)
class LowState:
    motor_state: list[MotorState]  # 12 motores
    imu_state: IMUState
    battery_capacity_pct: int      # Batería 0-100

class MotorState:
    q: float      # Posición (rad)
    dq: float     # Velocidad (rad/s)
    ddq: float    # Aceleración (rad/s²)
    tau_est: float  # Torque estimado (Nm)
    temperature: float  # Temperatura (°C)

class IMUState:
    quaternion: list[float]  # [w, x, y, z]
    gyroscope: list[float]   # [x, y, z] (rad/s)
    accelerometer: list[float]  # [x, y, z] (m/s²)
    rpy: list[float]         # [roll, pitch, yaw] (rad)
```

### Mapa de motores del B2

| ID | Pierna | Articulación | Rango (rad) |
|----|--------|--------------|-------------|
| 0  | FL     | Hip Roll     | [-1.0, 1.0] |
| 1  | FL     | Hip Pitch    | [-1.5, 3.4] |
| 2  | FL     | Knee         | [-2.7, -0.8]|
| 3  | FR     | Hip Roll     | [-1.0, 1.0] |
| 4  | FR     | Hip Pitch    | [-1.5, 3.4] |
| 5  | FR     | Knee         | [-2.7, -0.8]|
| 6  | RL     | Hip Roll     | [-1.0, 1.0] |
| 7  | RL     | Hip Pitch    | [-3.4, 1.5] |
| 8  | RL     | Knee         | [0.8, 2.7]  |
| 9  | RR     | Hip Roll     | [-1.0, 1.0] |
| 10 | RR     | Hip Pitch    | [-3.4, 1.5] |
| 11 | RR     | Knee         | [0.8, 2.7]  |

FL=Frontal-Izquierda, FR=Frontal-Derecha, RL=Trasera-Izquierda, RR=Trasera-Derecha

---

## Código: monitor de estado en tiempo real

```python title="s4_monitor_lowstate.py"
#!/usr/bin/env python3
"""
Monitor de articulaciones y IMU via SDK2 LowState.
Muestra posición, velocidad y temperatura de cada motor.
"""
import time
import rclpy
from sdk2_bridge_sim import SDK2Bridge  # (1)!

# Robot real:
# from unitree_sdk2py.core.channel import ChannelFactory, ChannelSubscriber
# from unitree_sdk2py.idl.unitree_go.msg.dds_ import LowState_
# ChannelFactory.Instance().Init(0)

TEMP_WARN = 60.0  # °C — alerta de temperatura  # (2)!

def print_motor_table(state):
    import os; os.system("clear")
    print(f"{'Motor':<6} {'Pierna':<5} {'Articulación':<14} {'q (rad)':>8} {'dq (r/s)':>9} {'τ (Nm)':>7} {'Temp °C':>8}")
    print("-" * 60)
    labels = [
        ("FL", "Hip Roll"), ("FL", "Hip Pitch"), ("FL", "Knee"),
        ("FR", "Hip Roll"), ("FR", "Hip Pitch"), ("FR", "Knee"),
        ("RL", "Hip Roll"), ("RL", "Hip Pitch"), ("RL", "Knee"),
        ("RR", "Hip Roll"), ("RR", "Hip Pitch"), ("RR", "Knee"),
    ]
    for i, (leg, joint) in enumerate(labels):
        m = state.motor_state[i]
        flag = " ⚠" if m.temperature > TEMP_WARN else ""
        print(f"{i:<6} {leg:<5} {joint:<14} {m.q:>8.3f} {m.dq:>9.3f} {m.tau_est:>7.2f} {m.temperature:>7.1f}{flag}")
    imu = state.imu_state
    print(f"\nIMU — Roll:{imu.rpy[0]:>6.3f} Pitch:{imu.rpy[1]:>6.3f} Yaw:{imu.rpy[2]:>6.3f} rad")
    print(f"      Acc: {imu.accelerometer}")

def main():
    rclpy.init()
    bridge = SDK2Bridge()
    try:
        while True:
            state = bridge.get_low_state()  # (3)!
            if state:
                print_motor_table(state)
            time.sleep(0.1)  # 10 Hz para la visualización
    except KeyboardInterrupt:
        pass
    finally:
        bridge.destroy()
        rclpy.shutdown()

if __name__ == '__main__':
    main()
```

1. En robot real: usar `ChannelSubscriber("rt/lowstate", LowState_)`
2. El B2 permite operación hasta ~80 °C; por encima de 90 °C el controlador reducirá torque
3. `get_low_state()` en el bridge devuelve el último `LowState` recibido

---

## LowCmd: estructura (referencia, no ejecutar en sim)

```python
# Solo para referencia — no enviar en simulación
class MotorCmd:
    mode: int     # 0=idle, 1=torque, 10=posición PD
    q: float      # Posición objetivo (rad)
    dq: float     # Velocidad objetivo (rad/s)
    tau: float    # Torque feed-forward (Nm)
    kp: float     # Ganancia proporcional
    kd: float     # Ganancia derivativa
```

### Ejemplo de modo PD (solo robot real en reposo)

```python
# Mantener posición actual (ganancia baja = modo suave)
cmd = LowCmd_()
for i in range(12):
    cmd.motor_cmd[i].mode = 10   # Modo PD
    cmd.motor_cmd[i].q   = current_q[i]  # Posición actual
    cmd.motor_cmd[i].kp  = 20.0  # Ganancia proporcional
    cmd.motor_cmd[i].kd  = 0.5   # Ganancia derivativa
    cmd.motor_cmd[i].tau = 0.0   # Sin feedforward
cmd.crc = CRC().Crc(cmd)
publisher.Write(cmd)
```

---

## Ejercicios

### Ejercicio 1 — Monitor básico
Ejecuta `s4_monitor_lowstate.py` con `sdk2_bridge_sim`. Desplaza el robot (mueve, gira) y observa cómo cambian las lecturas de `q` y `dq` de los motores. ¿Qué motores cambian más durante una traslación frontal?

### Ejercicio 2 — Extractor de IMU
Extrae solo los datos del IMU (roll, pitch, yaw + acelerómetro) y publícalos como `geometry_msgs/TwistStamped` en un tópico ROS 2 `/imu_viz`. Verifica con `ros2 topic echo`.

### Ejercicio 3 — Alarma de temperatura
Extiende el monitor para que emita una alerta de ROS 2 (`get_logger().warn`) cuando cualquier motor supere `TEMP_WARN`. Encapsula la lógica en una función `check_thermal(state) -> list[int]` que devuelva los IDs de motores en alerta.

### Ejercicio 4 — Análisis de simetría
Compara los valores de `q` de las articulaciones FL vs FR (índices 0,1,2 vs 3,4,5) durante el caminar. ¿Son simétricas? ¿Qué implica una asimetría significativa?

### Ejercicio 5 — LowState a CSV (robot real)
Durante una sesión de robot real, registra LowState a 100 Hz durante 10 segundos mientras el B2 camina. Guarda en CSV. Calcula la amplitud de oscilación de cada articulación de rodilla.

---

## Pasa al robot real

!!! tip "Habilitación de LowState en hardware"
    En robot real, `rt/lowstate` se publica automáticamente a 500 Hz sin necesidad de configuración adicional. El primer mensaje llega en ~10 ms tras `ChannelFactory.Instance().Init()`.

    ```python
    # Leer LowState en robot real
    from unitree_sdk2py.core.channel import ChannelFactory, ChannelSubscriber
    from unitree_sdk2py.idl.unitree_go.msg.dds_ import LowState_

    ChannelFactory.Instance().Init(0)  # 0 = dominio DDS local

    latest = None
    def handler(msg): global latest; latest = msg

    sub = ChannelSubscriber("rt/lowstate", LowState_)
    sub.Init(handler, 10)
    ```

---

## Referencias

- [B2 — Joint ranges y mapa de motores](../b2-industrial.md)
- [SDK2 LowCmd/LowState reference](https://support.unitree.com/home/en/developer/SDK2)
- [Unitree CRC utility](https://github.com/unitreerobotics/unitree_sdk2_python/blob/main/unitree_sdk2py/utils/crc.py)
