---  
title: "Navegación Basada en Odometría (Move Square)"  
---

**Un node combinado de publisher y subscriber para lograr control basado en odometría...**

A continuación encontrarás una plantilla de script de Python para mostrarte cómo puedes publicar en `/cmd_vel` y suscribirte a `/odom` en el mismo node. Esto te ayudará a construir un controlador de *lazo cerrado* para hacer que tu robot siga una **trayectoria de movimiento cuadrada** de tamaño: **1m x 1m**. 

Puedes publicar comandos de velocidad en `/cmd_vel` para hacer que el robot se mueva, monitorear la *posición* y *orientación* del robot en tiempo real, determinar cuándo se ha completado el movimiento deseado, y luego actualizar los comandos de velocidad en consecuencia.  

## Enfoque Sugerido

Moverse en un cuadrado puede lograrse alternando entre dos estados de movimiento diferentes de forma secuencial: *Avanzar* y *girar* en el lugar. Al inicio de cada paso de movimiento podemos leer la odometría actual del robot, y luego usarla como referencia para comparar y saber cuándo la posición/orientación del robot ha cambiado en la cantidad requerida, por ejemplo:

1. Con el robot estacionario, **lee la odometría** para determinar su posición X e Y actual en el entorno.
1. **Avanza** hasta que la posición X e Y del robot indiquen que se ha movido 1m hacia adelante.
1. **Detén** el movimiento hacia adelante.
1. **Lee la odometría del robot** para determinar su orientación actual ("yaw"/<code>&theta;<sub>z</sub></code>).
1. **Gira en el lugar** hasta que la orientación del robot cambie 90&deg; (o el equivalente en radianes).
1. **Detén** el giro.
1. Repite.  

### El Código

```python title="move_square.py"
--8<-- "code_templates/move_square.py"
```

1. Importa el mensaje `TwistStamped` para publicar comandos de velocidad en `/cmd_vel`.
2. Importa el mensaje `Odometry`, para usar al suscribirse al topic `/odom`.
3. Importa el método `quaternion_to_euler` de `tb3_tools.py`... 
    
    Este es un método útil que está incluido en [la Plantilla de Package ROS 2](https://github.com/tom-howard/ros2_pkg_template/blob/main/ros2_pkg_template_modules/tb3_tools.py){target="_blank"} para convertir la orientación de cuaterniones a ángulos de Euler (sobre [los ejes principales](../part2.md#principal-axes)).

    ¡Cualquier package de ROS 2 que crees con nuestra plantilla de package ROS 2 contendrá este método para que lo uses!

4. Finalmente, importa algunas operaciones matemáticas útiles (y `pi`), que pueden resultar útiles para esta tarea:

    <center>

    | Operación Matemática | Implementación en Python |
    | :---: | :---: |
    | $\sqrt{a+b}$ | `#!python sqrt(a+b)` |
    | $a^{2}+(bc)^{3}$ | `#!python pow(a, 2) + pow(b*c, 3)` |
    | $\pi r^2$ | `#!python pi * pow(r, 2)` |

    </center>

5. Aquí establecemos un mensaje `TwistStamped`, que podemos poblar con velocidades y luego publicar en `/cmd_vel` dentro del método `timer_callback()` (para hacer que el robot se mueva).

6. Aquí definimos algunas variables que podemos usar para almacenar bits relevantes de datos de odometría mientras nuestro node está corriendo (y leerlos de vuelta para implementar control con retroalimentación):
    * `self.x`, `self.y` y `self.theta_z` serán usados por el `odom_callback()` para almacenar la pose **actual** del robot
    * `self.xref`, `self.yref` y `self.theta_zref` pueden usarse en el método `timer_callback()` para llevar un registro de dónde **estaba** el robot en un momento dado (y determinar cuánto se ha movido desde ese punto)

7. También necesitaremos hacer un seguimiento de cuánto ha viajado el robot (o girado) para determinar cuándo ha ocurrido suficiente movimiento para desencadenar un cambio al estado alternativo, es decir:
    
    * `if` viajó 1 metro, `then`: girar
    * `if` giró 90&deg;, `then`: avanzar

8. Aquí obtenemos la orientación actual del robot (en cuaterniones) y la convertimos a ángulos de Euler (en radianes) sobre [los ejes principales](../part2.md#principal-axes), donde:
    * "roll" = <code>&theta;<sub>x</sub></code>
    * "pitch" = <code>&theta;<sub>y</sub></code>
    * "yaw" = <code>&theta;<sub>z</sub></code>

9. Solo nos interesan `x`, `y` y <code>&theta;<sub>z</sub></code>, así que los asignamos a variables de clase `self.x`, `self.y` y `self.theta_z`, para que podamos acceder a ellos en cualquier parte dentro de nuestra clase `Square()`.

10. A veces, puede tomar unos momentos para que llegue el primer mensaje del topic, y es útil saber cuándo ha ocurrido eso para saber que estás tratando con datos reales del topic. Aquí, simplemente estamos estableciendo una bandera en `True` una vez que la función callback ha ejecutado por primera vez (es decir, el primer mensaje del topic *ha* sido recibido).
 
## Enfoque Alternativo: Seguimiento de Puntos de Referencia

Una trayectoria de movimiento cuadrada puede definirse completamente por las coordenadas de sus cuatro esquinas, y podemos hacer que el robot se mueva hacia cada una de estas esquinas una por una, usando su sistema de odometría para monitorear su posición en tiempo real, y adaptando las velocidades lineales y angulares en consecuencia.

Esto es un poco más complicado, y es posible que quieras esperar hasta que tengas un poco más de experiencia con ROS antes de abordarlo de esta manera.
