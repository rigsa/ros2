---  
title: "Un Node Simple de Control de Velocidad (Move Circle)"
---

## El Código Inicial

Comienza regresando al archivo `publisher.py` de tu package `part1_pubsub` ([o regresa aquí](../part1/publisher.md)), y copia el contenido en tu nuevo archivo `move_circle.py`. Luego, adapta el código de la siguiente manera.

## Creando el Node "Move Circle"

### Importaciones

Una vez más, `rclpy` y la clase `Node` de la librería `rclpy.node` son vitales para cualquier node que creemos, por lo que las primeras dos importaciones permanecerán iguales.

Sin embargo, necesitamos importar el tipo de mensaje usado por el topic `/cmd_vel` aquí, para poder formatear los comandos de velocidad apropiadamente. Podemos encontrar toda la información necesaria sobre este tipo de mensaje usando el comando `ros2 topic info`:

``` { .bash .no-copy }
$ ros2 topic info /cmd_vel
Type: geometry_msgs/msg/TwistStamped
...
```

Y así nuestra importación de mensaje se convierte en:

```py
from geometry_msgs.msg import TwistStamped # (1)!
```

1. En lugar de: `#!py from example_interfaces.msg import String`

### Cambiar el Nombre de la Clase

Anteriormente nuestra clase publisher se llamaba `#!python SimplePublisher()`, cámbiala a `#!python Circle`:

```py
class Circle(Node):
```

### Inicializando la Clase

1. Inicializa el node con un nombre apropiado:

    ```python
    super().__init__("move_circle")
    ```

1. Cambia los parámetros de `create_publisher()`:

    ```python
    self.my_publisher = self.create_publisher(
        msg_type=??, # (1)!
        topic=??, # (2)!
        qos_profile=10,
    )
    ```

    1. ¿Cuál es el nombre de la interfaz que estamos usando aquí?
    2. ¿Cuál es el nombre del topic al que queremos publicar nuestros comandos de velocidad?

1. Necesitaremos publicar comandos de velocidad a una tasa de al menos 10 Hz, así que define esto aquí, y luego configura un timer en consecuencia:

    ```py
    publish_rate = 10 # Hz
    self.timer = self.create_timer(
        timer_period_sec=1/publish_rate, 
        callback=self.timer_callback
    )
    ```

### Modificando el Timer Callback

Aquí publicaremos nuestros comandos de velocidad:

```py
def timer_callback(self):
    radius = 0.5 # meters
    linear_velocity = 0.1 # meters per second [m/s]
    angular_velocity = ?? # radians per second [rad/s] # (1)!

    topic_msg = TwistStamped() # (2)!
    topic_msg.twist.linear.x = linear_velocity
    topic_msg.twist.angular.z = angular_velocity
    self.my_publisher.publish(topic_msg) # (3)!
    
    self.get_logger().info( # (4)!
        f"Linear Velocity: {topic_msg.twist.linear.x:.2f} [m/s], "
        f"Angular Velocity: {topic_msg.twist.angular.z:.2f} [rad/s].",
        throttle_duration_sec=1, # (5)!
    )

```

1. Habiendo definido el radio del círculo, y la velocidad *lineal* a la que queremos que se mueva el robot, ¿cómo calcularíamos la velocidad *angular* que debería aplicarse?

    Considera la ecuación de velocidad angular:

    <figure markdown>
      ![](./ang_vel_eqn.svg){width=200}
    </figure>

    $$
    \omega=\frac{v}{r}
    $$

2. `/cmd_vel` usa mensajes `TwistStamped`, así que instanciamos uno aquí, y asignamos los valores de velocidad lineal y angular (según se estableció arriba) a los campos del mensaje relevantes. Recuerda, [hablamos de todo esto aquí](../part2.md#velocity-commands).

3. Una vez que se han establecido los campos de velocidad apropiados, publica el mensaje.

4. Publica un Mensaje de *Log* de ROS para informarnos (en el terminal) de los valores de control de velocidad que está publicando el node.

5. [Recuerda en el Subscriber de Odometría](./odom_subscriber.md#modifying-the-message-callback) cómo usamos un contador (`#!py self.counter`) y una declaración `#!py if()` para controlar la frecuencia con la que se generaban estos mensajes de log?

    En realidad podemos lograr exactamente lo mismo simplemente proporcionando un argumento `throttle_duration_sec` a la llamada `get_logger().info()`. ¿Mucho más fácil, verdad?

### Actualizando "Main"

Una vez más, no olvides actualizar las partes relevantes de la función `main` para asegurarte de que estamos instanciando la clase `Circle()`, haciendo spin y apagándola correctamente.

## Dependencias del Package

Nuestro node `move_circle.py` tiene una nueva importación de package:

```py
from geometry_msgs.msg import TwistStamped
```

Nuestro package `part2_navigation` por lo tanto tiene una nueva dependencia, así que necesitamos agregarla al archivo `package.xml` de nuestro package.

Anteriormente agregamos `nav_msgs` a este (para el node `odom_subscriber.py`). Debajo de esto, agrega una nueva `#!xml <exec_depend>` para `geometry_msgs`:

```xml title="package.xml"
<exec_depend>rclpy</exec_depend>
<exec_depend>nav_msgs</exec_depend>
<exec_depend>geometry_msgs</exec_depend>  <!-- (1)! -->
```

1. ¡AGREGA ESTA LÍNEA!

Guarda el archivo y ciérralo.
