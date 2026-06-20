# S6: Simulación Avanzada — sim_lite, Gazebo y Validación Pre-Deploy

## Objetivos

- Usar sim_lite para validar código antes de desplegar en el B2 físico
- Comprender las diferencias entre sim_lite, Gazebo e Isaac Sim
- Implementar un mundo personalizado para scenarios de prueba
- Crear una estrategia de testing sim → real con diferencias documentadas

---

## Comparativa de simuladores para el B2

| Característica            | **sim_lite** (sandbox) | **Gazebo Harmonic**   | **Isaac Sim**         |
|---------------------------|------------------------|-----------------------|-----------------------|
| Latencia de setup         | < 5 s                  | ~30 s                 | ~2 min                |
| Física de contacto        | Simplificada (2D)      | ODE/Bullet (3D)       | PhysX 5 (3D avanzado) |
| Sensor LiDAR              | Raycast 2D (`/scan`)   | Raycast 3D            | Raycast 3D + GPU      |
| Cámara RGB                | Imagen sintética       | Rendering básico      | RTX rendering         |
| Carga de CPU              | Baja (~1 núcleo)       | Media (~4 núcleos)    | Alta (GPU requerida)  |
| Fidelidad dinámica        | Baja                   | Media                 | Alta                  |
| Uso recomendado           | Algoritmos ROS 2       | Integración + SLAM    | ML / RL / inspección  |

**Para este módulo:** usamos sim_lite. Para SLAM con Cartographer o Nav2 real, ver [S7: Percepción y Navegación](s7-percepcion-nav.md).

---

## Mundos de sim_lite disponibles

El sandbox incluye tres mundos predefinidos:

| Mundo                  | Descripción                                 | Uso recomendado        |
|------------------------|---------------------------------------------|------------------------|
| `unitree_empty`        | Sala vacía 10×10 m                          | S1-S3, conceptual      |
| `unitree_obstacles`    | Obstáculos estáticos distribuidos           | S4-S5, navegación      |
| `unitree_inspection`   | Sala industrial con 3 puntos de inspección  | S6-S7, caso integrado  |

Para cambiar el mundo en sim_lite:

```bash
# En el terminal del sandbox
export SIM_WORLD=unitree_inspection
ros2 launch sim_lite b2_sim.launch.py world:=unitree_inspection
```

---

## Diferencias documentadas: sim_lite vs robot real

Conocer estas diferencias es crítico para un despliegue seguro:

| Comportamiento          | sim_lite                          | B2 físico                                   |
|-------------------------|-----------------------------------|---------------------------------------------|
| Tiempo de respuesta     | Instantáneo                       | 50-200 ms (comunicación DDS)                |
| LiDAR NaN               | Solo fuera del rango              | También en reflectivos, luz solar directa   |
| Odometría               | Sin deriva (perfecta)             | Deriva acumulativa, especialmente en giros  |
| IMU                     | Sin ruido                         | Ruido gaussiano ~0.01 m/s²                  |
| Fricción del suelo      | Ideal                             | Variable según superficie                   |
| Batería                 | Siempre 100%                      | Se descarga (~2 h de operación continua)    |
| Inercia del robot       | Mínima                            | Significativa (13 kg B2 + carga)            |
| Stop de emergencia      | `StopMove()` para instantáneamente| Robot desacelera ~0.3 s                     |

---

## Configurar un escenario de prueba personalizado

```python title="s6_scenario_runner.py"
#!/usr/bin/env python3
"""
Ejecuta un escenario de prueba reproducible en sim_lite.
Define: posición inicial, secuencia de comandos, criterios de éxito.

Patrón: Arrange → Act → Assert (igual que un test unitario).
"""
import time, math
import rclpy
from rclpy.node import Node
from nav_msgs.msg import Odometry
from sensor_msgs.msg import LaserScan
from geometry_msgs.msg import Twist

from sdk2_bridge_sim import LocoClientSim as LocoClient

@dataclass
class ScenarioResult:
    name: str
    passed: bool
    reason: str = ""

class ScenarioRunner(Node):
    def __init__(self):
        super().__init__("scenario_runner")
        self._pos = (0.0, 0.0)
        self._min_lidar = float("inf")
        self._loco = LocoClient()
        self._loco.Init()
        self._loco.SwitchGait(1)

        self.create_subscription(Odometry,  "/odom", self._odom_cb, 10)
        self.create_subscription(LaserScan, "/scan", self._scan_cb, 10)

    def _odom_cb(self, msg):
        p = msg.pose.pose.position
        self._pos = (p.x, p.y)

    def _scan_cb(self, msg):
        valid = [r for r in msg.ranges
                 if not (math.isnan(r) or math.isinf(r))]
        self._min_lidar = min(valid) if valid else float("inf")

    def spin_for(self, seconds):
        t0 = time.time()
        while time.time() - t0 < seconds:
            rclpy.spin_once(self, timeout_sec=0.05)

    # ── Escenarios ────────────────────────────────────────────

    def scenario_forward_2m(self) -> ScenarioResult:
        """El robot debe avanzar al menos 1.8 m en 10 s."""
        x0, y0 = self._pos
        self._loco.Move(0.3, 0.0, 0.0)
        self.spin_for(10.0)
        self._loco.StopMove()
        dist = math.hypot(self._pos[0] - x0, self._pos[1] - y0)
        passed = dist >= 1.8
        return ScenarioResult(
            "forward_2m", passed,
            f"Avanzó {dist:.2f} m (esperado ≥ 1.8 m)")

    def scenario_obstacle_stop(self) -> ScenarioResult:
        """El robot debe parar antes de 0.5 m de un obstáculo."""
        self._loco.Move(0.2, 0.0, 0.0)
        deadline = time.time() + 15.0
        while time.time() < deadline:
            rclpy.spin_once(self, timeout_sec=0.05)
            if self._min_lidar < 0.5:
                self._loco.StopMove()
                return ScenarioResult(
                    "obstacle_stop", True,
                    f"Paró a {self._min_lidar:.2f} m del obstáculo")
        self._loco.StopMove()
        return ScenarioResult(
            "obstacle_stop", False,
            "No encontró obstáculo en 15 s (¿mundo vacío?)")

    def scenario_rotate_360(self) -> ScenarioResult:
        """El robot debe girar 360° y volver a la orientación original."""
        import rclpy
        from sensor_msgs.msg import Imu
        initial_yaw = self._get_yaw()
        self._loco.Move(0.0, 0.0, 0.8)
        self.spin_for(8.5)  # 8.5 s * 0.8 rad/s ≈ 6.8 rad > 2π
        self._loco.StopMove()
        final_yaw = self._get_yaw()
        # Diferencia de yaw debe ser < 0.3 rad (vuelta completa)
        diff = abs(final_yaw - initial_yaw)
        passed = diff < 0.3
        return ScenarioResult(
            "rotate_360", passed,
            f"Yaw inicial={math.degrees(initial_yaw):.1f}° final={math.degrees(final_yaw):.1f}°")

    def _get_yaw(self) -> float:
        rclpy.spin_once(self, timeout_sec=0.3)
        return 0.0  # Placeholder — implementar desde /odom.orientation


def main():
    from dataclasses import dataclass
    rclpy.init()
    runner = ScenarioRunner()
    runner.spin_for(1.0)  # Esperar datos iniciales

    scenarios = [
        runner.scenario_forward_2m,
        runner.scenario_obstacle_stop,
        runner.scenario_rotate_360,
    ]

    results = []
    for scenario_fn in scenarios:
        print(f"Ejecutando: {scenario_fn.__name__}...")
        result = scenario_fn()
        results.append(result)
        icon = "✓" if result.passed else "✗"
        print(f"  {icon} {result.name}: {result.reason}")
        runner.spin_for(1.0)  # Pausa entre escenarios

    passed = sum(1 for r in results if r.passed)
    print(f"\n{passed}/{len(results)} escenarios pasaron")

    runner.destroy_node()
    rclpy.shutdown()

if __name__ == "__main__":
    main()
```

---

## Estrategia de validación sim → real

```
┌──────────────────────────────────────────────────────────┐
│                  Pipeline de validación                   │
│                                                          │
│  1. Unit tests (sin ROS 2, sin sim)                      │
│     pytest tests/unit/                                   │
│                                                          │
│  2. Integration tests (sim_lite)                         │
│     pytest tests/integration/ --sim=sim_lite             │
│     → s5_health_check.py                                 │
│     → s6_scenario_runner.py                             │
│                                                          │
│  3. Validación en sim_lite con mundo real                 │
│     Medir: distancias recorridas, tiempos, frecuencias   │
│     Comparar contra valores esperados del real           │
│                                                          │
│  4. Robot real (slot reservado)                          │
│     Primero: s5_health_check.py                          │
│     Luego: escenarios en orden de complejidad creciente  │
│     Velocidad inicial: MAX_SPEED * 0.5                   │
└──────────────────────────────────────────────────────────┘
```

---

## Ejercicios

### Ejercicio 1 — Comparar mundos
Ejecuta `s6_scenario_runner.py:scenario_forward_2m` en `unitree_empty` y en `unitree_obstacles`. ¿Difieren las distancias recorridas? ¿Por qué?

### Ejercicio 2 — Medir deriva de odometría
Haz que el robot complete un cuadrado de 2×2 m (4 lados × 2 m con 3 giros de 90°). Mide cuánto se aleja la posición final de la posición inicial en el simulador. Anota el resultado para comparar en el robot real.

### Ejercicio 3 — Inyección de fallo
Modifica `s6_scenario_runner.py` para añadir un escenario que falle intencionalmente: busca un objeto que no existe en el mundo. Verifica que el runner reporta el fallo correctamente.

### Ejercicio 4 — Mundo personalizado
Edita el archivo YAML de `unitree_inspection` para añadir una pared adicional. Lanza el simulador con el mundo modificado y verifica que el LiDAR lo detecta.

### Ejercicio 5 — Informe HTML de escenarios
Modifica `ScenarioRunner` para que al finalizar genere un archivo HTML con los resultados de los escenarios (tabla con nombre, resultado, descripción, timestamp).

---

## Pasa al robot real

!!! warning "Diferencias críticas sim → real"
    Antes de tu primera sesión con el B2 físico, documenta estos valores del simulador para poder comparar:

    | Métrica                         | sim_lite (tu medición) | B2 real (a medir) |
    |---------------------------------|------------------------|-------------------|
    | Tiempo hasta 1 m a 0.3 m/s     | ___ s                  | ___ s             |
    | Deriva odometría tras giro 360° | ___ m                  | ___ m             |
    | LiDAR mín. ante pared a 1 m    | ___ m                  | ___ m             |
    | Tiempo de frenado desde 0.3 m/s | 0 s (instantáneo)      | ___ s             |

    Ajusta tus controladores basándote en las diferencias observadas.

---

## Referencias

- [sim_lite — descripción del simulador](../../sandbox-guide.md)
- [Gazebo Harmonic + ROS 2 Jazzy](https://gazebosim.org/docs/harmonic/ros2_integration/)
- [S7: Percepción y Navegación — SLAM con Gazebo](s7-percepcion-nav.md)
- [Isaac Lab para Go2 — entrenamiento RL](../go2-isaac-lab.md)
