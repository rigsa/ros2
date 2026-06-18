---
title: "U4: Comportamientos de Alto Nivel (SportClient)"
description: "Activa los comportamientos físicos del Go2/B2 (stand, sit, hello, dance) usando servicios ROS 2 estándar."
---

# U4: Comportamientos de Alto Nivel

## ¿Qué es el SportClient?

El SDK de Unitree expone una API llamada **SportClient** que permite activar
comportamientos físicos predefinidos en el robot. Los comandos se envían como
mensajes DDS a `rt/api/sport/request` y el robot ejecuta el comportamiento solicitado.

En este módulo **no interactuamos directamente con el SDK**. En cambio,
`unitree_ros2_bridge.py` envuelve cada comportamiento en un **servicio ROS 2**
de tipo `std_srvs/Trigger`:

```
Tu código (cliente de servicio)
        ↓  /sport/hello
  unitree_ros2_bridge.py
        ↓  SportClient::Hello()
    Robot Go2/B2
```

En el simulador (`sim_lite`), los mismos servicios están disponibles pero en lugar de
mover un robot real, muestran el nombre del comportamiento en la ventana de pygame
durante 2 segundos - útil para verificar que tu secuencia de llamadas es correcta.

## Lista completa de comportamientos

| Servicio | Comportamiento | API ID |
|---|---|---|
| `/sport/stand_up` | Levantarse en posición de pie | 1004 |
| `/sport/stand_down` | Bajar el cuerpo hacia el suelo | 1005 |
| `/sport/sit` | Sentarse (postura de descanso) | 1009 |
| `/sport/recovery_stand` | Levantarse desde una caída | 1006 |
| `/sport/balance_stand` | Posición de equilibrio activo | 1002 |
| `/sport/hello` | Agitar una pata en señal de saludo | 1016 |
| `/sport/stretch` | Estiramiento | 1017 |
| `/sport/dance1` | Secuencia de danza 1 | 1022 |
| `/sport/dance2` | Secuencia de danza 2 | 1023 |
| `/sport/front_flip` | Voltereta frontal ⚠️ EDU/B2 only | 1030 |

!!! warning "FrontFlip"
    `front_flip` requiere que el robot tenga batería > 50%, espacio libre de
    al menos 2 m al frente, y solo está disponible en el Go2 EDU (no en la
    versión estándar). En el simulador no tiene restricciones.

## `std_srvs/Trigger` - el tipo de servicio

Todos los comportamientos usan el mismo tipo de servicio: `std_srvs/srv/Trigger`.

```python
from std_srvs.srv import Trigger

# No tiene campos de solicitud - simplemente "activa" el comportamiento
req = Trigger.Request()   # vacío

# Respuesta
# resp.success: True si el robot ejecutó el comportamiento
# resp.message: descripción del resultado
```

Esto es idéntico a cómo aprendiste a llamar servicios en la [Parte 4](../course/part4.md),
excepto que aquí el tipo de servicio no tiene parámetros de entrada.

## Configuración del sandbox

Abre el sandbox con **"Unitree U4: Comportamientos Sport"**.

- Mundo: `unitree_empty` (con servicios `/sport/*` activos)
- Archivo semilla: `unitree_sport.py`

Para verificar que los servicios están disponibles:
```bash
ros2 service list | grep sport
```
Deberías ver los 10 servicios listados.

```bash
# Llamar un servicio manualmente desde la terminal:
ros2 service call /sport/hello std_srvs/srv/Trigger {}
```

## Archivo semilla: `unitree_sport.py`

El nodo crea un cliente para cada comportamiento y ejecuta la secuencia:

```
stand_up → hello → stretch → sit
```

Para compilar y ejecutar:
```bash
cd ~/ros2_ws
colcon build --packages-select unitree_u4_sport --symlink-install
source install/setup.bash
ros2 run unitree_u4_sport unitree_sport.py
```

Observa la ventana de `sim_lite`: cada comportamiento aparecerá como un banner
amarillo durante 2 segundos.

## Ejercicios

!!! note "Ejercicio 1 - Secuencia personalizada"
    Modifica la función `_secuencia()` en `unitree_sport.py` para que el robot ejecute:
    ```
    stand_up → balance_stand → dance1 → sit
    ```
    Agrega una pausa de 2 s entre cada comportamiento.

!!! note "Ejercicio 2 - Función genérica"
    Escribe una función `ejecutar(nombre: str)` que acepte el nombre del comportamiento
    como string y llame al servicio correcto sin usar un `if/elif` largo.
    
    **Pista**: guarda los clientes en un diccionario `self._clientes[nombre]`.

!!! note "Ejercicio 3 - Robot espera confirmación"
    Modifica el nodo para que espere 3 s entre comportamientos **solo si el servicio
    respondió con `success=True`**. Si falló, reintenta hasta 3 veces antes de continuar.

!!! note "Ejercicio 4 - Combina movimiento y comportamientos"
    Crea un nuevo nodo que:
    1. Llame a `stand_up`
    2. Avance 1 m (usando `/cmd_vel`)
    3. Llame a `hello`
    4. Regrese al punto de partida
    5. Llame a `sit`
    
    Para esto necesitarás combinar código de U2 (locomoción) y U4 (sport).

## Relación con Servicios y Acciones (Partes 4 y 5)

Los servicios `/sport/*` son clientes de servicio estándar de ROS 2 - exactamente
lo que aprendiste en la [Parte 4](../course/part4.md). La única diferencia es que
aquí el servicio tiene un efecto físico en el robot en lugar de un resultado numérico.

En la [Parte 5](../course/part5.md) aprendiste sobre **acciones** para tareas de larga
duración. Los comportamientos del SportClient (como `dance1`) son candidatos naturales
para implementarse como actions (duran ~2-5 s y tienen feedback de progreso), pero
por simplicidad en este módulo los tratamos como servicios sincrónicos.

---

Continúa con [U5 - LiDAR y Detección de Obstáculos](u5-lidar.md).
