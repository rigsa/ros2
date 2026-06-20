# S1: Introducción al SDK2 — Arquitectura y Modelos de Comunicación

## Objetivos

Al finalizar este módulo serás capaz de:

- Explicar qué es el SDK2 de Unitree y en qué se diferencia de la API ROS 2
- Describir los tres modelos de comunicación del SDK2: Pub/Sub, Req/Resp y punto a punto
- Identificar el rol del DDS subyacente (CycloneDDS) en la arquitectura del SDK2
- Reconocer los canales de comunicación internos del B2 y cuáles son accesibles desde el PC2

---

## El SDK2: interfaz nativa del robot

Los robots Unitree (Go2, B2, H1-2) exponen un SDK oficial llamado **Unitree SDK2** que permite comunicarse directamente con el robot sin necesidad de ROS 2. El SDK2 es la capa más cercana al hardware disponible para el desarrollador.

```
┌──────────────────────────────────────────────────────┐
│                  Tu código (Python/C++)               │
├──────────────────────────────────────────────────────┤
│              Unitree SDK2  (unitree_sdk2_python)      │
├──────────────────────────────────────────────────────┤
│       DDS Middleware  (CycloneDDS, RTPS/DDSI)         │
├──────────────────────────────────────────────────────┤
│     Red  ──  Ethernet / WiFi  ──  Red interna B2      │
├──────────────────────────────────────────────────────┤
│    MCU B2:  LowCmd / LowState / MotorCmd / ...        │
└──────────────────────────────────────────────────────┘
```

Cuando usas ROS 2 con el B2, también estás usando el SDK2 internamente; el paquete `unitree_ros2_bridge` es simplemente una capa de traducción.

---

## Modelos de comunicación en SDK2

El SDK2 soporta tres patrones que mapean directamente a primitivas DDS:

### 1. Publicador / Suscriptor (Pub/Sub)
Estado continuo publicado por el robot a alta frecuencia (500 Hz en el caso del estado bajo nivel).

| Tópico DDS                          | Dirección  | Descripción                     |
|-------------------------------------|------------|---------------------------------|
| `rt/lowstate`                       | Robot → PC | Posición y velocidad de 12 motores, IMU |
| `rt/sportmodestate`                 | Robot → PC | Velocidad base, postura, modo   |
| `rt/wirelesscontroller`             | Robot → PC | Señales del mando a distancia   |
| `rt/lowcmd`                         | PC → Robot | Comandos directos a motores     |

### 2. Solicitud / Respuesta (Req/Resp)
Servicios RPC asincrónicos para acciones discretas.

| Servicio DDS               | Descripción                              |
|----------------------------|------------------------------------------|
| `rt/api/sport/request`     | Comportamientos: stand_up, sit, hello…   |
| `rt/api/loco/request`      | Control de locomoción avanzado           |
| `rt/api/robot_state/request` | Consultar modo, parámetros del sistema |

### 3. Acción (Streaming Req/Resp)
Para comandos continuos que necesitan retroalimentación periódica (ej. trayectorias de brazo en H1-2).

---

## Comparativa SDK2 vs ROS 2

| Característica         | SDK2 directo                  | ROS 2 bridge                    |
|------------------------|-------------------------------|----------------------------------|
| Latencia               | ~1 ms (DDS nativo)            | ~5–15 ms (doble serialización)  |
| Frecuencia de estado   | 500 Hz (LowState)             | Limitada por el bridge (~100 Hz)|
| Ecosistema             | Mínimo (solo Unitree)         | Amplio (Nav2, RViz, MoveIt…)    |
| Curva de aprendizaje   | API propia, docs en inglés    | ROS 2 estándar                  |
| Simuladores            | Solo hardware Unitree          | Gazebo, sim_lite, Isaac Sim…    |
| Acceso al hardware     | Total (motores, IMU, batería) | Parcial (lo que expone el bridge)|

**Regla práctica:** usa SDK2 directo cuando necesites control a baja latencia o acceso a datos no expuestos por el bridge ROS 2. Usa ROS 2 para el grueso del desarrollo de aplicaciones.

---

## Arquitectura interna del B2

El B2 tiene dos computadoras:

- **MCU (microcontrolador)**: controla los 12 motores y el IMU a 500 Hz. No accesible directamente.
- **PC2 (Jetson Orin / Intel NUC)**: ejecuta Ubuntu, el SDK2 interno, y el `unitree_ros2_bridge`. **Es el punto de acceso del desarrollador.**

```
[B2 PC2]──Ethernet──[Tu laptop / sandbox Cloud Run]
    │
    ├── CycloneDDS (SDK2 topics, /rt/lowstate, /rt/sport...)
    └── ROS 2 (si el bridge está activo: /odom, /scan, /cmd_vel...)
```

!!! note "Nota sobre redes"
    El B2 crea su propia red WiFi (`Unitree_B2_XXXX`) y también acepta conexión por Ethernet. Para el sandbox remoto se usa un gateway en el laboratorio — ver [S3: Acceso al PC2](s3-acceso-pc2.md).

---

## Setup del sandbox para este módulo

!!! abstract "Parte del curso: `sdk2_s1`"
    Selecciona **SDK2 S1 — Introducción** al crear tu sesión. El simulador `sim_lite` con mundo `unitree_empty` se iniciará automáticamente.

    El paquete semilla `sdk2_bloque1_s1` incluye:
    - `sdk2_bridge_sim.py` — wrapper que expone la API SDK2 sobre sim_lite
    - `s1_explorar_arquitectura.py` — script de ejercicio

---

## Código de ejemplo: introspección de canales SDK2

En simulación, usamos `sdk2_bridge_sim` que replica la interfaz del SDK2 real:

```python title="s1_explorar_arquitectura.py"
#!/usr/bin/env python3
"""
Explora la arquitectura del SDK2 usando el wrapper de simulación.
En robot real: cambia LocoClientSim por unitree_sdk2py.b2.LocoClient
"""
import rclpy
from sdk2_bridge_sim import SDK2Bridge  # (1)!

def main():
    rclpy.init()
    bridge = SDK2Bridge()  # (2)!

    # --- Pub/Sub: leer estado del sport mode ---
    state = bridge.get_sport_state()  # (3)!
    print(f"Velocidad lineal: {state.velocity[0]:.3f} m/s")
    print(f"Posición X: {state.position[0]:.3f} m")
    print(f"Modo actual: {state.mode}")

    # --- Req/Resp: consultar parámetros del sistema ---
    info = bridge.get_robot_info()  # (4)!
    print(f"Modelo: {info.model}")
    print(f"Batería: {info.battery_pct}%")

    bridge.destroy()
    rclpy.shutdown()

if __name__ == '__main__':
    main()
```

1. En robot real: `from unitree_sdk2py.b2.loco_client import LocoClient`
2. `SDK2Bridge` inicializa el nodo ROS 2 interno que habla con sim_lite
3. Equivale a suscribirse a `rt/sportmodestate` en DDS real
4. Equivale a llamar `rt/api/robot_state/request` en DDS real

---

## Ejercicios

### Ejercicio 1 — Diagrama de capas
Dibuja (en papel o en el editor) el stack completo desde tu script Python hasta el motor del B2. Incluye: tu código → SDK2 → DDS → red → PC2 → MCU → motor.

### Ejercicio 2 — Comparativa de frecuencia
Modifica `s1_explorar_arquitectura.py` para imprimir el estado del robot en un bucle y medir cuántas veces por segundo llegan actualizaciones. Compara con los 500 Hz de LowState y los ~30 Hz del simulador.

### Ejercicio 3 — SDK2 vs ROS 2 topics
Ejecuta `ros2 topic list` en el terminal. Identifica cuáles de esos tópicos existen también como canales DDS nativos del SDK2. ¿Cuáles solo existen en ROS 2?

### Ejercicio 4 — Trazar el flujo de un comando
Traza el recorrido completo de `bridge.move(0.5, 0, 0)` desde Python hasta los motores. ¿Cuántas capas de serialización/deserialización ocurren?

---

## Pasa al robot real

!!! tip "Conectarse al B2 físico"
    Cuando tengas acceso a una sesión de robot (ver [Cola de Robot](../../../robot-queue)), el cambio de sim a hardware es de **una sola línea**:

    ```python
    # Simulación (sandbox):
    from sdk2_bridge_sim import SDK2Bridge
    bridge = SDK2Bridge()

    # Robot real (mismo código, diferente import):
    from unitree_sdk2py.b2.loco_client import LocoClient
    # Asegúrate de que CYCLONEDDS_URI apunta al gateway del laboratorio
    ```

    El resto del código es idéntico.

---

## Referencias

- [Unitree SDK2 Python — GitHub](https://github.com/unitreerobotics/unitree_sdk2_python)
- [B2 Industrial — Specs y hardware](../b2-industrial.md)
- [DDSI-RTPS specification — OMG](https://www.omg.org/spec/DDSI-RTPS/)
