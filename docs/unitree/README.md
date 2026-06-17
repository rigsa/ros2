---
title: "Unitree Go2/B2 con ROS 2"
description: "Módulos del curso para robots cuadrúpedos Unitree Go2 EDU y B2, usando ROS 2 Jazzy."
---

# Módulos Unitree Go2/B2

Estos módulos extienden el curso base de ROS 2 para trabajar con robots cuadrúpedos
[Unitree Go2 EDU](https://www.unitree.com/go2) y [B2](https://www.unitree.com/b2).

El material asume que completaste los módulos principales del curso (Partes 1–6) y que
ya dominas los conceptos de publishers, subscribers, servicios y acciones de ROS 2.

## ¿Por qué es diferente programar un cuadrúpedo?

| Característica | TurtleBot3 Waffle | Unitree Go2/B2 |
|---|---|---|
| Tipo de locomoción | Tracción diferencial (2 DOF) | Holonómica — 4 patas (3 DOF) |
| Control base | Plugin diff-drive de Gazebo | `SportClient` del SDK2 de Unitree |
| LiDAR | 2D nativo (`LaserScan`) | 3D nube de puntos (→ slice 2D) |
| Comportamientos extra | Solo movimiento | StandUp, Sit, Hello, Dance, FrontFlip, … |
| Middleware | Fast DDS (default ROS 2) | CycloneDDS por Ethernet (en hardware real) |

La buena noticia: a pesar de estas diferencias, **tu código ROS 2 usa los mismos topics
y servicios estándar**. El puente `unitree_ros2_bridge.py` se encarga de la traducción
al SDK en hardware real; en el simulador `sim_lite` provee exactamente la misma
interfaz. Puedes desarrollar y probar en el sandbox y después desplegar en el robot
sin cambiar ninguna línea de tu código.

## El principio "escribe una vez, ejecuta en cualquier lugar"

```
Tu código del curso
      ↓ mismos topics y servicios ROS 2
 /cmd_vel  /odom  /scan  /sport/*
      ↓                        ↓
  sim_lite.py            unitree_ros2_bridge.py
  (simulador,                  (robot real,
   ~150 MB RAM)                 SDK de Unitree)
```

## Módulos de este curso

### Fundamentos (U1–U6)

| Módulo | Tema | Archivo semilla |
|---|---|---|
| [U1 — Introducción](u1-introduccion.md) | Arquitectura, bridge, comparación | — |
| [U2 — Locomoción](u2-locomocion.md) | `/cmd_vel` holonómico, 3 DOF | `unitree_move.py` |
| [U3 — Odometría](u3-odometria.md) | `/odom`, quaternion→yaw, tracking de posición | `unitree_odom.py` |
| [U4 — Comportamientos](u4-comportamientos.md) | Servicios `/sport/*`, SportClient API | `unitree_sport.py` |
| [U5 — LiDAR](u5-lidar.md) | `/scan`, detección de obstáculos | `unitree_lidar.py` |
| [U6 — Autonomía](u6-autonomia.md) | Integración: odom + LiDAR + movimiento | `unitree_autonomy.py` |

### Soluciones industriales (U7–U12)

| Módulo | Tema | Archivo semilla |
|---|---|---|
| [U7 — SLAM](u7-slam.md) | Mapeado con slam_toolbox, árbol de TF, guardado de mapa | `unitree_slam.py` |
| [U8 — Navegación con Mapa](u8-navegacion-mapa.md) | POIs en YAML, ruta de inspección, controlador proporcional | `unitree_waypoint_nav.py` |
| [U9 — Rutinas de Inspección](u9-rutinas-inspeccion.md) | FSM completa, parámetros ROS 2, reintentos, logging | `unitree_inspection.py` |
| [U10 — Tags ArUco](u10-aruco.md) | Detección visual de marcadores, pose estimation, acercamiento fino | `unitree_aruco.py` |
| [U11 — Gestión de Batería](u11-bateria.md) | `BatteryState`, umbrales, retorno autónomo al dock | `unitree_battery.py` |
| [U12 — Logging y Reportes](u12-logging.md) | CSV, JSON, rosbag2, niveles de log, análisis offline | `unitree_logger.py` |

## Entorno de práctica

Todos los módulos se pueden trabajar en el sandbox del curso (en el navegador) con
`sim_lite` en modo holonómico. Activa el mundo correcto seleccionando el módulo en el
[portal del sandbox](../../software/browser-ros2.md):

- **U1–U4**: mundo `unitree_empty` — espacio abierto, motor holonómico
- **U5–U6**: mundo `unitree_obstacles` — campo con obstáculos, motor holonómico
- **U7–U12**: mundo `unitree_inspection` — planta industrial con 4 estaciones (ArUco), dock de carga y POIs etiquetados

Los mismos archivos `.py` funcionan sin cambios en el robot real una vez que
`unitree_ros2_bridge.py` esté corriendo en el mismo host que el robot.

## Lecturas de referencia

- [Portando a Unitree (interfaces)](../course/extras/porting-to-unitree.md) —
  mapeo completo de topics del curso base a sus equivalentes en Go2/B2
- [SDK de Python de Unitree (unitree_sdk2py)](https://github.com/unitreerobotics/unitree_sdk2_python)
- [Repositorio de autonomía Go2](https://github.com/rigsa/unitree_rigsa)
  (stack de navegación completo, referencia para trabajos avanzados)
