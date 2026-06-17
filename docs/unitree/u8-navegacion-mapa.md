---
title: "U8: Puntos de Interés y Navegación con Mapa"
description: "Define POIs en un archivo YAML y navega a ellos secuencialmente usando odometría y configuración externa."
---

# U8: Puntos de Interés y Navegación con Mapa

## De la autonomía reactiva a la misión planificada

En U6 el robot navegaba hacia un solo objetivo hard-codeado. En un sistema
industrial real necesitas:

1. **Definir los POIs externamente** — sin recompilar el código
2. **Navegar a varios puntos en secuencia** — ruta de inspección/patrulla
3. **Ejecutar una acción específica** en cada punto (inspeccionar, cargar, skip)
4. **Repetir la rutina** según una programación

## Mundo `unitree_inspection`

El sandbox U8 usa el mundo de inspección con 4 puntos de interés predefinidos:

| ID | Nombre | Posición | ArUco | Acción |
|---|---|---|---|---|
| 1 | Station A | (2.5, 1.5) | #1 | inspeccionar |
| 2 | Station B | (2.5, -1.5) | #2 | inspeccionar |
| 3 | Station C | (-1.5, 2.5) | #3 | inspeccionar |
| 0 | Dock | (-3.5, 0.0) | #0 | cargar |

En la ventana de `sim_lite` verás los labels **A**, **B**, **C** y ⚡ sobre cada
pillar, y el dock en cian.

## Configuración de misión en YAML (sin recompilar)

El archivo `unitree_waypoint_nav.py` carga los POIs desde un YAML. Puedes
sobreescribir la lista interna apuntando a un archivo externo:

```yaml
# /home/student/ros2_ws/src/mi_mision/config/pois.yaml
pois:
  - {name: "Panel A",  x:  2.5, y:  1.5, aruco_id: 1, action: "inspect"}
  - {name: "Panel B",  x:  2.5, y: -1.5, aruco_id: 2, action: "inspect"}
  - {name: "Panel C",  x: -1.5, y:  2.5, aruco_id: 3, action: "inspect"}
  - {name: "Dock",     x: -3.5, y:  0.0, aruco_id: 0, action: "charge"}
```

```bash
POIS_FILE=/home/student/ros2_ws/src/mi_mision/config/pois.yaml \
  ros2 run unitree_u8_navigation unitree_waypoint_nav.py
```

## Configuración del sandbox

```bash
cd ~/ros2_ws
colcon build --packages-select unitree_u8_navigation --symlink-install
source install/setup.bash
ros2 run unitree_u8_navigation unitree_waypoint_nav.py
```

El robot visitará las 4 estaciones en orden, ejecutando:
- `hello` en las estaciones de inspección
- `dock` + espera + `undock` en el dock

## El controlador de posición

El nodo usa el mismo controlador proporcional del módulo U6, ahora encapsulado
en `_navegar_a()`:

```python
def _navegar_a(self, x_obj, y_obj, nombre) -> bool:
    while rclpy.ok():
        dx, dy = x_obj - self.x, y_obj - self.y
        if math.hypot(dx, dy) < RADIO_LLEGADA:
            return True
        err_yaw = normalizar(math.atan2(dy, dx) - self.yaw)
        vyaw    = KP_YAW * err_yaw     # proporcional
        vx      = VEL_MAX * (1 - |err_yaw| / π)   # reduce si desviado
        self._cmd(vx, 0.0, vyaw)
```

El radio de llegada (`RADIO_LLEGADA = 0.40 m`) es lo suficientemente grande
para que el robot se considere "en el POI" aunque no esté perfectamente centrado.
En U10 aprenderás a usar ArUco para acercarte más precisamente.

## Ejercicios

!!! note "Ejercicio 1 — Ruta personalizada"
    Crea un archivo `pois.yaml` con una ruta diferente (cambia el orden,
    agrega puntos intermedios) y corre la misión con `POIS_FILE=...`.

!!! note "Ejercicio 2 — Ciclos de patrulla"
    Modifica el nodo para que repita la ruta `N` veces (donde `N` es
    un argumento de línea de comandos). Al final de cada ciclo, registra
    el tiempo y la batería consumida.

!!! note "Ejercicio 3 — Tolerancia de error"
    El robot a veces llega "cerca" pero no exactamente al POI. Agrega
    lógica para que el robot se detenga dentro de `RADIO_LLEGADA` y
    luego haga una corrección fina hasta estar a < 0.15 m del objetivo.

!!! note "Ejercicio 4 — Acciones parametrizables"
    Agrega un campo `duracion_s` al YAML para que la acción en cada POI
    dure un tiempo configurable:
    ```yaml
    - {name: "Panel A", x: 2.5, y: 1.5, aruco_id: 1,
       action: "inspect", duracion_s: 5.0}
    ```

## Para hardware real: Nav2

En el robot real, para rutas largas o entornos complejos, considera usar
Nav2 en lugar del controlador proporcional simple:

```python
from nav2_simple_commander.robot_navigator import BasicNavigator
from geometry_msgs.msg import PoseStamped

nav = BasicNavigator()
nav.waitUntilNav2Active()

goal = PoseStamped()
goal.header.frame_id = "map"
goal.pose.position.x = 2.5
goal.pose.position.y = 1.5
nav.goToPose(goal)

while not nav.isTaskComplete():
    feedback = nav.getFeedback()
    print(f"Distancia: {feedback.distance_remaining:.2f} m")
```

Nav2 planifica rutas óptimas evitando obstáculos del mapa. Requiere
`slam_toolbox` o AMCL activos (ver U7).

---

Continúa con [U9 — Rutinas de Inspección Industrial](u9-rutinas-inspeccion.md).
