---
title: "B7: Detección de Objetos con YOLO"
description: "Usa YOLOv8 sobre el feed de cámara del K1 para detectar pelota y personas."
---

# B7: Detección de Objetos con YOLO

## Instalación

YOLOv8 ya está instalado en el sandbox Booster:
```bash
python3 -c "from ultralytics import YOLO; print('YOLO OK')"
```

## Detector básico con YOLOv8

```python
#!/usr/bin/env python3
import rclpy, cv2, numpy as np
from rclpy.node import Node
from sensor_msgs.msg import Image
from ultralytics import YOLO

class YoloDetector(Node):
    def __init__(self):
        super().__init__('yolo_detector')
        self.model = YOLO('yolov8n.pt')   # nano — más rápido
        self.create_subscription(Image, '/camera/image_raw', self.callback, 10)

    def callback(self, msg):
        bgr = np.frombuffer(msg.data, dtype=np.uint8).reshape(msg.height, msg.width, 3)
        results = self.model(bgr, verbose=False)
        for box in results[0].boxes:
            cls  = int(box.cls[0])
            name = self.model.names[cls]
            conf = float(box.conf[0])
            x1, y1, x2, y2 = map(int, box.xyxy[0])
            self.get_logger().info(f'{name} ({conf:.0%})  bbox=({x1},{y1})-({x2},{y2})')
```

## Detección de pelota (clase 32 = sports ball)

```python
BALL_CLASS = 32   # COCO class id for sports ball

def callback(self, msg):
    bgr = np.frombuffer(msg.data, dtype=np.uint8).reshape(msg.height, msg.width, 3)
    results = self.model(bgr, verbose=False, classes=[BALL_CLASS, 0])  # 0=persona
    for box in results[0].boxes:
        name = self.model.names[int(box.cls[0])]
        cx = (box.xyxy[0][0] + box.xyxy[0][2]) / 2
        cy = (box.xyxy[0][1] + box.xyxy[0][3]) / 2
        self.get_logger().info(f'Detectado: {name} en ({cx:.0f},{cy:.0f})')
```

## Tarea

Combina el detector YOLO con el controlador de locomoción de B6 para que el robot
se aproxime a la pelota detectada.
