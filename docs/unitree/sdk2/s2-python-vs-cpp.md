# S2: SDK2 en Python vs C++ — Comparativa Técnica

## Objetivos

- Comparar la API de SDK2 en Python (`unitree_sdk2_python`) y C++ (`unitree_sdk2`)
- Identificar escenarios donde cada lenguaje es la elección correcta
- Configurar el entorno Python en el sandbox y en el PC2 del B2
- Escribir el equivalente Python de un programa C++ de SDK2 típico

---

## Arquitectura de los bindings

Unitree publica dos SDKs oficiales que comparten el mismo protocolo DDS:

```
C++  unitree_sdk2        →  DDS nativo (CycloneDDS C++)
Python unitree_sdk2_python →  DDS via pybind11 / cyclone-dds-python
```

Ambos serializan los mismos tipos IDL (`unitree_go`, `unitree_hg`) para mensajes DDS. El protocolo en la red es idéntico; solo cambia la API del cliente.

---

## Tabla comparativa

| Criterio                     | C++ SDK2                        | Python SDK2                      |
|------------------------------|---------------------------------|----------------------------------|
| **Latencia de publicación**  | ~0.05 ms                        | ~0.2 ms (overhead GIL + pybind) |
| **Frecuencia máxima fiable** | 500 Hz (LowCmd a motores)       | ~200 Hz (práctico para scripts) |
| **Tiempo de arranque**       | Rápido (binario compilado)      | Lento en cold start (~1 s)      |
| **Iteración / prototipado**  | Lento (recompila cada cambio)   | Rápido (edit → run)             |
| **Acceso completo al SDK2**  | Sí (todas las features)         | Sí (parity ≥ SDK2 v1.2)        |
| **Integración con NumPy**    | No directa                      | Nativa                          |
| **Facilidad en el curso**    | Compleja (CMake, headers)       | Directa (pip install)           |

**Conclusión para el curso:** usaremos Python en todos los ejercicios del sandbox. C++ es relevante si necesitas control de motores a 500 Hz en producción (ej. controlador de locomoción personalizado).

---

## Setup del entorno Python

### En el sandbox (ya preinstalado)

```bash
# Verificar instalación
python3 -c "import unitree_sdk2py; print('OK')"

# Ver versión y módulos disponibles
python3 -c "import unitree_sdk2py; help(unitree_sdk2py)"
```

### En el PC2 del B2 / laptop del lab (instalación manual)

```bash
# Requisitos: Ubuntu 22.04/24.04, Python 3.10+
pip3 install unitree_sdk2_python

# Instalar CycloneDDS (dependency)
pip3 install cyclone-dds

# Configurar interfaz de red (reemplazar eth0 con tu interfaz)
export CYCLONEDDS_URI='<CycloneDDS><Domain><General><NetworkInterfaceAddress>eth0</NetworkInterfaceAddress></General></Domain></CycloneDDS>'
```

---

## API Python: estructura de módulos

```
unitree_sdk2py/
├── b2/
│   ├── loco_client.py      # LocoClient — locomotion (B2 específico)
│   └── sport_client.py     # SportClient — behaviors
├── h1/
│   ├── loco_client.py      # H1-2 locomotion
│   └── hand_client.py      # H1-2 dexterous hands
├── go2/
│   ├── loco_client.py      # Go2 locomotion
│   └── sport_client.py
├── core/
│   ├── channel.py          # ChannelPublisher / ChannelSubscriber
│   ├── channel_factory.py  # ChannelFactory.Instance()
│   └── sdk2_msg/          # Auto-generated IDL Python types
└── utils/
    └── crc.py             # CRC para LowCmd
```

---

## Equivalencia Python / C++

### C++ (referencia)
```cpp
#include "unitree/robot/b2/loco_client.hpp"

int main() {
    ChannelFactory::Instance()->Init(0, "eth0");
    LocoClient loco_client;
    loco_client.Init();
    loco_client.Move(0.5f, 0.0f, 0.0f);  // vx, vy, vyaw
    return 0;
}
```

### Python equivalente

```python title="sdk2_move_python.py"
#!/usr/bin/env python3
"""
Equivalente Python del ejemplo C++ de locomotion.
Sandbox: usa sdk2_bridge_sim en lugar del import real.
"""
import time

# ── Simulación (sandbox) ────────────────────────────
from sdk2_bridge_sim import LocoClientSim as LocoClient  # (1)!

# ── Robot real (PC2 o laptop en la red del B2) ──────
# from unitree_sdk2py.core.channel import ChannelFactory
# from unitree_sdk2py.b2.loco_client import LocoClient
# ChannelFactory.Instance().Init(0, "eth0")

def main():
    loco = LocoClient()
    loco.Init()

    print("Moviéndose hacia adelante...")
    loco.Move(0.5, 0.0, 0.0)  # vx=0.5 m/s, vy=0, vyaw=0  # (2)!
    time.sleep(2.0)

    print("Rotando...")
    loco.Move(0.0, 0.0, 0.5)  # vx=0, vy=0, vyaw=0.5 rad/s  # (3)!
    time.sleep(2.0)

    loco.StopMove()
    print("Detenido.")

if __name__ == '__main__':
    main()
```

1. Swapping this one line transitions the exact same code to real hardware
2. `LocoClient.Move(vx, vy, vyaw)` — holonomic, units: m/s and rad/s
3. B2 supports lateral movement (vy ≠ 0) unlike differential robots

---

## SDK2 de bajo nivel en Python: LowCmd / LowState

Para control directo de motores (sin pasar por LocoClient):

```python title="sdk2_lowlevel_python.py"
#!/usr/bin/env python3
"""Control de bajo nivel: leer LowState, publicar LowCmd."""
import time
from unitree_sdk2py.core.channel import ChannelFactory, ChannelSubscriber, ChannelPublisher
from unitree_sdk2py.idl.unitree_go.msg.dds_ import LowState_, LowCmd_
from unitree_sdk2py.utils.crc import CRC

# NOTA: Este ejercicio solo funciona en robot real.
# El LowCmd a 500 Hz puede causar movimientos bruscos — ¡usar con precaución!

latest_state: LowState_ = None

def state_handler(msg: LowState_):
    global latest_state
    latest_state = msg

def main():
    ChannelFactory.Instance().Init(0, "eth0")

    sub = ChannelSubscriber("rt/lowstate", LowState_)
    sub.Init(state_handler, 10)

    pub = ChannelPublisher("rt/lowcmd", LowCmd_)
    pub.Init()

    time.sleep(0.5)  # Esperar primer mensaje

    if latest_state:
        for i, motor in enumerate(latest_state.motor_state):
            print(f"Motor {i:02d}: q={motor.q:.3f} rad, dq={motor.dq:.3f} rad/s")
```

!!! warning "Solo en robot real"
    La publicación en `rt/lowcmd` afecta directamente a los motores. No existe en sim_lite. Úsalo solo durante la sesión de robot real con el B2 en modo seguro.

---

## Ejercicios

### Ejercicio 1 — Medir latencia
Escribe un script que publique una marca de tiempo en un tópico y la consuma inmediatamente, midiendo el round-trip. Compara Python vs la latencia teórica de C++ (0.05 ms).

### Ejercicio 2 — LocoClient move en simulación
Usa `sdk2_bridge_sim` para mover el robot describiendo un cuadrado de 1 m de lado. Mide el tiempo de cada lado con `time.time()`.

### Ejercicio 3 — Introspección de tipos IDL
Ejecuta `python3 -c "from unitree_sdk2py.idl.unitree_go.msg.dds_ import LowState_; print(LowState_.__annotations__)"`. Enumera los campos del mensaje y compara con la documentación oficial.

### Ejercicio 4 — Comparativa de frecuencia
Suscríbete a `sportmodestate` (a través de `sdk2_bridge_sim`) y mide cuántos mensajes recibes por segundo. ¿Cuánto añade el wrapper Python comparado con los 500 Hz nativos?

### Ejercicio 5 — Port a B2 vs Go2
Examina `unitree_sdk2py/b2/loco_client.py` y `unitree_sdk2py/go2/loco_client.py`. ¿Qué métodos existen en B2 pero no en Go2? (Pista: capacidades de carga del B2.)

---

## Pasa al robot real

!!! tip "Checklist para robot real"
    1. Conectar laptop/gateway a la red del B2 (WiFi `Unitree_B2_XXXX` o Ethernet)
    2. Verificar conectividad: `ping 192.168.123.1`
    3. Configurar interfaz DDS: `export CYCLONEDDS_URI='...'`
    4. Cambiar el import de `sdk2_bridge_sim` al real
    5. Probar `ChannelFactory.Instance().Init(0)` antes de cualquier comando de movimiento

---

## Referencias

- [unitree_sdk2_python — PyPI](https://pypi.org/project/unitree_sdk2_python/)
- [Unitree SDK2 C++ Reference](https://support.unitree.com/home/en/developer/SDK2)
- [CycloneDDS Python docs](https://cyclonedds.io/docs/cyclonedds-python/)
