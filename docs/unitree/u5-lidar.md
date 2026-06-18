---
title: "U5: LiDAR y Detección de Obstáculos"
description: "Procesa el LaserScan del Go2/B2 y construye un robot que evita obstáculos de forma reactiva."
---

# U5: LiDAR y Detección de Obstáculos

## El LiDAR en el curso base (Parte 3)

En la [Parte 3](../course/part3.md) aprendiste a suscribirte a `sensor_msgs/LaserScan`
y procesar el array de distancias. Todo ese conocimiento aplica directamente aquí.

La interfaz es **idéntica**:

```python
from sensor_msgs.msg import LaserScan

def scan_callback(self, msg: LaserScan):
    # msg.ranges es una lista de N distancias (metros)
    # msg.angle_increment es el ángulo entre rayos consecutivos
    # msg.range_min y msg.range_max son los límites válidos
    distancia_frente = msg.ranges[0]    # rayo apuntando hacia adelante
```

## Diferencia en hardware real: LiDAR 3D vs. 2D

El robot diferencial del curso tiene un LiDAR **2D** que produce de forma nativa `LaserScan`.

El Go2/B2 tiene un **LiDAR L1 de 32 líneas** (3D) que produce `PointCloud2`:
- Publica en `/utlidar/cloud`
- Tiene puntos en todas las alturas (suelo, cuerpo, techo)

Para usar el código del módulo U5 (y de la Parte 3 del curso base) sin cambios,
`unitree_ros2_bridge.py` convierte la nube de puntos 3D en un `LaserScan` 2D
extrayendo el corte horizontal a la altura del cuerpo del robot (~0.30 m):

```
PointCloud2                  LaserScan 2D
(todos los puntos)   →       (solo puntos a ~0.30 m de altura)
/utlidar/cloud               /scan
```

Tu código solo ve el `LaserScan` final - la conversión es transparente.

## Configuración del sandbox

Abre el sandbox con **"Unitree U5: LiDAR y Obstáculos"**.

- Mundo: `unitree_obstacles` - 8 cilindros grises esparcidos en la arena
- Archivo semilla: `unitree_lidar.py`
- El robot verde aparecerá en el centro; los rayos del LiDAR son visibles en la pantalla

Verifica que los datos lleguen:
```bash
ros2 topic echo /scan --field ranges --max-count 1
```

## Archivo semilla: `unitree_lidar.py`

El nodo implementa **evasión reactiva simple**:

1. Divide el scan en sectores (frontal, izquierdo, derecho)
2. Si hay un obstáculo a menos de `DISTANCIA_MINIMA` al frente → girar
3. Si no → avanzar

```bash
cd ~/ros2_ws
colcon build --packages-select unitree_u5_lidar --symlink-install
source install/setup.bash
ros2 run unitree_u5_lidar unitree_lidar.py
```

El robot debería deambular por el mundo `unitree_obstacles` sin chocar.
Observa los rayos rojos (impactos detectados) y azules (espacio libre) en la
ventana de `sim_lite`.

## Estructura del `LaserScan` - recordatorio

```
Índice 0   = frente del robot    (0°)
Índice 90  = izquierda           (90° antihorario)  si n_rays=360
Índice 180 = atrás               (180°)
Índice 270 = derecha             (-90° / 270°)
```

Siempre verifica `msg.range_min <= val <= msg.range_max` antes de usar un valor:
los valores fuera de rango (`inf`, `nan`) indican que el rayo no encontró ningún
objeto dentro del rango máximo del sensor.

```python
def distancia_frontal(msg: LaserScan, sector_grados: int = 30) -> float:
    """Distancia mínima en el sector frontal (±sector_grados)."""
    n   = len(msg.ranges)
    inc = msg.angle_increment
    half = sector_grados // 2
    vals = []
    for d in range(-half, half + 1):
        ang = math.radians(d) % (2 * math.pi)
        idx = int(round(ang / inc)) % n
        v = msg.ranges[idx]
        if msg.range_min <= v <= msg.range_max:
            vals.append(v)
    return min(vals) if vals else float("inf")
```

## Ejercicios

!!! note "Ejercicio 1 - Imprimir distancias por sector"
    Modifica `_scan_cb()` en `unitree_lidar.py` para que imprima la distancia mínima
    en **cuatro sectores**: frontal, trasero, izquierdo, derecho. Imprime máximo
    una vez por segundo (usa `throttle_duration_sec=1.0`).

!!! note "Ejercicio 2 - Mapa de obstáculos"
    Escribe una función que recorra todos los 360 rayos y devuelva las coordenadas `(x, y)`
    de cada punto de impacto (en el marco del robot). Imprime la lista como log.
    
    ```python
    def puntos_impacto(msg: LaserScan):
        puntos = []
        for i, r in enumerate(msg.ranges):
            if msg.range_min <= r <= msg.range_max:
                angulo = msg.angle_min + i * msg.angle_increment
                x = r * math.cos(angulo)
                y = r * math.sin(angulo)
                puntos.append((x, y))
        return puntos
    ```

!!! note "Ejercicio 3 - Evasión mejorada con desplazamiento lateral"
    El robot actual gira cuando detecta un obstáculo. Mejóralo: si hay obstáculo al
    frente pero espacio a la izquierda, usa `vy > 0` (desplazamiento lateral) en lugar
    de girar. Esto aprovecha el movimiento holonómico del Go2/B2.

!!! note "Ejercicio 4 - Patrullero de perímetro"
    Haz que el robot circule por el borde interior de la arena (a ~0.5 m de la pared)
    usando el LiDAR para mantener la distancia. Cuando detecte una distancia menor a
    0.4 m al frente, gira 15° y continúa.

## Diferencia clave con la Parte 3 del curso base

En la Parte 3 usaste el LiDAR para **construir un mapa con SLAM**. En este módulo
lo usas para **navegación reactiva** - el robot no tiene mapa, solo reacciona a lo
que ve en este momento. Las dos formas de usar el LiDAR son complementarias:

| Enfoque | Técnica | Cuándo usarlo |
|---|---|---|
| Reactivo (este módulo) | Array de `ranges` → reglas si/entonces | Evasión simple, tiempo real |
| Basado en mapa (Parte 3) | SLAM → costmap → planner | Navegación hacia objetivos distantes |

---

Continúa con [U6 - Autonomía Integrada](u6-autonomia.md).
