---
title: "G1 EDU: Robot Humanoide de Investigación"
description: "El Unitree G1 EDU con 29 DOF, manos dextrosas y stack de RL. Teleoperation con LeRobot y OpenWBT, Isaac Lab, papers de referencia."
---

# Unitree G1 EDU: Humanoide de Investigación

El [Unitree G1 EDU](https://www.unitree.com/g1) es la plataforma humanoide de investigación
de Unitree. Con 29 grados de libertad y manos dextrosas opcionales, es una de las
plataformas más accesibles para investigación en locomoción, manipulación y control
de cuerpo completo.

!!! info "Relación con el curso"
    El G1 usa el mismo `unitree_sdk2` que el Go2 EDU. El bridge `unitree_ros2_bridge.py`
    funciona con modificaciones menores. Los conceptos del curso (publishers, servicios,
    acciones, SLAM, logging) se aplican directamente al G1.

## Comparación G1 vs H1 vs Go2 EDU

| Característica | Go2 EDU Plus | G1 EDU | H1 |
|---|---|---|---|
| Tipo | Cuadrúpedo | Humanoide | Humanoide |
| Altura | ~0.6 m (de pie) | **1.27 m** | 1.8 m |
| Peso | 15 kg | **35 kg** | 47 kg |
| DOF | 12 | **29–47** | 19 |
| Manos | — | **Dextrosas (opc.)** | Básicas |
| Velocidad máx. | 3.5 m/s | **2.0 m/s** | 3.0 m/s |
| Compute | Orin NX 100 TOPS | Orin NX | Orin NX |
| Precio | ~$16 000 | desde **$43 900** | ~$90 000 |
| SDK | unitree_sdk2 | unitree_sdk2 | unitree_sdk2 |

## Configuraciones del G1

| Variante | DOF | Manos | TOPS | Precio |
|---|---|---|---|---|
| G1 Standard | 23 | Básicas | 40 | ~$16 000 |
| G1 EDU | 29 | Básicas | 100 | ~$43 900 |
| G1 EDU Ultimate A | 29 + manos dextrosas | **Dextrosas 4-DOF** | 100 | ~$90 000 |

Las **manos dextrosas** tienen 4 DOF por mano (2 por dedo × 2 dedos + muñeca), permitiendo
agarres precisos y manipulación de objetos delicados.

## Arquitectura de joints

```
Torso
├── Brazo izquierdo (7 DOF)
│   ├── Hombro: abducción, flexión, rotación
│   ├── Codo: flexión
│   ├── Muñeca: rotación, flexión
│   └── Mano: dedos (en Ultimate A)
├── Brazo derecho (7 DOF, simétrico)
├── Cadera izquierda (3 DOF)
├── Rodilla izquierda (1 DOF)
├── Tobillo izquierdo (2 DOF)
└── Lado derecho (6 DOF, simétrico)
```

Total: 29 DOF en G1 EDU, hasta 47 con manos dextrosas completas.

## Interfaz ROS 2 y SDK2

El G1 usa la misma arquitectura DDS que el Go2. Los topics DDS son:

| Topic DDS | Descripción |
|---|---|
| `rt/lf/lowstate` | Estado de todos los joints (posición, velocidad, torque) |
| `rt/lf/lowcmd` | Comando de joints a baja frecuencia |
| `rt/sportmodestate` | Estado cinemático del cuerpo |

Para correr el bridge del curso con el G1 (modificación mínima):

```python
# En unitree_ros2_bridge.py, cambiar el import:
# from unitree_sdk2py.idl.unitree_go.msg.dds_ import SportModeState_
# por:
from unitree_sdk2py.idl.unitree_hg.msg.dds_ import LowState_ as G1LowState_

# El resto del bridge es idéntico al del Go2
```

## LeRobot + G1 — teleoperation y aprendizaje por imitación

[LeRobot](https://github.com/huggingface/lerobot) de HuggingFace soporta el G1 de forma
nativa, permitiendo teleoperation, grabación de demos y entrenamiento de políticas de
manipulación-locomoción.

### Instalación

```bash
# Crear entorno
conda create -y -n lerobot python=3.12
conda activate lerobot

# Instalar SDK de Unitree
git clone https://github.com/unitreerobotics/unitree_sdk2_python.git
cd unitree_sdk2_python
pip install -e .
cd ..

# Instalar LeRobot
git clone https://github.com/huggingface/lerobot.git
cd lerobot
pip install -e ".[unitree_g1]"
```

### Teleoperation con joystick

```bash
# En el G1 (SSH 192.168.123.18):
python src/lerobot/robots/unitree_g1/run_g1_server.py --camera

# En tu laptop:
lerobot-teleoperate \
  --robot.type=unitree_g1 \
  --robot.is_simulation=false \
  --robot.robot_ip=192.168.123.18 \
  --teleop.type=unitree_g1 \
  --teleop.id=wbc_unitree \
  --display_data=true \
  --robot.controller=HolosomaLocomotionController
```

### Grabar demos para aprendizaje por imitación

```bash
# Grabar 10 demos de "agarrar un objeto"
lerobot-record \
  --robot.type=unitree_g1 \
  --robot.is_simulation=false \
  --robot.robot_ip=192.168.123.18 \
  --teleop.type=unitree_g1 \
  --teleop.id=wbc_unitree \
  --dataset.repo_id=tu-usuario/g1-grasp-demo \
  --dataset.single_task="Agarrar el cubo rojo" \
  --dataset.num_episodes=10 \
  --dataset.episode_time_s=20 \
  --dataset.push_to_hub=true
```

### Entrenar política con π₀ (pi05)

```bash
python src/lerobot/scripts/lerobot_train.py \
  --dataset.repo_id=tu-usuario/g1-grasp-demo \
  --policy.type=pi05 \
  --policy.pretrained_path=lerobot/pi05_base \
  --output_dir=./outputs/g1_grasp \
  --steps=5000 \
  --batch_size=32 \
  --policy.device=cuda
```

### Desplegar la política entrenada

```bash
python examples/rtc/eval_with_real_robot.py \
  --policy.path=tu-usuario/g1-grasp-output \
  --policy.device=cuda \
  --robot.type=unitree_g1 \
  --robot.is_simulation=false \
  --robot.controller=HolosomaLocomotionController \
  --task="Agarrar el cubo rojo" \
  --duration=60 \
  --fps=30
```

### Exoesqueleto Homunculus (locomoción + manipulación)

Para teleoperation de cuerpo completo sin Apple Vision Pro, existe el **Homunculus
Exoskeleton** — un exoesqueleto open-source de 7 DOF para controlar los brazos del G1:

**Repositorio:** [github.com/nepyope/hmc_exo](https://github.com/nepyope/hmc_exo)

```bash
# Calibrar exoesqueleto
lerobot-calibrate \
  --teleop.type=unitree_g1 \
  --teleop.left_arm_config.port=/dev/ttyACM1 \
  --teleop.right_arm_config.port=/dev/ttyACM0 \
  --teleop.id=exo
```

## OpenWBT — teleoperation con Apple Vision Pro

**Repositorio:** [github.com/GalaxyGeneralRobotics/OpenWBT](https://github.com/GalaxyGeneralRobotics/OpenWBT)

OpenWBT (Open Whole-Body Teleoperation) permite controlar el G1 con:
- **Cuerpo superior**: Apple Vision Pro captura las poses de las manos del operador
- **Cuerpo inferior**: joysticks para caminar/girar

Solo **un operador** controla el robot completo.

**Robots soportados:** G1, H1

**Entornos soportados:** Real robot, MuJoCo, Isaac Sim 4.5

```bash
git clone https://github.com/GalaxyGeneralRobotics/OpenWBT.git
pip install pyzmq pyrealsense2

# Configurar red WiFi del robot
# Lanzar en MuJoCo (sin hardware):
python openwbt/mujoco_sim.py --robot g1

# Lanzar en robot real:
python openwbt/real_robot.py --network_interface eth0 --robot g1
```

## Isaac Lab + G1 — entrenamiento RL

El repositorio oficial `unitree_rl_lab` incluye el G1 de 29 DOF:

```bash
# Entrenar control de locomoción para G1
./unitree_rl_lab.sh -t --task Unitree-G1-29dof-Velocity

# Con curriculum de terreno
./unitree_rl_lab.sh -t --task Unitree-G1-29dof-Rough-Velocity

# Visualizar en Isaac Sim (headful)
./unitree_rl_lab.sh -p --task Unitree-G1-29dof-Velocity
```

El G1 en Isaac Lab usa el mismo pipeline sim2real que el Go2:
```
Entrenamiento → MuJoCo sim2sim → Deploy C++ → G1 real
```

## Investigación con G1 EDU — papers de referencia

### Control de cuerpo completo

| Paper | Qué hace | Código |
|---|---|---|
| [AMO: Adaptive Motion Optimization](https://arxiv.org/abs/2505.03738) | Whole-body control hiper-dexterous | — |
| [OmniH2O](https://arxiv.org/abs/2406.08858) | Teleoperation H2R + learning | [github](https://github.com/LeCAR-Lab/human2humanoid) |
| [CHILD](https://arxiv.org/abs/2508.00162) | Teleoperation humanoid completo | — |

### Loco-manipulación

| Paper | Qué hace | Código |
|---|---|---|
| [Helpful DoggyBot](https://arxiv.org/abs/2410.00231) | Fetch de objetos con VLM + RL en Go2 | [Project](https://helpful-doggybot.github.io) |
| [LATENT](https://arxiv.org/abs/2503.xxxxx) | G1 jugando tenis (Tsinghua) | — |

### Plataformas open-source humanoides

| Plataforma | Institución | Código |
|---|---|---|
| Berkeley Humanoid | UC Berkeley | [github](https://github.com/HybridRobotics/cassie-mujoco-sim) |
| ToddlerBot | MIT | [arxiv](https://arxiv.org/abs/2502.00893) |
| LeRobot | HuggingFace | [github](https://github.com/huggingface/lerobot) |

## Conectar G1 EDU a ROS 2

```bash
# 1. Conectar por Ethernet al G1 (IP: 192.168.123.161)
ping 192.168.123.161

# 2. Configurar entorno
export RMW_IMPLEMENTATION=rmw_cyclonedds_cpp

# 3. Instalar SDK
pip install unitree_sdk2py

# 4. Verificar conexión DDS
python3 - <<'EOF'
from unitree_sdk2py.core.channel import ChannelFactory
ChannelFactory.Instance().Init(0, "eth0")
print("DDS conectado al G1")
EOF

# 5. Lanzar bridge (con adapter mínimo para G1)
python3 unitree_ros2_bridge.py --network_interface eth0

# 6. Verificar topics
ros2 topic list
# /cmd_vel  /odom  /battery_state  /scan (si LiDAR conectado)
```

## Modelo de programación: mismas ideas del curso

El código del curso (U1-U12) aplica con ajustes mínimos:

```python
#!/usr/bin/env python3
"""Mover el G1 con los mismos topics que el Go2."""
import rclpy
from rclpy.node import Node
from geometry_msgs.msg import TwistStamped

class MoverG1(Node):
    def __init__(self):
        super().__init__("mover_g1")
        # EXACTAMENTE el mismo código que en unitree_move.py (U2)
        self._pub_cmd = self.create_publisher(TwistStamped, "/cmd_vel", 10)
        self.create_timer(0.1, self._mover)

    def _mover(self):
        msg = TwistStamped()
        msg.twist.linear.x = 0.2   # caminar hacia adelante
        self._pub_cmd.publish(msg)

rclpy.init()
rclpy.spin(MoverG1())
```

El G1 puede caminar, girar y usar sus brazos a través de los mismos servicios
`/sport/*` del bridge. Las diferencias son de configuración de hardware, no de código.

## Seguridad — el G1 es más grande que el Go2

!!! danger "Protocolo de seguridad obligatorio"
    El G1 pesa 35 kg y puede causar lesiones si cae.

    1. **Siempre** ten al robot suspendido con cables de seguridad al aprender locomoción
    2. Despeja 2 metros alrededor del robot durante movimiento autónomo
    3. Ten un operador listo en el botón de parada de emergencia
    4. Para experimentos de manipulación, usa la versión en simulación primero:
       ```bash
       lerobot-teleoperate --robot.is_simulation=true ...
       ```
    5. La primera vez que ejecutes una política nueva, usa velocidades reducidas:
       ```bash
       # Overridear velocidad máxima en el bridge
       export G1_MAX_VEL=0.2
       ```
