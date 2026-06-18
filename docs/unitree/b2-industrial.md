---
title: "B2: Robot Industrial de Inspección"
description: "Especificaciones del Unitree B2, diferencias respecto al Go2 EDU, y su uso en aplicaciones industriales reales."
---

# Unitree B2: Robot Cuadrúpedo Industrial

## ¿Por qué B2 para inspección industrial?

El [Unitree B2](https://www.unitree.com/b2) es la plataforma robótica cuadrúpeda de grado
industrial de Unitree. A diferencia del Go2 EDU (orientado a educación e investigación),
el B2 está diseñado para operar en entornos industriales reales con condiciones adversas.

## Especificaciones técnicas clave

| Característica | Unitree Go2 EDU | Unitree B2 |
|---|---|---|
| Peso del robot | 15 kg | 60 kg |
| Carga útil | 5 kg | 20 kg |
| Velocidad máx. | 3.5 m/s | 3.3 m/s |
| Protección IP | IP54 | **IP67** - sumergible |
| Batería | 43.6 V / 8 Ah | 43.6 V / 40 Ah |
| Autonomía | ~2 h | **~4 h** |
| LiDAR | Hesai XT-16 (opcional) | **Hesai AT128** (integrado) |
| Cámaras | 4 cámaras de profundidad | 4 cámaras de profundidad + RGB |
| Temperatura de operación | 0-40 °C | **-20 a 55 °C** |
| Grado de inspección | Educativo/investigación | **Industrial** |

## SDK y compatibilidad de software

El B2 usa exactamente el mismo SDK que el Go2: `unitree_sdk2` / `unitree_sdk2py`.
El puente `unitree_ros2_bridge.py` del curso funciona sin cambios en el B2.

```python
# Esto funciona idéntico en Go2 EDU y B2:
sport_client.Move(vx=0.5, vy=0.0, vyaw=0.0)
sport_client.StandUp()
sport_client.Hello()
```

La única diferencia es la **interfaz de red**: el B2 usa una interfaz Ethernet dedicada
y puede requerir configuración adicional de CycloneDDS para redes industriales.

## Sensores adicionales del B2

### LiDAR Hesai AT128

El B2 lleva integrado un **LiDAR de 128 canales** con 300 m de alcance, frente al LiDAR
opcional de 16 canales del Go2. Para el curso, el bridge convierte el `PointCloud2` 3D
del AT128 en un `LaserScan` 2D idéntico al que usa sim_lite.

Para SLAM 3D con el AT128 (en entornos reales), usa **FAST-LIO2**:
→ [SLAM Avanzado con FAST-LIO2](slam-avanzado.md)

### Sistema de visión

El B2 incluye cámaras RGB adicionales que permiten inspección visual de mayor calidad.
Para el curso, estas cámaras se mapean al topic `/camera/image_raw` via el bridge.

## Aplicaciones de inspección industrial típicas

El B2 se usa en aplicaciones donde el Go2 EDU no es apropiado:

### 1. Inspección de infraestructura energética
- Tuberías de gas y petróleo
- Subestaciones eléctricas
- Plantas de energía (temperatura de operación extendida)

### 2. Inspección minera y subterránea
- IP67: resiste polvo fino y salpicaduras
- Sensor LiDAR de mayor alcance para túneles
- Batería de larga duración (4 h de autonomía)

### 3. Inspección de plantas industriales
- Lectura automatizada de instrumentos (manómetros, termómetros)
- Detección de fugas mediante cámara térmica (accesorio)
- Registro de condiciones ambientales

### 4. Seguridad perimetral
- Patrullas nocturnas (cámaras de profundidad funcionan en oscuridad)
- Detección de intrusos
- Verificación de estado de puertas y accesos

## Rutina de inspección industrial con B2

La misma rutina que aprendes en U9 (`unitree_inspection.py`) se ejecuta en el B2
sin modificaciones. Para un despliegue industrial añadirías:

```python
# Extensiones industriales (no incluidas en el sandbox):
# 1. Lectura de instrumentos via cámara RGB + OCR
# 2. Termografía (cámara térmica como sensor adicional)  
# 3. Reporte automático a sistema SCADA
# 4. Integración con sistema de gestión de activos (EAM)
```

## Diferencias de configuración de red

```bash
# Go2 EDU - configuración típica de red
export RMW_IMPLEMENTATION=rmw_cyclonedds_cpp
# El Go2 actúa como AP WiFi o se conecta a la red local

# B2 - configuración industrial típica
export RMW_IMPLEMENTATION=rmw_cyclonedds_cpp
# IP estática en interfaz Ethernet dedicada (ej. 192.168.123.x)
# Puede requerir VLAN separation para entornos industriales
# Ver: https://support.unitree.com/home/zh/B2_developer
```

## Seguridad y protocolos industriales

!!! warning "Protocolo de seguridad para B2"
    El B2 pesa 60 kg. Antes de activar el movimiento:
    
    1. Asegúrate de que el área de 3 metros alrededor esté libre de personas.
    2. Ten a una persona lista para pulsar el botón de parada de emergencia.
    3. Usa `sport_client.StopMove()` (ID 1003) como parada suave antes de apagar.
    4. Nunca ejecutes `FrontFlip()` en entornos industriales - riesgo de daño.

## Preparación del robot para sesiones de inspección

```bash
# Secuencia de inicio estándar para B2
# 1. Verificar batería:
ros2 topic echo /battery_state --once

# 2. Levantar el robot (desde posición de descanso):
ros2 service call /sport/recovery_stand std_srvs/srv/Trigger

# 3. Verificar LiDAR activo:
ros2 topic hz /scan   # debe ser ~10 Hz

# 4. Lanzar rutina de inspección:
ros2 run <paquete> unitree_inspection.py

# 5. Al terminar, siempre sentar antes de apagar:
ros2 service call /sport/sit std_srvs/srv/Trigger
```

---

Continúa con [SLAM Avanzado (FAST-LIO2)](slam-avanzado.md) para 3D mapping con el LiDAR AT128 del B2.
