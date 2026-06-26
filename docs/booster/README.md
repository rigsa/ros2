---
title: "Curso Booster K1 — Introducción"
description: "Curso completo de ROS 2 con el robot humanoide Booster K1. 10 módulos, desde cero hasta misión autónoma."
---

# Curso Booster K1

Aprende ROS 2 usando el **Booster K1** — el robot humanoide de 95 cm que ganó el RoboCup 2025 KidSize.

## Módulos del curso

| Módulo | Tema | Mundo |
|--------|------|-------|
| [B1](b1-introduccion.md) | Hardware y arquitectura | — |
| [B2](b2-locomocion.md) | Locomoción bípeda | `booster_empty` |
| [B3](b3-pubsub.md) | Publishers y Subscribers | `booster_empty` |
| [B4](b4-articulaciones.md) | Articulaciones e IMU | `booster_empty` |
| [B5](b5-comportamientos.md) | Comportamientos y Servicios | `booster_empty` |
| [B6](b6-camara.md) | Cámara RGBD y OpenCV | `booster_obstacles` |
| [B7](b7-yolo.md) | Detección con YOLO | `booster_soccer` |
| [B8](b8-lidar.md) | LiDAR y obstáculos | `booster_obstacles` |
| [B9](b9-robocup.md) | Arquitectura RoboCup | `booster_soccer` |
| [B10](b10-mision.md) | Misión autónoma integrada | `booster_inspection` |

## Requisitos

- Acceso al sandbox (botón **Sandbox** en cada módulo)
- No se requiere experiencia previa con ROS 2

## El patrón bridge

Tu código usa topics ROS 2 estándar. En el sandbox, `booster_sim_lite.py` los simula.
En el robot real, `booster_ros2_bridge.py` traduce al SDK de Booster automáticamente.
**El mismo código funciona en ambos entornos.**
