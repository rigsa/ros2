---
title: "B1: Introducción al K1 — Hardware y Arquitectura"
description: "Especificaciones del Booster K1, modos de operación, conexión y el patrón bridge para ROS 2."
---

# B1: Introducción al K1

## El robot

| Propiedad | Valor |
|-----------|-------|
| Altura | 95 cm |
| Peso | 19.5 kg |
| Grados de libertad | 22 DoF |
| Velocidad máxima | ~0.4 m/s |
| Cómputo (EDU) | Jetson Orin NX 8GB — 117 TOPS |
| Batería (EDU) | 5 Ah — ~80 min |
| Conectividad | Ethernet, WiFi 6, Bluetooth 5.2 |
| IP por defecto | 192.168.10.102 |

## Modos de operación

El K1 pasa secuencialmente por estos estados al encenderse:

```
DAMP → PREP → WALK → CUSTOM → PROTECT (automático al caer)
```

- **DAMP**: articulaciones pasivas (seguro para maniobrar manualmente)
- **PREP**: posición de pie con control de posición (espera 3 s)
- **WALK**: responde a comandos de locomoción
- **CUSTOM**: control via SDK (requiere fixture de desarrollo)
- **PROTECT**: modo seguro automático al detectar caída

## Los 22 grados de libertad

```
Cabeza (2):    head_yaw, head_pitch
Brazo izq (4): l_shoulder_pitch, l_shoulder_roll, l_shoulder_yaw, l_elbow_pitch
Brazo der (4): r_shoulder_pitch, r_shoulder_roll, r_shoulder_yaw, r_elbow_pitch
Pierna izq (6): l_hip_pitch, l_hip_roll, l_hip_yaw, l_knee_pitch, l_ankle_pitch, l_ankle_roll
Pierna der (6): r_hip_pitch, r_hip_roll, r_hip_yaw, r_knee_pitch, r_ankle_pitch, r_ankle_roll
```

## Arquitectura del sistema

```
┌──────────────────────────────────┐
│         Tu código ROS 2          │
│  /cmd_vel  /odom  /joint_states  │
│  /imu/data  /camera/image_raw    │
│  /scan  /sport/*                 │
└──────────────┬───────────────────┘
               │ topics ROS 2 estándar
   ┌───────────┴───────────┐
   │                       │
┌──▼──────────┐   ┌────────▼──────────────┐
│booster_sim_ │   │ booster_ros2_bridge.py │
│lite.py      │   │ (robot real)           │
│(simulador)  │   │ booster_robotics_sdk   │
└─────────────┘   └───────────┬───────────┘
                               │ SDK FastDDS
                        ┌──────▼──────┐
                        │ Booster K1  │
                        │(hardware)   │
                        └─────────────┘
```

## Conexión al robot real

```bash
# Configurar red: PC en 192.168.10.10 / 255.255.255.0
ssh booster@192.168.10.102   # contraseña: 123456

# Instalar SDK Python
pip install booster_robotics_sdk_python --user

# Verificar conexión
python3 -c "from booster_robotics_sdk_python import RobotClient; print('SDK OK')"
```

!!! info "En el sandbox"
    No necesitas conexión física. El sandbox usa `booster_sim_lite.py`
    que publica los mismos topics que el robot real.
