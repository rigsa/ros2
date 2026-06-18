---
title: "SLAM Avanzado: FAST-LIO2 y 3D Mapping"
description: "Mapeo 3D con FAST-LIO2 para el LiDAR Hesai del B2. Comparación con slam_toolbox 2D."
---

# SLAM Avanzado: Mapeo 3D con FAST-LIO2

## ¿Por qué dos métodos de SLAM?

El curso usa dos enfoques de SLAM según el entorno:

| Método | Sensor | Dónde se usa | Instalación |
|---|---|---|---|
| **slam_toolbox** (2D) | `/scan` LaserScan | Sandbox (sim_lite) y real | `apt install ros-jazzy-slam-toolbox` ✅ |
| **FAST-LIO2** (3D) | PointCloud2 + IMU | Solo B2 hardware real | Compilar desde fuente |

En el sandbox del curso siempre uses **slam_toolbox** (U7). FAST-LIO2 es para cuando tengas
acceso al B2 real y quieras aprovechar su LiDAR 3D Hesai AT128.

## slam_toolbox (2D) - lo que uses en el sandbox

`slam_toolbox` construye un mapa 2D de ocupación a partir de datos `LaserScan` (/scan).

Comando del sandbox (ver [U7](u7-slam.md) para detalles completos):

```bash
ros2 launch slam_toolbox online_async_launch.py \
  slam_params_file:=/opt/seed/slam_params/unitree_inspection_slam.yaml
```

**Ventajas**: simple, ROS 2 nativo, funciona en el sandbox, compatible con Nav2.

**Limitaciones**: solo usa datos 2D. En un pasillo industrial con muchos objetos a la
misma altura, los scans 2D pueden ser escasos o ruidosos.

## FAST-LIO2 (3D) - para el B2 real

[FAST-LIO2](https://github.com/hku-mars/FAST_LIO) (Fast LiDAR-Inertial Odometry v2) es
un algoritmo de odometría y mapeo LiDAR-Inercial diseñado específicamente para plataformas
ágiles como robots cuadrúpedos.

### ¿Por qué FAST-LIO2 para B2?

- Usa LiDAR 3D + **IMU** juntos → mucho más robusto ante el movimiento de las patas
- Frecuencia de actualización de odometría: **100-500 Hz** (vs. ~10 Hz de slam_toolbox)
- Gestiona las vibraciones del cuerpo del robot (el B2 genera mucho movimiento en el cuerpo)
- Genera un **mapa 3D de puntos** (ikd-tree) además de la odometría
- Funciona en exteriores e interiores

### Arquitectura de FAST-LIO2 con B2

```
Unitree B2
├── LiDAR Hesai AT128  ─→ /utlidar/cloud (PointCloud2)  ─┐
└── IMU integrada      ─→ /imu/data       (Imu)         ─┴─→  FAST-LIO2  ─→ /Odometry
                                                                              /cloud_registered
                                                                              /tf (map→odom)
```

Con el bridge activo, el canal `/utlidar/cloud` está disponible directamente en ROS 2.
El IMU del B2 se accede vía: `ChannelSubscriber("rt/imu_state", IMUState_)` en el SDK,
y el bridge lo republica en `/imu/data`.

### Instalación de FAST-LIO2 en el host del robot (fuera del sandbox)

```bash
# En el computador conectado al B2 (no dentro del sandbox)
cd ~/ros2_ws/src

# Clonar FAST-LIO2 con soporte para ROS 2
git clone --recursive https://github.com/Ericsii/FAST_LIO_ROS2.git

# Dependencias
sudo apt install -y \
  ros-jazzy-pcl-ros \
  ros-jazzy-pcl-conversions \
  libeigen3-dev \
  libpcl-dev

# Compilar
cd ~/ros2_ws
colcon build --packages-select fast_lio --cmake-args -DCMAKE_BUILD_TYPE=Release

# Cargar
source install/setup.bash
```

### Configurar FAST-LIO2 para el Hesai AT128 del B2

```yaml
# ~/ros2_ws/src/FAST_LIO_ROS2/config/b2_hesai_at128.yaml
common:
  lid_topic:  "/utlidar/cloud"      # topic del LiDAR en B2
  imu_topic:  "/imu/data"           # topic del IMU (via bridge)
  time_sync_en: false
  extrinsic_est_en: true

preprocess:
  lidar_type: 2        # Hesai Pandar series
  scan_line: 128       # AT128 tiene 128 canales
  timestamp_unit: 3    # ns
  blind: 0.5           # ignorar puntos a menos de 0.5 m (cuerpo del robot)
  point_filter_num: 1

mapping:
  acc_cov: 0.1
  gyr_cov: 0.1
  b_acc_cov: 0.0001
  b_gyr_cov: 0.0001
  fov_degree: 360.0
  det_range: 100.0     # alcance del AT128 hasta 300 m
  extrinsic_T: [-0.012, 0.022, 0.495]   # posición del LiDAR en el B2 (ajustar)
  extrinsic_R: [1,0,0, 0,1,0, 0,0,1]
```

### Ejecutar FAST-LIO2 con B2

```bash
# Terminal 1 - bridge del robot (Go2/B2 via SDK)
python3 ~/unitree_ros2_bridge.py --network_interface eth0

# Terminal 2 - FAST-LIO2
ros2 launch fast_lio mapping.launch.py \
  config_file:=b2_hesai_at128.yaml

# Terminal 3 - visualizar en RViz
ros2 run rviz2 rviz2
# Agrega: PointCloud2 → /cloud_registered
#          Odometry → /Odometry
```

### Convertir el mapa 3D a 2D para Nav2

FAST-LIO2 genera una nube de puntos 3D. Para usar con Nav2 (que espera un mapa 2D),
usa `pointcloud_to_laserscan` para crear un /scan a partir de la nube:

```bash
ros2 launch pointcloud_to_laserscan pointcloud_to_laserscan_launch.py
```

Luego usa slam_toolbox en modo localization con el mapa 2D previamente guardado:

```bash
ros2 launch slam_toolbox localization_launch.py \
  slam_params_file:=/opt/seed/slam_params/unitree_inspection_slam.yaml \
  map_file_name:=/home/student/mapa_inspeccion
```

## Comparación práctica

| Escenario | Recomendación |
|---|---|
| Sandbox sim_lite (curso) | `slam_toolbox` 2D |
| Go2 EDU en laboratorio cerrado | `slam_toolbox` 2D con LiDAR 2D |
| B2 en planta industrial | **FAST-LIO2** 3D + slam_toolbox 2D para Nav2 |
| B2 en exteriores o terreno irregular | **FAST-LIO2** 3D (es mucho más robusto) |
| Pasillo con poco features (pocas paredes) | FAST-LIO2 3D (el 2D puede perder localización) |

## Ejercicios (requieren B2 real)

!!! note "Ejercicio avanzado 1 - Comparar odometría"
    Conecta al B2. Ejecuta simultáneamente FAST-LIO2 y el bridge (que usa `SportModeState`
    para odometría). Compara `/Odometry` (FAST-LIO2) vs. `/odom` (bridge). ¿Cuál deriva menos?

!!! note "Ejercicio avanzado 2 - Mapa 3D de la planta"
    Construye un mapa 3D completo de tu laboratorio usando FAST-LIO2. Guarda la nube de
    puntos con:
    ```bash
    ros2 run pcl_ros pointcloud_to_pcd /cloud_registered
    ```
    Abre el .pcd en CloudCompare y mide la distancia entre dos paredes conocidas.

!!! note "Ejercicio avanzado 3 - Pipeline completo"
    1. Mapear con FAST-LIO2 (3D)
    2. Extraer corte 2D con `pointcloud_to_laserscan`
    3. Guardar mapa 2D con `map_saver_cli`
    4. Localizar con AMCL
    5. Navegar con Nav2 + `unitree_nav2_client.py`
