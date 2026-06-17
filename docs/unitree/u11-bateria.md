---
title: "U11: Gestión de Batería y Supervisión"
description: "Monitorea el estado de batería y toma decisiones autónomas: alertas, regreso al dock, reanudación de misión."
---

# U11: Gestión de Batería y Supervisión

## ¿Por qué es crítica la gestión de batería?

Un robot industrial que se queda sin batería en medio de una misión es un
problema operacional: puede quedar varado en una zona de acceso difícil,
interrumpir un proceso, o en casos extremos dañar el equipo.

Un sistema robusto de gestión de batería debe:
1. **Monitorear** el nivel continuamente
2. **Alertar** cuando se acerca a umbrales críticos
3. **Decidir autónomamente** cuándo interrumpir la misión y cargar
4. **Reanudar** automáticamente cuando tenga suficiente energía
5. **Registrar** el historial de batería para análisis

## El topic `/battery_state`

`sim_lite` publica `sensor_msgs/BatteryState` a 1 Hz:

```python
from sensor_msgs.msg import BatteryState

def _battery_cb(self, msg: BatteryState):
    porcentaje = msg.percentage * 100.0    # 0.0-1.0 → 0-100%
    voltaje    = msg.voltage               # voltios
    corriente  = msg.current               # amperios (negativo = descargando)
    cargando   = (msg.power_supply_status ==
                  BatteryState.POWER_SUPPLY_STATUS_CHARGING)
```

En `sim_lite`:
- La batería drena **0.5%/s** en movimiento y **0.05%/s** en reposo
- Carga **2%/s** cuando está acoplada al dock
- Inicia al **80%** por defecto (configurable con `SIM_BATTERY_START=XX`)

## Configuración del sandbox

Para una sesión con batería baja (útil para probar el retorno al dock):

```bash
# La variable de entorno se pasa al contenedor desde el formulario del sandbox,
# o puedes exportarla antes de iniciar el simulador
export SIM_BATTERY_START=25
```

```bash
cd ~/ros2_ws
colcon build --packages-select unitree_u11_battery --symlink-install
source install/setup.bash
ros2 run unitree_u11_battery unitree_battery.py
```

Observa el indicador de batería en la ventana de `sim_lite` (barra en la
esquina inferior izquierda). Cuando llega al 20% el robot iniciará el retorno
al dock automáticamente.

## Umbrales de batería

El nodo `unitree_battery.py` implementa tres umbrales:

| Umbral | Porcentaje | Acción |
|---|---|---|
| Alerta | 35% | Log de advertencia, misión continúa |
| Crítico | 20% | Interrumpe misión, regresa al dock |
| Reanudar | 80% | Desacopla del dock, reanuda |

Estos son configurables como parámetros ROS 2:

```bash
ros2 run unitree_u11_battery unitree_battery.py \
  --ros-args -p umbral_alerta:=40 -p umbral_critico:=25 -p umbral_reanudar:=85
```

## La máquina de estados de batería

```
NORMAL ──(< 35%)──→ ALERTA ──(< 20%)──→ CRITICO
                                            │
                                      navega al dock
                                            │
                                         CARGANDO ──(> 80%)──→ LISTO
                                                                  │
                                                          reanuda misión
```

## Integración con el nodo de misión

El gestor de batería y el nodo de misión pueden correr en paralelo. El gestor
publica en `/battery/status` y la misión puede suscribirse para pausar:

```bash
# Terminal 1: gestor de batería
ros2 run unitree_u11_battery unitree_battery.py

# Terminal 2: rutina de inspección
ros2 run unitree_u9_inspection unitree_inspection.py

# Terminal 3: monitorear el estado
ros2 topic echo /battery/status
```

Para una integración más estrecha (el nodo de misión pausa cuando el gestor
indica batería crítica), usa un topic de comandos:

```python
# En el nodo de misión:
self.create_subscription(String, "/battery/status", self._battery_status_cb, 10)

def _battery_status_cb(self, msg):
    if "CRITICO" in msg.data:
        self._pausar_mision()
```

## Dock de carga: acoplamiento y desacoplamiento

El servicio `/sport/dock` verifica que el robot esté a < 1.0 m del dock antes
de acoplar. En `sim_lite` el dock está en `(-3.5, 0.0)` (pillar cian con ⚡).

```bash
# Verificar que el dock está disponible
ros2 service list | grep dock

# Acoplar manualmente (para pruebas)
ros2 service call /sport/dock std_srvs/srv/Trigger {}

# Verificar estado de carga
ros2 topic echo /battery_state --field percentage
```

## En hardware real (unitree_ros2_bridge.py)

El bridge lee el estado de batería del SDK de Unitree y lo republica en
`/battery_state` con el mismo formato, así este módulo funciona sin cambios.

El dock físico del Go2 EDU/B2 usa comunicación por contacto eléctrico —
el robot debe estar correctamente alineado para cargar. Para un acoplamiento
preciso combina este módulo con U10 (ArUco en el dock):

```
Navega cerca del dock → detecta ArUco #0 → acercamiento fino → /sport/dock
```

## Ejercicios

!!! note "Ejercicio 1 — Monitor en tiempo real"
    Suscríbete a `/battery_state` e imprime el estado cada 5 s en formato
    de tabla:
    ```
    [14:23:10] batería: 67.3%  voltaje: 24.2V  estado: DESCARGANDO
    ```

!!! note "Ejercicio 2 — Historial de batería"
    Registra el porcentaje de batería junto con la posición `(x, y)` cada
    10 s. Al finalizar, imprime cuál fue la posición del robot cuando la
    batería llegó a su mínimo.

!!! note "Ejercicio 3 — Regreso preventivo"
    En lugar de esperar a que la batería llegue al 20% crítico, implementa
    un retorno preventivo: calcula la distancia hasta el dock y estima si
    hay suficiente batería para llegar. Formula: si `batería_actual - batería_para_llegar < 15%`, regresa ahora.

!!! note "Ejercicio 4 — Integración completa"
    Combina `unitree_inspection.py` y `unitree_battery.py` en un launch file
    de Python que inicie ambos nodos simultáneamente:
    ```python
    # launch/inspection_with_battery.launch.py
    from launch import LaunchDescription
    from launch_ros.actions import Node

    def generate_launch_description():
        return LaunchDescription([
            Node(package="unitree_u9_inspection",
                 executable="unitree_inspection.py"),
            Node(package="unitree_u11_battery",
                 executable="unitree_battery.py"),
        ])
    ```

---

Continúa con [U12 — Logging, Diagnósticos y Reportes](u12-logging.md).
