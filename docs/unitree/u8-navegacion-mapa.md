---
title: "U8: Puntos de Interés y Navegación con Mapa"
description: "Define POIs en un archivo YAML y navega a ellos con dos enfoques: controlador P (odometría) y Nav2 (stack completo)."
---

# U8: Puntos de Interés y Navegación con Mapa

## De la autonomía reactiva a la misión planificada

En U6 el robot navegaba hacia un solo objetivo hard-codeado. En un sistema
industrial real necesitas:

1. **Definir los POIs externamente** - sin recompilar el código
2. **Navegar a varios puntos en secuencia** - ruta de inspección/patrulla
3. **Ejecutar una acción específica** en cada punto (inspeccionar, cargar, skip)
4. **Repetir la rutina** según una programación

Este módulo presenta **dos enfoques** para lograr eso:

| Enfoque | Tecnología | Cuándo usarlo |
|---|---|---|
| **A - Manual** | Controlador proporcional + odometría | Aprendizaje, rutas simples, sandbox |
| **B - Nav2** | Stack completo de navegación ROS 2 | Despliegues industriales reales, entornos complejos |

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

Ambos enfoques cargan los POIs desde un YAML externo:

```yaml
# /home/student/ros2_ws/src/mi_mision/config/pois.yaml
pois:
  - {name: "Panel A",  x:  2.5, y:  1.5, aruco_id: 1, action: "inspect"}
  - {name: "Panel B",  x:  2.5, y: -1.5, aruco_id: 2, action: "inspect"}
  - {name: "Panel C",  x: -1.5, y:  2.5, aruco_id: 3, action: "inspect"}
  - {name: "Dock",     x: -3.5, y:  0.0, aruco_id: 0, action: "charge"}
```

---

## Enfoque A: Navegación manual con odometría

### ¿Cómo funciona?

El nodo `unitree_waypoint_nav.py` implementa un **controlador proporcional (P-controller)**
que usa solo la odometría del robot (`/odom`) para estimar su posición y calcular las
velocidades necesarias para llegar a cada POI.

Este enfoque es útil para **entender la teoría de control** - es lo mismo que hace
Nav2 internamente, pero simplificado para que puedas leerlo y modificarlo.

### Configuración del sandbox

```bash
cd ~/ros2_ws
colcon build --packages-select unitree_u8_navigation --symlink-install
source install/setup.bash
ros2 run unitree_u8_navigation unitree_waypoint_nav.py
```

Con un archivo YAML externo:

```bash
POIS_FILE=/home/student/ros2_ws/src/mi_mision/config/pois.yaml \
  ros2 run unitree_u8_navigation unitree_waypoint_nav.py
```

El robot visitará las 4 estaciones en orden, ejecutando:
- `hello` en las estaciones de inspección
- `dock` + espera + `undock` en el dock

### El controlador de posición

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

### Limitaciones del Enfoque A

- La odometría **acumula error** - en rutas largas el robot puede derivar varios centímetros
- **No evita obstáculos dinámicos** - si algo bloquea el camino, el robot chocará
- Solo funciona en entornos donde los POIs son accesibles en línea recta

---

## Enfoque B: Navegación con Nav2 (stack completo)

### ¿Cuándo usar Nav2?

Nav2 es el stack de navegación estándar de ROS 2. Requiere más configuración inicial,
pero ofrece:

- **Planificación global de rutas** - encuentra el camino óptimo usando el mapa de U7
- **Evasión de obstáculos** - el costmap detecta y rodea obstáculos en tiempo real
- **Localización robusta** - AMCL corrige el error de odometría usando el LiDAR
- **Behaviors recuperables** - si el robot se atasca, Nav2 intenta maniobras de recuperación

### Prerequisito: mapa de U7

El Enfoque B requiere tener un mapa guardado del módulo U7 (SLAM con slam_toolbox).
Si no lo tienes, ve a [U7 - SLAM](u7-slam.md) y guarda el mapa antes de continuar.

```bash
# Verificar que tienes el mapa de U7
ls /home/student/ros2_ws/src/mapa_inspeccion.*
# Deberías ver: mapa_inspeccion.yaml  mapa_inspeccion.pgm
```

### Lanzar el stack Nav2

Abre tres terminales en el sandbox:

```bash
# Terminal 1 - servir el mapa guardado en U7
ros2 run nav2_map_server map_server --ros-args \
  -p yaml_filename:=/home/student/ros2_ws/src/mapa_inspeccion.yaml
ros2 lifecycle set /map_server configure
ros2 lifecycle set /map_server activate

# Terminal 2 - Nav2 stack
ros2 launch nav2_bringup bringup_launch.py \
  map:=/home/student/ros2_ws/src/mapa_inspeccion.yaml \
  params_file:=/opt/seed/nav2_params/unitree_nav2_params.yaml

# Terminal 3 - cliente Nav2
ros2 run unitree_u8_navigation unitree_nav2_client.py
```

### El cliente Nav2

El nodo `unitree_nav2_client.py` usa la API de alto nivel `BasicNavigator` para
enviar los POIs a Nav2 en lugar de calcular velocidades manualmente:

```python
from nav2_simple_commander.robot_navigator import BasicNavigator
from geometry_msgs.msg import PoseStamped

nav = BasicNavigator()
nav.waitUntilNav2Active()

for poi in pois:
    goal = PoseStamped()
    goal.header.frame_id = "map"
    goal.header.stamp = nav.get_clock().now().to_msg()
    goal.pose.position.x = poi["x"]
    goal.pose.position.y = poi["y"]
    goal.pose.orientation.w = 1.0

    nav.goToPose(goal)

    while not nav.isTaskComplete():
        feedback = nav.getFeedback()
        print(f"Distancia restante: {feedback.distance_remaining:.2f} m")

    result = nav.getResult()
    if result == TaskResult.SUCCEEDED:
        ejecutar_accion(poi["action"])
```

Nav2 planifica la ruta completa, evita obstáculos, y entrega el control a tu código
solo cuando el robot llega al objetivo. Tú solo necesitas manejar la lógica de negocio
(qué hacer en cada POI).

### Parámetros de Nav2 para el Unitree

El archivo `/opt/seed/nav2_params/unitree_nav2_params.yaml` está preconfigurado para:

- Radio del robot: 0.35 m (huella del Go2/B2 con margen)
- Velocidad máxima: 0.6 m/s (lineal), 1.0 rad/s (angular)
- Costmap con inflación de 0.5 m alrededor de obstáculos
- Planner: NavFn (Dijkstra global) + DWB (controller local)
- Tolerancia de llegada: 0.25 m (más estricta que el Enfoque A)

---

## ¿Cuándo usar cada enfoque?

| Criterio | Enfoque A (P-controller) | Enfoque B (Nav2) |
|---|---|---|
| Complejidad de setup | Ninguna - corre directamente | Requiere mapa previo (U7) |
| Precisión | ±0.40 m (deriva odométrica) | ±0.25 m (corrección con LiDAR) |
| Evasión de obstáculos | No | Sí (costmap dinámico) |
| Rutas largas (>10 m) | Deriva acumulada | Localización corregida |
| Entorno del sandbox | ✅ Ideal | ✅ Funciona |
| Despliegue industrial real | Solo para POC simple | ✅ Recomendado |
| Valor pedagógico | Alto - ves la física del control | Medio - abstracción mayor |

**Recomendación**: aprende primero el Enfoque A para entender cómo funciona el control
de posición. Usa el Enfoque B cuando pases a un despliegue real donde la robustez importa.

---

## Ejercicios

!!! note "Ejercicio 1 - Ruta personalizada (Enfoque A)"
    Crea un archivo `pois.yaml` con una ruta diferente (cambia el orden,
    agrega puntos intermedios) y corre la misión con `POIS_FILE=...`.

!!! note "Ejercicio 2 - Ciclos de patrulla (Enfoque A)"
    Modifica el nodo para que repita la ruta `N` veces (donde `N` es
    un argumento de línea de comandos). Al final de cada ciclo, registra
    el tiempo y la batería consumida.

!!! note "Ejercicio 3 - Tolerancia de error (Enfoque A)"
    El robot a veces llega "cerca" pero no exactamente al POI. Agrega
    lógica para que el robot se detenga dentro de `RADIO_LLEGADA` y
    luego haga una corrección fina hasta estar a < 0.15 m del objetivo.

!!! note "Ejercicio 4 - Acciones parametrizables (Enfoque A)"
    Agrega un campo `duracion_s` al YAML para que la acción en cada POI
    dure un tiempo configurable:
    ```yaml
    - {name: "Panel A", x: 2.5, y: 1.5, aruco_id: 1,
       action: "inspect", duracion_s: 5.0}
    ```

!!! note "Ejercicio 5 - Comparar derivas (ambos enfoques)"
    Ejecuta la misma ruta de 4 POIs con el Enfoque A y con el Enfoque B.
    Mide la distancia entre la posición estimada por odometría y la posición
    real (usa RViz para visualizar `/odom` vs. la pose estimada por AMCL en Nav2).
    ¿Cuánta diferencia ves al completar los 4 POIs?

!!! note "Ejercicio 6 - Recuperación de fallos (Enfoque B)"
    Con Nav2 activo, coloca un obstáculo en el camino al POI B directamente
    (usando el panel de sim_lite). Observa cómo Nav2 replanifica la ruta
    automáticamente. Compara qué pasaría con el Enfoque A en la misma situación.

---

Continúa con [U9 - Rutinas de Inspección Industrial](u9-rutinas-inspeccion.md).
