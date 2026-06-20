# S7: Percepción y Navegación — SLAM, Nav2 y Stack Completo en el B2

## Objetivos

- Construir un mapa 2D del entorno con SLAM Toolbox y el LiDAR del B2
- Configurar Nav2 para navegación autónoma basada en el mapa
- Integrar la cámara RGB para detección de objetos en la ruta
- Componer un stack de autonomía completo: SLAM → Mapa → Nav2 → Misión

---

## Stack de percepción y navegación

```
┌──────────────────────────────────────────────────────────┐
│                   Stack completo B2                       │
│                                                          │
│  Sensores                                                 │
│  /scan (LiDAR) ─────────────────────────────┐            │
│  /odom (odometría) ──────────────────────┐  │            │
│  /imu/data ──────────────────────────────┤  │            │
│                                           ▼  ▼            │
│  SLAM Toolbox                                             │
│  slam_toolbox → /map (OccupancyGrid)                     │
│              → /tf: map → odom                           │
│                          │                               │
│                          ▼                               │
│  Nav2                                                     │
│  /map + /odom + /scan → Planner → /cmd_vel               │
│  /navigate_to_pose   ← Goal (RViz / código)              │
│                          │                               │
│                          ▼                               │
│  Tu misión                                               │
│  action_client → NavigateToPose → waypoints              │
│  /camera/image_raw → detección → parada condicionada     │
└──────────────────────────────────────────────────────────┘
```

---

## Parte 1: SLAM con SLAM Toolbox

### Lanzar SLAM en sim_lite

```bash
# Terminal 1: simulador
ros2 launch sim_lite b2_sim.launch.py world:=unitree_inspection

# Terminal 2: SLAM Toolbox (modo online async)
ros2 launch slam_toolbox online_async_launch.py \
    slam_params_file:=$(ros2 pkg prefix tu_paquete)/share/tu_paquete/config/slam_b2.yaml

# Terminal 3: teleop para construir el mapa
ros2 run teleop_twist_keyboard teleop_twist_keyboard
```

### Configuración SLAM para el B2

```yaml title="config/slam_b2.yaml"
slam_toolbox:
  ros__parameters:
    # Parámetros del solver
    solver_plugin: solver_plugins::CeresSolver
    ceres_linear_solver: SPARSE_NORMAL_CHOLESKY
    ceres_preconditioner: SCHUR_JACOBI
    ceres_trust_strategy: LEVENBERG_MARQUARDT
    ceres_dogleg_type: TRADITIONAL_DOGLEG

    # Frecuencia de procesamiento
    map_update_interval: 5.0          # s entre actualizaciones del mapa
    resolution: 0.05                  # m/celda — 5 cm de resolución

    # Frames TF
    base_frame: base_link
    odom_frame: odom
    map_frame: map

    # Parámetros del scan
    scan_topic: /scan
    minimum_travel_distance: 0.1      # m — actualizar solo si el robot se mueve
    minimum_travel_heading: 0.1       # rad — o si gira

    # Modo
    mode: mapping                     # 'mapping' o 'localization'
    use_scan_matching: true
    use_scan_barycenter: true

    # Guardar mapa
    map_file_name: /tmp/mapa_b2
    map_start_at_dock: false
```

### Guardar el mapa

```bash
# Guardar el mapa cuando esté completo
ros2 run nav2_map_server map_saver_cli -f /tmp/mapa_b2
# Genera: mapa_b2.pgm + mapa_b2.yaml
```

---

## Parte 2: Navegación autónoma con Nav2

### Configuración Nav2 para el B2

```yaml title="config/nav2_b2.yaml"
bt_navigator:
  ros__parameters:
    use_sim_time: false
    global_frame: map
    robot_base_frame: base_link
    odom_topic: /odom
    bt_loop_duration: 10
    default_server_timeout: 20
    navigators: ["navigate_to_pose", "navigate_through_poses"]
    navigate_to_pose:
      plugin: "nav2_bt_navigator::NavigateToPoseNavigator"

controller_server:
  ros__parameters:
    controller_frequency: 20.0
    controller_plugins: ["FollowPath"]
    FollowPath:
      plugin: "nav2_regulated_pure_pursuit_controller::RegulatedPurePursuitController"
      desired_linear_vel: 0.3          # m/s — conservador para el B2
      max_linear_accel: 0.5
      max_linear_decel: 0.5
      lookahead_dist: 0.6
      use_velocity_scaled_lookahead_dist: true
      max_angular_accel: 1.0

local_costmap:
  ros__parameters:
    update_frequency: 5.0
    publish_frequency: 2.0
    global_frame: odom
    robot_base_frame: base_link
    robot_radius: 0.45               # Radio del B2 (m)
    inflation_radius: 0.3
    plugins: ["voxel_layer", "inflation_layer"]
    voxel_layer:
      plugin: "nav2_costmap_2d::VoxelLayer"
      observation_sources: scan
      scan:
        topic: /scan
        max_obstacle_height: 2.0
        clearing: true
        marking: true

global_costmap:
  ros__parameters:
    update_frequency: 1.0
    publish_frequency: 1.0
    global_frame: map
    robot_base_frame: base_link
    robot_radius: 0.45
    resolution: 0.05
    plugins: ["static_layer", "obstacle_layer", "inflation_layer"]
    static_layer:
      plugin: "nav2_costmap_2d::StaticLayer"
      map_topic: /map
```

### Launch file completo Nav2

```python title="launch/b2_nav2.launch.py"
"""Launch Nav2 con el mapa guardado del B2."""
from launch import LaunchDescription
from launch.actions import IncludeLaunchDescription
from launch.launch_description_sources import PythonLaunchDescriptionSource
from launch_ros.actions import Node
from ament_index_python.packages import get_package_share_directory
import os

def generate_launch_description():
    pkg = get_package_share_directory("tu_paquete")
    nav2_pkg = get_package_share_directory("nav2_bringup")

    return LaunchDescription([
        # Servidor de mapas (mapa pre-construido)
        Node(
            package="nav2_map_server",
            executable="map_server",
            parameters=[{
                "yaml_filename": os.path.join(pkg, "maps", "mapa_b2.yaml"),
                "topic_name": "/map",
                "frame_id": "map"
            }]
        ),
        # Localización AMCL (si tienes mapa previo)
        Node(
            package="nav2_amcl",
            executable="amcl",
            parameters=[os.path.join(pkg, "config", "nav2_b2.yaml")]
        ),
        # Stack Nav2 completo
        IncludeLaunchDescription(
            PythonLaunchDescriptionSource(
                os.path.join(nav2_pkg, "launch", "navigation_launch.py")
            ),
            launch_arguments={
                "params_file": os.path.join(pkg, "config", "nav2_b2.yaml"),
                "use_sim_time": "false"
            }.items()
        ),
    ])
```

---

## Parte 3: Navegación autónoma desde código

```python title="s7_nav2_mission.py"
#!/usr/bin/env python3
"""
Ejecuta una misión de navegación de 3 waypoints con Nav2.
Integra detección de objetos con cámara en cada waypoint.

Compatible con sim_lite + Nav2 y con el B2 real.
"""
import math, time
import rclpy
from rclpy.node import Node
from rclpy.action import ActionClient
from nav2_msgs.action import NavigateToPose
from geometry_msgs.msg import PoseStamped, Quaternion
from sensor_msgs.msg import Image
from cv_bridge import CvBridge
import cv2

# Waypoints de misión (x, y, yaw en el frame 'map')
WAYPOINTS = [
    (2.0,  0.0,  0.0),    # Estación 1
    (2.0,  2.0,  1.57),   # Estación 2 — girar 90°
    (0.0,  2.0,  3.14),   # Estación 3 — girar 180°
]

def yaw_to_quat(yaw: float) -> Quaternion:
    q = Quaternion()
    q.w = math.cos(yaw / 2)
    q.z = math.sin(yaw / 2)
    return q

class MissionNode(Node):
    def __init__(self):
        super().__init__("mission_node")
        self._nav_client = ActionClient(self, NavigateToPose, "navigate_to_pose")
        self._bridge = CvBridge()
        self._latest_img = None
        self.create_subscription(Image, "/camera/image_raw",
                                 self._img_cb, 10)

    def _img_cb(self, msg: Image):
        self._latest_img = self._bridge.imgmsg_to_cv2(msg, "bgr8")

    def navigate_to(self, x: float, y: float, yaw: float,
                    timeout_s: float = 60.0) -> bool:
        """Envía un goal a Nav2 y espera a que llegue."""
        goal = NavigateToPose.Goal()
        goal.pose = PoseStamped()
        goal.pose.header.frame_id = "map"
        goal.pose.header.stamp = self.get_clock().now().to_msg()
        goal.pose.pose.position.x = x
        goal.pose.pose.position.y = y
        goal.pose.pose.orientation = yaw_to_quat(yaw)

        self._nav_client.wait_for_server(timeout_sec=5.0)
        future = self._nav_client.send_goal_async(goal)
        rclpy.spin_until_future_complete(self, future, timeout_sec=10.0)

        goal_handle = future.result()
        if not goal_handle or not goal_handle.accepted:
            self.get_logger().error("Goal rechazado por Nav2")
            return False

        result_future = goal_handle.get_result_async()
        rclpy.spin_until_future_complete(self, result_future,
                                         timeout_sec=timeout_s)
        return result_future.result() is not None

    def inspect_at_waypoint(self, idx: int) -> dict:
        """Captura imagen y realiza inspección básica en el waypoint."""
        rclpy.spin_once(self, timeout_sec=0.5)

        result = {"waypoint": idx, "time": time.time(), "objects": []}

        if self._latest_img is not None:
            # Análisis simple: color dominante en ROI central
            h, w = self._latest_img.shape[:2]
            roi = self._latest_img[h//4:3*h//4, w//4:3*w//4]
            mean_bgr = roi.mean(axis=(0, 1))
            result["mean_bgr"] = mean_bgr.tolist()

            # Guardar imagen
            path = f"/tmp/waypoint_{idx}_{int(time.time())}.jpg"
            cv2.imwrite(path, self._latest_img)
            result["image"] = path

        self.get_logger().info(f"Inspección waypoint {idx}: {result}")
        return result


def main():
    rclpy.init()
    node = MissionNode()

    if not node._nav_client.wait_for_server(timeout_sec=10.0):
        node.get_logger().error("Nav2 no disponible — ¿está Nav2 activo?")
        rclpy.shutdown()
        return

    mission_log = []

    for i, (x, y, yaw) in enumerate(WAYPOINTS):
        node.get_logger().info(f"→ Navegando al waypoint {i+1} ({x:.1f}, {y:.1f})")
        arrived = node.navigate_to(x, y, yaw, timeout_s=90.0)

        if arrived:
            node.get_logger().info(f"✓ Llegó al waypoint {i+1}")
            entry = node.inspect_at_waypoint(i + 1)
            mission_log.append(entry)
        else:
            node.get_logger().warn(f"✗ No llegó al waypoint {i+1} — abortando misión")
            break

    # Volver al origen
    node.get_logger().info("→ Volviendo al origen")
    node.navigate_to(0.0, 0.0, 0.0)

    import json
    report = f"/tmp/nav_mission_{int(time.time())}.json"
    with open(report, "w") as f:
        json.dump(mission_log, f, indent=2)
    node.get_logger().info(f"Misión completada. Reporte: {report}")

    node.destroy_node()
    rclpy.shutdown()

if __name__ == "__main__":
    main()
```

---

## Ejercicios

### Ejercicio 1 — Construcción de mapa
Lanza SLAM Toolbox en `unitree_inspection`. Usando `teleop_twist_keyboard`, explora todo el mundo. Guarda el mapa y visualízalo en RViz. ¿Hay zonas con poca resolución? ¿Por qué?

### Ejercicio 2 — Localización AMCL
Carga el mapa guardado con `map_server` y lanza `amcl`. Desplaza el robot a una posición aleatoria y publica la pose inicial en `/initialpose` via RViz. Verifica que AMCL converge.

### Ejercicio 3 — Waypoint único con Nav2
Usando `s7_nav2_mission.py`, modifica `WAYPOINTS` para incluir solo un punto a (3.0, 1.5, 0.0). Lanza Nav2 y verifica que el robot llega al punto. Mide el error posicional (distancia real vs goal).

### Ejercicio 4 — Obstáculo dinámico
Con el robot navegando hacia un waypoint, publica un obstáculo en el costmap publicando en `/scan` (simula un obstáculo con un nodo publicador). Verifica que Nav2 replanifica la ruta.

### Ejercicio 5 — Misión completa integrada
Integra `s7_nav2_mission.py` con el sistema de patrulla del Bloque 1 (`s7_patrol_system.py`). La misión debe: navegar a 3 waypoints con Nav2, en cada punto ejecutar `inspect_at_waypoint()` y guardar el log JSON. El watchdog del módulo S7 bloque 1 debe seguir activo durante toda la misión.

---

## Pasa al robot real

!!! success "SLAM + Nav2 en el B2 físico"
    El stack completo funciona en el robot real sin cambios de código. Las diferencias a tener en cuenta:

    1. **Construye el mapa primero** (sesión de mapping dedicada, sin Nav2 activo):
       ```bash
       ros2 launch slam_toolbox online_async_launch.py \
           slam_params_file:=config/slam_b2.yaml
       # Teleop para explorar, luego guarda el mapa
       ros2 run nav2_map_server map_saver_cli -f maps/mapa_laboratorio
       ```

    2. **Segunda sesión**: carga el mapa y activa Nav2 + AMCL:
       ```bash
       ros2 launch tu_paquete b2_nav2.launch.py
       ```

    3. **Aumenta los radios del costmap** en el B2 real:
       - `robot_radius: 0.55` (0.45 sim → 0.55 real, margen de seguridad adicional)
       - `inflation_radius: 0.4`

    4. **Velocidad máxima conservadora** para la primera sesión:
       - `desired_linear_vel: 0.2` (reducir de 0.3 a 0.2 m/s)

---

## Referencias

- [SLAM Toolbox — docs.nav2.org](https://docs.nav2.org/tutorials/docs/navigation2_with_slam.html)
- [Nav2 Getting Started](https://docs.nav2.org/getting_started/)
- [U7: SLAM en Go2](../u7-slam.md)
- [U8: Navegación con mapa](../u8-navegacion-mapa.md)
- [S7: Caso integrado SDK2](../sdk2/s7-caso-integrado.md)
