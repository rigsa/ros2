---
title: "U1: Introducción al Unitree Go2/B2"
description: "Arquitectura del robot, el SDK de Unitree, y el patrón bridge que permite usar ROS 2 estándar en hardware real."
---

# U1: Introducción al Unitree Go2/B2

## El robot cuadrúpedo

El [Unitree Go2 EDU](https://www.unitree.com/go2) y el [B2](https://www.unitree.com/b2)
son robots cuadrúpedos (cuatro patas) diseñados para investigación y desarrollo.
A diferencia de los robots de ruedas que usamos en el resto del curso, estos robots:

- Se **mueven sobre patas** — tienen una dinámica mucho más compleja que las ruedas
- Son **holonómicos** — pueden moverse en cualquier dirección sin girar primero
- Tienen **comportamientos de alto nivel** integrados (sentarse, saludar, bailar, voltear)
- Llevan un **LiDAR 3D** en lugar del LiDAR 2D del TurtleBot3

El Go2 EDU tiene acceso al SDK completo de Unitree. El B2 es la versión más grande e
industrial y comparte la misma familia de API.

## Arquitectura del sistema

```
┌─────────────────────────────────────────────────────────┐
│                  Tu código ROS 2                         │
│  publishers  ·  subscribers  ·  service clients          │
│   /cmd_vel        /odom           /sport/*               │
│   /scan       /camera/image_raw                          │
└──────────────────────┬──────────────────────────────────┘
                       │ interfaces ROS 2 estándar
           ┌───────────┴───────────┐
           │                       │
    ┌──────▼───────┐      ┌────────▼──────────┐
    │  sim_lite.py  │      │ unitree_ros2_bridge│
    │  (simulador)  │      │    (hardware real) │
    │  ~150 MB RAM  │      │  unitree_sdk2_python│
    └──────────────┘      └────────┬──────────┘
                                   │ SDK DDS / Ethernet
                           ┌───────▼────────┐
                           │  Unitree Go2/B2 │
                           │  (hardware real) │
                           └────────────────┘
```

El componente clave del diseño es el **puente** (`unitree_ros2_bridge.py`):
un nodo ROS 2 que se ejecuta junto al robot y traduce entre:

- Los **topics estándar** que tu código usa (igual que en el curso base)
- La **API SportClient** del SDK de Unitree que el robot necesita

## ¿Qué es el SDK de Unitree?

El `unitree_sdk2` (y su versión Python `unitree_sdk2_python`) es la biblioteca
oficial de Unitree para comunicarse con los robots Go2/B2. Usa **CycloneDDS** sobre
Ethernet para enviar comandos al robot a baja latencia.

Las API principales del SDK relevantes para este curso son:

### SportClient — control de movimiento y comportamientos

```python
sport_client.Move(vx, vy, vyaw)    # Mover el robot (holonómico)
sport_client.StandUp()             # Levantarse
sport_client.StandDown()           # Bajar
sport_client.Sit()                 # Sentarse
sport_client.Hello()               # Agitar la pata
sport_client.Dance1()              # Bailar
sport_client.FrontFlip()           # Voltereta frontal (EDU solamente)
# ... y muchos más (ver ros2_sport_client.h, IDs 1001-1032)
```

### Datos de estado

El robot publica continuamente su estado (posición estimada, velocidades, orientación)
en el topic DDS `rt/sportmodestate` (tipo `SportModeState_`). El bridge lee esto y lo
republica como `nav_msgs/Odometry` en `/odom`.

### LiDAR

El LiDAR L1 del Go2 publica una **nube de puntos 3D** en `/utlidar/cloud`
(`sensor_msgs/PointCloud2`). El bridge extrae un corte horizontal a la altura del
cuerpo y lo convierte a `sensor_msgs/LaserScan`, idéntico al del TurtleBot3.

## Diferencias de red

En hardware real, el Go2/B2 se comunica con el PC vía **Ethernet** con CycloneDDS:

```bash
# Variables de entorno necesarias en el host del robot
export RMW_IMPLEMENTATION=rmw_cyclonedds_cpp
```

En el sandbox y en la simulación se usa Fast DDS (el default de ROS 2 Jazzy)
— no necesitas cambiar nada.

## El Go2 tiene 3 DOF, el TurtleBot3 tiene 2

| Velocidad | TurtleBot3 Waffle | Unitree Go2/B2 |
|---|---|---|
| `vx` (adelante/atrás) | ✅ | ✅ |
| `vy` (izquierda/derecha) | ❌ diferencial | ✅ holonómico |
| `vyaw` (rotación) | ✅ | ✅ |

Tu código del curso base (que solo usa `vx` y `vyaw`) **funciona sin cambios** en el
Go2 — simplemente no está usando la capacidad de desplazamiento lateral.

## Resumen: lo que cambia vs. lo que se mantiene

| Concepto | ¿Cambia? | Detalle |
|---|---|---|
| Publishers y subscribers de ROS 2 | ❌ | Exactamente igual |
| Servicios y acciones de ROS 2 | ❌ | Exactamente igual |
| Nombres de topics | Parcialmente | `/cmd_vel`, `/odom`, `/scan` iguales; agregar `vy` |
| Configuración de red | Sí (hardware) | CycloneDDS + Ethernet |
| Iniciar el robot | Sí | Ejecutar `unitree_ros2_bridge.py` primero |
| Tu código `.py` | ❌ | Cero cambios necesarios |

## Actividad de este módulo

Este módulo es conceptual — no hay ejercicio de código.

1. Lee esta página completa.
2. Explora la guía de porting:
   [Portando a Unitree](../course/extras/porting-to-unitree.md).
3. Abre una sesión del sandbox con **"Unitree U1: Introducción"** y familiarízate
   con el mundo `unitree_empty` de `sim_lite` (verde = holonómico).
4. Ejecuta en una terminal del sandbox:
   ```bash
   ros2 topic list
   ros2 service list | grep sport
   ```
   Verás `/cmd_vel`, `/odom`, `/scan` y todos los `/sport/*` listos para usar.

Cuando termines, continúa con [U2 — Locomoción Holonómica](u2-locomocion.md).
