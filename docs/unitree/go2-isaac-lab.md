---
title: "Go2 en Isaac Sim / Isaac Lab"
description: "Entrena políticas de locomoción y navegación para el Go2 en NVIDIA Isaac Lab, y despliégalas en el robot real con sim2real."
---

# Go2 EDU en NVIDIA Isaac Sim / Isaac Lab

NVIDIA Isaac Lab es el entorno de referencia para entrenamiento de políticas de RL para
robots físicos. Para el Go2 existen múltiples proyectos open-source que van desde URDF
básico hasta pipelines completos de entrenamiento + sim2real.

## Ecosistema de herramientas NVIDIA para robótica

```
Isaac Sim        ← simulador de física (PhysX + RTX rendering)
     ↓
Isaac Lab        ← framework de RL sobre Isaac Sim (reemplaza a Isaac Gym)
     ↓
Isaac ROS        ← paquetes ROS 2 acelerados por GPU (perception, Nav2, etc.)
     ↓
Isaac Perceptor  ← pipeline de percepción 3D para navegación autónoma
```

Para el Go2 el camino más directo es **Isaac Lab → política de locomoción → ROS 2**.

## Proyectos open-source para Go2 en Isaac

### 1. `unitree_rl_lab` — Oficial de Unitree Robotics

**Repositorio:** [github.com/unitreerobotics/unitree_rl_lab](https://github.com/unitreerobotics/unitree_rl_lab)

El repositorio oficial de Unitree con implementaciones de RL para Go2, G1 y H1.
Basado en **Isaac Lab 2.3.0+** y **Isaac Sim 5.1.0+**.

```bash
# Instalación
git clone https://github.com/unitreerobotics/unitree_rl_lab.git
cd unitree_rl_lab

# Requiere conda con Isaac Lab ya instalado
conda activate isaaclab   # entorno de Isaac Lab

# Entrenar política de locomoción para Go2
./unitree_rl_lab.sh -t --task Unitree-Go2-Velocity-v0

# Visualizar entrenamiento
./unitree_rl_lab.sh -p --task Unitree-Go2-Velocity-v0
```

**Robots soportados:**
- `Unitree-Go2-Velocity-v0` — locomoción con velocidades variables
- `Unitree-G1-29dof-Velocity` — G1 de 29 DOF
- `Unitree-H1-Velocity` — H1 humanoid

**Pipeline de deployment:**
```
Entrenamiento Isaac Lab (GPU)
        ↓
Validación Sim2Sim en MuJoCo
        ↓
Compilación C++ del controlador
        ↓
Deploy en Go2 EDU real
```

El directorio `deploy/` contiene el controlador C++ que se compila con CMake e
interfaza directamente con `unitree_sdk2`:

```bash
cd deploy
mkdir build && cd build
cmake .. -DCMAKE_BUILD_TYPE=Release
make -j$(nproc)

# Ejecutar en el robot (conectado por Ethernet)
./unitree_controller --interface eth0 --policy ../policies/go2_velocity.pt
```

### 2. `isaac-go2-ros2` — Plataforma de navegación

**Repositorio:** [github.com/Zhefan-Xu/isaac-go2-ros2](https://github.com/Zhefan-Xu/isaac-go2-ros2)

Plataforma para testing de **navegación, toma de decisiones y tareas autónomas**
del Go2 en Isaac Sim con interfaz ROS 2 completa.

**Requisitos:**
- Isaac Sim 4.5 (`~/isaacsim/`)
- Isaac Lab 2.1.0 (conda)
- ROS 2 Humble

**Entornos disponibles:**

| ID | Entorno | Descripción |
|---|---|---|
| 0 | Warehouse basic | Almacén vacío |
| 1 | Warehouse forklifts | Con carretillas elevadoras |
| 2 | Warehouse shelves | Con estanterías |
| 3 | Warehouse full | Almacén completo |
| 4 | Obstacle sparse | Campo con pocos obstáculos |
| 5 | Obstacle medium | Densidad media |
| 6 | Obstacle dense | Alta densidad de obstáculos |

**Topics ROS 2 publicados:**

| Topic | Tipo | Descripción |
|---|---|---|
| `/unitree_go2/cmd_vel` | `Twist` | Control de velocidad |
| `/unitree_go2/odom` | `Odometry` | Odometría |
| `/unitree_go2/lidar/point_cloud` | `PointCloud2` | LiDAR simulado |
| `/unitree_go2/camera/color` | `Image` | Cámara RGB |
| `/unitree_go2/camera/depth` | `Image` | Profundidad |
| `/unitree_go2/camera/segmentation` | `Image` | Segmentación semántica |

```bash
# Lanzar simulación en entorno de almacén
python launch_go2_warehouse.py --env_id 2 --num_robots 1

# En otra terminal: teleop
ros2 run teleop_twist_keyboard teleop_twist_keyboard \
  --ros-args -r cmd_vel:=/unitree_go2/cmd_vel

# Visualizar en RViz2
ros2 launch isaac_go2_ros2 rviz2.launch.py
```

**Integración con RL:**

El repositorio incluye ejemplos de agentes RL preentrenados que usan la interfaz
ROS 2 para recibir observaciones y publicar acciones:

```python
# Cargar política preentrenada
import torch

policy = torch.jit.load("policies/go2_flat_terrain.pt")

# Loop de control
obs = get_observation()     # de los topics ROS 2
action = policy(obs)        # inferencia
publish_cmd_vel(action)     # publicar en /unitree_go2/cmd_vel
```

### 3. `go2_omniverse` — URDFs y configs para Isaac Lab

**Repositorio:** [github.com/abizovnuralem/go2_omniverse](https://github.com/abizovnuralem/go2_omniverse)

Proporciona los **URDFs calibrados**, configuraciones de sensores y workflows de
sim2real para Go2 y G1 en Isaac Lab.

```bash
git clone https://github.com/abizovnuralem/go2_omniverse.git

# Incluye:
# - go2/urdf/go2.urdf         ← URDF del Go2
# - go2/usd/go2.usd           ← modelo USD para Isaac Sim
# - g1/urdf/g1_29dof.urdf     ← URDF del G1 (29 DOF)
# - configs/go2_sensors.yaml  ← configuración de cámara, LiDAR, IMU
```

Este repositorio es el punto de partida para crear tareas de RL customizadas en Isaac Lab.

### 4. `Go2_Isaac_ros2` — Navegación + YOLO + LLM

**Repositorio:** [github.com/sallu-786/Go2_Isaac_ros2](https://github.com/sallu-786/Go2_Isaac_ros2)

Plataforma avanzada que integra:
- Navegación autónoma con política RL preentrenada
- **Detección de objetos con YOLO** en tiempo real
- **Control por LLM** (comandos en lenguaje natural)
- Interfaz web con visualización de grafo de topics

```bash
git clone https://github.com/sallu-786/Go2_Isaac_ros2.git

# Políticas disponibles:
# actor_critic/  — locomotion policy flat terrain
# student/       — locomotion policy rough terrain
```

## Instalar Isaac Lab — guía rápida

**Requisitos mínimos:**
- GPU NVIDIA con ≥ 12 GB VRAM (RTX 3080 Ti / A4000 o superior)
- CUDA 12.x
- Ubuntu 22.04
- RAM: 32 GB recomendado

```bash
# 1. Instalar Isaac Sim 5.1.0
# Descargar desde: https://developer.nvidia.com/isaac/sim
# Extrae en ~/isaacsim/

# 2. Clonar Isaac Lab
git clone https://github.com/isaac-sim/IsaacLab.git
cd IsaacLab

# 3. Crear entorno conda
./isaaclab.sh --conda isaaclab
conda activate isaaclab

# 4. Instalar
./isaaclab.sh --install

# 5. Verificar instalación
./isaaclab.sh -p source/standalone/tutorials/00_sim/create_empty.py
```

## Workflow completo: entrenar y desplegar en Go2

### Paso 1: Entrenar política de locomoción

```bash
# En el PC con GPU (puede tardar 2-8 horas)
conda activate isaaclab

./unitree_rl_lab.sh -t \
  --task Unitree-Go2-Velocity-v0 \
  --headless \         # sin renderizado (más rápido)
  --max_iterations 5000

# Los checkpoints se guardan en logs/Go2Velocity/
```

### Paso 2: Validar en MuJoCo (sim2sim)

```bash
# Instalar MuJoCo
pip install mujoco

# Ejecutar la política en MuJoCo
python deploy/mujoco_sim.py \
  --policy logs/Go2Velocity/model_5000.pt \
  --urdf go2/urdf/go2.urdf
```

MuJoCo es un simulador diferente a Isaac Sim — si la política funciona en ambos,
es más probable que funcione en hardware real (el "transfer gap" es menor).

### Paso 3: Desplegar en Go2 real

```bash
# En el host conectado al Go2 por Ethernet
export RMW_IMPLEMENTATION=rmw_cyclonedds_cpp

# Compilar el controlador de deployment
cd deploy && mkdir build && cd build
cmake .. && make -j4

# Poner el robot en modo de control bajo nivel
ros2 service call /sport/damp std_srvs/srv/Trigger

# Ejecutar la política (comando de referencia de velocidad desde /cmd_vel)
./unitree_go2_controller \
  --policy ../../logs/Go2Velocity/model_5000.pt \
  --interface eth0 \
  --cmd_vel_topic /cmd_vel
```

### Paso 4: Conectar con la pila de navegación

Con la política de locomoción activa como "capa de bajo nivel", puedes usar
la pila de ROS 2 del curso como "capa de alto nivel":

```
Nav2 (planificador de ruta)
        ↓ /cmd_vel
  Política RL (locomotion)    ← reemplaza la marcha stock del SDK
        ↓ LowCmd DDS
      Go2 EDU (hardware)
```

```python
# El nodo de locomoción RL se suscribe a /cmd_vel
# y traduce velocidades a comandos de joint:
self.create_subscription(Twist, "/cmd_vel", self._vel_cb, 10)

def _vel_cb(self, msg):
    obs = self._build_observation(msg.linear.x, msg.linear.y, msg.angular.z)
    action = self._policy(obs)        # inferencia de la red neuronal
    self._apply_lowcmd(action)        # enviar a los motores
```

## Temas de investigación habilitados

Con Isaac Lab + Go2 EDU puedes explorar:

| Tema | Recursos recomendados |
|---|---|
| Locomoción en terreno irregular | `unitree_rl_lab` Velocity tasks con terrain curriculum |
| Navegación semántica | `isaac-go2-ros2` + segmentation topic |
| Manipulación + locomoción | `go2_omniverse` con D1 arm URDF |
| Multi-robot | `isaac-go2-ros2` `--num_robots N` |
| Control con LLM | `Go2_Isaac_ros2` portal web |
| Sim2Real transfer | `unitree_rl_lab` deploy pipeline |

## Referencia rápida de requisitos por proyecto

| Proyecto | Isaac Sim | Isaac Lab | ROS 2 | GPU VRAM |
|---|---|---|---|---|
| `unitree_rl_lab` | 5.1.0 | 2.3.0 | Humble | 16 GB |
| `isaac-go2-ros2` | 4.5.0 | 2.1.0 | Humble | 12 GB |
| `go2_omniverse` | 4.x+ | 2.x+ | Humble | 8 GB |
| `Go2_Isaac_ros2` | 4.5.0 | 2.1.0 | Humble | 12 GB |

!!! tip "Sin GPU? Usa el sandbox del curso"
    Si no tienes GPU disponible, `sim_lite.py` del sandbox es suficiente para el
    curso U1-U12. Isaac Lab se necesita solo para investigación de RL y sim2real.
    El sandbox no requiere GPU y corre en el navegador.
