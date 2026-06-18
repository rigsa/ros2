---
title: "U6: Autonomía Integrada"
description: "Combina odometría, LiDAR y locomoción en un único nodo que navega hacia un objetivo evitando obstáculos."
---

# U6: Autonomía Integrada

## Objetivo del módulo

Este módulo integra todos los conceptos aprendidos en U2-U5 en un único sistema
autónomo. Al completarlo habrás construido un robot que puede:

1. **Inicializarse** (levantarse con `stand_up`)
2. **Navegar hacia un objetivo** usando odometría para conocer su posición
3. **Evitar obstáculos** de forma reactiva con el LiDAR
4. **Ejecutar un comportamiento** al llegar (saludo)

El mismo código funcionará en el simulador y en hardware real.

## Arquitectura del nodo `unitree_autonomy.py`

```
        Sensores                    Actuadores
    ┌─────────┐                  ┌──────────────┐
    │  /odom  │──→ x, y, yaw ──→│              │
    └─────────┘                  │   Máquina    │──→ /cmd_vel
    ┌─────────┐                  │   de estados │
    │  /scan  │──→ dist_frente ─→│              │──→ /sport/*
    └─────────┘                  └──────────────┘
                                       ↓
                              iniciando → navegando
                              evasion → llegado
```

El nodo usa una **máquina de estados finita (FSM)** de 4 estados:

| Estado | Qué hace | Transición |
|---|---|---|
| `iniciando` | Llama a `/sport/stand_up`, espera 1 s | → `navegando` |
| `navegando` | Controlador P de dirección + avance | → `evasion` si obstáculo; → `llegado` si llegó |
| `evasion` | Gira hasta que el frente esté libre | → `navegando` |
| `llegado` | Detiene el robot, llama a `/sport/hello` | - (terminal) |

## Configuración del sandbox

Abre el sandbox con **"Unitree U6: Autonomía Integrada"**.

- Mundo: `unitree_obstacles` - 8 obstáculos en la arena
- Archivo semilla: `unitree_autonomy.py`
- El objetivo por defecto es `(2.0, 1.5)` metros

```bash
cd ~/ros2_ws
colcon build --packages-select unitree_u6_autonomy --symlink-install
source install/setup.bash
ros2 run unitree_u6_autonomy unitree_autonomy.py
```

Observa en la ventana de `sim_lite`:
- La traza verde del recorrido del robot
- Los rayos rojos del LiDAR detectando obstáculos durante la evasión
- El banner amarillo `👋 Hello` cuando llega al objetivo

## El controlador de dirección proporcional

El corazón de la navegación es un controlador proporcional simple:

```python
# Ángulo hacia el objetivo (en el marco del mundo)
angulo_objetivo = math.atan2(dy, dx)

# Error de orientación (diferencia entre adónde miro y adónde debo ir)
error_yaw = normalizar_angulo(angulo_objetivo - self.yaw)

# Velocidad angular proporcional al error (K = ganancia)
vyaw = K * error_yaw

# Velocidad lineal: máxima cuando estoy bien alineado, baja cuando estoy desviado
factor_alineacion = 1.0 - min(1.0, abs(error_yaw) / math.pi)
vx = VEL_MAX * factor_alineacion
```

Este es el mismo patrón que el **controlador proporcional** de la Parte 2, aplicado
a la orientación en lugar de a la distancia.

## Ejercicios

!!! note "Ejercicio 1 - Cambiar el objetivo"
    Cambia `X_OBJETIVO` y `Y_OBJETIVO` en `unitree_autonomy.py` para navegar a
    diferentes puntos del mapa. Prueba con `(3.0, 0.0)`, `(-2.0, 2.0)` y `(0.0, -3.0)`.
    
    Observa cómo el robot rodea los obstáculos que encuentre en el camino.

!!! note "Ejercicio 2 - Múltiples waypoints"
    Modifica el nodo para navegar por una **lista de objetivos** en secuencia.
    Cuando llegue al primero, el siguiente se convierte en el objetivo activo.
    
    ```python
    WAYPOINTS = [(2.0, 1.5), (-1.5, 2.0), (0.0, 0.0)]   # regresa al origen
    ```

!!! note "Ejercicio 3 - Evasión con desplazamiento lateral"
    El comportamiento de evasión actual solo gira. Mejóralo: si el obstáculo
    está al frente pero hay espacio a la derecha, usa `vy < 0` para deslizarse
    hacia la derecha en lugar de girar. Aprovecha los 3 DOF del Go2/B2.
    
    Para decidir a cuál lado moverse, compara la distancia medida a ±45° del frente.

!!! note "Ejercicio 4 - Comportamiento al llegar"
    En lugar de solo saludar, haz que el robot:
    1. Se detenga
    2. Gire 360° lentamente (escaneo del entorno)
    3. Guarde el ángulo con el mayor espacio libre
    4. Apunte en esa dirección
    5. Luego salude
    
    Este es el núcleo de un comportamiento de "exploración".

!!! note "Ejercicio 5 - Prueba en hardware real"
    Si tienes acceso a un Go2 EDU o B2:
    1. Asegúrate de que `unitree_ros2_bridge.py` esté corriendo
    2. Verifica que `/odom`, `/scan` y `/sport/*` estén publicando/disponibles
    3. Ejecuta `unitree_autonomy.py` **sin cambios** - debería funcionar igual que en sim
    4. Empieza con velocidades bajas (`VEL_AVANCE_MAX = 0.15`) en tu primera prueba

## Limitaciones de la odometría en hardware real

El dead-reckoning (odometría) acumula error con el tiempo. En el simulador es
perfecto porque se calcula exactamente de los comandos. En hardware real:

- El error crece ~1-5% de la distancia recorrida por sesión
- En superficies irregulares (al aire libre) el error es mayor
- Para navegación a largo plazo, combina odometría con SLAM (ver Parte 3)

Para distancias cortas (< 10 m) como los ejercicios de este módulo, la odometría
del SDK del Go2 es suficientemente precisa.

## ¿Qué sigue?

Con los módulos U1-U6 has construido un sistema de navegación autónomo completo para
robots cuadrúpedos usando ROS 2 estándar. Los pasos siguientes para trabajo avanzado:

- **SLAM + Nav2**: adaptar el stack de autonomía de `unitree_rigsa` (SLAM usando el
  LiDAR 3D completo + planificador de rutas Nav2)
- **RealSense + OpenCV**: portar los algoritmos de la Parte 6 del curso a la cámara
  de profundidad del Go2/B2 (ver [guía de porting](../course/extras/porting-to-unitree.md))
- **Behaviors personalizados**: implementar acciones ROS 2 que combinen movimiento y
  comportamientos sport para secuencias más complejas
