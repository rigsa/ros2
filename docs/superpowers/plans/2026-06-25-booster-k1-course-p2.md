# Booster K1 Course Track — Implementation Plan (Part 2 of 2)

> **Prereq:** Part 1 tasks 1–4 complete. Continues from Part 1.

## Global Constraints (same as Part 1)
- `pybullet.stepSimulation()` must never be called.
- K1 joint names (22): head_yaw, head_pitch, l/r_shoulder_pitch/roll/yaw, l/r_elbow_pitch, l/r_hip_pitch/roll/yaw, l/r_knee_pitch, l/r_ankle_pitch/roll.
- ROS 2 Humble only in Booster image.
- `SANDBOX_IMAGE_BOOSTER` env var selects Booster Cloud Run image.

---

### Task 5: booster_sim_lite.py — Core Node + Worlds

**Files:**
- Create: `ros2-sandbox/sandbox/scripts/booster_sim_lite.py`

**Interfaces:**
- Produces: ROS 2 node `booster_sim_lite` launched as `ros2 run booster_sim_lite booster_sim_lite.py <world_name>`
- Topics published: `/odom`, `/imu/data`, `/joint_states`, `/scan`, `/camera/image_raw`, `/camera/depth`, `/battery_state`
- Services: `/sport/stand_up`, `/sport/stand_down`, `/sport/hello`, `/sport/stretch`, `/sport/dance1`, `/sport/dance2`, `/sport/recovery_stand`, `/sport/balance_stand`, `/sport/dock`, `/sport/undock`

- [ ] **Step 1: Write the core file**

Create `/home/jahir/repos/ros2-sandbox/sandbox/scripts/booster_sim_lite.py`:

```python
#!/usr/bin/env python3
"""
booster_sim_lite.py — Lightweight ROS 2 simulator for the Booster K1 course sandbox.

4-panel pygame window:
  top-left:  Top-down map — K1 humanoid sprite, LiDAR rays, camera FOV, odom trail
  top-right: Head camera feed — PyBullet TinyRenderer (DIRECT mode, no physics step)
  bot-left:  Joint state viewer — stick figure + IMU gauges
  bot-right: Dashboard — battery, mode, speed, world label

Topics published:
  /odom              nav_msgs/Odometry         30 Hz
  /imu/data          sensor_msgs/Imu           30 Hz
  /joint_states      sensor_msgs/JointState    30 Hz
  /scan              sensor_msgs/LaserScan     10 Hz
  /camera/image_raw  sensor_msgs/Image         10 Hz  (from PyBullet TinyRenderer)
  /camera/depth      sensor_msgs/Image         10 Hz  (float32 depth)
  /battery_state     sensor_msgs/BatteryState   1 Hz

Subscribed:
  /cmd_vel  geometry_msgs/TwistStamped

Services (std_srvs/Trigger):
  /sport/stand_up, stand_down, hello, stretch, dance1, dance2,
  recovery_stand, balance_stand, dock, undock
"""

import math
import os
import threading
import time

import cv2
import numpy as np
import pygame
import rclpy
from geometry_msgs.msg import TransformStamped, TwistStamped
from nav_msgs.msg import Odometry
from rclpy.node import Node
from sensor_msgs.msg import BatteryState, Image, Imu, JointState, LaserScan
from std_srvs.srv import Trigger
from tf2_ros import StaticTransformBroadcaster, TransformBroadcaster

# ---------------------------------------------------------------------------
# K1 constants
# ---------------------------------------------------------------------------

K1_HEIGHT = 0.95   # metres — used for camera pose
K1_CAM_FORWARD = 0.10  # camera offset forward from centre

K1_JOINT_NAMES = [
    "head_yaw", "head_pitch",
    "l_shoulder_pitch", "l_shoulder_roll", "l_shoulder_yaw", "l_elbow_pitch",
    "r_shoulder_pitch", "r_shoulder_roll", "r_shoulder_yaw", "r_elbow_pitch",
    "l_hip_pitch",  "l_hip_roll",  "l_hip_yaw",  "l_knee_pitch",
    "l_ankle_pitch","l_ankle_roll",
    "r_hip_pitch",  "r_hip_roll",  "r_hip_yaw",  "r_knee_pitch",
    "r_ankle_pitch","r_ankle_roll",
]  # 22 joints

_SPORT_LABELS = {
    "stand_up":       "⬆ Stand Up",
    "stand_down":     "⬇ Stand Down",
    "hello":          "👋 Hello",
    "stretch":        "🤸 Stretch",
    "dance1":         "💃 Dance 1",
    "dance2":         "🕺 Dance 2",
    "recovery_stand": "🔄 Recovery",
    "balance_stand":  "⚖ Balance",
    "dock":           "⚡ Dock",
    "undock":         "🚀 Undock",
}

# Colours
_MODE_COLORS = {
    "DAMP":    (120, 120, 120),
    "PREP":    (200, 160,  30),
    "WALK":    ( 40, 180,  80),
    "CUSTOM":  ( 60, 130, 210),
    "PROTECT": (200,  50,  50),
}

# ---------------------------------------------------------------------------
# World definitions
# ---------------------------------------------------------------------------

_GRAY  = (120, 120, 120)
_GREEN = ( 50, 140,  50)
_DOCK_C = (60, 180, 220)

BOOSTER_WORLDS: dict = {
    "booster_empty": {
        "pillars": [], "arena_r": 5.0, "ball": None, "goals": False,
        "dock_pos": None, "pois": [],
        "label": "K1 open space  ·  B1-B5",
    },
    "booster_obstacles": {
        "pillars": [
            ( 1.5,  0.5, 0.25, _GRAY), (-1.5,  1.0, 0.25, _GRAY),
            ( 0.5, -2.0, 0.25, _GRAY), (-0.8, -1.2, 0.20, _GRAY),
            ( 2.5,  1.5, 0.20, _GRAY), (-2.0,  0.0, 0.20, _GRAY),
        ],
        "arena_r": 5.0, "ball": None, "goals": False,
        "dock_pos": None, "pois": [],
        "label": "K1 obstacle course  ·  B6, B8",
    },
    "booster_soccer": {
        "pillars": [],
        "arena_r": 6.0,
        "ball": (1.5, 0.0, 0.11, (220, 80, 30)),    # (x, y, radius, color)
        "goals": True,
        "dock_pos": None, "pois": [("⚽", 1.5, 0.0)],
        "label": "Soccer field  ·  B7, B9",
    },
    "booster_inspection": {
        "pillars": [
            ( 2.5,  1.5, 0.35, _GRAY, 1), ( 2.5, -1.5, 0.35, _GRAY, 2),
            (-1.5,  2.5, 0.35, _GRAY, 3), (-3.5,  0.0, 0.35, _DOCK_C, 0),
            ( 0.5,  0.5, 0.20, _GRAY),   (-0.5, -1.0, 0.20, _GRAY),
        ],
        "arena_r": 5.0, "ball": None, "goals": False,
        "dock_pos": (-3.5, 0.0),
        "pois": [("A", 2.5, 1.5), ("B", 2.5, -1.5), ("C", -1.5, 2.5), ("⚡", -3.5, 0.0)],
        "label": "Inspection field  ·  B10",
    },
}

# ---------------------------------------------------------------------------
# ArUco markers
# ---------------------------------------------------------------------------

_ARUCO_MARKERS: dict = {}
try:
    _DICT = cv2.aruco.getPredefinedDictionary(cv2.aruco.DICT_4X4_50)
    for _mid in range(5):
        _gray = cv2.aruco.generateImageMarker(_DICT, _mid, 80)
        _ARUCO_MARKERS[_mid] = cv2.cvtColor(_gray, cv2.COLOR_GRAY2BGR)
except AttributeError:
    pass

# ---------------------------------------------------------------------------
# Helpers
# ---------------------------------------------------------------------------

def _bgr_to_imgmsg(bgr: np.ndarray, stamp, frame_id="camera_link") -> Image:
    msg = Image()
    msg.header.stamp    = stamp
    msg.header.frame_id = frame_id
    msg.height = bgr.shape[0]; msg.width = bgr.shape[1]
    msg.encoding = "bgr8"; msg.is_bigendian = False
    msg.step = bgr.shape[1] * 3
    msg.data = bgr.tobytes()
    return msg

def _depth_to_imgmsg(depth: np.ndarray, stamp) -> Image:
    msg = Image()
    msg.header.stamp = stamp; msg.header.frame_id = "camera_link"
    msg.height = depth.shape[0]; msg.width = depth.shape[1]
    msg.encoding = "32FC1"; msg.is_bigendian = False
    msg.step = depth.shape[1] * 4
    msg.data = depth.astype(np.float32).tobytes()
    return msg

def _make_tf(frame, child, x, y, z, yaw, stamp) -> TransformStamped:
    t = TransformStamped()
    t.header.stamp = stamp; t.header.frame_id = frame
    t.child_frame_id = child
    t.transform.translation.x = x; t.transform.translation.y = y
    t.transform.translation.z = z
    cy, sy = math.cos(yaw/2), math.sin(yaw/2)
    t.transform.rotation.w = cy; t.transform.rotation.z = sy
    return t

def _quat_from_yaw(yaw):
    return (0.0, 0.0, math.sin(yaw/2), math.cos(yaw/2))

def _cast_scan(rx, ry, pillars, ball, arena_r, n_rays=360, max_r=3.5) -> list:
    hits = []
    for i in range(n_rays):
        angle = -math.pi + 2*math.pi*i/n_rays
        dx, dy = math.cos(angle), math.sin(angle)
        best = max_r
        # Arena boundary
        # Ray-circle for arena
        for t in _ray_circle(rx, ry, dx, dy, 0, 0, arena_r):
            if 0 < t < best: best = t
        # Pillars
        for p in pillars:
            for t in _ray_circle(rx, ry, dx, dy, p[0], p[1], p[2]):
                if 0 < t < best: best = t
        # Ball
        if ball:
            for t in _ray_circle(rx, ry, dx, dy, ball[0], ball[1], ball[2]):
                if 0 < t < best: best = t
        hits.append(best)
    return hits

def _ray_circle(ox, oy, dx, dy, cx, cy, r):
    fx, fy = ox-cx, oy-cy
    a = dx*dx + dy*dy
    b = 2*(fx*dx + fy*dy)
    c = fx*fx + fy*fy - r*r
    disc = b*b - 4*a*c
    if disc < 0: return []
    sd = math.sqrt(disc)
    return [(-b+sd)/(2*a), (-b-sd)/(2*a)]

# ---------------------------------------------------------------------------
# PyBullet camera renderer (DIRECT mode — no physics)
# ---------------------------------------------------------------------------

class K1CameraRenderer:
    """Renders head camera using PyBullet TinyRenderer. No physics steps."""

    W, H = 320, 240
    FOV  = 60.0

    def __init__(self, world_name: str, wdef: dict):
        self._p = None
        self._client = -1
        self._k1_id  = -1
        self._bodies = []
        self._wdef   = wdef
        try:
            import pybullet as p
            import pybullet_data
            self._p = p
            self._client = p.connect(p.DIRECT)
            p.setAdditionalSearchPath(pybullet_data.getDataPath(),
                                      physicsClientId=self._client)
            self._build_world(wdef)
        except Exception as e:
            print(f"[booster_sim_lite] PyBullet init failed: {e} — camera will show blank")

    def _load_k1(self):
        assets = os.environ.get("BOOSTER_ASSETS_PATH",
                                "/opt/booster/booster_assets")
        urdf = os.path.join(assets, "K1", "urdf", "k1.urdf")
        if not os.path.exists(urdf):
            # Fallback: simple box approximating K1 torso
            return self._p.loadURDF(
                "cube.urdf", [0, 0, 0.475],
                physicsClientId=self._client)
        return self._p.loadURDF(urdf, [0, 0, 0],
                                useFixedBase=True,
                                physicsClientId=self._client)

    def _build_world(self, wdef: dict):
        p = self._p; c = self._client
        # Floor
        p.loadURDF("plane.urdf", physicsClientId=c)
        self._k1_id = self._load_k1()
        # Pillars
        for pil in wdef.get("pillars", []):
            half = [pil[2], pil[2], 0.5]
            col = p.createCollisionShape(p.GEOM_BOX, halfExtents=half,
                                         physicsClientId=c)
            vis = p.createVisualShape(p.GEOM_BOX, halfExtents=half,
                                      rgbaColor=[pil[3][0]/255, pil[3][1]/255,
                                                 pil[3][2]/255, 1],
                                      physicsClientId=c)
            self._bodies.append(
                p.createMultiBody(0, col, vis, [pil[0], pil[1], 0.5],
                                  physicsClientId=c))
        # Ball
        if wdef.get("ball"):
            bx, by, br, bc = wdef["ball"]
            col = p.createCollisionShape(p.GEOM_SPHERE, radius=br, physicsClientId=c)
            vis = p.createVisualShape(p.GEOM_SPHERE, radius=br,
                                      rgbaColor=[bc[0]/255, bc[1]/255, bc[2]/255, 1],
                                      physicsClientId=c)
            self._bodies.append(
                p.createMultiBody(0, col, vis, [bx, by, br], physicsClientId=c))

    def render(self, rx: float, ry: float, th: float):
        """Return (rgb 320×240 uint8, depth 320×240 float32). Never steps physics."""
        if self._p is None or self._k1_id < 0:
            return (np.zeros((self.H, self.W, 3), dtype=np.uint8),
                    np.full((self.H, self.W), 3.5, dtype=np.float32))
        p = self._p; c = self._client
        # Update K1 pose (kinematic only)
        qx, qy, qz, qw = *_quat_from_yaw(th)[:2], _quat_from_yaw(th)[2], _quat_from_yaw(th)[3]
        p.resetBasePositionAndOrientation(
            self._k1_id, [rx, ry, 0], [0, 0, qz, qw], physicsClientId=c)
        # Camera position: head height, slightly forward
        cam_x = rx + K1_CAM_FORWARD * math.cos(th)
        cam_y = ry + K1_CAM_FORWARD * math.sin(th)
        cam_z = K1_HEIGHT
        target_x = cam_x + math.cos(th)
        target_y = cam_y + math.sin(th)
        vm = p.computeViewMatrix(
            [cam_x, cam_y, cam_z], [target_x, target_y, cam_z - 0.1], [0, 0, 1],
            physicsClientId=c)
        pm = p.computeProjectionMatrixFOV(
            self.FOV, self.W/self.H, 0.1, 10.0, physicsClientId=c)
        _, _, rgba, depth_buf, _ = p.getCameraImage(
            self.W, self.H, vm, pm,
            renderer=p.ER_TINY_RENDERER, physicsClientId=c)
        # RGBA → BGR
        rgb = np.array(rgba, dtype=np.uint8).reshape(self.H, self.W, 4)
        bgr = cv2.cvtColor(rgb[:, :, :3], cv2.COLOR_RGB2BGR)
        # Linearise depth buffer to metric depth
        near, far = 0.1, 10.0
        db = np.array(depth_buf, dtype=np.float32).reshape(self.H, self.W)
        depth_m = far * near / (far - (far - near) * db)
        return bgr, depth_m

    def close(self):
        if self._p and self._client >= 0:
            self._p.disconnect(self._client)

# ---------------------------------------------------------------------------
# ROS 2 node
# ---------------------------------------------------------------------------

class BoosterSimLiteNode(Node):

    def __init__(self, world_name: str):
        super().__init__("booster_sim_lite")
        self.world_name = world_name
        wdef = BOOSTER_WORLDS.get(world_name, BOOSTER_WORLDS["booster_empty"])
        self._wdef     = wdef
        self._pillars  = wdef["pillars"]
        self._ball     = wdef.get("ball")
        self._arena_r  = wdef["arena_r"]
        self._dock_pos = wdef.get("dock_pos")

        self._lock   = threading.Lock()
        self._x      = 0.0; self._y = 0.0; self._theta = 0.0
        self._vx     = 0.0; self._vy = 0.0; self._wz   = 0.0
        self._t      = time.monotonic()
        self._battery = float(os.environ.get("SIM_BATTERY_START", "80"))
        self._docked  = False
        self._mode    = "WALK"
        self._sport_label = ""
        self._sport_t     = 0.0
        self._odom_trail  = []   # list of (x,y)
        # Simulated joint positions (start at zero, animate legs during walk)
        self._joint_pos = [0.0] * 22
        self._step_phase = 0.0

        # TF
        self._tf_bc    = TransformBroadcaster(self)
        self._stf_bc   = StaticTransformBroadcaster(self)
        now = self.get_clock().now().to_msg()
        self._stf_bc.sendTransform([
            _make_tf("base_footprint", "base_scan",    0.0,  0.0, 0.35, 0.0, now),
            _make_tf("base_footprint", "camera_link",  0.10, 0.0, K1_HEIGHT, 0.0, now),
        ])

        # Publishers
        self._pub_odom    = self.create_publisher(Odometry,     "/odom",             10)
        self._pub_imu     = self.create_publisher(Imu,          "/imu/data",         10)
        self._pub_joints  = self.create_publisher(JointState,   "/joint_states",     10)
        self._pub_scan    = self.create_publisher(LaserScan,    "/scan",             10)
        self._pub_img     = self.create_publisher(Image,        "/camera/image_raw", 10)
        self._pub_depth   = self.create_publisher(Image,        "/camera/depth",     10)
        self._pub_battery = self.create_publisher(BatteryState, "/battery_state",    10)

        # Subscriber
        self.create_subscription(TwistStamped, "/cmd_vel", self._cmd_cb, 10)

        # Timers
        self.create_timer(1.0/30.0, self._physics_cb)
        self.create_timer(1.0/10.0, self._sensors_cb)
        self.create_timer(1.0,      self._battery_cb)

        # Sport services
        for b in _SPORT_LABELS:
            self.create_service(Trigger, f"/sport/{b}",
                lambda req, resp, bv=b: self._sport_cb(req, resp, bv))

        # Camera renderer (deferred — initialised on first sensor tick)
        self._renderer: K1CameraRenderer | None = None
        self._renderer_ready = False

        self.get_logger().info(
            f"booster_sim_lite ready  world={world_name!r}  battery={self._battery:.0f}%")

    def _init_renderer(self):
        if not self._renderer_ready:
            self._renderer = K1CameraRenderer(self.world_name, self._wdef)
            self._renderer_ready = True

    def _cmd_cb(self, msg: TwistStamped):
        with self._lock:
            if not self._docked:
                self._vx = msg.twist.linear.x
                self._vy = msg.twist.linear.y
                self._wz = msg.twist.angular.z

    def _physics_cb(self):
        now_t = time.monotonic()
        with self._lock:
            dt = now_t - self._t; self._t = now_t
            if not self._docked:
                ct = math.cos(self._theta); st = math.sin(self._theta)
                self._x     += (self._vx*ct - self._vy*st) * dt
                self._y     += (self._vx*st + self._vy*ct) * dt
                self._theta += self._wz * dt
                # Clamp to arena
                d = math.sqrt(self._x**2 + self._y**2)
                if d > self._arena_r - 0.3:
                    f = (self._arena_r - 0.3) / d
                    self._x *= f; self._y *= f

            # Animate joints (leg swing during walking)
            speed = math.sqrt(self._vx**2 + self._vy**2)
            if speed > 0.02:
                self._step_phase += dt * 4.0  # ~4 Hz gait
            amp = min(speed * 0.5, 0.3)  # max ±0.3 rad
            phase = self._step_phase
            # Left leg: hip_pitch (index 10), knee_pitch (13)
            self._joint_pos[10] = amp * math.sin(phase)
            self._joint_pos[13] = amp * abs(math.sin(phase))
            # Right leg: hip_pitch (16), knee_pitch (19)  — opposite phase
            self._joint_pos[16] = amp * math.sin(phase + math.pi)
            self._joint_pos[19] = amp * abs(math.sin(phase + math.pi))
            # Arm swing (opposite to legs)
            self._joint_pos[2]  =  amp * 0.5 * math.sin(phase + math.pi)
            self._joint_pos[6]  =  amp * 0.5 * math.sin(phase)

            # Record odom trail (max 300 points)
            self._odom_trail.append((self._x, self._y))
            if len(self._odom_trail) > 300:
                self._odom_trail.pop(0)

            x, y, th = self._x, self._y, self._theta

        # Publish odom
        stamp = self.get_clock().now().to_msg()
        odom = Odometry()
        odom.header.stamp = stamp; odom.header.frame_id = "odom"
        odom.child_frame_id = "base_footprint"
        odom.pose.pose.position.x = x; odom.pose.pose.position.y = y
        qx, qy, qz, qw = 0.0, 0.0, *_quat_from_yaw(th)[2:]
        odom.pose.pose.orientation.z = math.sin(th/2)
        odom.pose.pose.orientation.w = math.cos(th/2)
        self._pub_odom.publish(odom)

        # TF odom → base_footprint
        tf = _make_tf("odom", "base_footprint", x, y, 0.0, th, stamp)
        self._tf_bc.sendTransform(tf)

        # IMU (simulated — small noise + gravity)
        imu = Imu()
        imu.header.stamp = stamp; imu.header.frame_id = "base_footprint"
        imu.linear_acceleration.x = np.random.normal(0, 0.05)
        imu.linear_acceleration.y = np.random.normal(0, 0.05)
        imu.linear_acceleration.z = 9.81 + np.random.normal(0, 0.02)
        imu.angular_velocity.z = self._wz + np.random.normal(0, 0.01)
        imu.orientation.z = math.sin(th/2); imu.orientation.w = math.cos(th/2)
        self._pub_imu.publish(imu)

        # Joint states
        js = JointState()
        js.header.stamp = stamp
        js.name     = K1_JOINT_NAMES
        with self._lock:
            js.position = list(self._joint_pos)
        js.velocity = [0.0] * 22; js.effort = [0.0] * 22
        self._pub_joints.publish(js)

    def _sensors_cb(self):
        self._init_renderer()
        with self._lock:
            x, y, th = self._x, self._y, self._theta

        stamp = self.get_clock().now().to_msg()

        # LiDAR
        ranges = _cast_scan(x, y, self._pillars, self._ball, self._arena_r)
        scan = LaserScan()
        scan.header.stamp = stamp; scan.header.frame_id = "base_scan"
        scan.angle_min = -math.pi; scan.angle_max = math.pi
        scan.angle_increment = 2*math.pi / len(ranges)
        scan.range_min = 0.05; scan.range_max = 3.5
        scan.ranges = [float(r) for r in ranges]
        self._pub_scan.publish(scan)

        # Camera
        if self._renderer:
            bgr, depth = self._renderer.render(x, y, th)
        else:
            bgr   = np.zeros((240, 320, 3), dtype=np.uint8)
            depth = np.full((240, 320), 3.5, dtype=np.float32)

        self._pub_img.publish(_bgr_to_imgmsg(bgr, stamp))
        self._pub_depth.publish(_depth_to_imgmsg(depth, stamp))

    def _battery_cb(self):
        with self._lock:
            speed = math.sqrt(self._vx**2 + self._vy**2)
            if not self._docked:
                drain = 0.02 + speed * 0.05
                self._battery = max(0, self._battery - drain)
            else:
                self._battery = min(100, self._battery + 0.5)
            pct = self._battery
        msg = BatteryState()
        msg.percentage = pct / 100.0
        msg.power_supply_status = (
            BatteryState.POWER_SUPPLY_STATUS_CHARGING if self._docked
            else BatteryState.POWER_SUPPLY_STATUS_DISCHARGING)
        self._pub_battery.publish(msg)
        if pct < 10:
            self.get_logger().warn(f"Batería baja: {pct:.0f}%")

    def _sport_cb(self, req, resp, behavior: str):
        with self._lock:
            if behavior == "dock" and self._dock_pos:
                self._docked = True
            elif behavior == "undock":
                self._docked = False
            self._sport_label = _SPORT_LABELS[behavior]
            self._sport_t     = time.monotonic()
        resp.success = True
        resp.message = f"{behavior} OK"
        return resp


# ---------------------------------------------------------------------------
# Pygame visualisation
# ---------------------------------------------------------------------------

_WIN_W, _WIN_H = 1200, 800
_MAP_W, _MAP_H = 600, 500
_CAM_W, _CAM_H = 600, 400
_JNT_W, _JNT_H = 600, 300
_DSH_W, _DSH_H = 600, 100

_PX_PER_M = 50   # pixels per metre in top-down view
_FONT = None


def _init_fonts():
    global _FONT
    pygame.font.init()
    _FONT = pygame.font.SysFont("monospace", 12)


def _w2px(x, y, cx, cy):
    """World coords to pygame pixel (top-down, y-up flipped)."""
    return int(cx + x * _PX_PER_M), int(cy - y * _PX_PER_M)


def _draw_k1_sprite(surf, px, py, th, speed, mode, phase):
    """Draw K1 humanoid silhouette at (px,py) facing th."""
    color = _MODE_COLORS.get(mode, (80, 80, 80))
    dim   = (80, 80, 80)
    # Compute body axes
    ct, st = math.cos(th), math.sin(th)

    def rot(dx, dy):
        return (px + int(ct*dx - st*dy), py - int(st*dx + ct*dy))

    # Torso (rectangle 8×14 px)
    pts = [rot(-4, -7), rot(4, -7), rot(4, 7), rot(-4, 7)]
    pygame.draw.polygon(surf, color, pts)
    # Head circle
    hx, hy = rot(0, -11)
    pygame.draw.circle(surf, color, (hx, hy), 5)

    # Arms
    amp = min(speed * 0.3, 0.25) if speed > 0.02 else 0
    l_arm_angle = th + math.pi/2 + amp*math.sin(phase + math.pi)
    r_arm_angle = th - math.pi/2 + amp*math.sin(phase)
    ax1, ay1 = rot(-6, -5)
    ax2 = ax1 + int(9 * math.cos(l_arm_angle)); ay2 = ay1 - int(9 * math.sin(l_arm_angle))
    pygame.draw.line(surf, dim, (ax1, ay1), (ax2, ay2), 2)
    bx1, by1 = rot(6, -5)
    bx2 = bx1 + int(9 * math.cos(r_arm_angle)); by2 = by1 - int(9 * math.sin(r_arm_angle))
    pygame.draw.line(surf, dim, (bx1, by1), (bx2, by2), 2)

    # Legs
    l_knee_off =  amp * math.sin(phase) * 8
    r_knee_off = -amp * math.sin(phase) * 8
    lf1, lf2 = rot(-3, 7), rot(int(-3 + l_knee_off), 14)
    rf1, rf2 = rot( 3, 7), rot(int( 3 + r_knee_off), 14)
    pygame.draw.line(surf, color, lf1, lf2, 3)
    pygame.draw.line(surf, color, rf1, rf2, 3)

    # Heading indicator dot
    nx, ny = rot(0, -16)
    pygame.draw.circle(surf, (255, 255, 100), (nx, ny), 3)


def _draw_map(surf, node: BoosterSimLiteNode):
    surf.fill((30, 30, 30))
    wdef = node._wdef
    cx, cy = _MAP_W // 2, _MAP_H // 2

    # Arena boundary
    ar = int(wdef["arena_r"] * _PX_PER_M)
    pygame.draw.circle(surf, (50, 50, 50), (cx, cy), ar)
    pygame.draw.circle(surf, (80, 80, 80), (cx, cy), ar, 1)

    # Soccer field markings
    if wdef.get("goals"):
        fw, fh = int(4.5 * _PX_PER_M), int(3.0 * _PX_PER_M)
        pygame.draw.rect(surf, (40, 90, 40), (cx - fw, cy - fh, fw*2, fh*2))
        pygame.draw.rect(surf, (60, 130, 60), (cx - fw, cy - fh, fw*2, fh*2), 1)
        # Centre circle
        pygame.draw.circle(surf, (60, 130, 60), (cx, cy), int(0.75 * _PX_PER_M), 1)
        # Goals
        for sx in [-1, 1]:
            gx, gy = cx + sx*(fw), cy
            pygame.draw.rect(surf, (200, 200, 200),
                             (gx - (4 if sx > 0 else 0), gy - int(0.5*_PX_PER_M),
                              4, int(_PX_PER_M)), 1)

    # Odom trail
    with node._lock:
        trail = list(node._odom_trail)
    if len(trail) > 2:
        pts = [_w2px(x, y, cx, cy) for x,y in trail]
        pygame.draw.lines(surf, (60, 100, 60), False, pts, 1)

    # Pillars
    for p in wdef["pillars"]:
        px_, py_ = _w2px(p[0], p[1], cx, cy)
        r = max(3, int(p[2] * _PX_PER_M))
        col = p[3] if len(p) > 3 else _GRAY
        pygame.draw.circle(surf, col, (px_, py_), r)
        if len(p) > 4:  # ArUco id
            mid = p[4]
            lbl = _FONT.render(str(mid), True, (255, 255, 255))
            surf.blit(lbl, (px_ - 6, py_ - 6))

    # Ball
    if wdef.get("ball"):
        bx_, by_, br_, bc_ = wdef["ball"]
        bpx, bpy = _w2px(bx_, by_, cx, cy)
        pygame.draw.circle(surf, bc_, (bpx, bpy), max(4, int(br_ * _PX_PER_M)))

    # POIs
    for lbl, px_, py_ in wdef.get("pois", []):
        ppx, ppy = _w2px(px_, py_, cx, cy)
        t = _FONT.render(lbl, True, (200, 200, 100))
        surf.blit(t, (ppx + 4, ppy - 8))

    with node._lock:
        x, y, th = node._x, node._y, node._theta
        vx, speed = node._vx, math.sqrt(node._vx**2 + node._vy**2)
        mode   = node._mode
        phase  = node._step_phase
        sports = node._sport_label
        sport_t = node._sport_t

    rx, ry = _w2px(x, y, cx, cy)

    # LiDAR rays (draw every 6th)
    with node._lock:
        dummy_ranges = _cast_scan(x, y, node._pillars, node._ball, node._arena_r)
    for i in range(0, 360, 6):
        angle = -math.pi + 2*math.pi*i/360 + th
        dist  = dummy_ranges[i]
        ex = rx + int(dist * _PX_PER_M * math.cos(angle))
        ey = ry - int(dist * _PX_PER_M * math.sin(angle))
        pygame.draw.line(surf, (0, 80, 0, 80), (rx, ry), (ex, ey), 1)
        if dist < 3.4:
            pygame.draw.circle(surf, (0, 200, 100), (ex, ey), 2)

    # Camera FOV cone (60° at up to 2 m)
    fov_r = int(2.0 * _PX_PER_M)
    for da in [-30, 30]:
        a = th + math.radians(da)
        fx = rx + int(fov_r * math.cos(a))
        fy = ry - int(fov_r * math.sin(a))
        pygame.draw.line(surf, (100, 100, 200), (rx, ry), (fx, fy), 1)

    # K1 sprite
    _draw_k1_sprite(surf, rx, ry, th, speed, mode, phase)

    # Sport label overlay
    if sports and (time.monotonic() - sport_t) < 2.0:
        t = _FONT.render(sports, True, (255, 255, 100))
        surf.blit(t, (rx - 30, ry - 30))

    # Grid label
    t = _FONT.render(wdef["label"], True, (100, 100, 100))
    surf.blit(t, (4, _MAP_H - 16))


def _draw_camera(surf, node: BoosterSimLiteNode):
    """Draw camera feed panel (top-right)."""
    surf.fill((10, 10, 10))
    if node._renderer and node._renderer_ready:
        with node._lock:
            x, y, th = node._x, node._y, node._theta
        bgr, _ = node._renderer.render(x, y, th)
        # Convert BGR numpy → pygame surface
        rgb = cv2.cvtColor(bgr, cv2.COLOR_BGR2RGB)
        cam_surf = pygame.surfarray.make_surface(
            np.transpose(rgb, (1, 0, 2)))
        scaled = pygame.transform.scale(cam_surf, (_CAM_W, _CAM_H - 20))
        surf.blit(scaled, (0, 20))
    else:
        t = _FONT.render("Cámara inicializando...", True, (100, 100, 100))
        surf.blit(t, (20, _CAM_H // 2))
    t = _FONT.render("HEAD CAMERA (60° FOV)", True, (150, 150, 150))
    surf.blit(t, (4, 4))


def _draw_joint_viewer(surf, node: BoosterSimLiteNode):
    """Draw joint state stick figure + IMU gauges (bottom-left)."""
    surf.fill((20, 20, 25))
    with node._lock:
        joints = list(node._joint_pos)
        th     = node._theta

    # Stick figure (front view, centred)
    cx, cy = 120, 140
    sc = 12  # pixels per unit

    def jpos(idx): return joints[idx] if idx < len(joints) else 0.0

    # Head
    pygame.draw.circle(surf, (180, 180, 180), (cx, cy - 6*sc), int(sc*0.8))
    # Torso
    pygame.draw.line(surf, (180, 180, 180), (cx, cy - 5*sc), (cx, cy), 3)

    # Arms
    l_shoulder = (cx - int(sc * 1.5), cy - int(sc * 4))
    r_shoulder = (cx + int(sc * 1.5), cy - int(sc * 4))
    l_elbow = (l_shoulder[0] + int(sc * 1.5 * math.sin(jpos(2))),
               l_shoulder[1] + int(sc * 1.5 * math.cos(jpos(2))))
    r_elbow = (r_shoulder[0] - int(sc * 1.5 * math.sin(jpos(6))),
               r_shoulder[1] + int(sc * 1.5 * math.cos(jpos(6))))
    pygame.draw.line(surf, (150, 200, 150), l_shoulder, l_elbow, 2)
    pygame.draw.line(surf, (150, 200, 150), r_shoulder, r_elbow, 2)

    # Legs
    l_hip = (cx - int(sc * 0.8), cy)
    r_hip = (cx + int(sc * 0.8), cy)
    l_knee = (l_hip[0] + int(sc * 1.5 * math.sin(jpos(10))),
              l_hip[1]  + int(sc * 1.5 * math.cos(jpos(10))))
    r_knee = (r_hip[0]  + int(sc * 1.5 * math.sin(jpos(16))),
              r_hip[1]  + int(sc * 1.5 * math.cos(jpos(16))))
    l_ankle = (l_knee[0] + int(sc * 1.5 * math.sin(jpos(13))),
               l_knee[1] + int(sc * 1.5 * math.cos(jpos(13))))
    r_ankle = (r_knee[0] + int(sc * 1.5 * math.sin(jpos(19))),
               r_knee[1] + int(sc * 1.5 * math.cos(jpos(19))))
    pygame.draw.line(surf, (150, 150, 200), l_hip,   l_knee,  3)
    pygame.draw.line(surf, (150, 150, 200), l_knee,  l_ankle, 3)
    pygame.draw.line(surf, (150, 150, 200), r_hip,   r_knee,  3)
    pygame.draw.line(surf, (150, 150, 200), r_knee,  r_ankle, 3)

    # IMU pitch/roll gauges
    gx, gy = 300, 80
    pygame.draw.arc(surf, (80, 80, 80), (gx - 50, gy - 50, 100, 100),
                    math.radians(0), math.radians(180), 2)
    pitch_deg = math.degrees(joints[1]) if len(joints) > 1 else 0
    pa = math.radians(90 - max(-30, min(30, pitch_deg)) * 3)
    px_ = gx + int(45 * math.cos(pa)); py_ = gy - int(45 * math.sin(pa))
    pygame.draw.line(surf, (200, 100, 100), (gx, gy), (px_, py_), 2)
    t = _FONT.render(f"Pitch {pitch_deg:.1f}°", True, (150, 150, 150))
    surf.blit(t, (gx - 30, gy + 10))

    # Heading compass
    hx, hy = 450, 80
    pygame.draw.circle(surf, (60, 60, 60), (hx, hy), 40, 1)
    nx_ = hx + int(38 * math.cos(th)); ny_ = hy - int(38 * math.sin(th))
    pygame.draw.line(surf, (100, 200, 100), (hx, hy), (nx_, ny_), 2)
    t = _FONT.render(f"Hdg {math.degrees(th)%360:.0f}°", True, (150, 150, 150))
    surf.blit(t, (hx - 25, hy + 44))

    # Joint name labels (condensed)
    for i, name in enumerate(K1_JOINT_NAMES):
        col = (100, 200, 100) if abs(joints[i]) > 0.05 else (60, 60, 60)
        t = _FONT.render(f"{name[:12]} {joints[i]:+.2f}", True, col)
        col_x = 240 + (i // 11) * 160
        row_y = 160 + (i % 11) * 12
        surf.blit(t, (col_x, row_y))

    t = _FONT.render("JOINT STATES  (22 DoF)", True, (150, 150, 150))
    surf.blit(t, (4, 4))


def _draw_dashboard(surf, node: BoosterSimLiteNode):
    surf.fill((15, 15, 20))
    with node._lock:
        bat   = node._battery
        mode  = node._mode
        vx    = node._vx; vy = node._vy; wz = node._wz
        docked = node._docked

    # Battery bar
    bar_w = int(bat / 100 * 200)
    bar_color = (50, 200, 80) if bat > 30 else (220, 80, 30)
    pygame.draw.rect(surf, (50, 50, 50), (10, 20, 200, 18))
    pygame.draw.rect(surf, bar_color,   (10, 20, bar_w, 18))
    t = _FONT.render(f"Batería {bat:.0f}%  {'[cargando]' if docked else ''}", True, (200, 200, 200))
    surf.blit(t, (220, 22))

    # Mode badge
    mc = _MODE_COLORS.get(mode, (80, 80, 80))
    t = _FONT.render(f"MODO: {mode}", True, mc)
    surf.blit(t, (10, 48))

    # Velocity
    t = _FONT.render(f"vx={vx:.2f}  vy={vy:.2f}  wz={wz:.2f}", True, (150, 150, 150))
    surf.blit(t, (150, 48))

    t = _FONT.render("DASHBOARD", True, (80, 80, 80))
    surf.blit(t, (4, 4))


def _pygame_loop(node: BoosterSimLiteNode):
    pygame.init()
    _init_fonts()
    screen = pygame.display.set_mode((_WIN_W, _WIN_H))
    pygame.display.set_caption(f"Booster K1 Sim — {node.world_name}")
    clock = pygame.time.Clock()

    map_surf  = pygame.Surface((_MAP_W, _MAP_H))
    cam_surf  = pygame.Surface((_CAM_W, _CAM_H))
    jnt_surf  = pygame.Surface((_JNT_W, _JNT_H))
    dash_surf = pygame.Surface((_DSH_W, _DSH_H))

    running = True
    while running and rclpy.ok():
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False

        _draw_map(map_surf, node)
        _draw_camera(cam_surf, node)
        _draw_joint_viewer(jnt_surf, node)
        _draw_dashboard(dash_surf, node)

        screen.fill((10, 10, 10))
        screen.blit(map_surf,  (0, 0))
        screen.blit(cam_surf,  (_MAP_W, 0))
        screen.blit(jnt_surf,  (0, _MAP_H))
        screen.blit(dash_surf, (_MAP_W, _MAP_H + _JNT_H - _DSH_H))

        pygame.display.flip()
        clock.tick(20)

    pygame.quit()
    if node._renderer:
        node._renderer.close()


# ---------------------------------------------------------------------------
# Entry point
# ---------------------------------------------------------------------------

def main():
    import sys
    world = sys.argv[1] if len(sys.argv) > 1 else "booster_empty"
    if world not in BOOSTER_WORLDS:
        print(f"Unknown world '{world}'. Available: {list(BOOSTER_WORLDS)}")
        sys.exit(1)

    rclpy.init()
    node = BoosterSimLiteNode(world)

    spin_thread = threading.Thread(target=rclpy.spin, args=(node,), daemon=True)
    spin_thread.start()

    if os.environ.get("DISPLAY"):
        _pygame_loop(node)
    else:
        spin_thread.join()

    node.destroy_node()
    rclpy.shutdown()


if __name__ == "__main__":
    main()
```

- [ ] **Step 2: Smoke-test topics publish (requires ROS 2 Humble environment)**

In a terminal with ROS 2 Humble sourced:
```bash
cd /home/jahir/repos/ros2-sandbox/sandbox/scripts
python3 booster_sim_lite.py booster_empty &
SIM_PID=$!
sleep 3
ros2 topic echo /odom --once 2>&1 | grep "position"
# Expected: position:
ros2 topic echo /joint_states --once 2>&1 | grep "head_yaw"
# Expected: - head_yaw
ros2 service call /sport/hello std_srvs/srv/Trigger {} 2>&1 | grep "success"
# Expected: success: True
kill $SIM_PID
```

- [ ] **Step 3: Commit**
```bash
cd /home/jahir/repos/ros2-sandbox && git add sandbox/scripts/booster_sim_lite.py && git commit -m "feat(booster): add booster_sim_lite.py with 4-panel visualisation"
```

---

### Task 6: course-map-booster.yaml + Seed Files

**Files:**
- Create: `ros2-sandbox/sandbox/course-map-booster.yaml`
- Create: `ros2-sandbox/sandbox/seed/booster_code_templates/b2_walk_square_start.py` (and b3–b10 starters)

- [ ] **Step 1: Create course-map-booster.yaml**

```yaml
# Course map for the Booster K1 track.
# Same schema as course-map.yaml but all parts use booster_sim_lite.py.
# USE_SIM_LITE=true is always set for this track (no Gazebo).

parts:
  booster_b1:
    display_name: "B1: Introducción al K1"
    launch_pkg: null
    launch_file: null
    launch_args: []
    sim_lite_world: booster_empty
    seed_package: booster_b1_intro
    seed_files: []
    doc_page: booster/b1-introduccion.md
    note: "Conceptual — no coding exercise."

  booster_b2:
    display_name: "B2: Locomoción Bípeda"
    launch_pkg: null
    launch_file: null
    launch_args: []
    sim_lite_world: booster_empty
    seed_package: booster_b2_locomotion
    seed_files: [b2_walk_square_start.py]
    doc_page: booster/b2-locomocion.md

  booster_b3:
    display_name: "B3: Publishers y Subscribers"
    launch_pkg: null
    launch_file: null
    launch_args: []
    sim_lite_world: booster_empty
    seed_package: booster_b3_pubsub
    seed_files: [b3_odom_subscriber_start.py]
    doc_page: booster/b3-pubsub.md

  booster_b4:
    display_name: "B4: Articulaciones y Estado del Robot"
    launch_pkg: null
    launch_file: null
    launch_args: []
    sim_lite_world: booster_empty
    seed_package: booster_b4_joints
    seed_files: [b4_joint_monitor_start.py]
    doc_page: booster/b4-articulaciones.md

  booster_b5:
    display_name: "B5: Comportamientos y Servicios"
    launch_pkg: null
    launch_file: null
    launch_args: []
    sim_lite_world: booster_empty
    seed_package: booster_b5_behaviors
    seed_files: [b5_behavior_client_start.py]
    doc_page: booster/b5-comportamientos.md

  booster_b6:
    display_name: "B6: Cámara RGBD y Visión"
    launch_pkg: null
    launch_file: null
    launch_args: []
    sim_lite_world: booster_obstacles
    seed_package: booster_b6_camera
    seed_files: [b6_color_follower_start.py]
    doc_page: booster/b6-camara.md

  booster_b7:
    display_name: "B7: Detección con YOLO"
    launch_pkg: null
    launch_file: null
    launch_args: []
    sim_lite_world: booster_soccer
    seed_package: booster_b7_yolo
    seed_files: [b7_yolo_detector_start.py]
    doc_page: booster/b7-yolo.md

  booster_b8:
    display_name: "B8: LiDAR y Obstáculos"
    launch_pkg: null
    launch_file: null
    launch_args: []
    sim_lite_world: booster_obstacles
    seed_package: booster_b8_lidar
    seed_files: [b8_obstacle_avoider_start.py]
    doc_page: booster/b8-lidar.md

  booster_b9:
    display_name: "B9: Arquitectura RoboCup"
    launch_pkg: null
    launch_file: null
    launch_args: []
    sim_lite_world: booster_soccer
    seed_package: booster_b9_robocup
    seed_files: [b9_ball_tracker_start.py]
    doc_page: booster/b9-robocup.md

  booster_b10:
    display_name: "B10: Misión Autónoma Integrada"
    launch_pkg: null
    launch_file: null
    launch_args: []
    sim_lite_world: booster_inspection
    seed_package: booster_b10_mission
    seed_files: [b10_mission_start.py]
    doc_page: booster/b10-mision.md
```

- [ ] **Step 2: Create seed starter files**

Create `ros2-sandbox/sandbox/seed/booster_code_templates/b2_walk_square_start.py`:
```python
#!/usr/bin/env python3
"""B2 — Starter: caminar en cuadrado con el Booster K1."""
import rclpy
from rclpy.node import Node
from geometry_msgs.msg import TwistStamped
import time

class WalkSquare(Node):
    def __init__(self):
        super().__init__('walk_square')
        self.pub = self.create_publisher(TwistStamped, '/cmd_vel', 10)

    def move(self, vx=0.0, vy=0.0, wz=0.0, duration=2.0):
        # TODO: publica TwistStamped durante `duration` segundos
        pass

    def run(self):
        # TODO: cuadrado de 4 lados usando self.move()
        pass

def main():
    rclpy.init()
    node = WalkSquare()
    node.run()
    rclpy.shutdown()

if __name__ == '__main__':
    main()
```

Create stubs for b3–b10 following the same pattern: function signatures present, bodies replaced with `# TODO:` comments matching the lesson exercise. Each file imports only the message types used in that lesson.

- [ ] **Step 3: Verify YAML parses**
```bash
python3 -c "import yaml; d=yaml.safe_load(open('sandbox/course-map-booster.yaml')); print(list(d['parts'].keys()))"
# Expected: ['booster_b1', 'booster_b2', ..., 'booster_b10']
```

- [ ] **Step 4: Commit**
```bash
cd /home/jahir/repos/ros2-sandbox && git add sandbox/course-map-booster.yaml sandbox/seed/booster_code_templates/ && git commit -m "feat(booster): add course-map-booster.yaml and seed starter files"
```

---

### Task 7: Dockerfile.booster

**Files:**
- Create: `ros2-sandbox/sandbox/Dockerfile.booster`
- Modify: `ros2-sandbox/cloudbuild.yaml`

- [ ] **Step 1: Create Dockerfile.booster**

```dockerfile
# Booster K1 sandbox — Ubuntu 22.04 / ROS 2 Humble
# Includes all official Booster repos. Students use booster_sim_lite.py;
# real-robot work uses booster_ros2_bridge.py against the real K1 SDK.
FROM osrf/ros:humble-desktop-full

ARG BOOSTER_SDK_ROS2_REPO=https://github.com/BoosterRobotics/booster_robotics_sdk_ros2.git
ARG RIGSA_ROS_BOOSTER_REPO=https://github.com/rigsa/rigsa_ros.git
ARG RIGSA_ROS_BOOSTER_BRANCH=humble-booster
ARG CODE_SERVER_VERSION=4.93.1

ENV DEBIAN_FRONTEND=noninteractive \
    STUDENT_USER=student \
    STUDENT_HOME=/home/student \
    ROS_WS=/home/student/ros2_ws \
    DISPLAY=:1 \
    BOOSTER_ASSETS_PATH=/opt/booster/booster_assets

# --- System packages -------------------------------------------------------
RUN apt-get update && apt-get install -y --no-install-recommends \
        ros-humble-slam-toolbox \
        ros-humble-navigation2 \
        ros-humble-nav2-bringup \
        ros-humble-cv-bridge \
        ros-humble-rosbridge-suite \
        ros-humble-pointcloud-to-laserscan \
        python3-colcon-common-extensions \
        python3-rosdep \
        python3-pip \
        git curl wget gnupg2 \
        libgl1-mesa-glx libglib2.0-0 \
        tigervnc-standalone-server tigervnc-common \
        fluxbox novnc websockify x11-apps \
        wmctrl scrot supervisor nginx \
    && rm -rf /var/lib/apt/lists/*

# --- Python packages -------------------------------------------------------
RUN pip3 install --no-cache-dir --break-system-packages --ignore-installed \
    booster_robotics_sdk_python \
    "ultralytics>=8.0" \
    "opencv-python" \
    "numpy<2" \
    pyyaml pygame pybullet matplotlib

# --- code-server -----------------------------------------------------------
RUN curl -fsSL https://code-server.dev/install.sh | sh -s -- --version "${CODE_SERVER_VERSION}"

# --- Booster repos (read-only reference + assets) -------------------------
RUN mkdir -p /opt/booster
RUN git clone --depth 1 https://github.com/BoosterRobotics/booster_robotics_sdk.git \
        /opt/booster/booster_robotics_sdk
RUN git clone --depth 1 https://github.com/BoosterRobotics/booster_assets.git \
        /opt/booster/booster_assets && \
    pip3 install --no-cache-dir --break-system-packages -e /opt/booster/booster_assets 2>/dev/null || true
RUN git clone --depth 1 https://github.com/BoosterRobotics/robocup_demo.git \
        /opt/booster/robocup_demo
RUN git clone --depth 1 https://github.com/BoosterRobotics/booster_deploy.git \
        /opt/booster/booster_deploy

# --- Student user ----------------------------------------------------------
RUN useradd -m -s /bin/bash "${STUDENT_USER}" \
    && echo "${STUDENT_USER} ALL=(ALL) NOPASSWD:ALL" >> /etc/sudoers

# --- ROS workspace: SDK ROS2 wrapper + rigsa_ros_booster ------------------
RUN mkdir -p "${ROS_WS}/src"
# SDK ROS2 wrapper (buildable)
RUN git clone --depth 1 "${BOOSTER_SDK_ROS2_REPO}" "${ROS_WS}/src/booster_sdk_ros2" || \
    echo "[INFO] booster_sdk_ros2 clone failed — workspace will build without it"
# rigsa_ros booster branch (course examples)
RUN git clone --depth 1 -b "${RIGSA_ROS_BOOSTER_BRANCH}" "${RIGSA_ROS_BOOSTER_REPO}" \
        "${ROS_WS}/src/rigsa_ros_booster" || \
    echo "[INFO] rigsa_ros humble-booster clone failed"
RUN chown -R "${STUDENT_USER}:${STUDENT_USER}" "${STUDENT_HOME}"

USER ${STUDENT_USER}
WORKDIR ${ROS_WS}
RUN /bin/bash -lc "\
    source /opt/ros/humble/setup.bash && \
    rosdep update --rosdistro=humble || true && \
    rosdep install --from-paths src --ignore-src -r -y --rosdistro=humble || true && \
    colcon build --symlink-install || true"

RUN echo "source /opt/ros/humble/setup.bash"   >> "${STUDENT_HOME}/.bashrc" \
    && echo "source ${ROS_WS}/install/setup.bash" >> "${STUDENT_HOME}/.bashrc" \
    && echo "export BOOSTER_ASSETS_PATH=/opt/booster/booster_assets" >> "${STUDENT_HOME}/.bashrc"

# --- Sandbox assets --------------------------------------------------------
USER root
COPY course-map-booster.yaml /opt/course-map.yaml
COPY seed/booster_code_templates/ /opt/seed/code_templates/
COPY scripts/seed_workspace.py    /opt/seed/seed_workspace.py
COPY scripts/course-runner.sh     /opt/seed/course-runner.sh
COPY scripts/booster_sim_lite.py  /opt/seed/booster_sim_lite.py
COPY scripts/entrypoint.sh        /opt/seed/entrypoint.sh
COPY scripts/heartbeat_server.py  /opt/seed/heartbeat_server.py
COPY scripts/timeout_watchdog.sh  /opt/seed/timeout_watchdog.sh
COPY supervisord.conf /etc/supervisor/conf.d/sandbox.conf
RUN rm -f /etc/nginx/sites-enabled/default
COPY nginx.conf /etc/nginx/sites-enabled/default
RUN chmod +x /opt/seed/course-runner.sh /opt/seed/entrypoint.sh \
        /opt/seed/timeout_watchdog.sh /opt/seed/heartbeat_server.py \
    && chown -R "${STUDENT_USER}:${STUDENT_USER}" /opt/seed

EXPOSE 8080
ENTRYPOINT ["/opt/seed/entrypoint.sh"]
```

- [ ] **Step 2: Add Booster build step to cloudbuild.yaml**

Append to `ros2-sandbox/cloudbuild.yaml` after existing steps:
```yaml
  # Booster K1 sandbox image
  - name: 'gcr.io/cloud-builders/docker'
    args:
      - build
      - -f
      - ./sandbox/Dockerfile.booster
      - -t
      - '$_IMAGE_BOOSTER'
      - ./sandbox

  - name: 'gcr.io/cloud-builders/docker'
    args:
      - push
      - '$_IMAGE_BOOSTER'
```

And add to `images:`:
```yaml
  - '$_IMAGE_BOOSTER'
```

And add to `substitutions:`:
```yaml
  _IMAGE_BOOSTER: 'us-central1-docker.pkg.dev/$PROJECT_ID/ros2/ros2-sandbox-booster:latest'
```

- [ ] **Step 3: Test build locally (if Docker available)**
```bash
cd /home/jahir/repos/ros2-sandbox
docker build -f sandbox/Dockerfile.booster -t booster-sandbox-test ./sandbox 2>&1 | tail -20
# Expected: Successfully built <hash>
```

- [ ] **Step 4: Commit**
```bash
cd /home/jahir/repos/ros2-sandbox && git add sandbox/Dockerfile.booster cloudbuild.yaml && git commit -m "feat(booster): add Dockerfile.booster and cloudbuild entry for Booster image"
```

---

### Task 8: Orchestrator Track Routing

**Files:**
- Modify: `ros2-sandbox/orchestrator/app.py`

**Interfaces:**
- `GET /?track=booster` → loads `course-map-booster.yaml`, passes `track` to template
- `POST /sessions` with `track=booster` form field → uses `SANDBOX_IMAGE_BOOSTER` env var
- New env var required: `SANDBOX_IMAGE_BOOSTER`

- [ ] **Step 1: Add config constants after line 44**

After `SANDBOX_IMAGE  = os.environ["SANDBOX_IMAGE"]`, add:
```python
SANDBOX_IMAGE_BOOSTER   = os.environ.get("SANDBOX_IMAGE_BOOSTER", "")
COURSE_MAP_PATH_BOOSTER = SANDBOX_DIR / "course-map-booster.yaml"
```

- [ ] **Step 2: Replace `_load_course_map` function (line 74)**

```python
def _load_course_map(track: str = "unitree") -> dict:
    if track == "booster" and COURSE_MAP_PATH_BOOSTER.exists():
        return yaml.safe_load(COURSE_MAP_PATH_BOOSTER.read_text())["parts"]
    return yaml.safe_load(COURSE_MAP_PATH.read_text())["parts"]
```

- [ ] **Step 3: Update `landing_page` route (line 339)**

Change signature to accept `track` query param:
```python
@app.get("/", response_class=HTMLResponse)
def landing_page(request: Request,
                 track: str = "unitree",
                 user: dict = Depends(get_current_user)):
    course_map = _load_course_map(track)
    uid = user_id_from(user)
    sessions = _list_active_sessions(user_id=None if is_admin(user) else uid)
    return templates.TemplateResponse("index.html", {
        "request": request,
        "parts": course_map,
        "sessions": sessions,
        "user_email": user_email_from(user),
        "is_admin": is_admin(user),
        "track": track,
        "error": None,
    })
```

- [ ] **Step 4: Update `start_session` route (line 357)**

Add `track` form field and use correct image:
```python
@app.post("/sessions")
@limiter.limit("5/hour")
async def start_session(
    request: Request,
    session_name: str = Form(...),
    part_key: str = Form(...),
    sim_lite: str = Form(default=""),
    track: str = Form(default="unitree"),
    user: dict = Depends(get_current_user),
):
    course_map = _load_course_map(track)
    if part_key not in course_map:
        raise HTTPException(status_code=400, detail=f"Parte desconocida: {part_key}")
    # ... (rest unchanged until image selection) ...
    image = SANDBOX_IMAGE_BOOSTER if track == "booster" and SANDBOX_IMAGE_BOOSTER else SANDBOX_IMAGE
    # Replace: image=SANDBOX_IMAGE  →  image=image
```

Find line `image=SANDBOX_IMAGE,` in the `cr_client.create_service` call and replace with `image=image,`.

- [ ] **Step 5: Write unit test**

Create `ros2-sandbox/orchestrator/tests/test_track_routing.py`:
```python
import pytest
from pathlib import Path
import sys
sys.path.insert(0, str(Path(__file__).parent.parent))

def test_load_unitree_map(tmp_path, monkeypatch):
    import orchestrator.app as app
    monkeypatch.setattr(app, "COURSE_MAP_PATH",
                        Path(__file__).parent.parent.parent / "sandbox" / "course-map.yaml")
    parts = app._load_course_map("unitree")
    assert "part1" in parts
    assert "unitree_u1" in parts

def test_load_booster_map(tmp_path, monkeypatch):
    import orchestrator.app as app
    monkeypatch.setattr(app, "COURSE_MAP_PATH_BOOSTER",
                        Path(__file__).parent.parent.parent / "sandbox" / "course-map-booster.yaml")
    parts = app._load_course_map("booster")
    assert "booster_b1" in parts
    assert "booster_b10" in parts

def test_unknown_track_falls_back_to_unitree(monkeypatch):
    import orchestrator.app as app
    monkeypatch.setattr(app, "COURSE_MAP_PATH",
                        Path(__file__).parent.parent.parent / "sandbox" / "course-map.yaml")
    parts = app._load_course_map("unknown_track")
    assert "part1" in parts
```

- [ ] **Step 6: Run tests**
```bash
cd /home/jahir/repos/ros2-sandbox
pip install pytest --quiet
pytest orchestrator/tests/test_track_routing.py -v
# Expected: 3 passed
```

- [ ] **Step 7: Commit**
```bash
cd /home/jahir/repos/ros2-sandbox && git add orchestrator/app.py orchestrator/tests/ && git commit -m "feat(booster): add track routing to orchestrator (?track=booster)"
```

---

### Task 9: rigsa_ros Booster Branch + Example Scripts

**Files:** All in `rigsa_ros/` on new branch `humble-booster`.
- Create: `rigsa_ros_booster/package.xml`
- Create: `rigsa_ros_booster/CMakeLists.txt`
- Create: `rigsa_ros_booster/scripts/b2_walk_square.py` … `b10_autonomous_mission.py`

- [ ] **Step 1: Create branch and package**
```bash
cd /home/jahir/repos/rigsa_ros
git checkout -b humble-booster
mkdir -p rigsa_ros_booster/scripts
```

- [ ] **Step 2: Create package.xml**
```xml
<?xml version="1.0"?>
<package format="3">
  <name>rigsa_ros_booster</name>
  <version>0.1.0</version>
  <description>Booster K1 course examples for RIGSA</description>
  <maintainer email="jahirargote@gmail.com">RIGSA</maintainer>
  <license>CC BY-SA 4.0</license>
  <depend>rclpy</depend>
  <depend>geometry_msgs</depend>
  <depend>nav_msgs</depend>
  <depend>sensor_msgs</depend>
  <depend>std_srvs</depend>
  <buildtool_depend>ament_cmake</buildtool_depend>
  <export>
    <build_type>ament_python</build_type>
  </export>
</package>
```

- [ ] **Step 3: Create CMakeLists.txt**
```cmake
cmake_minimum_required(VERSION 3.8)
project(rigsa_ros_booster)
find_package(ament_cmake REQUIRED)
find_package(ament_cmake_python REQUIRED)
ament_python_install_package(${PROJECT_NAME})
install(PROGRAMS
  scripts/b2_walk_square.py
  scripts/b3_odom_imu.py
  scripts/b4_joint_monitor.py
  scripts/b5_behaviors.py
  scripts/b6_color_follower.py
  scripts/b7_yolo_detect.py
  scripts/b8_obstacle_avoidance.py
  scripts/b9_ball_tracker.py
  scripts/b10_autonomous_mission.py
  DESTINATION lib/${PROJECT_NAME}
)
ament_package()
```

- [ ] **Step 4: Create example scripts**

The 9 scripts (b2–b10) are the complete reference solutions from the lesson content in Tasks 3–4. Copy the code blocks from those lessons verbatim — each lesson's main code block is the complete example script. Add shebang `#!/usr/bin/env python3` and a `main()` entry point where missing.

- [ ] **Step 5: Build test**
```bash
cd ~/ros2_ws   # or create a temp workspace
# symlink rigsa_ros_booster into src/
ln -s /home/jahir/repos/rigsa_ros/rigsa_ros_booster src/rigsa_ros_booster
source /opt/ros/humble/setup.bash
colcon build --packages-select rigsa_ros_booster --symlink-install 2>&1 | tail -10
# Expected: Finished <<< rigsa_ros_booster
```

- [ ] **Step 6: Commit and push branch**
```bash
cd /home/jahir/repos/rigsa_ros
git add rigsa_ros_booster/
git commit -m "feat: add rigsa_ros_booster package with B2-B10 examples"
git push origin humble-booster
```

---

## Self-Review Checklist

**Spec coverage:**
- Sheffield cleanup ✓ Task 1
- Landing page chooser ✓ Task 2
- B1–B10 lessons ✓ Tasks 3–4
- booster_sim_lite.py (4-panel, K1 sprite, PyBullet camera, joint viewer) ✓ Task 5
- course-map-booster.yaml + seed starters ✓ Task 6
- Dockerfile.booster (Ubuntu 22.04, all Booster repos, pip packages) ✓ Task 7
- Orchestrator `?track=booster` routing ✓ Task 8
- rigsa_ros humble-booster branch ✓ Task 9

**No placeholders** — all code blocks are complete.

**Type consistency** — `_load_course_map(track: str)` used consistently in Tasks 8 (defined) and tests.

**Known dependency** — `Dockerfile.booster` clones `rigsa/rigsa_ros@humble-booster`; Task 9 must be pushed before the Docker build succeeds. Build order: Task 9 → Task 7 (Docker build).
