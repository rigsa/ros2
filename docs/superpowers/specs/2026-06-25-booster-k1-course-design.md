# Booster K1 Course Track — Design Spec
**Date:** 2026-06-25  
**Repos:** `ros2`, `ros2-sandbox`, `rigsa_ros`

---

## 1. Summary

Add a full standalone Booster K1 humanoid course track to the RIGSA ROS 2 course site. The track runs independently of the existing Unitree track — students complete B1–B10 without any prerequisite Parts 1–6 knowledge. The site gains a landing-page track chooser. The sandbox gains a second Docker image based on Ubuntu 22.04 / ROS 2 Humble that includes all official Booster repos and a visually rich sim. Sheffield module codes (AMR31001, etc.) are removed from course-map and docs navigation.

---

## 2. MkDocs Site Changes

### 2.1 Landing page (`docs/index.md`)

Replace the current homepage with a two-card track chooser using Material for MkDocs grid cards:

- **Card A — Robots Cuadrúpedos (Unitree Go2 · AS2 · B2)**: links to `course/` root, badge "ROS 2 Jazzy", sandbox button
- **Card B — Robot Humanoide (Booster K1)**: links to `booster/` root, badge "ROS 2 Humble", sandbox button

### 2.2 Nav restructure

```
docs/
  index.md              ← NEW: track chooser
  course/               ← Unitree Parts 1–6 (unchanged)
  unitree/              ← U1–U12 + SDK2 + B2 blocks (unchanged)
  booster/              ← NEW: B1–B10
    .pages
    README.md
    b1-introduccion.md … b10-mision.md
  about/                ← unchanged (Sheffield CC BY-SA attribution stays)
  software/             ← unchanged
  amr/                  ← Sheffield codes stripped from .pages + README.md title
  com/                  ← Sheffield codes stripped
  ele/                  ← Sheffield codes stripped
```

### 2.3 Sheffield module code cleanup

| File | Old value | New value |
|------|-----------|-----------|
| `docs/.pages` line 7 | `"AMR31001": amr` | `"Laboratorios AMR": amr` |
| `docs/amr/.pages` line 2 | `"AMR31001": README.md` | `"Laboratorios de Robótica Móvil": README.md` |
| `ros2-sandbox/sandbox/course-map.yaml:92` | `"AMR31001 Lab 1: Mobile Robotics"` | `"Laboratorio 1: Robótica Móvil"` |
| `ros2-sandbox/sandbox/course-map.yaml:103` | `"AMR31001 Lab 2: Feedback Control"` | `"Laboratorio 2: Control Retroalimentado"` |

The two CC BY-SA 4.0 attribution mentions in `docs/course/README.md:40` and `docs/about/license.md:15` are **not touched**.

---

## 3. Booster K1 Course — B1–B10 (all in Spanish)

Full standalone track. Assumes zero ROS 2 prior knowledge. Same "write once, run anywhere" pattern as Unitree track: code written against `booster_sim_lite.py` topics runs unchanged on real K1 hardware via `booster_ros2_bridge.py`.

| Module | Title | Core skill | Sim world |
|--------|-------|-----------|-----------|
| B1 | Introducción al K1: Hardware y Arquitectura | K1 specs, operating modes (DAMP/PREP/WALK/CUSTOM/PROTECT), connection, bridge pattern | — |
| B2 | Locomoción Bípeda | `/cmd_vel` omnidirectional, walk square, figure-8 | `booster_empty` |
| B3 | Publishers y Subscribers | ROS 2 pub/sub fundamentals using K1 topics, `/odom`, `/imu/data` | `booster_empty` |
| B4 | Articulaciones y Estado del Robot | `/joint_states` (22 DoF), posture monitoring | `booster_empty` |
| B5 | Comportamientos y Servicios | Predefined actions via `/sport/*` services (wave, stand, fall-recovery) | `booster_empty` |
| B6 | Cámara RGBD y Visión con OpenCV | `/camera/image_raw` + `/camera/depth`, color detection, approach object | `booster_obstacles` |
| B7 | Detección de Objetos con YOLO | YOLOv8 on camera feed, ball/person detection, vision-guided approach | `booster_soccer` |
| B8 | LiDAR y Evitación de Obstáculos | `/scan` (simulated 360°), reactive avoidance, safe navigation | `booster_obstacles` |
| B9 | Arquitectura RoboCup: Vision + Brain | Study `robocup_demo` pipeline (read-only), vision-guided ball tracking exercise | `booster_soccer` |
| B10 | Misión Autónoma Integrada | Capstone: walk → detect → approach → report → return | `booster_inspection` |

Each lesson follows the same structure as existing Unitree modules: conceptual intro, architecture diagram, step-by-step exercise, expected output, "en el robot real" callout box.

---

## 4. `booster_sim_lite.py` — Visually Rich Simulator

**File:** `ros2-sandbox/sandbox/scripts/booster_sim_lite.py`  
**Pattern:** Mirrors `sim_lite.py` exactly — standalone ROS 2 node, no physics simulation.

### 4.1 Topics published

```
/cmd_vel          ← input  (TwistStamped)
/odom             → nav_msgs/Odometry
/imu/data         → sensor_msgs/Imu  (9-axis, simulated noise)
/joint_states     → sensor_msgs/JointState  (22 DoF, realistic Booster K1 joint names)
/camera/image_raw → sensor_msgs/Image  (320×240 RGB, PyBullet TinyRenderer)
/camera/depth     → sensor_msgs/Image  (320×240 float32 depth)
/scan             → sensor_msgs/LaserScan  (360°, 3.5 m max range)
/sport/*          → services: stand, wave, handshake, fall_recovery, dance
/battery_state    → sensor_msgs/BatteryState  (drains during WALK, charges at dock)
```

### 4.2 Sim worlds

| World | Contents | K1 start |
|-------|----------|----------|
| `booster_empty` | Open 8×8 m arena | Center |
| `booster_obstacles` | Arena + 6 cylindrical pillars | Center |
| `booster_soccer` | Green 9×6 m field, 1 ball sphere, 2 goal post pairs | Kickoff spot |
| `booster_inspection` | 3 inspection stations (ArUco 1–3), 1 dock zone (ArUco 0) | Entry point |

### 4.3 Pygame window layout (4-panel, no GPU required)

```
┌─────────────────────────────┬──────────────────────┐
│  TOP-DOWN MAP (pygame)      │  HEAD CAMERA FEED     │
│                             │  320×240              │
│  K1 humanoid silhouette     │  PyBullet TinyRenderer│
│  (vector, multi-angle,      │  (DIRECT mode, CPU)   │
│   leg animation on move)    │  shows world objects  │
│                             │  in perspective       │
│  LiDAR rays overlay         ├──────────────────────┤
│  Camera FOV cone            │  JOINT STATE VIEWER   │
│  Odom trail                 │  Stick figure 22 DoF  │
│  Obstacle outlines          │  IMU pitch/roll dials │
│                             │  Battery + mode badge │
└─────────────────────────────┴──────────────────────┘
```

### 4.4 K1 humanoid sprite

Drawn procedurally in pygame (no external asset). Proportions match real K1 (95 cm, 22 DoF):
- Head circle, torso rectangle, 2 arms (upper + lower), 2 legs (upper + lower + foot)
- Color by mode: gray=DAMP, yellow=PREP, green=WALK, blue=CUSTOM, red=PROTECT
- Leg animation: sine-wave step cycle tied to `/cmd_vel` linear.x magnitude
- Sprite rendered at 8 rotation angles, cached at startup

### 4.5 Camera feed (PyBullet TinyRenderer — DIRECT mode, no physics)

```python
physics_client = pybullet.connect(pybullet.DIRECT)   # no GUI, no simulation step
k1_id = pybullet.loadURDF("booster_assets/k1/urdf/k1.urdf", useFixedBase=True)
# World objects placed as static bodies
# Each tick: update head pose only, render camera
pybullet.resetBasePositionAndOrientation(k1_id, [rx, ry, 0.95], quat)
_, _, rgba, depth, _ = pybullet.getCameraImage(320, 240, viewMatrix, projMatrix,
                                                renderer=pybullet.ER_TINY_RENDERER)
# pybullet.stepSimulation() is NEVER called
```

Renders at 10 Hz. Depth image derived from PyBullet depth buffer → float32 metric distances.

### 4.6 Joint state viewer

Stick figure drawn in right panel. 22 joints mapped to segments. Active joints (non-zero velocity command) highlighted yellow. IMU shown as two arc gauges (pitch ±30°, roll ±30°). Battery bar + mode label.

---

## 5. Booster Docker Image (`Dockerfile.booster`)

**Base:** `osrf/ros:humble-desktop-full` (Ubuntu 22.04, ROS 2 Humble)

### 5.1 Booster repos baked in

| Repo | Image path | Build? | Purpose |
|------|-----------|--------|---------|
| `BoosterRobotics/booster_robotics_sdk` | `/opt/booster/sdk` | No (C++ study) | Low-level SDK reference |
| `BoosterRobotics/booster_robotics_sdk_ros2` | `/opt/ros_ws/src/booster_sdk_ros2` | Yes (colcon, depends on SDK headers at `/opt/booster/sdk`) | ROS 2 wrapper |
| `BoosterRobotics/booster_assets` | `/opt/booster/booster_assets` | pip -e | K1 URDF for TinyRenderer |
| `BoosterRobotics/robocup_demo` | `/opt/booster/robocup_demo` | No (study only) | B9 architecture study |
| `BoosterRobotics/booster_deploy` | `/opt/booster/booster_deploy` | No (study only) | RL deployment reference |
| `rigsa/rigsa_ros` (booster branch) | `/opt/ros_ws/src/rigsa_ros_booster` | Yes (colcon) | K1 course example nodes |

### 5.2 Python packages

```
booster_robotics_sdk_python   # K1 SDK Python bindings
booster-assets                # pip -e (from cloned repo)
ultralytics                   # YOLOv8 (B7)
opencv-python
numpy<2
pyyaml
pybullet                      # TinyRenderer (booster_sim_lite.py)
pygame
matplotlib
```

### 5.3 Sim files

```
sandbox/
  Dockerfile.booster           ← new
  course-map-booster.yaml      ← new
  scripts/
    booster_sim_lite.py        ← new
    booster_ros2_bridge.py     ← new stub for real K1 hardware
  seed/
    booster_code_templates/    ← B1–B10 starter .py files
```

### 5.4 No TurtleBot3 packages

`ros-humble-turtlebot3*` packages are not installed. This is a clean K1-only image.

---

## 6. Orchestrator — Track Routing

`orchestrator/app.py` reads a `?track=` query param:
- `?track=unitree` (default) → reads `course-map.yaml`, routes to `sandbox-unitree` Cloud Run service
- `?track=booster` → reads `course-map-booster.yaml`, routes to `sandbox-booster` Cloud Run service

Landing page card buttons pass `?track=booster` or `?track=unitree`. Two separate Cloud Run services deployed from `cloudbuild.yaml` with a new `_TRACK` substitution variable.

---

## 7. `rigsa_ros` — New Booster Branch

New branch `humble-booster` in `rigsa_ros`. Adds:

```
rigsa_ros_booster/
  package.xml
  CMakeLists.txt
  scripts/
    b2_walk_square.py
    b3_imu_subscriber.py
    b4_joint_monitor.py
    b5_behaviors.py
    b6_camera_color.py
    b7_yolo_detect.py
    b8_obstacle_avoidance.py
    b9_ball_tracker.py
    b10_autonomous_mission.py
  seed/                        ← starter templates (incomplete versions)
    b2_walk_square_start.py … b10_start.py
```

---

## 8. Out of Scope

- RL training (booster_gym, booster_train) — requires GPU and Isaac Sim; not sandbox-compatible
- MuJoCo/Webots full physics simulation — `booster_sim_lite.py` covers the teaching needs
- Booster T1 robot — only K1 is in scope
- `htwk-gym`, `NUbots_K1` repos — referenced in B9 reading material only, not cloned into image

---

## 9. Implementation Order

1. Sheffield cleanup (course-map.yaml + docs/.pages, docs/amr/.pages) — 10 min, no risk
2. Landing page (`docs/index.md`) — MkDocs grid card HTML
3. `booster/` docs tree — B1–B10 markdown lessons
4. `booster_sim_lite.py` — sim node (largest single file)
5. `Dockerfile.booster` + `course-map-booster.yaml`
6. Orchestrator track routing
7. `rigsa_ros` booster branch — example + seed scripts
8. Deploy test
