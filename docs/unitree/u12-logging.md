---
title: "U12: Logging, Diagnósticos y Reportes de Misión"
description: "Registra datos de misión en CSV, genera reportes JSON, usa niveles de logging correctamente y depura con rosbag2."
---

# U12: Logging, Diagnósticos y Reportes de Misión

## Por qué el logging es una habilidad de producción

Un sistema robótico sin logging adecuado es intransigente: cuando algo falla en
producción (y fallará), no tienes datos para diagnosticar. Un buen sistema de
logging te permite:

- **Depurar** reproduciendo exactamente qué pasó con los datos de la misión
- **Auditar** - demostrar que el robot realizó las inspecciones correctamente
- **Optimizar** - identificar qué partes de la ruta consumen más batería
- **Reportar** - generar documentación automática de las misiones

## Dos sistemas de logging en ROS 2

### 1. `rclpy.logging` - para logs del nodo

Escribe al terminal y al sistema de logging de ROS 2:

```python
self.get_logger().debug("Dato de depuración detallado")
self.get_logger().info("Estado normal del sistema")
self.get_logger().warn("Situación anómala pero recuperable")
self.get_logger().error("Error que afecta la misión")
self.get_logger().fatal("Error crítico - el nodo debe terminar")
```

**Cuándo usar cada nivel:**
- `DEBUG`: datos del sensor, velocidades publicadas - demasiado para producción
- `INFO`: inicio/fin de estados, llegada a POIs, cambios de misión
- `WARN`: batería baja, ArUco no detectado, timeout (recuperable)
- `ERROR`: fallo de navegación, servicio no disponible (no recuperable en el ciclo)
- `FATAL`: hardware inaccesible, fallo de seguridad

**Filtrar por nivel:**
```bash
# Solo INFO y superior (por defecto)
ros2 run mi_pkg mi_nodo

# Solo DEBUG y superior (modo diagnóstico)
ros2 run mi_pkg mi_nodo --ros-args --log-level debug
```

### 2. `logging` de Python - para archivos de log

Para escribir a archivo además del terminal:

```python
import logging

logger = logging.getLogger("mission")
logger.setLevel(logging.DEBUG)

# Handler de archivo
fh = logging.FileHandler("/home/student/ros2_ws/src/logs/mission.log")
fh.setFormatter(logging.Formatter("%(asctime)s [%(levelname)s] %(message)s"))
logger.addHandler(fh)

# Usar exactamente como rclpy:
logger.info("Esto va al archivo Y al terminal")
```

## Registrar datos de misión en CSV

El formato CSV es adecuado para datos de series temporales porque:
- Es legible por humanos y por cualquier herramienta (Excel, pandas, Python)
- Permite análisis offline sin ROS instalado
- Puede crecer indefinidamente sin problemas de memoria

```python
import csv, time
from pathlib import Path

csv_path = Path("/home/student/ros2_ws/src/logs/mission.csv")
with open(csv_path, "w", newline="") as f:
    writer = csv.DictWriter(f, fieldnames=[
        "timestamp_s", "x", "y", "yaw_deg", "battery_pct"
    ])
    writer.writeheader()

    # En cada ciclo de muestreo:
    writer.writerow({
        "timestamp_s": time.time(),
        "x":           self.x,
        "y":           self.y,
        "yaw_deg":     math.degrees(self.yaw),
        "battery_pct": self.battery_pct,
    })
    f.flush()   # ← importante: escribe al disco inmediatamente
```

## Generar reportes JSON

Al finalizar una misión, genera un resumen estructurado:

```python
import json
from datetime import datetime

reporte = {
    "meta": {
        "fecha":      datetime.now().isoformat(),
        "duracion_s": elapsed,
        "operador":   os.environ.get("STUDENT_USER", "unknown"),
    },
    "resumen": {
        "pois_visitados":  len(resultados),
        "aruco_detectados": sum(1 for r in resultados if r["detectado"]),
        "bateria_inicial":  batt_inicio,
        "bateria_final":    batt_final,
        "distancia_m":      distancia_total,
    },
    "estaciones": resultados,
}
with open("report.json", "w") as f:
    json.dump(reporte, f, indent=2, ensure_ascii=False)
```

## rosbag2 - grabar y reproducir misiones completas

`rosbag2` graba todos los topics en un archivo y te permite reproducirlos
después, como si el robot estuviera corriendo de nuevo:

```bash
# Grabar (durante una misión)
ros2 bag record -o mision_2025_06_01 /odom /scan /battery_state /camera/image_raw

# Listar el contenido
ros2 bag info mision_2025_06_01/

# Reproducir (para depuración o análisis)
ros2 bag play mision_2025_06_01/ --rate 2.0   # 2x velocidad
```

Usa el bag grabado para:
- Depurar el detector ArUco con imágenes reales de la misión
- Verificar que la odometría coincide con la trayectoria esperada
- Reproducir el escenario que causó un fallo

## Configuración del sandbox

```bash
cd ~/ros2_ws
colcon build --packages-select unitree_u12_logging --symlink-install
source install/setup.bash

# Terminal 1: iniciar el logger
ros2 run unitree_u12_logging unitree_logger.py

# Terminal 2: correr cualquier nodo de misión en paralelo
ros2 run unitree_u9_inspection unitree_inspection.py

# Terminal 3: seguir los logs en tiempo real
tail -f ~/ros2_ws/src/logs/mission_*.log
```

Al terminar (Ctrl+C en el logger), se generarán automáticamente:
- `~/ros2_ws/src/logs/mission_<timestamp>.csv`
- `~/ros2_ws/src/logs/report_<timestamp>.json`

## Analizar los datos con pandas (fuera de ROS)

```python
import pandas as pd
import matplotlib.pyplot as plt

df = pd.read_csv("mission_20250601_142315.csv")
df["timestamp"] = pd.to_datetime(df["timestamp_s"], unit="s")
df = df.set_index("timestamp")

# Trayectoria
plt.figure(figsize=(8, 8))
plt.plot(df["x"], df["y"], "b-", linewidth=0.5)
plt.scatter(df["x"].iloc[0], df["y"].iloc[0], color="green", s=100, label="inicio")
plt.scatter(df["x"].iloc[-1], df["y"].iloc[-1], color="red",   s=100, label="fin")
plt.xlabel("x (m)")
plt.ylabel("y (m)")
plt.title("Trayectoria de la misión")
plt.legend()
plt.savefig("trajectory.png")

# Batería en el tiempo
df["battery_pct"].plot(title="Batería durante la misión")
plt.ylabel("%")
plt.savefig("battery_history.png")
```

## Ejercicios

!!! note "Ejercicio 1 - Logging con niveles correctos"
    Revisa el código de `unitree_inspection.py` e identifica al menos
    3 lugares donde el nivel de log podría mejorarse (ej: cambiar INFO
    a DEBUG para datos de sensor frecuentes).

!!! note "Ejercicio 2 - CSV de trayectoria"
    Corre `unitree_logger.py` mientras `unitree_waypoint_nav.py` completa
    una misión. Abre el CSV generado y calcula manualmente la distancia
    total recorrida sumando las distancias entre puntos consecutivos.

!!! note "Ejercicio 3 - Grabar y reproducir con rosbag2"
    1. Graba una misión completa con `ros2 bag record -o mi_bag /odom /battery_state`
    2. Reproduce el bag: `ros2 bag play mi_bag/`
    3. Corre `unitree_logger.py` mientras se reproduce
    4. Compara el CSV generado con el del ejercicio 2

!!! note "Ejercicio 4 - Reporte HTML"
    Modifica `generar_reporte_final()` en `unitree_logger.py` para que
    además del JSON genere un archivo `report.html` con una tabla legible
    y el historial de batería en texto. Utiliza f-strings de Python
    para generar el HTML (no necesitas ninguna librería extra).
