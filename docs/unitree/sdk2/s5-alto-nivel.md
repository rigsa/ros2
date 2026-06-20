# S5: Interfaces de Alto Nivel — LocoClient y Modos de Locomoción

## Objetivos

- Usar `LocoClient` para control de movimiento completo del B2
- Cambiar entre modos de locomoción: normal, stair-climbing, obstacle avoidance
- Encadenar movimientos con sincronización temporal precisa
- Comparar `LocoClient` con el tópico `/cmd_vel` de ROS 2

---

## LocoClient: la interfaz de alto nivel

`LocoClient` es el cliente de más alto nivel del SDK2 para locomoción. Usa el servicio DDS `rt/api/loco/request` y abstrae completamente el control de postura y zancada:

```
Tu código  →  LocoClient.Move(vx, vy, vyaw)
                    │
              rt/api/loco/request  (DDS)
                    │
             Controlador de locomoción del B2
             (gait planning, foot placement, balance)
                    │
             LowCmd @ 500 Hz a los 12 motores
```

### vs /cmd_vel en ROS 2

| Característica       | `LocoClient.Move()`     | `/cmd_vel` (ROS 2)         |
|----------------------|-------------------------|----------------------------|
| Protocolo            | DDS nativo (SDK2)       | ROS 2 topic                |
| Latencia             | ~1 ms                   | ~5-15 ms                   |
| Modo de locomoción   | Configurable (ver tabla)| Siempre `normal_stand`     |
| Acceso a modos avanzados | Sí                  | No (solo velocidad)        |
| Curva de aprendizaje | SDK2 Python             | ROS 2 estándar             |

**Regla práctica:** Para aplicaciones de alto nivel (SLAM, Nav2, ROS 2), usa `/cmd_vel`. Para prototipos que necesiten gait switching o máximo rendimiento, usa `LocoClient`.

---

## Modos de locomoción del B2

```python
class LocoClient:
    def SwitchGait(self, gait: int) -> int: ...
```

| Código | Nombre          | Descripción                              | Uso                      |
|--------|-----------------|------------------------------------------|--------------------------|
| 0      | `kPose`         | Solo control de postura, sin movimiento  | Fotografías, inspección  |
| 1      | `kWalk`         | Marcha estándar (por defecto)            | Navegación general       |
| 2      | `kRun`          | Trote, velocidad máxima ~2 m/s           | Desplazamiento rápido    |
| 3      | `kClimb`        | Modo escaleras y rampas                  | Entornos industriales    |
| 4      | `kObstAvoid`    | Esquiva de obstáculos autónoma (B2 Pro)  | Terreno complejo         |

---

## API completa de LocoClient

```python
# Métodos principales del LocoClient
loco.Move(vx: float, vy: float, vyaw: float)  # m/s, m/s, rad/s
loco.StopMove()                                # Parar inmediatamente
loco.SwitchGait(gait: int) -> int             # Cambiar modo de marcha
loco.SetBalanceMode(mode: int)                 # 0=normal, 1=rigid (B2 carga)
loco.SetBodyHeight(height: float)              # Altura del cuerpo (±0.15 m relativo)
loco.SetFeetHeight(height: float)              # Altura de paso de las patas
loco.Euler(roll: float, pitch: float, yaw: float)  # Solo en modo kPose
loco.Squat()                                   # Agacharse (posición de transporte)
loco.RecoveryStand()                           # Levantarse tras caída
```

---

## Código completo: controlador de locomoción avanzado

```python title="s5_loco_client.py"
#!/usr/bin/env python3
"""
Controlador usando LocoClient — locomotion completo del B2.
Demuestra: Move, SwitchGait, SetBodyHeight, Euler.
"""
import time
import rclpy
from sdk2_bridge_sim import LocoClientSim as LocoClient  # (1)!

# Robot real:
# from unitree_sdk2py.core.channel import ChannelFactory
# from unitree_sdk2py.b2.loco_client import LocoClient
# ChannelFactory.Instance().Init(0)

def main():
    rclpy.init()
    loco = LocoClient()
    loco.Init()

    # ── Modo 1: marcha normal ───────────────────────────────
    print("Marcha normal → adelante")
    loco.SwitchGait(1)            # Walk  # (2)!
    loco.Move(0.5, 0.0, 0.0)
    time.sleep(2.0)
    loco.StopMove()

    # ── Modo 2: ajuste de altura del cuerpo ─────────────────
    print("Subiendo altura del cuerpo")
    loco.SetBodyHeight(0.1)       # +10 cm sobre la posición por defecto  # (3)!
    time.sleep(1.0)
    loco.Move(0.3, 0.0, 0.0)     # Más lento en posición alta
    time.sleep(2.0)
    loco.StopMove()
    loco.SetBodyHeight(0.0)       # Volver a altura normal

    # ── Modo 3: pose estática con Euler ─────────────────────
    print("Inspeccionando (pose estática)")
    loco.SwitchGait(0)            # kPose  # (4)!
    loco.Euler(0.0, 0.15, 0.0)   # Pitch de 15° — simula mirar hacia abajo
    time.sleep(2.0)
    loco.Euler(0.0, 0.0, 0.0)    # Volver a horizontal

    # ── Modo 4: movimiento lateral (holonómico) ──────────────
    print("Deslizamiento lateral")
    loco.SwitchGait(1)
    loco.Move(0.0, 0.3, 0.0)     # vy = 0.3 m/s (solo posible en cuadrúpedo)  # (5)!
    time.sleep(2.0)
    loco.StopMove()

    loco.Squat()                  # Posición de transporte
    print("Completo.")
    rclpy.shutdown()

if __name__ == '__main__':
    main()
```

1. `sdk2_bridge_sim` traduce las llamadas a `/cmd_vel` y `/sport/*` del sim_lite
2. Cambiar de gait puede tardar ~0.5 s (el robot reconfigura el paso)
3. Rango: -0.15 m (muy bajo) a +0.15 m. Útil para pasar bajo obstáculos o inspección de techos
4. En `kPose` el robot no responde a `Move()` — solo a `Euler()`
5. Solo cuadrúpedos soportan `vy ≠ 0`; robots de 2 ruedas ignoran este campo

---

## Patrón: movimiento con timeout de seguridad

```python title="s5_safe_move.py"
#!/usr/bin/env python3
"""
Mueve el robot durante un tiempo máximo y luego para.
Patrón recomendado para todos los ejercicios con hardware real.
"""
import time
import threading
from sdk2_bridge_sim import LocoClientSim as LocoClient
import rclpy

def move_timed(loco, vx, vy, vyaw, duration_s):
    """Mueve durante `duration_s` segundos, luego para."""
    loco.Move(vx, vy, vyaw)
    time.sleep(duration_s)
    loco.StopMove()

def main():
    rclpy.init()
    loco = LocoClient()
    loco.Init()
    loco.SwitchGait(1)

    # Cuadrado de 1 m de lado
    for _ in range(4):
        move_timed(loco, 0.5, 0.0, 0.0, 2.0)   # Avanzar 1 m @ 0.5 m/s
        time.sleep(0.3)
        move_timed(loco, 0.0, 0.0, 1.57, 1.0)  # Girar 90° @ 1.57 rad/s

    loco.StopMove()
    rclpy.shutdown()
```

---

## Ejercicios

### Ejercicio 1 — Figura en 8
Programa un trayecto en forma de 8 usando `Move(vx, vy, vyaw)` con combinaciones simultáneas de velocidad lineal y angular.

### Ejercicio 2 — Cambio de altura adaptativo
Crea una función `adaptive_height(obstacle_height_m)` que ajuste `SetBodyHeight()` según un obstáculo detectado por el LiDAR (usa la distancia frontal de `/scan`).

### Ejercicio 3 — Modo inspección
Implementa una rutina de inspección de 360°: el robot se detiene, activa `kPose`, barre ±15° en roll y ±10° en pitch, captura 4 imágenes de cámara (`/camera/image_raw`), y publica los paths de las imágenes guardadas.

### Ejercicio 4 — Comparativa de velocidades
Mide la velocidad real del robot (de `/odom`) mientras publicas diferentes valores de `vx` en `Move()`. ¿A qué `vx` se satura la velocidad real? ¿Difiere entre modos `kWalk` y `kRun`?

### Ejercicio 5 — Recuperación de caída (sim)
Simula una situación de caída invirtiendo el pitch del robot (no disponible en sim_lite pero sí en sim 3D). Implementa un nodo que monitorice `imu_state.rpy[1]` y llame a `loco.RecoveryStand()` si `|pitch| > 0.8 rad`.

---

## Pasa al robot real

!!! warning "Antes de mover el B2 físico"
    1. Asegúrate de que el área alrededor del robot esté despejada (radio mínimo 2 m)
    2. Usa siempre `loco.SwitchGait(1)` antes de `Move()` — nunca muevas en `kPose`
    3. Limita velocidades a ≤ 0.5 m/s en interiores
    4. Ten un operador físicamente presente con el mando a distancia para emergencias
    5. El mando a distancia tiene prioridad sobre cualquier comando de software

---

## Referencias

- [LocoClient Python API — Unitree SDK2](https://support.unitree.com/home/en/developer/SDK2)
- [B2 locomotion modes](../b2-industrial.md)
- [U2: Locomoción Holonómica (ROS 2 equivalente)](../u2-locomocion.md)
