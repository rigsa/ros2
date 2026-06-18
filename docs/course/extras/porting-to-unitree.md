---
title: "Portando a un Unitree Go2/B2"
description: "Cómo las interfaces de ROS 2 que practicas en las Partes 1-6 se mapean a un Unitree Go2 EDU, AS2 EDU o B2."
---

Este curso enseña ROS 2 usando un robot diferencial simulado (Partes 1-6).
Pero casi todo lo que escribes  - 
publishers/subscribers, services, actions, y las interfaces basadas en topics que usas para
controlar el robot y leer sus sensores - **no es específico de ningún modelo de robot**.
Es ROS 2 estándar. Si tu objetivo final es una plataforma diferente - por ejemplo un
[Unitree Go2 EDU](https://www.unitree.com/go2) o [B2](https://www.unitree.com/b2)  - 
los *patrones* que has aprendido se transfieren directamente. Lo que cambia es qué topics y
APIs se encuentran del otro lado de tu node.

!!! note "El robot Go2 EDU también está disponible en el laboratorio"
    Además del robot diferencial utilizado en las simulaciones del curso, el laboratorio
    cuenta con robots **Unitree Go2 EDU, AS2 EDU y B2** disponibles para experimentación. Las
    indicaciones de esta página son especialmente relevantes si planeas trabajar con ellos.

Esta página mapea cada interfaz del curso a su equivalente en Unitree, basándose en dos
proyectos de integración de Unitree existentes: un [stack de autonomía completo para Go2](https://github.com/rigsa/unitree_rigsa)
(derivado del `autonomy_stack_go2` de CMU) y una [configuración de desarrollo para B2](https://github.com/rigsa/sdk_unitree).
Ninguno de esos proyectos es material del curso - son código de puesta en marcha para robots reales  - 
pero son la mejor referencia disponible para "¿cómo se ve la interfaz real?".

!!! note "Esta es una guía solo de documentación"
    No existe ninguna simulación Gazebo de Go2/B2 para este curso (todavía). Esta página trata sobre
    portar tu *código* una vez que pasas de la simulación TurtleBot3 del curso a
    hardware Unitree real (o simulado) - no cambia nada sobre cómo se realizan los
    laboratorios en sí.

## Mapeo de Interfaces

| Interfaz del Curso | Robot diferencial (Partes 1-6) | Equivalente Unitree Go2 EDU / AS2 EDU | Equivalente Unitree B2 |
|---|---|---|---|
| `/cmd_vel` ([`TwistStamped`](../part2/move_square.md)) | Plugin Gazebo de tracción diferencial; 2 DOFs controlables (`vx`, `vyaw`) | Sin subscriber `/cmd_vel` por defecto. El movimiento de alto nivel va a través de `SportClient::Move(vx, vy, vyaw)` de `unitree_api` - nota que Go2 es **holonómico** (3 DOFs, puede desplazarse lateralmente con `vy`). Ya existe un puente `/cmd_vel` → `Move()` (aunque deshabilitado) en `go2_sport_api/src/vel_ctrl_repub.cpp` | Misma familia de API de movimiento de alto nivel `SportClient`/`unitree_sdk2`, configurada sobre CycloneDDS/red del host (ver configuración Docker de `sdk_unitree`) |
| `/odom` ([`Odometry`](../part2/odom_subscriber.md)) | Estimación de posición del propio plugin diff-drive de Gazebo | `unitree_go::msg::SportModeState` (referenciado en `vel_ctrl_repub.cpp`) lleva la estimación de posición/velocidad propia del Go2; escribe un node delgado que lo republique como `nav_msgs/Odometry` y tu lógica existente de `move_square.py`/`quaternion_to_euler` no necesita más cambios | El stack SLAM a bordo (`point_lio_unilidar`, ver el README de `unitree_rigsa`) es la fuente de posición análoga para plataformas clase B2 que ejecutan el mismo stack de autonomía |
| `/scan` ([`LaserScan`](../part3/lidar_subscriber.md)) | LiDAR 2D nativo | El LiDAR L1 del Go2 es **3D** (nube de puntos), publicado en `/utlidar/cloud` - no es un `LaserScan` nativo. Necesitarás un slice pointcloud→laserscan (por ejemplo, `pointcloud_to_laserscan`) antes de que la lógica de procesamiento de arrays de `lidar_subscriber.py` se aplique sin modificaciones - esta es la única brecha de interfaz real, no solo un cambio de nombre de topic | Mismo modelo de sensado basado en nube de puntos |
| `/camera/image_raw` ([`Image`](../part6/object_detection.md)) | Plugin de cámara Gazebo (sim) / cámara RGB del robot real | Publicado como `/camera/image/raw`, mismo tipo `sensor_msgs/Image` - tu pipeline de `cv_bridge`/OpenCV (`object_detection.py`, `line_follower.py`) se porta sin cambios una vez suscrito al nombre correcto del topic | Cámara de profundidad RealSense, configurada de manera idéntica a cualquier otra integración RealSense de ROS 2 (ver la instalación de `ros-humble-realsense2-camera` en el Dockerfile de `sdk_unitree`) |
| `rigsa_interfaces/srv/NumberGame` ([servicio personalizado](../part4/number_game_client.md)) | Solo pedagógico - sin equivalente específico del robot | N/A - el *patrón de solicitud/respuesta de servicio* es lo que se transfiere, no este mensaje en particular | N/A |
| `rigsa_interfaces/action/CameraSweep` ([action personalizada](../part5/minimal_action_client.md)) | Solo pedagógico | Las APIs de "truco" de alto nivel del Go2 (`Hello`, `Stretch`, `Dance1`/`Dance2`, `FrontFlip`, ...) en `ros2_sport_client.h` son llamadas de larga duración tipo objetivo - un objetivo natural para un action server del mundo real, envuelto de la misma manera que `CameraSweep`/`ExploreForward` en este curso | Misma familia de API `SportClient` |

## Redes: Una Diferencia de Configuración, No de Código

Los robots Go2/B2 EDU se comunican sobre **CycloneDDS** en un enlace Ethernet con red del host
al computador a bordo del robot (`RMW_IMPLEMENTATION=rmw_cyclonedds_cpp`,
`network_mode: host` en Docker), en lugar de la configuración RMW predeterminada usada para el
robot diferencial simulado en este curso. Ninguno de tu código de node necesita cambiar para esto  - 
es una preocupación de entorno/launch, no algo que el código `rclpy` tenga que contemplar.

## El Go2 tiene más grados de libertad que el robot diferencial

El robot diferencial del curso solo puede moverse hacia adelante/atrás y rotar
(`vx`, `vyaw`). El Go2 es holonómico y también puede desplazarse lateralmente (`vy`). Cualquier código del curso
que solo establezca `vx`/`vyaw` (por ejemplo, `move_square.py`) sigue funcionando sin modificaciones en un
Go2 - simplemente no estás usando una capacidad que el cuadrúpedo tiene y que el robot diferencial no tiene.

## Archivos de Referencia

- `unitree_rigsa/src/utilities/unitree_pkgs/go2_sport_api/include/common/ros2_sport_client.h`
  - la API completa de `SportClient` (movimiento + actions de "trucos")
- `unitree_rigsa/src/utilities/unitree_pkgs/go2_sport_api/src/vel_ctrl_repub.cpp`
  - el puente de topic nativo Go2 ↔ `/cmd_vel`/`/odom` referenciado anteriormente
- `unitree_rigsa/README.md` - nombres de topics de LiDAR/cámara/IMU, stack SLAM, calibración
- `sdk_unitree/.docker/Dockerfile`, `docker-compose.yml` - configuración Docker/redes para B2