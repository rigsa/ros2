---
title: "Simulación Gazebo con Unitree (instalación local)"
description: "Cómo configurar un entorno Gazebo con el B2 o Go2 en tu máquina local."
---

# Simulación Gazebo con Robots Unitree (instalación local)

El sandbox del curso usa `sim_lite` para los módulos Unitree (U1-U12) porque es muy
ligero (~150 MB RAM vs. 3-4 GB de Gazebo). Pero si tienes un PC potente y quieres
una simulación Gazebo más realista del B2 o Go2, puedes configurarlo localmente.

## Requisitos mínimos

- Ubuntu 24.04 o 22.04
- ROS 2 Jazzy instalado
- Gazebo Harmonic (la versión compatible con Jazzy)
- GPU recomendada (para renderizado fluido)
- RAM: 8 GB mínimo, 16 GB recomendado para B2

## Opción 1: go2_ros2_sdk con Gazebo

El repositorio oficial [unitree_ros2](https://github.com/unitreerobotics/unitree_ros2)
incluye paquetes de descripción y simulación.

```bash
# Instalación en tu ros2_ws local
cd ~/ros2_ws/src

# Clonar descripción del robot
git clone https://github.com/unitreerobotics/unitree_ros2.git

# Instalar dependencias
cd ~/ros2_ws
rosdep install --from-paths src --ignore-src -r -y

# Compilar
colcon build --packages-select unitree_go unitree_api go2_description --symlink-install
source install/setup.bash
```

## Opción 2: mundo de inspección con robot diferencial como placeholder

Si los paquetes de Unitree son difíciles de compilar, puedes usar el mundo de
inspección incluido en el sandbox con un robot diferencial como placeholder.
El mundo (`industrial_inspection.world`) tiene la misma geometría que el mundo
`unitree_inspection` de sim_lite.

```bash
# Copiar el mundo desde el sandbox
cp /opt/seed/worlds/industrial_inspection.world ~/ros2_ws/src/

# Lanzar con TurtleBot3 (como placeholder)
export TURTLEBOT3_MODEL=waffle
ros2 launch turtlebot3_gazebo turtlebot3_world.launch.py \
  world:=~/ros2_ws/src/industrial_inspection.world
```

Todo el código del curso (unitree_*.py) funciona con TurtleBot3 porque los topics
son idénticos. La única diferencia: TurtleBot3 es diferencial (no holonómico), por lo
que el movimiento lateral (`vy`) no funcionará.

## Opción 3: MuJoCo (recomendado para B2)

Unitree proporciona simulaciones MuJoCo para el B2 con mejor fidelidad física que
Gazebo para robots cuadrúpedos.

```bash
pip install mujoco
pip install unitree_sdk2py

# Simulación B2 en MuJoCo (viene con el SDK)
python3 -m unitree_sdk2py.examples.b2.mujoco_sim
```

## Pasos siguientes

Una vez que tengas Gazebo/MuJoCo configurado:

1. Tu código de los módulos U1-U12 funciona sin cambios
2. Para hardware real: conecta el robot y lanza `unitree_ros2_bridge.py`
3. Consulta [B2: Robot Industrial](../unitree/b2-industrial.md) para specs del hardware
4. Para SLAM 3D: ver [SLAM Avanzado con FAST-LIO2](../unitree/slam-avanzado.md)
