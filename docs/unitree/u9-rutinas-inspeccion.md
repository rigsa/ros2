---
title: "U9: Rutinas de Inspección Industrial"
description: "Construye una rutina de inspección completa con FSM, parámetros ROS 2, confirmación ArUco y manejo de fallos."
---

# U9: Rutinas de Inspección Industrial

## De la navegación simple a la misión de inspección real

En U8 el robot navegaba a POIs y ejecutaba acciones básicas. Una rutina de
inspección industrial completa agrega:

- **Confirmación visual**: verificar que estás en la estación correcta (ArUco)
- **Manejo de fallos**: reintentar si algo sale mal
- **Parámetros configurables**: velocidad, radio, ciclos - sin recompilar
- **Logging estructurado**: saber qué pasó, cuándo y dónde
- **Ciclos repetidos**: la inspección no es un evento único

## ROS 2 Parameters - configurar sin recompilar

En lugar de variables hardcodeadas al principio del archivo, el nodo
`unitree_inspection.py` usa parámetros ROS 2:

```python
self.declare_parameter("ciclos",         1)
self.declare_parameter("vel_max",        0.35)
self.declare_parameter("radio_llegada",  0.40)
self.declare_parameter("max_reintentos", 2)
```

Puedes cambiarlos en tiempo de ejecución sin modificar el código:

```bash
# Pasar parámetros al lanzar el nodo
ros2 run unitree_u9_inspection unitree_inspection.py \
  --ros-args -p ciclos:=3 -p vel_max:=0.4 -p radio_llegada:=0.3

# O crear un archivo de parámetros
cat > inspection_params.yaml << 'EOF'
/rutina_inspeccion:
  ros__parameters:
    ciclos: 5
    vel_max: 0.30
    radio_llegada: 0.35
    max_reintentos: 3
    timeout_nav: 90.0
EOF
ros2 run unitree_u9_inspection unitree_inspection.py \
  --ros-args --params-file inspection_params.yaml
```

## La máquina de estados (FSM)

El nodo usa una FSM explícita con estados claramente definidos:

```
INICIANDO → NAVEGANDO ────────────────────────────────────→ COMPLETADO
                ↓ llegó al POI                                   ↑
           CONFIRMANDO   (busca ArUco 3 s)                       │
                ↓ ArUco encontrado / fallo → reintento           │
           INSPECCIONANDO (ejecuta hello/charge)                 │
                ↓ completado                                     │
           próximo POI ──────────────────────────────────────────┘
                                    ↓ batería crítica
                              RETORNANDO → CARGANDO → LISTO
```

Cada estado tiene transiciones bien definidas y logging en cada cambio.

## Configuración del sandbox

```bash
cd ~/ros2_ws
colcon build --packages-select unitree_u9_inspection --symlink-install
source install/setup.bash
ros2 run unitree_u9_inspection unitree_inspection.py
```

Para ver los logs en tiempo real en otra terminal:
```bash
ros2 topic echo /inspection/log
```

## Confirmación ArUco

Después de llegar a un POI, el nodo espera hasta 3 s a que el detector de cámara
confirme que el ArUco correcto está visible:

```python
# Esperar detección del ArUco esperado
t0 = time.monotonic()
while time.monotonic() - t0 < 3.0:
    rclpy.spin_once(self, timeout_sec=0.1)
    if self._aruco_detectado == poi.aruco_id:
        detectado = True
        break
```

Si no se detecta el ArUco en 3 s, el resultado se registra como `✗ NO DETECTADO`
pero la misión continúa (comportamiento configurable).

## Reintento automático

Si el robot no llega al POI (timeout o fallo de navegación), reintenta
`max_reintentos` veces antes de marcar el POI como fallido y continuar:

```python
for intento in range(self._reintentos + 1):
    llegado = self._navegar_a(poi)
    if llegado:
        # éxito
        break
    # fallo: registrar y reintentar
```

## Resumen de inspección

Al finalizar todos los ciclos, el nodo imprime un resumen:

```
=== RESUMEN DE INSPECCIÓN ===
[14:23:15] Station A     ✓ DETECTADO  ArUco=1  pos=(2.48, 1.52)
[14:23:48] Station B     ✓ DETECTADO  ArUco=2  pos=(2.51,-1.49)
[14:24:21] Station C     ✗ NO DETECTADO  ArUco=3  pos=(-1.47, 2.53)
[14:25:10] Dock          ✓ DETECTADO  ArUco=0  pos=(-3.48, 0.02)
Total: 4 inspecciones  ArUco detectados: 2/3
```

## Ejercicios

!!! note "Ejercicio 1 - Parámetros en archivo"
    Crea un archivo `patrol_params.yaml` con 3 ciclos y velocidad reducida.
    Corre la rutina con ese archivo de parámetros. Verifica que los ciclos
    se ejecutan en el log.

!!! note "Ejercicio 2 - Acción configurable por POI"
    Agrega un campo `wait_s` a la estructura `POI` y una acción `"wait"`
    que simplemente espera `wait_s` segundos en el POI (simula tomar una
    lectura de sensor). Añade una estación con `action: "wait", wait_s: 10`.

!!! note "Ejercicio 3 - Alerta de ArUco no detectado"
    Si 2 o más estaciones en el mismo ciclo fallan la detección ArUco,
    publica un mensaje en `/inspection/alert` (std_msgs/String) con
    `"ALERTA: X estaciones no confirmadas"`. En producción esto podría
    enviar un email o notificación.

!!! note "Ejercicio 4 - Dashboard en terminal"
    Usa la librería `curses` de Python para mostrar un panel en tiempo real:
    ```
    ┌─── INSPECCIÓN EN CURSO ──────────────────┐
    │ Ciclo: 2/3    POI: Station B    Estado: NAVEGANDO
    │ Batería: 72%  Pos: (1.23, -0.45)  Dist: 1.87 m
    │ Completados: A✓ B...             
    └──────────────────────────────────────────┘
    ```

---

Continúa con [U10 - Tags ArUco para Identificación Visual](u10-aruco.md).
