# S3: Visualización y Diagnóstico — RViz, TF Tree, rqt y PlotJuggler

## Objetivos

- Visualizar el estado del B2 en RViz con modelo URDF y TF
- Usar `rqt_graph` para diagnosticar conexiones entre nodos
- Monitorear series temporales de sensores con PlotJuggler
- Construir un dashboard de diagnóstico con `rqt`

---

## Stack de visualización del B2

```
Robot (sim o real)
  ├── /joint_states         → robot_state_publisher → /tf
  ├── /odom                 → → /tf (odom → base_link)
  ├── /scan                 → RViz: LaserScan display
  ├── /camera/image_raw     → RViz: Image display
  └── /imu/data             → RViz: Imu / PlotJuggler

                ┌──────────────┐
  /tf ─────────►│    RViz2     │
  /tf_static ──►│   (3D viz)   │
  /scan ───────►│              │
  /camera/* ──►│              │
                └──────────────┘
```

---

## TF y árbol de transformaciones del B2

El B2 tiene el siguiente árbol TF publicado por `robot_state_publisher`:

```
map
 └── odom
      └── base_link
           ├── imu_link
           ├── lidar_link
           ├── camera_link
           ├── FL_hip_link
           │    └── FL_thigh_link
           │         └── FL_calf_link
           │              └── FL_foot_link
           ├── FR_hip_link ...
           ├── RL_hip_link ...
           └── RR_hip_link ...
```

### Verificar el TF tree

```bash
# Ver el árbol TF completo en terminal
ros2 run tf2_tools view_frames

# El archivo frames.pdf se genera en el directorio actual
# Verificar una transformación específica
ros2 run tf2_ros tf2_echo odom base_link
```

---

## Lanzar RViz con config predefinida

```python title="launch/b2_viz.launch.py"
"""Launch file para visualización completa del B2."""
from launch import LaunchDescription
from launch_ros.actions import Node
import os
from ament_index_python.packages import get_package_share_directory

def generate_launch_description():
    pkg = get_package_share_directory("tu_paquete")
    rviz_config = os.path.join(pkg, "rviz", "b2_default.rviz")

    return LaunchDescription([
        # Publica el URDF del B2 (modelo 3D)
        Node(
            package="robot_state_publisher",
            executable="robot_state_publisher",
            parameters=[{
                "robot_description": open(
                    os.path.join(pkg, "urdf", "b2.urdf")).read()
            }]
        ),
        # RViz con configuración predefinida
        Node(
            package="rviz2",
            executable="rviz2",
            arguments=["-d", rviz_config],
            output="screen"
        ),
    ])
```

---

## Script de diagnóstico: publicar marcadores

```python title="s3_diagnostico_viz.py"
#!/usr/bin/env python3
"""
Publica marcadores de diagnóstico en RViz:
- Punto en la posición actual del robot (verde/rojo según obstáculo)
- Línea de trayectoria recorrida (últimas 100 posiciones)
- Texto con estado del LiDAR

Compatible con sim_lite y robot real.
"""
import math
import rclpy
from rclpy.node import Node
from nav_msgs.msg import Odometry
from sensor_msgs.msg import LaserScan
from visualization_msgs.msg import Marker, MarkerArray
from geometry_msgs.msg import Point
from std_msgs.msg import ColorRGBA

OBSTACLE_DIST = 0.8  # m — umbral para cambiar color del marcador

class DiagnosticViz(Node):
    def __init__(self):
        super().__init__("diagnostic_viz")
        self._pos_history: list[Point] = []
        self._min_lidar = float("inf")

        # Publishers de marcadores
        self._marker_pub = self.create_publisher(MarkerArray, "/b2/markers", 10)

        # Suscriptores
        self.create_subscription(Odometry,  "/odom", self._odom_cb, 10)
        self.create_subscription(LaserScan, "/scan", self._scan_cb, 10)

        # Publicar a 5 Hz
        self.create_timer(0.2, self._publish_markers)

    def _odom_cb(self, msg: Odometry):
        p = Point()
        p.x = msg.pose.pose.position.x
        p.y = msg.pose.pose.position.y
        p.z = 0.0
        self._pos_history.append(p)
        if len(self._pos_history) > 200:  # (1)!
            self._pos_history.pop(0)

    def _scan_cb(self, msg: LaserScan):
        ranges = [r for r in msg.ranges
                  if not (math.isnan(r) or math.isinf(r))]
        self._min_lidar = min(ranges) if ranges else float("inf")

    def _publish_markers(self):
        markers = MarkerArray()

        # ── Marcador 1: posición actual ───────────────────────
        pos_marker = Marker()
        pos_marker.header.frame_id = "odom"
        pos_marker.header.stamp = self.get_clock().now().to_msg()
        pos_marker.ns, pos_marker.id = "b2", 0
        pos_marker.type = Marker.SPHERE
        pos_marker.action = Marker.ADD
        if self._pos_history:
            pos_marker.pose.position = self._pos_history[-1]
        pos_marker.scale.x = pos_marker.scale.y = pos_marker.scale.z = 0.2
        # Verde si libre, rojo si obstáculo cercano
        if self._min_lidar < OBSTACLE_DIST:
            pos_marker.color = ColorRGBA(r=1.0, g=0.0, b=0.0, a=0.9)
        else:
            pos_marker.color = ColorRGBA(r=0.0, g=1.0, b=0.0, a=0.9)
        markers.markers.append(pos_marker)

        # ── Marcador 2: trayectoria ───────────────────────────
        if len(self._pos_history) > 1:
            path_marker = Marker()
            path_marker.header.frame_id = "odom"
            path_marker.header.stamp = self.get_clock().now().to_msg()
            path_marker.ns, path_marker.id = "b2", 1
            path_marker.type = Marker.LINE_STRIP
            path_marker.action = Marker.ADD
            path_marker.scale.x = 0.03
            path_marker.color = ColorRGBA(r=0.2, g=0.6, b=1.0, a=0.7)
            path_marker.points = list(self._pos_history)
            markers.markers.append(path_marker)

        # ── Marcador 3: texto estado LiDAR ────────────────────
        text_marker = Marker()
        text_marker.header.frame_id = "odom"
        text_marker.header.stamp = self.get_clock().now().to_msg()
        text_marker.ns, text_marker.id = "b2", 2
        text_marker.type = Marker.TEXT_VIEW_FACING
        text_marker.action = Marker.ADD
        if self._pos_history:
            text_marker.pose.position = Point(
                x=self._pos_history[-1].x,
                y=self._pos_history[-1].y,
                z=0.6)
        text_marker.scale.z = 0.15
        text_marker.color = ColorRGBA(r=1.0, g=1.0, b=1.0, a=1.0)
        lidar_str = f"{self._min_lidar:.2f}m" if self._min_lidar < 10.0 else "—"
        text_marker.text = f"LiDAR: {lidar_str}"
        markers.markers.append(text_marker)

        self._marker_pub.publish(markers)


def main():
    rclpy.init()
    rclpy.spin(DiagnosticViz())
    rclpy.shutdown()

if __name__ == "__main__":
    main()
```

1. Limitar historial a 200 puntos — suficiente para ~40 s de trayectoria a 5 Hz

---

## rqt_graph — Diagnosticar conexiones de nodos

```bash
# Ver el grafo de nodos y tópicos en tiempo real
rqt_graph

# Filtros útiles:
# - "Nodes only": muestra solo nodos (sin tópicos detallados)
# - "Nodes/Topics (all)": muestra todo el grafo
# - Desmarcar "Dead sinks" / "Leaf topics" para una vista más limpia
```

### Checklist para diagnosticar un nodo desconectado

```bash
# ¿El nodo está corriendo?
ros2 node list

# ¿Está publicando en el tópico esperado?
ros2 topic info /scan --verbose

# ¿Hay suscriptores?
ros2 topic info /cmd_vel --verbose

# ¿Datos llegando?
ros2 topic hz /odom
```

---

## PlotJuggler — Series temporales de sensores

PlotJuggler es la herramienta más potente para visualizar datos de sensores en tiempo real:

```bash
# Instalar (si no está en el sandbox)
sudo apt-get install ros-jazzy-plotjuggler-ros

# Lanzar
ros2 run plotjuggler plotjuggler
```

**Configuración para el B2:**

1. `File → Start ROS Topic Subscriber`
2. Selecciona: `/imu/data`, `/odom`, `/scan`
3. Arrastra `imu/data/linear_acceleration/x` al panel izquierdo
4. Usa `Layout → Import` con el archivo `b2_default_layout.xml` (incluido en el paquete)

---

## Ejercicios

### Ejercicio 1 — RViz básico
Abre RViz en el sandbox. Añade los displays: `LaserScan`, `Odometry`, `TF`. Mueve el robot simulado y verifica que la posición y el scan se actualizan.

### Ejercicio 2 — Árbol TF
Ejecuta `ros2 run tf2_tools view_frames` mientras el simulador está activo. Abre el PDF generado e identifica las 4 cadenas de articulaciones (FL, FR, RL, RR). ¿Cuántos frames hay en total?

### Ejercicio 3 — Marcadores en RViz
Lanza `s3_diagnostico_viz.py` y añade el display `MarkerArray` en RViz apuntando a `/b2/markers`. Mueve el robot y observa la trayectoria. Coloca el robot cerca de una pared y verifica que el marcador de posición cambia a rojo.

### Ejercicio 4 — rqt_graph
Con `s2_b2_lifecycle_driver.py` activo, lanza `rqt_graph`. Toma una captura del grafo. Desactiva el driver (lifecycle deactivate) y toma otra captura. ¿Qué tópicos desaparecen?

### Ejercicio 5 — PlotJuggler + IMU
Con PlotJuggler activo, suscríbete a `/imu/data`. Mueve el robot y grafíca `linear_acceleration/x` y `linear_acceleration/y`. Exporta los datos a CSV para 30 segundos de movimiento.

---

## Pasa al robot real

!!! info "RViz y TF en el B2 físico"
    En hardware real, todos los displays de RViz funcionan igual. La diferencia visible:
    - La nube de puntos LiDAR (`/scan`) es mucho más densa (Hesai AT128, 128 planos)
    - El TF de las articulaciones se actualiza a 500 Hz (en sim puede ser más lento)
    - Añade el display `PointCloud2` apuntando a `/lidar/points` para visualización 3D

    Para grabar datos:
    ```bash
    ros2 bag record /scan /odom /imu/data /joint_states -o b2_sesion_$(date +%Y%m%d_%H%M%S)
    ```

---

## Referencias

- [RViz2 documentation — docs.ros.org](https://docs.ros.org/en/jazzy/Tutorials/Intermediate/RViz/RViz-User-Guide/)
- [PlotJuggler — plotjuggler.io](https://www.plotjuggler.io/)
- [TF2 — docs.ros.org](https://docs.ros.org/en/jazzy/Tutorials/Intermediate/Tf2/Introduction-To-Tf2.html)
- [S1: Arquitectura SDK2 + ROS 2](s1-arq-sdk2-ros2.md)
