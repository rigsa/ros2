# S3: Acceso al PC2 del Robot — SSH, Red y Configuración del Sistema

## Objetivos

- Conectar por SSH al PC2 del B2 desde la red del laboratorio o remotamente
- Configurar la interfaz de red para comunicación DDS con el robot
- Navegar el sistema de archivos del PC2 y localizar servicios SDK2
- Identificar procesos del sistema que no deben interrumpirse

---

## Arquitectura de red del B2

```
                    Internet
                       │
                 ┌─────▼──────┐
                 │  Gateway   │   Lab PC / Jetson (Ubuntu 24.04)
                 │ Cloudflare │   ├── unitree_ros2_bridge (ROS 2 ↔ SDK2)
                 │  Tunnel    │   ├── ttyd (terminal web HTTPS)
                 └─────┬──────┘   └── cloudflared (túnel)
                       │ HTTPS/WebSocket
            ┌──────────▼──────────┐
            │  Red del laboratorio │
            │  192.168.123.0/24    │
            └──┬──────────────┬───┘
               │              │
        ┌──────▼──────┐  ┌────▼──────┐
        │  B2 PC2     │  │ Tu laptop │
        │ 192.168.123.18│  │ (DHCP)  │
        └─────────────┘  └──────────┘
```

El B2 asigna:
- `192.168.123.18` — PC2 (Ubuntu, SSH disponible)
- `192.168.123.161` — MCU (no accesible directamente)
- Gateway: `192.168.123.1`

---

## Conexión SSH al PC2

### Desde el laboratorio (red local)

```bash
# Contraseña por defecto: 123
ssh unitree@192.168.123.18

# Primera vez: aceptar fingerprint
# Cambiar contraseña inmediatamente después:
passwd
```

### Desde el sandbox remoto (via terminal del laboratorio)

!!! abstract "Sesión de robot requerida"
    El botón **"Abrir Terminal del Robot"** en tu sesión activa (cuando tienes un slot reservado) abre una terminal web en el gateway del laboratorio. Desde ahí:

    ```bash
    # Desde el gateway del lab → al PC2 del B2
    ssh unitree@192.168.123.18
    ```

### Configurar SSH sin contraseña (solo para admin del lab)

```bash
# En tu laptop / gateway
ssh-keygen -t ed25519 -C "lab-gateway"
ssh-copy-id unitree@192.168.123.18
```

---

## Estructura del sistema de archivos del PC2

```
/home/unitree/
├── unitree_ros2/           # Workspace ROS 2 con el bridge oficial
│   ├── src/
│   │   └── unitree_ros2/  # Nodos: go2_robot_state_publisher, etc.
│   └── install/
├── unitree_sdk2/           # SDK2 C++ (headers + libs)
│   └── include/unitree/
├── Unitree/                # Scripts de configuración de fábrica
│   └── auto_run/          # Scripts de inicio automático
└── .bashrc                 # ROS sourcing + env vars del robot
```

---

## Procesos críticos del PC2

Al conectar, identifica los procesos que NO debes detener:

```bash
# Ver procesos Unitree
ps aux | grep -E "unitree|dds|sport|loco"
```

| Proceso                         | Rol                              | ¿Detener?   |
|---------------------------------|----------------------------------|-------------|
| `sport_mode`                    | Controlador de locomoción        | ❌ Nunca    |
| `dds_daemon`                    | Broker DDS local                 | ❌ Nunca    |
| `unitree_legged_sdk2`           | Bridge bajo nivel MCU ↔ PC2     | ❌ Nunca    |
| `ros2_unitree_bridge`           | Bridge ROS 2 (si está activo)    | ✅ Se puede |
| Scripts de usuario (`python3`)  | Tu código                        | ✅ Siempre  |

---

## Configuración de red para DDS

### Opción A: DDS en red local (in-situ, más sencillo)

```bash
# En tu laptop o en el PC2 del B2, definir la interfaz de red
export CYCLONEDDS_URI='<CycloneDDS>
  <Domain>
    <General>
      <NetworkInterfaceAddress>eth0</NetworkInterfaceAddress>
    </General>
  </Domain>
</CycloneDDS>'
```

Reemplaza `eth0` con tu interfaz real (`ip a` para ver la lista).

### Opción B: DDS vía unicast (acceso remoto, sandbox Cloud Run)

```bash
# El sandbox recibe esta config cuando tu slot de robot está activo
export CYCLONEDDS_URI='<CycloneDDS>
  <Domain>
    <Discovery>
      <Peers>
        <Peer Address="192.168.123.18"/>
      </Peers>
    </Discovery>
    <General>
      <AllowMulticast>false</AllowMulticast>
    </General>
  </Domain>
</CycloneDDS>'
```

### Verificar conectividad SDK2

```python title="s3_test_conexion.py"
#!/usr/bin/env python3
"""Verifica que el sandbox puede recibir datos del robot por DDS."""
import time

# ── Simulación ──────────────────────────────────────────
from sdk2_bridge_sim import SDK2Bridge
bridge = SDK2Bridge()

# ── Robot real: descomenta estas líneas ─────────────────
# from unitree_sdk2py.core.channel import ChannelFactory
# from unitree_sdk2py.b2.sport_client import SportClient
# ChannelFactory.Instance().Init(0, "eth0")
# bridge = SportClient()
# bridge.Init()

state = bridge.get_sport_state()
print(f"✓ Conectado — Posición: ({state.position[0]:.2f}, {state.position[1]:.2f})")
print(f"  Batería: {bridge.get_battery_pct()}%")
```

---

## WiFi del B2: configuración avanzada

El PC2 del B2 puede conectarse a una red WiFi externa además de crear su propia red:

```bash
# En el PC2 del B2
nmcli device wifi list
nmcli device wifi connect "NombreRed" password "contraseña"

# Verificar IP asignada
ip a show wlan0
```

!!! warning "No desconectes la red del B2 durante operación"
    Si el PC2 pierde conectividad con el MCU, el robot puede caer en estado de seguridad. Siempre configura la red con el robot en posición baja (sit) o con soporte físico.

---

## Ejercicios

### Ejercicio 1 — Explorar el PC2 (solo con acceso real)
Conectar al PC2 vía SSH (desde el gateway del lab). Listar procesos activos y encontrar el PID del sport_mode. Ejecutar `ros2 topic list` en el PC2 y comparar con lo que ves desde tu sandbox.

### Ejercicio 2 — Test de conectividad DDS
Usa `s3_test_conexion.py` en el sandbox. Primero con `sdk2_bridge_sim`. Cuando tengas un slot de robot real, cambia al cliente real y verifica que recibes datos del B2 físico.

### Ejercicio 3 — Configurar CYCLONEDDS_URI
Escribe un script Bash que configure automáticamente `CYCLONEDDS_URI` basándose en si la variable `ROBOT_GATEWAY_IP` está definida o no (simulación vs hardware).

### Ejercicio 4 — Explorar estructura de archivos
Describe la diferencia entre `/home/unitree/unitree_sdk2` y `/home/unitree/unitree_ros2`. ¿Cuál es la fuente de verdad del estado del robot?

---

## Pasa al robot real

!!! info "Acceso desde el sandbox"
    1. Reserva un slot en la **Cola de Robot** (panel 🤖 en tu sesión del sandbox)
    2. Cuando tu slot sea activo, el panel "Robot Real" aparecerá en tu sesión
    3. Haz clic en **"Abrir Terminal del Robot"** — esto abre un `ttyd` en el gateway del lab
    4. Desde ahí ejecuta: `ssh unitree@192.168.123.18`
    5. Tu `CYCLONEDDS_URI` ya estará configurado en el sandbox para hablar con el PC2

---

## Referencias

- [B2 Networking Guide — Unitree Support](https://support.unitree.com/home/en/developer/about_B2)
- [CycloneDDS configuration — cyclonedds.io](https://cyclonedds.io/docs/cyclonedds/latest/config/config_file_reference.html)
- Configuración de Gateway del Laboratorio — disponible en el repositorio `ros2-sandbox` (`lab-gateway-setup.md`)
