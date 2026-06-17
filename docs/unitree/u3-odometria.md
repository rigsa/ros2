---
title: "U3: Estado y Odometría"
description: "Lee la posición y orientación del Go2/B2 desde /odom y construye un controlador de posición simple."
---

# U3: Estado y Odometría

## La odometría en el curso base

En la [Parte 2](../course/part2.md) ya trabajaste con `nav_msgs/Odometry` para
leer la posición del TurtleBot3. El topic `/odom`, el tipo de mensaje y la
conversión quaternion → yaw son **idénticos** en el Go2/B2. Todo lo que
aprendiste ahí aplica directamente aquí.

La diferencia es el **origen de los datos**:

| Fuente | TurtleBot3 (Gazebo) | Unitree Go2/B2 |
|---|---|---|
| Posición | Plugin diff-drive de Gazebo | `SportModeState` del SDK (propioceptivo) |
| Orientación | Simulada | IMU + estimación del SDK |
| Velocidad | Simulada | `SportModeState.velocity[]` |

En el sandbox con `sim_lite` la odometría se calcula por dead-reckoning (igual
que en las Partes 1-2 del curso). Cuando el código corre en hardware real con
`unitree_ros2_bridge.py`, la odometría proviene del SDK del robot, que usa los
encoders de las articulaciones y la IMU.

## El mensaje `Odometry` — recordatorio

```python
from nav_msgs.msg import Odometry

def callback(msg: Odometry):
    # Posición (metros)
    x = msg.pose.pose.position.x
    y = msg.pose.pose.position.y

    # Orientación (quaternion → necesitas convertir a yaw)
    qx = msg.pose.pose.orientation.x
    qy = msg.pose.pose.orientation.y
    qz = msg.pose.pose.orientation.z
    qw = msg.pose.pose.orientation.w

    # Velocidades
    vx   = msg.twist.twist.linear.x
    vy   = msg.twist.twist.linear.y   # ← lateral (no nulo en Go2/B2)
    vyaw = msg.twist.twist.angular.z
```

El campo `twist.twist.linear.y` siempre fue cero en el TurtleBot3. En el Go2/B2
puede tener un valor distinto de cero cuando el robot se desplaza lateralmente.

## Configuración del sandbox

Abre el sandbox con **"Unitree U3: Estado y Odometría"**.

- Mundo: `unitree_empty`
- Archivo semilla: `unitree_odom.py`
- Puedes combinar este módulo con U2: en una terminal corre `unitree_odom.py`
  y en otra `unitree_move.py` para ver la posición cambiar en tiempo real.

## Archivo semilla: `unitree_odom.py`

El nodo se suscribe a `/odom` y en cada mensaje imprime:
- Posición `(x, y)` en metros
- Orientación `yaw` en grados
- Distancia al origen `|(x, y)|`
- Velocidades actuales `(vx, vy, vyaw)`

```bash
cd ~/ros2_ws
colcon build --packages-select unitree_u3_odometry --symlink-install
source install/setup.bash
ros2 run unitree_u3_odometry unitree_odom.py
```

En otra terminal, mueve el robot:
```bash
ros2 run unitree_u2_locomotion unitree_move.py
```

## Ejercicios

!!! note "Ejercicio 1 — Distancia recorrida"
    Modifica `unitree_odom.py` para que **imprima solo cada 0.5 s** (no a cada
    mensaje) y además acumule la distancia total recorrida (no la distancia al
    origen, sino la longitud del camino).
    
    **Pista**: guarda la posición anterior `(x_prev, y_prev)` y en cada callback
    calcula `dist += math.hypot(x - x_prev, y - y_prev)`.

!!! note "Ejercicio 2 — Posición en formato tabla"
    Usa `rclpy.logging.get_logger().info()` para imprimir la posición en una
    sola línea que se actualice en el terminal. O mejor aún, imprime en formato
    de tabla con `\r` para sobreescribir la línea anterior.

!!! note "Ejercicio 3 — Controlador de posición 1D"
    Escribe un nodo que mueva el robot exactamente `D` metros hacia adelante
    (configurable con una variable al principio del archivo) leyendo la odometría,
    **en lugar de usar `time.sleep()`**.
    
    Algoritmo sugerido:
    ```python
    D = 1.5  # metros objetivo
    
    # En el callback de odometría:
    if not llegado:
        distancia_actual = math.hypot(x, y)
        if distancia_actual >= D:
            publicar_velocidad(0, 0, 0)
            llegado = True
        else:
            publicar_velocidad(0.3, 0, 0)
    ```

!!! note "Ejercicio 4 — Controlador de orientación (proporcional)"
    Escribe un nodo que gire el robot hasta apuntar exactamente a `θ_objetivo` grados.
    Usa un controlador proporcional: `vyaw = K * error_yaw`, donde `K = 1.0` es
    la ganancia y `error_yaw = normalizar(θ_objetivo - yaw_actual)`.
    
    Recuerda normalizar el error al rango `[-π, π]`.

## El quaternion a Euler — ya lo conoces

La función `quaternion_a_euler()` en `unitree_odom.py` es exactamente la misma
que se usa en `move_square.py` de la Parte 2 del curso. No hay nada nuevo aquí.

Para un robot en un plano 2D, lo único que importa es el `yaw` (rotación sobre Z):

```python
def quaternion_a_euler(qx, qy, qz, qw):
    siny = 2.0 * (qw * qz + qx * qy)
    cosy = 1.0 - 2.0 * (qy * qy + qz * qz)
    yaw = math.atan2(siny, cosy)
    return yaw   # en radianes
```

---

Continúa con [U4 — Comportamientos Sport](u4-comportamientos.md).
