---
title: "U7: SLAM y Mapeo"
description: "Construye y guarda un mapa 2D del entorno con slam_toolbox usando el LiDAR del Go2/B2."
---

# U7: SLAM y Mapeo

## ¿Por qué necesitas un mapa?

En el módulo U6 el robot navegaba usando solo odometría - sabía dónde estaba relativo a
su posición inicial, pero no tenía conocimiento del entorno. Para aplicaciones
industriales reales necesitas que el robot:

1. **Construya un mapa** la primera vez que recorre el espacio
2. **Se localice** en ese mapa en ejecuciones posteriores
3. **Planifique rutas óptimas** evitando obstáculos conocidos

SLAM (**Simultaneous Localization and Mapping**) resuelve el problema de construir
un mapa mientras te localizas en él al mismo tiempo.

## sim_lite ahora publica TF

Para que `slam_toolbox` funcione necesita un árbol de transformadas (TF) completo.
A partir de esta versión, `sim_lite` publica automáticamente:

```
odom → base_footprint   (dinámica, 30 Hz - posición estimada del robot)
base_footprint → base_scan  (estática - posición del LiDAR respecto al robot)
base_footprint → camera_link (estática - posición de la cámara)
```

Esto significa que puedes lanzar `slam_toolbox` directamente contra `sim_lite`
y construir un mapa real, exactamente igual que en la Parte 3 del curso base con
el TurtleBot3.

## Configuración del sandbox

Abre el sandbox con **"Unitree U7: SLAM y Mapeo"**.

- Mundo: `unitree_inspection` - 4 pilares + obstáculos (mapa interesante)

### Terminal 1 - Lanzar SLAM

```bash
ros2 launch slam_toolbox online_async_launch.py \
  slam_params_file:=/opt/ros/jazzy/share/slam_toolbox/config/mapper_params_online_async.yaml
```

Deberías ver: `[slam_toolbox]: Mapper Parameters Loaded`.

### Terminal 2 - Explorar para construir el mapa

```bash
cd ~/ros2_ws
colcon build --packages-select unitree_u7_slam --symlink-install
source install/setup.bash
ros2 run unitree_u7_slam unitree_slam.py
```

El nodo mueve el robot en rectángulos concéntricos. Observa cómo el mapa
crece en el terminal: `conocidas=X%`.

### Terminal 3 - Visualizar en RViz

```bash
ros2 run rviz2 rviz2
```

En RViz, agrega:
- **Map** → topic `/map`
- **LaserScan** → topic `/scan` 
- **TF** (para ver los frames)
- **Robot Model** si tienes URDF (opcional)

### Terminal 4 - Guardar el mapa

```bash
ros2 run nav2_map_server map_saver_cli -f /home/student/ros2_ws/src/mi_mapa
```

Esto genera `mi_mapa.pgm` (imagen del mapa) y `mi_mapa.yaml` (metadatos).

## Estructura del mapa guardado

```yaml
# mi_mapa.yaml
image: mi_mapa.pgm     # imagen en escala de grises
resolution: 0.05       # 5 cm por pixel
origin: [-X, -Y, 0]    # posición del pixel (0,0) en el marco del mapa
occupied_thresh: 0.65
free_thresh: 0.25
```

En la imagen `.pgm`:
- **Negro** = obstáculo conocido
- **Blanco** = espacio libre conocido
- **Gris** = no explorado

## Localización en un mapa existente (AMCL)

Una vez que tienes el mapa, en ejecuciones posteriores usas AMCL
(Adaptive Monte Carlo Localization) para localizarte en él sin reconstruirlo:

```bash
# Servir el mapa
ros2 run nav2_map_server map_server --ros-args \
  -p yaml_filename:=/home/student/ros2_ws/src/mi_mapa.yaml

# Activar el servidor de ciclo de vida
ros2 lifecycle set /map_server configure
ros2 lifecycle set /map_server activate

# Lanzar AMCL
ros2 launch nav2_bringup localization_launch.py \
  map:=/home/student/ros2_ws/src/mi_mapa.yaml
```

## Diferencia entre SLAM para TurtleBot3 y Go2/B2

| Aspecto | TurtleBot3 (Parte 3) | Unitree Go2/B2 |
|---|---|---|
| Sensor | LiDAR 2D nativo | LiDAR 3D → slice 2D (`unitree_ros2_bridge`) |
| Topic | `/scan` (directo) | `/scan` (del bridge) |
| Comandos SLAM | Idénticos | Idénticos |
| Precisión real | Alta (plano 2D) | Alta (el slice 2D es limpio) |
| Tiempo de mapeo | Minutos | Minutos |

## Ejercicios

!!! note "Ejercicio 1 - Exploración manual"
    En lugar de usar `unitree_slam.py`, explora el mapa **manualmente** usando
    el teclado desde el terminal:
    ```bash
    ros2 run teleop_twist_keyboard teleop_twist_keyboard
    ```
    Intenta cubrir todo el espacio del mundo `unitree_inspection`.

!!! note "Ejercicio 2 - Verificar cobertura"
    Modifica `unitree_slam.py` para que imprima el porcentaje de celdas
    conocidas cada 5 s. Detén la exploración automáticamente cuando el
    mapa tenga > 70% de cobertura.

!!! note "Ejercicio 3 - Cargar y comparar mapas"
    Guarda mapas en dos ejecuciones distintas y compara los archivos `.pgm`.
    ¿Son idénticos? ¿Por qué podrían ser diferentes?

---

Continúa con [U8 - Navegación con Mapa y Puntos de Interés](u8-navegacion-mapa.md).
