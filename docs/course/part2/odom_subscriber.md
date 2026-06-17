---  
title: "Un Node Subscriber de Odometría"
---

## El Código Inicial

Habiendo copiado el archivo `subscriber.py` de tu package `part1_pubsub`, comenzarás con [el código discutido aquí](../part1/subscriber.md).

Veamos qué necesitamos cambiar ahora.

## De Simple Subscriber a Odom Subscriber

### Importaciones

Generalmente nos basaremos en `rclpy` y la clase `Node` de la librería `rclpy.node` para la mayoría de los nodes que crearemos, por lo que nuestras primeras dos importaciones permanecerán iguales. 

Sin embargo, ya no trabajaremos con mensajes de tipo `String`, así que necesitamos reemplazar esta línea para importar el tipo de mensaje correcto. Como sabemos [de antes en la Parte 2](../part2.md#odometry-explained), el topic `/odom` usa mensajes del tipo `nav_msgs/msg/Odometry`:

``` { .bash .no-copy }
$ ros2 topic info /odom
Type: nav_msgs/msg/Odometry
...
```

Esto nos dice todo lo que necesitamos saber para construir la declaración de importación de Python correctamente:

```py
from nav_msgs.msg import Odometry
```

También necesitarás importar una herramienta matemática del módulo `math`:

```py
from math import atan2
```

(por razones que quedarán más claras en breve.)

### Cambiar el Nombre de la Clase

Anteriormente nuestra clase se llamaba `#!python SimpleSubscriber()`, cámbiala a algo más apropiado ahora, por ejemplo: `#!python OdomSubscriber()`:

```py
class OdomSubscriber(Node):
```

### Inicializando la Clase

La estructura de esto permanece en gran medida igual, solo necesitamos modificar algunas cosas: 

1. Cambia el nombre que se usa para registrar el node en la Red ROS:

    ```python
    super().__init__("odom_subscriber")
    ```

1. Cambia los parámetros del subscriber:

    ```python
    self.my_subscriber = self.create_subscription(
        msg_type=Odometry, # (1)!
        topic="/odom", # (2)!
        callback=self.msg_callback, 
        qos_profile=10,
    )
    ```

    1. `/odom` usa el tipo de mensaje Odometry (como se importó arriba)
    2. El nombre del topic es `/odom`. También puedes omitir la barra diagonal al definir esto, por lo que `#!py topic="odom"` también funcionaría. 

1. Lo último que haremos dentro del método `__init__` de nuestra clase (después de haber configurado el subscriber) es inicializar un contador:

    ```py
    self.counter = 0 
    ```

    La razón de esto se explicará en breve...

### Calculando Ángulos de Euler a partir de Cuaterniones 

Después del método de clase `#!py __init__`, define un nuevo método dentro de la clase `#!py OdomSubscriber()`, llamado `quaternion_to_euler`:

```py
def quaternion_to_euler(self, orientation):
    x = orientation.x
    y = orientation.y
    z = orientation.z
    w = orientation.w

    yaw = # TODO: calculate yaw...

    return yaw # (in radians)
```

Esta función recibirá los datos de orientación del topic `/odom` (en cuaterniones) y necesita generar el ángulo `yaw` en radianes. Tu trabajo ahora es establecer el proceso de conversión real. Puedes ver cómo se hace esto mirando el módulo `tb3_tools.py` dentro de tu package `part2_navigation`[^tb3-tools][^auto-addison]:

[^tb3-tools]: `tb3_tools.py` proviene de la plantilla de Package ROS 2, ¡así que obtienes esto "de forma gratuita" con cada package que creas en este curso!
[^auto-addison]: El proceso de conversión de Cuaternión a Euler se toma de [esta publicación del blog Automatic Addison](https://automaticaddison.com/how-to-convert-a-quaternion-into-euler-angles-in-python/){target="_blank"}.


``` { .txt .no-copy }
.
├── CMakeLists.txt
├── package.xml
├── part2_navigation_modules
│   ├── __init__.py
│   └── tb3_tools.py <-- See here!
└── scripts
    ├── basic_velocity_control.py
    ├── odom_subscriber.py
    └── stop_me.py

```

Implementa el cálculo para que tu método `quaternion_to_euler()` realmente genere un ángulo de yaw correcto (en radianes) para el robot.

 

### Modificando el Message Callback

Dirígete al método de clase `msg_callback` existente ahora y cámbialo de la siguiente manera:

```py
def msg_callback(self, topic_message: Odometry): # (1)!

    pose = topic_message.pose.pose # (2)!
    
    # (3)!
    pos_x = pose.position.x
    pos_y = pose.position.y
    pos_z = pose.position.z
    
    yaw = self.quaternion_to_euler(pose.orientation) # (4)!

    if self.counter > 10: # (5)!
        self.counter = 0
        self.get_logger().info(
            f"x = {pos_x:.3f} (m), y = ? (m), yaw = ? (radians)"
        ) # (6)!
    else:
        self.counter += 1

```

1. Esta es una *anotación de tipo*. El topic al que nos estamos suscribiendo ha cambiado (antes `/my_topic`, ahora `/odom`), y el nuevo topic usa un tipo de dato diferente (también conocido como "Interfaz ROS"). Por lo tanto, actualizamos la anotación de tipo para que coincida con el nuevo tipo de datos que ingresará a este método callback (a través de la variable `topic_message`).
2. Solo nos interesa realmente la parte Pose de los datos de odometría, así que la asignamos a una variable.

3. Como ya sabemos, Pose contiene información sobre tanto la "posición" como la "orientación" del robot, extraemos primero los valores de posición y los asignamos a las variables `pos_x`, `pos_y` y `pos_z`.
    
    Los datos de posición se proporcionan en metros, por lo que no necesitamos hacer ninguna conversión sobre esto y podemos usar los datos directamente.

4. Los datos de orientación están en cuaterniones, por lo que necesitamos convertirlos a una representación de ángulo de Euler. Estamos llamando a un método de clase llamado `self.quaternion_to_euler()` para manejar esta conversión, que deberías haber establecido en el paso anterior.

5. Aquí imprimimos los valores que nos interesan en el terminal.

    Esta función callback se ejecutará cada vez que se publique un nuevo mensaje en el topic `odom`, lo cual ocurre a una tasa de aproximadamente 20 veces por segundo (20 Hz).
        
    ??? tip
        Podemos usar la función `ros2 topic hz` para decirnos esto:

        ``` { .txt .no-copy }
        $ ros2 topic hz /odom
        average rate: 18.358
        min: 0.037s max: 0.088s std dev: 0.01444s window: 20
        ``` 
    
    ¡Eso es muchos mensajes para imprimir en el terminal cada segundo! Por lo tanto, usamos una declaración `if` y un `counter` para asegurarnos de que nuestra declaración `print` solo se ejecute para 1 de cada 10 mensajes del topic en su lugar.

6. **Tarea**: ¡Continúa formateando el mensaje `print` para mostrar los tres valores de odometría que son relevantes para nuestro robot!  

### Actualizando "Main"

Lo único que queda por hacer ahora es actualizar las partes relevantes de la función `main` para asegurarte de que estás instanciando, haciendo spin y apagando tu node correctamente.

## Dependencias del Package

Una vez más, estamos importando un par de librerías de Python en nuestro node aquí, lo que significa que nuestro package tiene dos *dependencias*: `rclpy` y `nav_msgs`:

```py
import rclpy 
from rclpy.node import Node

from nav_msgs.msg import Odometry
```

Por lo tanto, deberíamos agregar estas dependencias a nuestro archivo `package.xml` (`part2_navigation/package.xml`). Ábrelo y encuentra la siguiente línea:

```xml
<exec_depend>rclpy</exec_depend>
```

La plantilla de package ya incluye una dependencia para `rclpy`, ya que esto es bastante fundamental para nuestro trabajo aquí, pero sí necesitamos agregar `nav_msgs` también, así que agrega la siguiente línea adicional debajo:

```xml
<exec_depend>nav_msgs</exec_depend>
```

Guarda el archivo y ciérralo.
