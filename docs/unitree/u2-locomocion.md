---
title: "U2: Locomoción Holonómica"
description: "Controla el movimiento del Go2/B2 con /cmd_vel TwistStamped, usando los tres grados de libertad holonómicos."
---

# U2: Locomoción Holonómica

## Revisión: `/cmd_vel` y `TwistStamped`

En la [Parte 2](../course/part2.md) del curso aprendiste a controlar el TurtleBot3
publicando `geometry_msgs/TwistStamped` en `/cmd_vel`:

```python
msg = TwistStamped()
msg.twist.linear.x  = 0.2    # avanzar
msg.twist.angular.z = 0.5    # girar
```

El Go2/B2 usa **exactamente el mismo topic y tipo de mensaje**. La única diferencia es
que ahora también puedes usar `linear.y` para desplazamiento lateral:

```python
msg = TwistStamped()
msg.twist.linear.x  =  0.2   # adelante/atrás  (m/s)
msg.twist.linear.y  =  0.1   # izquierda/derecha  (m/s)  ← NUEVO
msg.twist.angular.z = -0.3   # rotación (rad/s)
```

En el TurtleBot3 `linear.y` era ignorado (no puede desplazarse lateralmente).
En el Go2/B2 las tres componentes se ejecutan **simultáneamente**.

## Cinemática holonómica vs. diferencial

Un robot de tracción **diferencial** (como el Waffle) para ir a la derecha tiene que:
1. Girar 90° a la derecha
2. Avanzar la distancia deseada
3. Girar 90° a la izquierda para recuperar la orientación

Un robot **holonómico** (como el Go2) simplemente publica `vy > 0`:
```python
msg.twist.linear.y = 0.15   # deslizarse a la izquierda sin girar
```

Esto lo implementa el SDK de Unitree como `SportClient::Move(vx=0, vy=0.15, vyaw=0)`.

## Configuración del sandbox

Abre el sandbox con la parte **"Unitree U2: Locomoción Holonómica"**.

- Mundo: `unitree_empty` (arena abierta, robot verde = holonómico)
- Archivo semilla: `unitree_move.py` en `~/ros2_ws/src/unitree_u2_locomotion/scripts/`
- Topics disponibles:
  ```
  /cmd_vel   geometry_msgs/TwistStamped   (controla el robot)
  /odom      nav_msgs/Odometry            (posición actual)
  /scan      sensor_msgs/LaserScan        (LiDAR 360°)
  ```

## Archivo semilla: `unitree_move.py`

El archivo ya está en tu workspace. Ábrelo desde el explorador de código y léelo antes
de ejecutar. Contiene una secuencia de tres movimientos:

1. **Avance** — `vx = 0.3 m/s` durante 2 s
2. **Lateral** — `vy = 0.2 m/s` durante 2 s (¡nuevo!)
3. **Rotación** — `vyaw = 0.5 rad/s` durante 2 s

### Compilar y ejecutar

```bash
# Terminal 1: compilar
cd ~/ros2_ws
colcon build --packages-select unitree_u2_locomotion --symlink-install
source install/setup.bash

# Terminal 2: ver la posición en tiempo real
ros2 topic echo /odom --field pose.pose.position

# Terminal 1: ejecutar
ros2 run unitree_u2_locomotion unitree_move.py
```

Observa la ventana de `sim_lite` (la pantalla negra con el robot verde) — deberías ver:
- El robot moverse hacia adelante dejando una traza verde
- Luego desplazarse lateralmente (sin girar el cuerpo)
- Luego girar en su propio eje

## Ejercicios

!!! note "Ejercicio 1 — Cuadrado diferencial"
    Adapta `unitree_move.py` para que el robot trace un cuadrado de 1 m usando solo
    `vx` y `vyaw` (sin `vy`). Esto es equivalente a `move_square.py` de la Parte 2.
    
    **Pista**: necesitas calcular cuánto tiempo mantener `vx` constante para avanzar
    exactamente 1 m, y cuánto mantener `vyaw` para girar exactamente 90°.

!!! note "Ejercicio 2 — Cuadrado holonómico"
    Traza el mismo cuadrado pero **sin girar el robot** (el frente siempre apunta en
    la misma dirección). Usa solo `vx` y `vy` para los cuatro lados.
    
    Este movimiento **no es posible en el TurtleBot3** — solo en robots holonómicos.

!!! note "Ejercicio 3 — Círculo"
    Haz que el robot se mueva en un círculo de radio 1 m aplicando simultáneamente
    `vx` y `vyaw` constantes. Usa la relación `r = vx / vyaw` para calcular los
    valores correctos.

!!! note "Ejercicio 4 — Verificación con odometría"
    Agrega un subscriber a `/odom` en tu nodo y haz que el nodo se detenga
    automáticamente cuando haya recorrido exactamente 1 m desde el origen.
    (Pista: usa `math.hypot(x, y) >= 1.0`.)

## Notas sobre el hardware real

Cuando ejecutes `unitree_move.py` en el Go2/B2 real:

1. Asegúrate de que `unitree_ros2_bridge.py` esté corriendo en el mismo host.
2. El puente traduce la publicación en `/cmd_vel` a `SportClient::Move(vx, vy, vyaw)`.
3. Los límites de velocidad del robot real son más bajos que en la simulación:
   - `|vx| ≤ 1.5 m/s`  (recomendado ≤ 0.5 para inicio)
   - `|vy| ≤ 0.5 m/s`
   - `|vyaw| ≤ 1.5 rad/s`
4. **Siempre ten a mano un control remoto** para poder detener el robot manualmente.

!!! warning "Seguridad"
    En hardware real, empieza con velocidades bajas (0.1–0.2 m/s). Un robot cuadrúpedo
    que choca contra un obstáculo puede volcar o dañar sus actuadores. Confirma que la
    zona de prueba tenga al menos 3 × 3 m despejados.

---

Continúa con [U3 — Estado y Odometría](u3-odometria.md).
