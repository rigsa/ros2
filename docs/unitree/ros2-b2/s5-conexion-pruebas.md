# S5: Conexión y Pruebas — Validación de Red, Integration Tests y CI

## Objetivos

- Validar la conectividad DDS entre el sandbox y el PC2 del B2
- Escribir integration tests para código que interactúa con hardware
- Configurar un pipeline básico de CI para el paquete de robot
- Diagnosticar y resolver los problemas de red más comunes

---

## Checklist de conectividad antes de operar el robot

Antes de enviar cualquier comando al B2 físico, ejecuta esta verificación sistemática:

```
1. ¿El CYCLONEDDS_URI apunta al PC2 del B2?
   export | grep CYCLONEDDS

2. ¿El PC2 está online?
   ping 192.168.123.18

3. ¿El bridge ROS 2 está activo?
   ros2 topic list (debe mostrar /odom, /scan, /joint_states)

4. ¿Los tópicos reciben datos?
   ros2 topic hz /odom  (debe ser ~50 Hz)
   ros2 topic hz /imu/data  (debe ser ~500 Hz)

5. ¿La batería es suficiente?
   ros2 topic echo /b2/battery --once  (debe ser > 40%)

6. ¿El robot está en posición segura (de pie)?
   ros2 topic echo /odom --once  (z debe ser ~0.5 m)
```

---

## Script de health check automatizado

```python title="s5_health_check.py"
#!/usr/bin/env python3
"""
Verifica el estado del robot antes de iniciar operación.
Imprime un informe y sale con código 0 (OK) o 1 (fallo).
"""
import sys, time
import rclpy
from rclpy.node import Node
from nav_msgs.msg import Odometry
from sensor_msgs.msg import Imu, LaserScan, BatteryState

MIN_BATTERY = 40.0  # %
MAX_ODOM_LAT = 0.5  # s — tolerancia de latencia máxima

class HealthCheck(Node):
    def __init__(self):
        super().__init__("health_check")
        self.results = {
            "odom":    None,
            "imu":     None,
            "lidar":   None,
            "battery": None,
        }
        self.create_subscription(Odometry,    "/odom",       self._odom_cb,    1)
        self.create_subscription(Imu,         "/imu/data",   self._imu_cb,     1)
        self.create_subscription(LaserScan,   "/scan",       self._scan_cb,    1)
        self.create_subscription(BatteryState,"/b2/battery", self._battery_cb, 1)

    def _odom_cb(self, msg: Odometry):
        self.results["odom"] = msg
    def _imu_cb(self, msg: Imu):
        self.results["imu"] = msg
    def _scan_cb(self, msg: LaserScan):
        self.results["lidar"] = msg
    def _battery_cb(self, msg: BatteryState):
        self.results["battery"] = msg

    def wait_for_data(self, timeout=5.0) -> bool:
        t0 = time.time()
        while time.time() - t0 < timeout:
            rclpy.spin_once(self, timeout_sec=0.2)
            if all(v is not None for v in self.results.values()):
                return True
        return False

    def report(self) -> tuple[bool, list[str]]:
        checks = []
        ok = True

        # Odometría
        if self.results["odom"] is not None:
            z = self.results["odom"].pose.pose.position.z
            checks.append(f"✓ Odometría  (z={z:.2f} m)")
        else:
            checks.append("✗ Odometría  — SIN DATOS"); ok = False

        # IMU
        if self.results["imu"] is not None:
            az = self.results["imu"].linear_acceleration.z
            checks.append(f"✓ IMU        (az={az:.2f} m/s²)")
        else:
            checks.append("✗ IMU        — SIN DATOS"); ok = False

        # LiDAR
        if self.results["lidar"] is not None:
            n = len([r for r in self.results["lidar"].ranges
                     if not (r != r or r == float("inf"))])
            checks.append(f"✓ LiDAR      ({n} rangos válidos)")
        else:
            checks.append("✗ LiDAR      — SIN DATOS"); ok = False

        # Batería
        if self.results["battery"] is not None:
            pct = self.results["battery"].percentage * 100
            icon = "✓" if pct >= MIN_BATTERY else "✗"
            checks.append(f"{icon} Batería     ({pct:.0f}%)")
            if pct < MIN_BATTERY:
                ok = False
        else:
            checks.append("— Batería     (sin datos — asumir OK)")

        return ok, checks


def main():
    rclpy.init()
    hc = HealthCheck()
    print("Verificando sistema del B2...")
    hc.wait_for_data(timeout=6.0)
    ok, checks = hc.report()
    print("\n" + "\n".join(checks))
    print(f"\n{'SISTEMA OK — listo para operar' if ok else 'SISTEMA NO LISTO — revisa los errores'}")
    hc.destroy_node()
    rclpy.shutdown()
    sys.exit(0 if ok else 1)

if __name__ == "__main__":
    main()
```

---

## Integration tests con pytest + rclpy

```python title="test/test_bridge_integration.py"
"""
Integration test: verifica que los tópicos del bridge devuelven datos válidos.
Ejecutar: pytest test/test_bridge_integration.py -v
"""
import math, time
import pytest
import rclpy
from rclpy.node import Node
from nav_msgs.msg import Odometry
from sensor_msgs.msg import LaserScan, Imu

@pytest.fixture(scope="module")
def rclpy_context():
    rclpy.init()
    yield
    rclpy.shutdown()

class DataCollector(Node):
    def __init__(self):
        super().__init__("test_collector")
        self.odom_msgs: list[Odometry] = []
        self.scan_msgs: list[LaserScan] = []
        self.imu_msgs:  list[Imu] = []
        self.create_subscription(Odometry,  "/odom",     lambda m: self.odom_msgs.append(m), 10)
        self.create_subscription(LaserScan, "/scan",     lambda m: self.scan_msgs.append(m), 10)
        self.create_subscription(Imu,       "/imu/data", lambda m: self.imu_msgs.append(m),  10)

    def spin_for(self, seconds: float):
        t0 = time.time()
        while time.time() - t0 < seconds:
            rclpy.spin_once(self, timeout_sec=0.1)

@pytest.fixture(scope="module")
def collector(rclpy_context):
    node = DataCollector()
    node.spin_for(3.0)  # Recoger 3 s de datos
    yield node
    node.destroy_node()

class TestBridgeIntegration:
    def test_odom_received(self, collector):
        assert len(collector.odom_msgs) > 0, "/odom no recibido"

    def test_odom_frequency(self, collector):
        """Odometría debe llegar a al menos 20 Hz."""
        if len(collector.odom_msgs) < 2:
            pytest.skip("Pocos mensajes")
        t0 = collector.odom_msgs[0].header.stamp.sec
        t1 = collector.odom_msgs[-1].header.stamp.sec
        dt = max(t1 - t0, 1e-9)
        hz = len(collector.odom_msgs) / dt
        assert hz >= 20.0, f"Frecuencia de /odom demasiado baja: {hz:.1f} Hz"

    def test_scan_has_valid_ranges(self, collector):
        assert len(collector.scan_msgs) > 0, "/scan no recibido"
        msg = collector.scan_msgs[-1]
        valid = [r for r in msg.ranges if not (math.isnan(r) or math.isinf(r))]
        assert len(valid) > 0, "Todos los rangos LiDAR son NaN/Inf"

    def test_imu_gravity(self, collector):
        """Acelerómetro Z debe estar cerca de 9.81 m/s² en reposo."""
        assert len(collector.imu_msgs) > 0, "/imu/data no recibido"
        az = collector.imu_msgs[-1].linear_acceleration.z
        assert 8.0 < az < 11.0, f"IMU az inesperado: {az:.2f} (esperado ~9.81)"
```

Ejecutar:

```bash
cd ~/ros2_ws
colcon test --packages-select tu_paquete
# O directamente:
pytest src/tu_paquete/test/test_bridge_integration.py -v
```

---

## Problemas de red más comunes

### Sin datos en el sandbox (CYCLONEDDS)

```bash
# 1. Verifica que CYCLONEDDS_URI está definido
echo $CYCLONEDDS_URI

# 2. Ping al PC2
ping 192.168.123.18 -c 3

# 3. Si el sandbox no puede hacer ping, el túnel Cloudflare puede estar caído
# Contacta al administrador del laboratorio

# 4. Forzar unicast (evita problemas de multicast en Cloud Run)
export CYCLONEDDS_URI='<CycloneDDS>
  <Domain>
    <Discovery>
      <Peers><Peer Address="192.168.123.18"/></Peers>
    </Discovery>
    <General><AllowMulticast>false</AllowMulticast></General>
  </Domain>
</CycloneDDS>'
```

### Tópicos presentes pero sin datos

```bash
# Verificar el bridge en el PC2
ssh unitree@192.168.123.18
ros2 topic hz /odom  # Debe ser ~50 Hz en el PC2 directamente
ps aux | grep b2_bringup

# Si el bridge no está activo:
cd ~/unitree_ros2
source install/setup.bash
ros2 launch unitree_ros2_bringup b2.launch.py
```

---

## Ejercicios

### Ejercicio 1 — Ejecutar el health check
Lanza el simulador y ejecuta `s5_health_check.py`. Verifica que todos los checks pasan. Detén uno de los tópicos (`ros2 topic pub /scan sensor_msgs/LaserScan --qos-durability transient_local` con datos vacíos) y observa qué falla.

### Ejercicio 2 — Test de frecuencia
Añade un test al archivo `test_bridge_integration.py` que verifique que `/imu/data` llega a al menos 100 Hz. Ejecuta `colcon test` y verifica que pasa.

### Ejercicio 3 — Script de diagnóstico de red
Escribe un script Bash `check_network.sh` que: (1) verifique `CYCLONEDDS_URI`, (2) haga ping al PC2, (3) ejecute `ros2 topic list` y verifique que `/odom` y `/scan` aparecen, (4) imprima PASS o FAIL para cada verificación.

### Ejercicio 4 — Test de latencia
Mide la latencia entre el timestamp en el `header` de `/odom` y el tiempo de recepción en el callback. Publica los resultados como `Float64` en `/b2/odom_latency`. ¿Cuál es la latencia promedio en el sim? ¿Esperarías una diferencia en hardware real?

### Ejercicio 5 — Mock del bridge para unit tests
Crea un fixture pytest que publique datos sintéticos en `/odom` y `/scan` usando un nodo ROS 2 en el mismo proceso. Úsalo para probar `s5_health_check.py` sin necesitar el simulador activo.

---

## Pasa al robot real

!!! success "Flujo de validación pre-operación"
    Con el slot de robot activo, ejecuta en orden:

    ```bash
    # 1. Verificar conectividad
    ping 192.168.123.18

    # 2. Health check automatizado
    python3 s5_health_check.py
    # Todos los checks deben ser ✓ antes de continuar

    # 3. Solo si health check pasa, iniciar operación
    ros2 lifecycle set /b2_driver configure
    ros2 lifecycle set /b2_driver activate
    ```

    Si el health check falla en hardware real, **no actives el driver**. Contacta al administrador del laboratorio.

---

## Referencias

- [pytest-ros2 — testing con ROS 2](https://github.com/ros2/ros2cli)
- [Colcon testing — docs.ros.org](https://docs.ros.org/en/jazzy/Tutorials/Intermediate/Testing/)
- [S3: Acceso al PC2 — configuración de red](../sdk2/s3-acceso-pc2.md)
- [S1: Arquitectura SDK2 + ROS 2](s1-arq-sdk2-ros2.md)
