---
title: "AS2 EDU: El robot de inspección con IA embebida"
description: "Especificaciones del Unitree AS2 EDU, conectividad WiFi 6, CPU de 8 núcleos y uso en inspección autónoma con IA."
---

# Unitree AS2 EDU

El [Unitree AS2 EDU](https://www.unitree.com/mobile/As2) es el robot cuadrúpedo más
reciente de Unitree, diseñado para llenar el espacio entre el Go2 EDU (ligero, educativo)
y el B2 (pesado, industrial). Combina alta velocidad, conectividad WiFi 6 nativa y un
procesador de 8 núcleos capaz de ejecutar modelos de IA directamente en el robot.

## Especificaciones técnicas

| Característica | AS2 EDU | Go2 EDU | B2 |
|---|---|---|---|
| Peso | **18 kg** | 15 kg | 60 kg |
| Velocidad máx. | **5 m/s** | 3.5 m/s | 3.3 m/s |
| Carga útil (estática) | **65 kg** | 10 kg | 20 kg |
| Carga útil (caminando) | 15 kg | 5 kg | - |
| Batería (estándar) | 8 000 mAh | - | 40 Ah |
| Batería (larga) | 15 000 mAh | - | - |
| Autonomía | ~4 h (sin carga) | ~2 h | ~4 h |
| Conectividad | **WiFi 6 + BT 5.2 + 4G** | WiFi 5 + BT | Ethernet |
| LiDAR | **L2 / 64-128 líneas** | L1 (16 líneas) | Hesai AT128 (128 líneas) |
| CPU | **8 núcleos** | 4 núcleos | 4 núcleos |
| Protección | IP54 | IP54 | IP67 |
| Temperatura | -20 a 50 °C | 0 a 40 °C | -20 a 55 °C |
| Inclinación máx. | 40° | 30° | 30° |
| Subida de escalones | 25 cm | 20 cm | 20 cm |
| Ethernet | Gigabit | 100 Mbps | Gigabit |
| GPS / 4G | Sí (desactivado por defecto) | No | No |

## El AS2 EDU en inspección autónoma

### 1. Conectividad WiFi 6 nativa

El AS2 puede conectarse a tu red WiFi de laboratorio directamente, sin necesidad de un
cable Ethernet. Esto simplifica la puesta en marcha del bridge:

```bash
# AS2 EDU conectado a la red WiFi del robot (el robot actúa como AP)
export RMW_IMPLEMENTATION=rmw_cyclonedds_cpp
python3 unitree_ros2_bridge.py --network_interface wlan0

# O si el AS2 está conectado a tu red local (modo cliente)
python3 unitree_ros2_bridge.py --network_interface wlan0
```

El WiFi 6 (802.11ax) reduce la latencia de comunicación significativamente respecto
al WiFi 5 del Go2, importante para control reactivo en tiempo real.

### 2. Alta velocidad para cobertura de área

Con 5 m/s de velocidad máxima, el AS2 puede recorrer un área de inspección grande
en mucho menos tiempo que el Go2 (3.5 m/s) o el B2 (3.3 m/s).

Para aprovechar esto en los módulos del curso, aumenta las velocidades en los nodos:

```python
# En unitree_waypoint_nav.py o unitree_inspection.py
VEL_LINEAL_MAX  = 0.5    # m/s - puedes subir hasta 1.0-1.5 en el AS2
VEL_ANGULAR_MAX = 0.8    # rad/s
```

### 3. CPU de 8 núcleos - IA embebida

El AS2 integra un procesador de 8 núcleos capaz de ejecutar inferencia local.
Esto permite pipelines de inspección que no dependen de un servidor externo:

```
Cámara RGB
    ↓
Modelo de detección de defectos (ONNX / TensorFlow Lite)
    → corre en el AS2, sin red externa
    ↓
Publicar /inspection/anomalias en ROS 2
    ↓
unitree_inspection.py decide si detener, inspeccionar más o registrar
```

Esta capacidad se explota en futuros módulos avanzados; por ahora, el curso usa
detección ArUco clásica (OpenCV) que funciona en cualquier CPU.

### 4. GPS y 4G integrados (desactivados por defecto)

Para despliegues en exteriores, el AS2 puede activar el GPS y la conectividad 4G.
Esto abre la puerta a aplicaciones como:

- Navegación en entornos GPS (gasoductos, líneas eléctricas en campo abierto)
- Reporte en tiempo real a través de red móvil (sin WiFi local)
- Seguimiento de posición absoluta en mapas georeferenciados

Para el curso, estos módulos permanecen desactivados y se usa odometría interna.

## Compatibilidad con el SDK y el bridge

El AS2 usa exactamente el mismo `unitree_sdk2` que el Go2 EDU y el B2. El bridge
`unitree_ros2_bridge.py` funciona sin cambios de código:

```python
# Mismo SportClient, mismas llamadas:
sport_client.Move(vx=0.5, vy=0.1, vyaw=0.0)  # funciona en Go2, AS2 y B2
sport_client.StandUp()
sport_client.Hello()
```

El topic del LiDAR del AS2 (L2 o 64-128 líneas) es `/utlidar/cloud`, el mismo que
el Go2 L1. El bridge lo convierte a `/scan` (LaserScan) sin cambios adicionales.

Para SLAM 3D si tu AS2 lleva el LiDAR de 64-128 líneas, puedes usar FAST-LIO2:
→ [SLAM Avanzado con FAST-LIO2](slam-avanzado.md)

## Preparación del AS2 para sesiones de inspección

```bash
# 1. Verificar conectividad WiFi (AS2 actúa como AP: 192.168.123.x)
ping 192.168.123.161       # IP típica del AS2

# 2. Exportar variables de entorno
export RMW_IMPLEMENTATION=rmw_cyclonedds_cpp

# 3. Lanzar el bridge
python3 unitree_ros2_bridge.py --network_interface wlan0

# 4. Verificar topics disponibles (en otra terminal)
ros2 topic list
# Debes ver: /cmd_vel  /odom  /scan  /battery_state
ros2 service list | grep sport
# Debes ver: /sport/stand_up  /sport/sit  /sport/hello  ...

# 5. Levantar el robot
ros2 service call /sport/recovery_stand std_srvs/srv/Trigger

# 6. Ejecutar rutina de inspección
ros2 run unitree_u9_inspection unitree_inspection.py
```

## Diferencias de seguridad respecto al Go2

!!! warning "El AS2 es más rápido - más margen de seguridad"
    El AS2 puede alcanzar 5 m/s, el doble del Go2. En laboratorio:
    
    - Mantén un radio de seguridad de **4 metros** cuando el robot esté en modo autónomo
    - Usa las velocidades de los archivos semilla (≤ 0.5 m/s) para las prácticas del curso
    - El botón de parada de emergencia siempre debe estar al alcance
    - Llama a `ros2 service call /sport/stand_down std_srvs/srv/Trigger` como parada suave

## Escenarios del curso con AS2

Todos los módulos U1-U12 funcionan en el AS2 sin cambios. Adicionalmente, el AS2
es la plataforma recomendada para explorar:

- **Inspección de infraestructura en exteriores** (GPS + 4G)
- **Detección de anomalías con IA embebida** (8-core CPU)
- **Cobertura rápida de áreas grandes** (5 m/s)
- **Laboratorios sin infraestructura Ethernet** (WiFi 6)

---

Ver también:
- [B2: Robot Industrial](b2-industrial.md) - para entornos que requieren IP67 y mayor peso
- [SLAM Avanzado con FAST-LIO2](slam-avanzado.md) - 3D mapping con LiDAR de alta densidad
