---
title: "Papers y Recursos de Investigación"
description: "Colección curada de papers open-source y proyectos de GitHub para investigación con Unitree Go2, G1, H1 y B2."
---

# Papers y Recursos de Investigación para Unitree Robots

Colección curada de papers con código abierto y proyectos de GitHub activos para
investigación con robots Unitree. Organizado por tema.

## Navegación y SLAM

### Navigation autonomy stack para Go2

**`autonomy_stack_go2`** — CMU / Ji Zhang  
[github.com/jizhang-cmu/autonomy_stack_go2](https://github.com/jizhang-cmu/autonomy_stack_go2)

Stack completo de autonomía en C++ con:
- **Point-LIO**: odometría LiDAR-inercial (mejor que AMCL para cuadrúpedos)
- **FAR Planner**: planificador de rutas por grafo de visibilidad
- Modos: autónomo, smart joystick (autonomía + control humano), manual
- Compatible con Go2 EDU real y simulación ROS 2 Humble/Foxy

```bash
git clone https://github.com/jizhang-cmu/autonomy_stack_go2.git
# Simulación:
./system_simulation.sh
# Robot real (Ethernet):
./system_real_robot.sh
```

---

### Coverage path planning con mapa esquelético

**"Autonomous Navigation of Quadrupeds Using Coverage Path Planning with Morphological Skeleton Map"**  
ArXiv: [2504.17880](https://arxiv.org/abs/2504.17880) | Frontiers Robotics AI 2025  
Código: [github.com/asil-lab/go2-autonomous-navigation](https://github.com/asil-lab/go2-autonomous-navigation)

Usa el Go2 EDU para cobertura completa de áreas complejas:
- Extrae un **esqueleto morfológico** del mapa de ocupación (como el eje central de los pasillos)
- Genera rutas de cobertura eficientes que no requieren planificación global completa
- ROS 2 + Nav2, compatible con sim_lite via LaserScan

```bash
git clone https://github.com/asil-lab/go2-autonomous-navigation.git
```

---

### OrionNav — navegación semántica end-to-end

**"Open-Architecture End-to-End System for Real-World Autonomous Robot Navigation"**  
ArXiv: [2410.06239](https://arxiv.org/abs/2410.06239)  

Sistema modular para Go2 EDU con Hesai LiDAR + RealSense + 2× Jetson:
- Scene graph semántico con FC-CLIP (detección zero-shot de objetos)
- LiDAR 2D SLAM + planificador LLM (GPT-4-Turbo para alta nivel)
- Control Barrier Function para evitar colisiones
- **88.5%** de éxito en 96 tareas de recuperación de objetos en entorno real

---

### FAST-LIO2 — odometría 3D LiDAR-inercial

**"FAST-LIO2: Fast Direct LiDAR-Inertial Odometry"**  
ArXiv: [2107.06829](https://arxiv.org/abs/2107.06829) | RA-L 2022  
Código: [github.com/hku-mars/FAST_LIO](https://github.com/hku-mars/FAST_LIO)  
ROS 2 port: [github.com/Ericsii/FAST_LIO_ROS2](https://github.com/Ericsii/FAST_LIO_ROS2)

Odometría LiDAR-IMU de alta frecuencia (100-500 Hz) robusta a las vibraciones de
los cuadrúpedos. Ideal para B2 con Hesai AT128.

---

## Reinforcement Learning — locomoción

### unitree_rl_lab — oficial Unitree

[github.com/unitreerobotics/unitree_rl_lab](https://github.com/unitreerobotics/unitree_rl_lab)  
Isaac Lab 2.3.0 + Isaac Sim 5.1.0 · RSL-RL

Entrenamiento de locomoción para Go2, G1-29dof, H1. Pipeline completo:
entrenamiento → validación MuJoCo → deployment C++ en hardware.

```bash
./unitree_rl_lab.sh -t --task Unitree-Go2-Velocity-v0
./unitree_rl_lab.sh -t --task Unitree-G1-29dof-Velocity
```

---

### unitree_rl_gym — entorno PyBullet / Isaac Gym (clásico)

[github.com/unitreerobotics/unitree_rl_gym](https://github.com/unitreerobotics/unitree_rl_gym)

Entorno predecesor basado en Isaac Gym (antes de Isaac Lab). Útil como referencia
de curricula y recompensas para locomoción.

---

### Isaac Go2 ROS2 — navegación en Isaac Sim

[github.com/Zhefan-Xu/isaac-go2-ros2](https://github.com/Zhefan-Xu/isaac-go2-ros2)  
Isaac Sim 4.5 + Isaac Lab 2.1.0 + ROS 2 Humble

Plataforma para testing de navegación en almacenes y campos de obstáculos.
Política RL preentrenada incluida. Soporta YOLO, segmentación semántica, LLM.

---

### go2_omniverse — URDFs + configs Isaac Lab

[github.com/abizovnuralem/go2_omniverse](https://github.com/abizovnuralem/go2_omniverse)

URDFs calibrados, USD models y configs de sensores para Go2 y G1 en Isaac Lab.
Punto de partida para tareas de RL personalizadas.

---

## Manipulación loco-manipulation

### Helpful DoggyBot — fetch de objetos con VLM

**"Helpful DoggyBot: Open-World Object Fetching using Legged Robots and Vision-Language Models"**  
ArXiv: [2410.00231](https://arxiv.org/abs/2410.00231)  
Web: [helpful-doggybot.github.io](https://helpful-doggybot.github.io)

Go2 con un gripper 3D-printed usando VLM (Florence 2) + RL para agarrar y entregar
objetos sin entrenamiento específico de la tarea. Zero-shot transfer.

---

### D1 arm SDK y ROS 2

[github.com/unitreerobotics/unitree_arm_ros2](https://github.com/unitreerobotics/unitree_arm_ros2)

Paquete ROS 2 para el brazo D1 de Unitree (6 DOF + gripper). Incluye:
- Topics para posición cartesiana y de joints
- MoveIt 2 integration
- Ejemplos de pick & place

---

## Control de cuerpo completo — G1 Humanoid

### OpenWBT — teleoperation con Apple Vision Pro

[github.com/GalaxyGeneralRobotics/OpenWBT](https://github.com/GalaxyGeneralRobotics/OpenWBT)

G1 + H1: control de cuerpo completo con un solo operador.
Superior: Apple Vision Pro (poses de manos) · Inferior: joysticks.
Soporta: robot real, MuJoCo, Isaac Sim 4.5.

---

### OmniH2O — teleoperation H2R + imitation learning

**"OmniH2O: Universal and Dexterous Human-to-Humanoid Whole-Body Teleoperation and Learning"**  
ArXiv: [2406.08858](https://arxiv.org/abs/2406.08858)  
Código: [github.com/LeCAR-Lab/human2humanoid](https://github.com/LeCAR-Lab/human2humanoid)

Teleoperation de cuerpo completo con capacidad de aprender por imitación.
Aplicado a Go2 y G1.

---

### AMO: Adaptive Motion Optimization

**"AMO: Adaptive Motion Optimization for Hyper-Dexterous Humanoid Whole-Body Control"**  
ArXiv: [2505.03738](https://arxiv.org/abs/2505.03738)

Control de cuerpo completo altamente dexterous para el G1.

---

### LeRobot + G1

[huggingface.co/docs/lerobot/unitree_g1](https://huggingface.co/docs/lerobot/unitree_g1)

Framework de HuggingFace para:
- Teleoperation con joystick / exoesqueleto Homunculus
- Grabación de demos (lerobot-record)
- Entrenamiento de políticas (π₀/pi05, ACT, Diffusion Policy)
- Deployment con inferencia RTC en tiempo real

```bash
lerobot-teleoperate --robot.type=unitree_g1 ...
lerobot-record       --robot.type=unitree_g1 ...
lerobot-train        --dataset.repo_id=... --policy.type=pi05
```

---

## Interfaces y Gazebo / Simulación

### unitree_go2_ros2 — ROS 2 Jazzy + Gazebo Harmonic

[github.com/khaledgabr77/unitree_go2_ros2](https://github.com/khaledgabr77/unitree_go2_ros2)

Primera integración completa con **ROS 2 Jazzy + Gazebo Harmonic** (último Gazebo).
CHAMP controller, URDFs, teleoperation, spawner. En desarrollo activo — WIP para Nav2.

---

### CHAMP — controlador de cuadrúpedos para ROS 2

[github.com/chvmp/champ](https://github.com/chvmp/champ)

Framework general para cuadrúpedos en ROS 2. Soporta Go2, Spot, A1 y custom robots.
Proporciona control de gait, planificación de patas y Nav2 integration.

```bash
ros2 launch champ_bringup bringup.launch.py robot:=go2
```

---

### go2w agent SDK — control con agentes AI

[github.com/grasp-lyrl/unitree_go2w_agent_sdk](https://github.com/grasp-lyrl/unitree_go2w_agent_sdk)

SDK unificado para el Go2W (ruedas) con soporte para agentes AI:
- YOLOv8/v9 para detección de objetos
- RealSense RGB-D
- Interfaz para AgileX Piper arm
- ROS 2 bridge

---

## g1pilot — G1 en ROS 2

[github.com/hucebot/g1pilot](https://github.com/hucebot/g1pilot)

Paquete ROS 2 completo para el G1 humanoid:
- Control de joints con `sensor_msgs/JointState`
- Estado del robot en ROS 2
- Launch files para operación real y simulación

---

## Recursos de aprendizaje complementarios

### Cursos reconocidos de ROS 2

| Plataforma | Curso | Nivel |
|---|---|---|
| [The Construct](https://app.theconstruct.ai) | ROS 2 for Beginners / Intermediate / Advanced | Todos |
| [OpenRobotics](https://discourse.openrobotics.org/t/new-ros-2-skills-certification-courses/42181) | ROS 2 Skills Certification | Certificación |
| [Robocademy](https://robocademy.com) | ROS 2 + NVIDIA Isaac — learning path completo | Intermedio-Avanzado |
| [Udemy](https://www.udemy.com/course/ros2-for-beginners) | ROS 2 for Beginners (Jazzy 2026) | Principiante |

### Repositorios curatoriales

| Recurso | Descripción |
|---|---|
| [awesome-unitree-robots](https://github.com/shaoxiang/awesome-unitree-robots) | Lista curada de proyectos Unitree |
| [github.com/topics/unitree](https://github.com/topics/unitree?o=desc&s=forks) | Todos los repos por forks |
| [github.com/topics/unitree-go2](https://github.com/topics/unitree-go2) | Específicos del Go2 |

### Documentación oficial de Unitree

| Recurso | URL |
|---|---|
| SDK2 Python | [github.com/unitreerobotics/unitree_sdk2_python](https://github.com/unitreerobotics/unitree_sdk2_python) |
| SDK2 C++ | [github.com/unitreerobotics/unitree_sdk2](https://github.com/unitreerobotics/unitree_sdk2) |
| Unitree IL + LeRobot | [github.com/unitreerobotics/unitree_IL_lerobot](https://github.com/unitreerobotics/unitree_IL_lerobot) |
| ROS 2 to real (Go1/Go2) | [github.com/unitreerobotics/unitree_ros2_to_real](https://github.com/unitreerobotics/unitree_ros2_to_real) |
| Soporte técnico B2 | [support.unitree.com/home/zh/B2_developer](https://support.unitree.com/home/zh/B2_developer) |

---

## Guía de entrada rápida por objetivo

| Quiero... | Recurso |
|---|---|
| Navegar autónomamente con Go2 en laboratorio | `autonomy_stack_go2` (Point-LIO + FAR Planner) |
| Entrenar gait en simulación + deploy real | `unitree_rl_lab` (Isaac Lab) |
| Cobertura de área (inspección) | `go2-autonomous-navigation` (skeleton map) |
| Manipulación pick & place con Go2 + D1 | `unitree_arm_ros2` + `Helpful DoggyBot` |
| Teleoperation G1 de cuerpo completo | `OpenWBT` o `LeRobot + Homunculus Exo` |
| Imitation learning para tareas de manipulación | `LeRobot + π₀` |
| SLAM 3D con B2 + Hesai AT128 | `FAST-LIO2 ROS2 port` |
| Integración con Gazebo Harmonic (ROS 2 Jazzy) | `unitree_go2_ros2` (CHAMP) |
