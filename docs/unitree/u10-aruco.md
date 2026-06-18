---
title: "U10: Tags ArUco para Identificación Visual"
description: "Detecta marcadores ArUco con OpenCV, estima distancia y ángulo, y los usa como puntos de verificación de inspección."
---

# U10: Tags ArUco para Identificación Visual

## ¿Qué es un marcador ArUco?

Un marcador ArUco es un código binario 2D impreso en papel o superficie. OpenCV
puede detectarlo en tiempo real y calcular:

- **Su ID** (0 a N-1 según el diccionario)
- **Su posición** en la imagen (esquinas en píxeles)
- **Su pose** respecto a la cámara (traslación + rotación) - si conoces el tamaño físico

En aplicaciones industriales los ArUco sirven para:
- Identificar equipos, zonas o puntos de inspección unívocamente
- Guiar el acercamiento fino del robot (más preciso que solo odometría)
- Corregir la deriva de odometría anclandote a puntos conocidos del mapa
- Marcar el dock de carga para un acoplamiento preciso
- Verificar que el robot está exactamente donde debe estar

## sim_lite: ArUco reales en la cámara simulada

En el mundo `unitree_inspection`, `sim_lite` renderiza **marcadores ArUco reales**
(del diccionario `DICT_4X4_50`) sobre los pilares de inspección usando OpenCV.
Cuando te acercas a una estación, el marcador aparece en `/camera/image_raw` con
suficiente resolución para que `cv2.aruco.ArucoDetector` lo detecte.

Pruébalo antes de ejecutar el nodo:
```bash
ros2 run rqt_image_view rqt_image_view /camera/image_raw
# Acerca el robot a Station A para ver el marcador ArUco #1
```

## Diccionarios de ArUco

OpenCV incluye varios diccionarios predefinidos. Este módulo usa `DICT_4X4_50`:

| Diccionario | Marcadores | Tamaño | Robustez |
|---|---|---|---|
| `DICT_4X4_50` | 50 | 4×4 bits | Baja (para distancias cortas) |
| `DICT_5X5_100` | 100 | 5×5 bits | Media |
| `DICT_6X6_250` | 250 | 6×6 bits | Alta (recomendado para producción) |

Para producción usa `DICT_6X6_250`: más bits = menor tasa de falsos positivos.

## La API moderna de OpenCV ArUco (v4.7+)

```python
import cv2

# 1. Crear diccionario y detector
aruco_dict = cv2.aruco.getPredefinedDictionary(cv2.aruco.DICT_4X4_50)
params      = cv2.aruco.DetectorParameters()
detector    = cv2.aruco.ArucoDetector(aruco_dict, params)

# 2. Detectar en una imagen BGR
corners, ids, rejected = detector.detectMarkers(bgr_image)

# 3. Resultado:
#   corners: lista de arrays (1, 4, 2) - 4 esquinas por marcador en píxeles
#   ids:     array (N, 1) - ID de cada marcador detectado
#   rejected: candidatos que no pasaron la verificación
```

## Estimación de pose (distancia y ángulo)

Con las esquinas detectadas y los parámetros intrínsecos de la cámara:

```python
import numpy as np
from cv2 import solvePnP, SOLVEPNP_ITERATIVE

MARKER_SIZE = 0.25   # metros - tamaño real del marcador impreso

# Puntos 3D del marcador en su sistema de coordenadas local
half = MARKER_SIZE / 2
obj_pts = np.array([[-half,half,0],[half,half,0],[half,-half,0],[-half,-half,0]])
img_pts = corners[0][0].astype(np.float64)

ok, rvec, tvec = solvePnP(obj_pts, img_pts, K, D)
distancia = np.linalg.norm(tvec)           # metros al marcador
angulo    = math.atan2(-tvec[0], tvec[2])  # radianes (+ = izquierda)
```

## Configuración del sandbox

```bash
cd ~/ros2_ws
colcon build --packages-select unitree_u10_aruco --symlink-install
source install/setup.bash
ros2 run unitree_u10_aruco unitree_aruco.py
```

Publica en:
- `/aruco/detections` - JSON con ID, distancia y ángulo de cada marcador detectado
- `/aruco/image` - imagen con marcadores dibujados (visible en `rqt_image_view`)

Para ver las detecciones:
```bash
ros2 topic echo /aruco/detections
```

## Guía de acercamiento fino con ArUco

Una vez que detectas el marcador, puedes usar su ángulo para alinear el robot:

```python
def _acercar_a_aruco(self, aruco_id_objetivo: int, distancia_objetivo=0.6):
    """Mueve el robot hasta estar a distancia_objetivo m del marcador."""
    while rclpy.ok():
        det = self._ultima_deteccion(aruco_id_objetivo)
        if det is None:
            # Marcador no visible: girar lentamente para buscarlo
            self._cmd(0.0, 0.0, 0.2)
            continue

        dist_m   = det["distancia_m"]
        ang_deg  = det["angulo_deg"]

        if dist_m <= distancia_objetivo and abs(ang_deg) < 5.0:
            self._detener()
            return True   # correctamente posicionado

        # Corrección angular (proporcional)
        vyaw = -math.radians(ang_deg) * 0.8
        # Avance proporcional a la distancia restante
        vx = min(0.25, max(0.05, (dist_m - distancia_objetivo) * 0.5))
        self._cmd(vx, 0.0, vyaw)
```

## Generación de marcadores para imprimir

```python
import cv2
aruco_dict = cv2.aruco.getPredefinedDictionary(cv2.aruco.DICT_4X4_50)

for marker_id in range(4):
    marker_img = cv2.aruco.generateImageMarker(aruco_dict, marker_id, 300)
    cv2.imwrite(f"aruco_{marker_id}.png", marker_img)
    print(f"Guardado aruco_{marker_id}.png")
```

Imprime el resultado en papel. Para el dock usa el ID 0; para las estaciones
de inspección usa IDs 1, 2, 3.

## Ejercicios

!!! note "Ejercicio 1 - Lectura básica"
    Corre `unitree_aruco.py` y acerca el robot a cada estación manualmente
    (con `ros2 run teleop_twist_keyboard teleop_twist_keyboard`). Observa
    cómo cambia la distancia y el ángulo en `/aruco/detections`.

!!! note "Ejercicio 2 - Detección a distancia"
    ¿A qué distancia máxima detecta el nodo los marcadores? Aleja el robot
    despacio y registra la distancia máxima de detección de cada marcador.

!!! note "Ejercicio 3 - Acercamiento fino"
    Implementa la función `_acercar_a_aruco()` descrita arriba e intégrala
    en `unitree_waypoint_nav.py`: después de llegar al radio de llegada,
    usa ArUco para posicionarte a exactamente 0.5 m del marcador.

!!! note "Ejercicio 4 - Corrección de odometría"
    Cuando el robot está frente a un marcador conocido (ID + posición
    conocida del mapa), puedes calcular la posición real del robot y
    corregir la odometría. Implementa esta corrección y compara las
    posiciones antes y después.

---

Continúa con [U11 - Gestión de Batería y Supervisión](u11-bateria.md).
