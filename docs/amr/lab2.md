---  
title: "Lab 2: Control con Retroalimentación" 
---  

## Introducción

En el Lab 1 exploramos cómo funciona ROS 2 y cómo usar este framework para dar vida a un robot. Hagamos un repaso rápido de los puntos clave:

**Nodes**

* Son programas ejecutables (scripts Python, C++) que realizan tareas y operaciones específicas del robot.
* Típicamente, habrá muchos Nodes ejecutándose simultáneamente en un robot para que funcione.
* Podemos crear nuestros propios Nodes sobre lo que ya está en ejecución, para agregar funcionalidades adicionales.
* Recordarás que creamos nuestro propio Node (en Python) para hacer que nuestro TurtleBot3 Waffle siguiera una trayectoria cuadrada.

<figure markdown>
  ![](./lab2/ros_network.png){width=500px}
</figure>

**Topics e Interfaces de Mensajes**

* Todos los Nodes en ejecución en una red pueden comunicarse y pasarse datos entre sí usando un Principio de Comunicación basado en Publicador/Suscriptor.
* Los Topics de ROS son clave para esto: son esencialmente los canales de comunicación (o la tubería) a través de los cuales se pasan todos los datos entre los nodes.
* Diferentes topics comunican diferentes tipos de información usando estructuras de datos estandarizadas (llamadas *"Interfaces de Mensajes"*).
* Cualquier Node puede publicar (*escribir*) y/o suscribirse a (*leer*) cualquier Topic de ROS para pasar información o hacer que sucedan cosas.

<figure markdown>
  ![](./lab2/ros_comms.png){width=500px}
</figure>

Uno de los Topics de ROS clave con el que trabajamos la vez anterior fue `/cmd_vel`, que es un topic que comunica comandos de velocidad para hacer mover a un robot. Recordarás que para hacer mover a nuestro TurtleBot3 Waffle publicamos *Mensajes de Interface* `TwistStamped` en el topic `/cmd_vel`. Los mensajes de interface son *tipos de datos estructurados* definidos en ROS, y recordaremos brevemente la estructura del tipo de dato `TwistStamped` en breve...

**Control de Lazo Abierto**

Usamos un método basado en tiempo para controlar el movimiento de nuestro robot para que generara una trayectoria cuadrada. Este tipo de control es *de lazo abierto*: esperábamos que el robot se hubiera movido (o girado) en la cantidad requerida, pero no teníamos *retroalimentación* para decirnos si esto realmente se había logrado.

**Control de Lazo Cerrado**

En este laboratorio veremos cómo esto puede mejorarse, haciendo uso de algunos de los sensores a bordo de nuestro robot para decirnos dónde está el robot o qué puede ver en su entorno, con el fin de completar una tarea de manera más confiable y poder adaptarse mejor a los cambios e incertidumbre del entorno.

### Objetivos

En este laboratorio, construiremos algunos Nodes de ROS (en Python) que incorporan datos de algunos de los sensores de nuestro robot. Estos datos de sensores son publicados en topics específicos en la red ROS, y podemos construir Nodes de ROS para *suscribirnos* a estos. Veremos cómo los datos de estos sensores pueden usarse como *retroalimentación* para informar la toma de decisiones, permitiéndonos implementar algunas formas diferentes de *control de lazo cerrado* y hacer que nuestro robot sea más autónomo.

### Resultados de Aprendizaje

Al finalizar esta sesión serás capaz de:

1. Interpretar los datos del sistema de Odometría de un robot ROS y entender qué te dice sobre la posición y orientación de un robot en su entorno.
1. Usar datos del sensor LiDAR de un robot para hacer que el robot siga una pared.
1. Analizar imágenes de la cámara de un robot y usar esta información para seguir una línea de color en el suelo.
1. (Opcional) Usar la retroalimentación del sistema de odometría de un robot para *controlar* su posición en un entorno.


### Acceso rápido

* [Ejercicio 1: Explorar datos de Odometría](#ex1)
* [Ejercicio 2: Seguimiento de pared](#ex2)
* [Ejercicio 3: Seguimiento de línea](#ex3)
* [(Opcional) Ejercicio 4: Navegación basada en Odometría](#ex4)

## El Laboratorio

!!! info "Evaluación"
    Este laboratorio es **evaluado de forma sumativa**.

    1. Existe un **cuestionario post-lab** que deberás completar después de esta sesión, el cual será publicado en la plataforma del curso.
    1. También serás evaluado por el trabajo que realices **en el laboratorio** para los Ejercicios 2 y 3.

### Primeros pasos

#### Crear un paquete ROS

Necesitaremos un paquete ROS para trabajar durante esta sesión de laboratorio. Hemos creado una plantilla para ti, que contiene todos los recursos que necesitarás para hoy. Descárgala e instálala de la siguiente manera.

1. Abre una instancia de terminal en la laptop, ya sea usando el atajo de teclado ++ctrl+alt+t++, o haciendo clic en el ícono de la aplicación Terminal en la barra de favoritos del escritorio:
    
    <figure markdown>
      ![](../images/laptops/terminal_icon.svg){width=60px}
    </figure>

    La llamaremos **TERMINAL 1**.

1. En **TERMINAL 1**, ejecuta los siguientes comandos en orden:

    !!! tip
        Para **pegar** los siguientes comandos en la terminal usa ++ctrl+shift+v++
    
    ***
    **TERMINAL 1**:
    ```txt
    cd ~/ros2_ws/src/
    ```
    
    ```txt
    git clone https://github.com/tom-howard/amr31001_lab2.git
    ```

    !!! note
        Este repositorio proviene del curso original de la Universidad de Sheffield. El paquete ROS se llama `amr31001_lab2` — usa ese nombre en todos los comandos siguientes.
    
    ```txt
    cd ~/ros2_ws && \
      colcon build --symlink-install \
      --packages-select amr31001_lab2 && \
      source ~/.bashrc 
    ```
    ***

1. A continuación, abre el paquete en VS Code:

    ```bash
    code ./src/amr31001_lab2
    ```

1. Cuando se abra VS Code, navega al *Explorador de Archivos*:
    
    <figure markdown>
      ![](./lab2/vscode_explorer_package_xml.png){width=400px}
    </figure>

    ... encuentra un archivo llamado `package.xml` aquí y haz clic en él.

1. Busca las siguientes líneas en el archivo `package.xml`:

    ``` title="package.xml"
    <maintainer email="nombre.apellido1@institucion.edu">Nombre 1</maintainer>
    <maintainer email="nombre.apellido2@institucion.edu">Nombre 2</maintainer>
    ```

    Cambia `Nombre 1` a tu nombre completo, y `nombre.apellido1@institucion.edu` a tu correo institucional. Haz lo mismo para el otro miembro de tu grupo en la línea inferior.

    !!! warning "Post-lab"
        **¡Esto es importante para el post-lab!**

        Parte del trabajo que realices en este laboratorio será evaluado como parte del post-lab, por lo que es importante que podamos identificar a cada miembro de tu grupo. Si algún miembro del grupo no está listado aquí, ¡no recibirá calificación!

        Al ingresar los nombres, asegúrate de proporcionar nombres **Y** apellidos para cada miembro del grupo.

1. Guarda los cambios que acabas de hacer en tu archivo `package.xml`.

#### Lanzar ROS

Al igual que la última vez, ahora necesitarás poner en marcha ROS en tu robot.

1. Primero, identifica el robot que tienes asignado. Cada uno de nuestros robots tiene un nombre único: `robot-X`, donde `X` es el *'Número de Robot'*. Revisa la etiqueta impresa en la parte superior del robot para saber cuál te corresponde.

1. En **TERMINAL 1** escribe el siguiente comando para *vincular* la laptop y el robot, de modo que puedan trabajar juntos:

    ***
    
    **TERMINAL 1**:
    ``` { .txt .no-copy }
    waffle X pair
    ```
    **... reemplazando `X` con el número del robot que te ha sido asignado**.
    
    ***

1. Ingresa la contraseña del robot cuando se te solicite (te la indicaremos en el laboratorio).

    Es posible que veas un mensaje como este durante el proceso de vinculación:

    <figure markdown>
      ![](../images/laptops/ssh_auth.svg){width=600px}
    </figure>

    Si es así, simplemente escribe `yes` y presiona ++enter++ para confirmar que deseas continuar.

1. Una vez que el proceso de vinculación haya finalizado, deberías ver el mensaje `pairing complete`, mostrado en azul en la terminal.

1. Luego, en la misma terminal (**TERMINAL 1**), introduce el siguiente comando:

    ***
    **TERMINAL 1:**
    ``` { .txt .no-copy }
    waffle X term
    ```
    (nuevamente, reemplazando `X` con el número de **tu** robot).
    
    ***

    El texto que había en la terminal debería desaparecer y aparecerá un banner verde en la parte inferior de la ventana:
    
    <figure markdown>
      ![](../images/laptops/tmux.svg){width=600px}
    </figure>

    Esta es una instancia de terminal ejecutándose **en el robot**, y cualquier comando que ingreses aquí se **ejecutará en el robot** (¡no en la laptop!)

1. Ahora, lanza ROS en el robot ingresando el siguiente comando:

    ***
    **TERMINAL 1:**
    ```bash
    ros2 launch tuos_tb3_tools ros.launch.py
    ```

    !!! tip
        Para pegar texto en una terminal Linux deberás usar las teclas Control + **Shift** + V: ++ctrl+shift+v++

    ***

    Si todo va bien, el robot reproducirá un sonido *"do-re-mi"* y aparecerá un mensaje como este (entre todo el otro texto):

    ``` { .txt .no-copy }
    [tb3_status.py-#] ######################################
    [tb3_status.py-#] ### robot-X is up and running! ###
    [tb3_status.py-#] ######################################
    ```

    ¡ROS ya está funcionando en el robot y estamos listos para comenzar!

1. A continuación, conecta la laptop a la red ROS que acabamos de establecer en el robot. El robot y la laptop se comunican entre sí a través de la red inalámbrica, pero se requiere un paso más para vincularlos.

    Abre **una nueva instancia de terminal** en la laptop (ya sea con el atajo ++ctrl+alt+t++ o haciendo clic en el ícono de la terminal) e ingresa el siguiente comando:

    ***
    **TERMINAL 2**:
    ```bash
    ros2 run rmw_zenoh_cpp rmw_zenohd
    ```
    ***

    Deja **TERMINAL 1** y **TERMINAL 2** ejecutándose en segundo plano en todo momento mientras trabajas con tu robot en el laboratorio hoy.

### Odometría

Para comenzar consideraremos el sistema de *odometría* de un robot y para qué es útil.

> La odometría es el uso de datos de sensores de movimiento para estimar el cambio de posición a lo largo del tiempo. Es utilizada en robótica por algunos robots con patas o ruedas para estimar su posición relativa a una ubicación de inicio. [^wiki]

[^wiki]: https://en.wikipedia.org/wiki/Odometry

Por lo tanto, nuestro robot puede hacer un seguimiento de su posición (y orientación) mientras se mueve. Hace esto usando datos de dos fuentes:

1. **Encoders de rueda**: Nuestro robot tiene dos ruedas, cada una equipada con un encoder que mide el número de rotaciones que realiza la rueda.
1. Una **Unidad de Medición Inercial (IMU)**: Usando acelerómetros, giroscopios y brújulas, la IMU puede monitorear la velocidad lineal y angular del robot, y hacia qué dirección se dirige, en todo momento.

Estos datos se publican en un Topic de ROS llamado `/odom`.

#### :material-pen: Ejercicio 1: Explorar datos de Odometría {#ex1}

En el laboratorio anterior usamos algunos comandos `ros2` para identificar e interrogar topics activos en la red ROS. Hagámoslo de nuevo ahora, pero esta vez con el topic `/odom`.

1. Abre una nueva instancia de terminal en la laptop (presionando ++ctrl+alt+t++, o haciendo clic en el ícono de la aplicación Terminal, como lo hiciste antes). La llamaremos **TERMINAL 3**.

1. Como quizás recuerdes de la última vez, podemos usar el comando `ros2 topic` para *listar* todos los topics que están actualmente activos en la red. Introduce lo siguiente en **TERMINAL 3**:

    ***
    **TERMINAL 3**:
    ```bash
    ros2 topic list
    ```
    ***

    Debería aparecer una gran lista de elementos en la pantalla. ¿Puedes encontrar el topic `/odom`?
    
1. Averigüemos más sobre esto usando el comando `ros2 topic info`.

    ***
    **TERMINAL 3**:
    ```txt
    ros2 topic info /odom
    ```
    ***

    Esto debería proporcionar la siguiente salida:
    
    ```{ .txt .no-copy }
    Type: nav_msgs/msg/Odometry
    Publisher count: 1
    Subscription count: 0
    ```

    !!! info "Cuestionario Post-lab"
        ¿Qué significa todo esto? Discutimos esto [la última vez (en relación con el topic `/cmd_vel`)](./lab1.md#rostopic_info_explained), y quizás quieras volver a verlo para refrescar tu memoria.
    
    Basándose en lo anterior, sabemos que el topic `/odom` usa una estructura de datos `nav_msgs/msg/Odometry` (o *"interface"*).
    
    **Interfaces** (revisitado)
    
    Recuerda del Lab 1 que las estructuras de datos en ROS 2 se llaman *Interfaces*.
        
    De la salida anterior, `Type` se refiere al *tipo* de estructura de datos (es decir, el tipo de interface). La definición de `Type` siempre tiene tres partes: en este caso `nav_msgs`, `msg` y `Odometry`:
        
    1. `nav_msgs` es el nombre del paquete ROS al que pertenece esta interface (estructura de datos).
    1. `msg` nos indica que es una interface de *mensaje* de topic.
    1. `Odometry` es el *nombre* de la interface de mensaje.
    
1. Podemos usar el comando `ros2 interface` para encontrar más información sobre esto:

    ***
    **TERMINAL 3**:
    ```txt
    ros2 interface show nav_msgs/msg/Odometry
    ```
    ***

    Verás mucha información allí, pero trata de encontrar la línea que dice `Pose pose`:

    ``` { .txt .no-copy }
    Pose pose
            Point position
                    float64 x
                    float64 y
                    float64 z
            Quaternion orientation
                    float64 x 0
                    float64 y 0
                    float64 z 0
                    float64 w 1
    ```

    Aquí encontraremos información sobre la posición y orientación del robot (también conocida como *"Pose"*) en el entorno. Veamos estos datos en tiempo real...

1. Podemos ver los datos en vivo que se transmiten a través del topic `/odom`, usando el comando `ros2 topic echo`. Sabemos que el tipo de dato se llama `nav_msgs/msg/Odometry`, y anidado dentro de este está el atributo `pose` que nos interesa, así que:

    ***
    **TERMINAL 3**:
    ```txt
    ros2 topic echo /odom --field pose.pose
    ```
    ***

1. Lo que se nos presenta ahora son datos de Odometría en vivo del robot.
    
    Conduzcamos el robot un poco y observemos cómo cambia la pose de nuestro robot mientras lo hacemos.
    
1. Abre una nueva instancia de terminal presionando ++ctrl+alt+t++ o haciendo clic en el ícono de la terminal, como hiciste antes. La llamaremos **TERMINAL 4**:

    ***
    **TERMINAL 4**:
    ```bash
    ros2 run turtlebot3_teleop teleop_keyboard
    ```
    ***

1. Sigue las instrucciones proporcionadas en la terminal para conducir el robot:

    ??? tip "Recordatorio"

        <figure markdown>
          ![](../images/cli/teleop_keymap.svg)
        </figure>

    Mientras haces esto, ¡observa cómo los datos de `position` y `orientation` cambian en **TERMINAL 3**, en tiempo real!

    !!! info "Cuestionario Post-lab"
        ¿Qué valores de posición y orientación cambian (significativamente) cuando:
            
        1. ¿El robot gira sobre sí mismo (es decir, solo se aplica una velocidad *angular*)?
        1. ¿El robot avanza (es decir, solo se aplica una velocidad *lineal*)?
        1. ¿El robot se mueve en círculo (es decir, se aplican simultáneamente velocidades lineal *y* angular)?

        **¡Toma nota de las respuestas a estas preguntas, ya que pueden aparecer en el cuestionario post-lab!**

1. Cuando hayas visto suficiente, presiona ++ctrl+c++ en **TERMINAL 4** para detener el node `teleop_keyboard`. Luego, presiona ++ctrl+c++ en **TERMINAL 3** también, lo que detendrá el flujo en vivo de mensajes de Odometría que se muestran.

##### Resumen

**Pose** es una combinación de la *posición* y *orientación* de un robot en su entorno.

**Posición** nos indica la ubicación (en metros) del robot en su entorno. El punto donde estaba el robot cuando se encendió es el punto de referencia, por lo que los valores de distancia que observamos en el ejercicio anterior se citaron todos relativos a esta posición inicial.

Deberías haber notado que (a medida que el robot se movía) los términos `x` e `y` cambiaban, pero el término `z` debería haberse mantenido en cero. Esto se debe a que el plano `X-Y` es el suelo, ¡y cualquier cambio en la posición `z` significaría que el robot está flotando o volando sobre el suelo!

**Orientación** nos dice hacia dónde apunta el robot en su entorno, expresado en unidades de *Cuaterniones*; un sistema de orientación de cuatro términos. También deberías haber notado algunos de estos valores cambiando, ¡aunque puede que no haya sido inmediatamente obvio qué significaban los valores! Para los ejercicios adicionales en este laboratorio convertiremos esto a ángulos de Euler (en grados/radianes) para que los datos sean un poco más fáciles de entender.

En última instancia, la *posición* de nuestros robots puede cambiar tanto en los ejes `X` como `Y` (es decir, el plano del suelo), mientras que su *orientación* solo puede cambiar alrededor del eje `Z` (es decir, solo puede "guinear"/yaw):

<figure markdown>
  ![](../images/waffle/pose.svg){width=700px}
</figure>

#### Navegación basada en Odometría

Podemos usar la odometría de nuestro robot como señal de retroalimentación para informar la navegación del robot e implementar **control de lazo cerrado**. Hay un ejercicio final (opcional) al final de este laboratorio donde puedes explorar esto más a fondo (si tienes tiempo). Por ahora, consideremos otros flujos de datos en el robot y cómo *estos* podrían usarse para el control de lazo cerrado en su lugar.

### El Sensor LiDAR

Como ya sabes, el dispositivo negro que gira en la parte superior de tu robot es un *Sensor LiDAR*. Como se discutió anteriormente, este sensor usa pulsos láser para medir la distancia a objetos cercanos. El sensor gira continuamente para poder disparar estos pulsos láser a través de un arco completo de 360°, y generar un mapa bidimensional completo del entorno del robot.

Estos datos se publican en la red ROS en un topic llamado `/scan`. Usa los mismos métodos que usaste en el [Ejercicio 1](#ex1) para descubrir qué tipo de dato (*"interface"*) usa este topic.

!!! info "Cuestionario Post-lab"
    ¡Toma nota de esto, habrá una pregunta del cuestionario post-lab sobre ello!

Lanza RViz, para que podamos ver los datos de este sensor en tiempo real:

***
**TERMINAL 3**:
```bash
ros2 launch tuos_tb3_tools rviz.launch.py environment:=real
```
***

<figure markdown>
  ![](../images/waffle/real_rviz_vs_arena.png){width=700px}
</figure>

Los puntos verdes ilustran los datos del LiDAR. Extiende tu mano hacia el robot y observa si puedes verla siendo detectada por el sensor... debería formarse un grupo de puntos verdes en la pantalla para indicar dónde está tu mano en relación con el robot. Mueve tu mano y observa cómo el grupo de puntos se mueve en consecuencia. Acerca y aleja tu mano del robot y observa cómo los puntos también se acercan o alejan del robot en la pantalla.

Estos datos son realmente útiles y (como observamos durante la sesión de laboratorio anterior) nos permiten construir mapas bidimensionales de un entorno con considerable precisión. También hay muchas otras formas en que podemos usar estos datos, y en el siguiente ejercicio veremos cómo podemos usarlos como señal de retroalimentación para ¡hacer que nuestro robot detecte y siga paredes!

Cuando hayas terminado, cierra RViz presionando ++ctrl+c++ en **TERMINAL 3**.

#### :material-pen: Ejercicio 2: Seguimiento de pared {#ex2}

1. Regresa a VS Code, que debería seguir abierto desde antes.

1. En el Explorador de Archivos del lado izquierdo encuentra una carpeta llamada `scripts` y haz clic en el archivo `ex2.py` aquí, para mostrarlo en el editor.

1. Revisa el código y trata de entender qué está pasando. Hay algunas cosas a tener en cuenta:

    1. El **control de movimiento** es gestionado por una clase de Python externa llamada `Motion`, que se importa en la línea 7 (junto con otra clase llamada `Lidar` de la que hablaremos en breve):

        ```python
        from amr31001_lab2_modules.tb3_tools import Motion, Lidar
        ```

        La clase `Motion` se instancia en la línea 14:

        ```python
        self.motion = Motion(self) # (1)!
        ```

        1. La mayor parte del código en el archivo `ex2.py` está contenida dentro de una clase Python llamada `WallFollower`. Mira la línea 9:

            ```py
            class WallFollower(Node):
                ...
            ```

            `#!py self` permite que nuestra clase se refiera a sí misma.

            `#!py self.motion`, por ejemplo, nos permite acceder al atributo `motion` en cualquier parte dentro de la clase (siempre que nos refiramos a él como `#!py self.motion`).

        Un método de clase llamado `follow_wall()` contiene la mayor parte del código, y es aquí (en las líneas 49-51) donde llamamos al atributo `#!py self.motion` para hacer que el robot se mueva con una velocidad lineal de `x` (m/s) y/o una velocidad angular de `y` (rad/s):

        ``` { .py .no-copy }
        self.motion.move_at_velocity(
            linear = x, angular = y
        )
        ```

        Un método de clase llamado `on_shutdown()` maneja las operaciones de apagado que deben ocurrir cuando se detiene este node Python, y es *aquí* (línea 24) donde llamamos al objeto `#!py self.motion` nuevamente, pero esta vez para detener el robot:

        ``` { .py .no-copy }
        self.motion.stop()
        ```
   
    1. **Obtener datos del LiDAR** (como se discutió anteriormente) se logra suscribiéndose al topic `/scan`. Lo que esperamos que hayas identificado justo antes de comenzar este ejercicio es que el topic `/scan` nos proporciona datos del LiDAR en un formato definido como `sensor_msgs/msg/LaserScan`. Esta es una estructura de datos bastante compleja, así que para facilitar las cosas durante este laboratorio, hemos hecho todo el trabajo duro por ti, dentro de otra clase llamada `Lidar` (también importada anteriormente). Esta clase se instancia en la línea 15:

        ```python
        self.lidar = Lidar(self)
        ```

        Esta clase `Lidar` divide los datos del sensor LiDAR en varios segmentos para enfocarse en varias zonas distintas alrededor del cuerpo del robot (para hacer que los datos sean un poco más fáciles de manejar). Para cada uno de los segmentos (como se muestra en la figura a continuación) se puede obtener un único valor de distancia, que representa la distancia promedio a cualquier objeto(s) dentro de esa zona angular particular:

        <figure markdown>
          ![](./lab2/lidar_segments.png){width=500px}
        </figure>

        En nuestro código, podemos obtener la medición de distancia (en metros) de cada una de las zonas anteriores de la siguiente manera:

        1. `#!py self.lidar.distance.front` para obtener la distancia promedio a cualquier objeto(s) dentro de la zona *"Front"*.
        1. `#!py self.lidar.distance.l1` para obtener la distancia promedio a cualquier objeto(s) ubicado dentro de la zona LiDAR *"L1"*.
        1. `#!py self.lidar.distance.r1` para obtener la distancia promedio a cualquier objeto(s) ubicado dentro de la zona LiDAR *"R1"*.
            y así sucesivamente...
    
    1. La plantilla de código ha sido desarrollada para detectar una pared en el *lado izquierdo* del robot.
        1. Usamos mediciones de distancia de las zonas LiDAR L3 y L4 para determinar la alineación del robot con una pared a la izquierda.
        1. Esto se determina calculando la diferencia entre las mediciones de distancia reportadas de estas dos zonas:

            ```python
            wall_slope = self.lidar.distance.l3 - self.lidar.distance.l4
            ```

        1. Esta es una *diferencia espacial* entre los rayos LiDAR `l3` y `l4`, y puede usarse como una medida simple de la pendiente local de la pared o el desplazamiento relativo entre el robot y la pared.
        
            Si este valor está cerca de cero, entonces el robot y la pared están bien alineados. Si no, entonces el robot está en ángulo con respecto a la pared, y necesita ajustar su velocidad angular para corregir esto:

            <figure markdown>
              ![](./lab2/wall_slope.png){width=500px}
            </figure>  

1. Ejecuta el node tal como está, desde **TERMINAL 3**:

    ***
    **TERMINAL 3**:
    ```bash
    ros2 run amr31001_lab2 ex2.py
    ```
    ***

    Cuando hagas esto, notarás que el robot no se mueve en absoluto (¡aún!), pero los siguientes datos aparecen en la terminal:
    
    1. Las mediciones de distancia de cada una de las zonas LiDAR.
    1. El valor actual del parámetro `wall_slope`, es decir, qué tan bien alineado está actualmente el robot con una pared en su lado izquierdo.
    1. La decisión que ha tomado la instrucción `#!py if` sobre la acción apropiada que debe tomarse, dado el valor actual de `wall_slope`.

1. Ahora observa el código.

    1. El método de clase `follow_wall()` es llamado repetidamente a una tasa controlada. Esto se estableció en el método de clase `#!py __init__()`:
    
        ```py
        self.create_timer(
            timer_period_sec=0.1, # (1)!
            callback=self.follow_wall, # (2)!
        )
        ```

        1. La tasa a la que ejecutar una *"función de callback"*. Nota: definida en términos de *período* (en segundos), no *frecuencia* (en Hz).
        2. La función de callback a ejecutar a la tasa especificada, es decir, `follow_wall()`.

    1. El método de clase `follow_wall()` es esencialmente la parte principal de nuestro código: una serie de operaciones que se llamarán repetidamente a una tasa especificada.

        **¡Esta es la parte del código que necesitarás modificar!**

1. **Adaptar el código**:

    1. Primero, modifica el cálculo de `wall_slope` para que el robot observe una pared en su *lado derecho* **NO** en el izquierdo.

    1. **¡Asegúrate de guardar cualquier cambio en el código (en VS Code) antes de intentar probarlo en el robot!**
        
        Haz esto usando el atajo de teclado ++ctrl+s++, o yendo a `File` > `Save` desde el menú en la parte superior de la pantalla.

    1. A continuación, coloca el robot en el suelo con una pared a su derecha.
    1. Varía manualmente la alineación del robot y la pared y observa cómo la información que se imprime en la terminal cambia a medida que lo haces.
        
        !!! note "Pregunta"
            El node te dirá si cree que el robot necesita girar a la derecha o a la izquierda para mejorar su alineación actual con la pared. **¿Está tomando la decisión correcta?**

    1. Actualmente, todos los parámetros de velocidad dentro del método `#!py follow_wall()` están establecidos en cero.
        * Necesitarás establecer una velocidad *lineal* constante, para que el robot siempre esté avanzando. Establece un valor apropiado para esto ahora, editando la línea que actualmente dice:

            ```python
            lin_vel = 0.0
            ```
        
        * La velocidad *angular* del robot deberá ajustarse condicionalmente, para garantizar que el valor de `wall_slope` se mantenga lo más bajo posible en todo momento (es decir, el robot se mantiene alineado con la pared).
        
        Ajusta el valor de `ang_vel` en cada uno de los bloques de instrucción `#!py if` para que esto se logre bajo cada uno de los tres posibles escenarios.

    1. Con suerte, siguiendo los pasos anteriores, llegarás al punto en que puedas hacer que el robot siga una pared derecha razonablemente bien, ¡siempre que la pared permanezca razonablemente recta! Sin embargo, considera qué sucedería si el robot se enfrentara a alguna de las siguientes situaciones:

        <figure markdown>
          ![](./lab2/limitations.png){width=600px}
        </figure>

        Es posible que ya hayas observado esto durante tus pruebas... ¿cómo podrías adaptar el código para que tales situaciones puedan manejarse?

        ??? info "Pistas"
            
            1. ¡Es posible que debas considerar las mediciones de distancia de algunas otras zonas LiDAR!
            1. La plantilla `ex3.py` que se te proporcionó usa una instrucción `if` con tres casos diferentes:
                
                ```python
                if ...:

                elif ...:

                else:

                ```

                Es posible que debas agregar algunos casos adicionales para acomodar las situaciones adicionales discutidas anteriormente, por ejemplo:

                ```python
                if ...:

                elif ...:
                
                elif ...:
                
                elif ...:
                
                else:
                
                ```
    
    !!! info "Post-lab"
        Como se discutió anteriormente, ¡tu completitud de este ejercicio será evaluada como parte del post-lab!

### Cámaras y Visión Robótica

Nuestros robots tienen cámaras, dándoles la capacidad de *"ver"* su entorno. Los datos de la cámara pueden usarse como otra señal de retroalimentación para informar el control de lazo cerrado, que ahora aprovecharemos para implementar el *seguimiento de línea*. Lograremos esto usando un algoritmo de control bien establecido conocido como **Control PID**, usando los datos de la cámara de nuestro robot y aplicando algunas técnicas de procesamiento de imagen para detectar y *localizar* una línea de color impresa en el suelo.

Considera la siguiente imagen obtenida de la cámara de un robot, con una línea verde visible en el suelo:

<figure markdown>
  ![](./lab2/line_following/overview.png){width=600px}
</figure>

El Control PID es un algoritmo inteligente que tiene como objetivo minimizar el **Error** entre una **Referencia de Entrada**: una condición deseada que nos gustaría que mantuviera nuestro robot; y una **Señal de Retroalimentación**: la condición en la que se encuentra actualmente el robot (basada en datos del mundo real). El algoritmo PID calcula una **Salida de Control** apropiada para nuestro sistema que (cuando se sintoniza apropiadamente) actuará para minimizar este error.

Si queremos que nuestro robot siga con éxito una línea de color en el suelo, necesitará mantener esa línea en el centro de su campo visual en todo momento minimizando el **error** entre dónde está actualmente la línea (la **señal de retroalimentación**) y dónde debería estar (la **referencia de entrada**, es decir, el centro de su campo visual). En este caso, el algoritmo PID nos proporciona un comando de velocidad angular (la **salida de control**) para lograr esto.

El algoritmo PID completo es el siguiente:

$$
u(t)=K_{P} e(t) + K_{I}\int e(t)dt + K_{D}\dfrac{d}{dt}e(t)
$$

Donde $u(t)$ es la **Salida de Control**, $e(t)$ es el **Error** (como se ilustra en la figura anterior) y $K_{P}$, $K_{I}$ y $K_{D}$ son las **Ganancias** Proporcional, Integral y Diferencial respectivamente, que tienen diferentes efectos en un sistema en términos de su capacidad para mantener el estado deseado (la referencia de entrada). Debemos establecer valores apropiados para estas ganancias mediante un proceso llamado *sintonización*.

De hecho, para permitir que nuestro TurtleBot3 siga una línea, realmente solo necesitamos una ganancia *proporcional*, por lo que nuestro algoritmo de control puede simplificarse considerablemente:

$$
u(t)=K_{P} e(t)
$$

Esto es lo que se denomina un **Controlador "P"**, y la única ganancia que necesitamos establecer aquí es $K_{P}$.

#### :material-pen: Ejercicio 3: Seguimiento de línea {#ex3}

##### Parte A: Establecer una Señal de Retroalimentación (Detectar la Línea) {#ex3a}

1. Lanza RViz nuevamente en **TERMINAL 3**:

    ***
    **TERMINAL 3**:
    ```bash
    ros2 launch tuos_tb3_tools rviz.launch.py environment:=real
    ```
    ***

1. En el menú "Displays" del lado izquierdo, marca la casilla junto al elemento "Camera". Las imágenes en vivo de la cámara del robot deberían mostrarse entonces en la esquina inferior izquierda de la ventana de RViz.

1. Coloca el robot en el área para que la línea en el suelo sea visible en la visión del robot.

1. Ahora, lanza el node `ex3_colour_detection.py` en **TERMINAL 4**:

    ***
    **TERMINAL 4**:
    ```
    ros2 run amr31001_lab2 ex3_colour_detection.py
    ```
    ***

    Después de una breve pausa, debería abrirse una ventana que muestre un diagrama de dispersión junto con una imagen sin procesar obtenida de la cámara del robot.

    <figure markdown>
      ![](./lab2/line_following/hsv_cam_img.png){width=700px}
    </figure>

    El diagrama de dispersión muestra todos los diferentes colores que están presentes en la imagen de la cámara sin procesar. Estos se representan en términos de los valores de *Matiz* (Hue) y *Saturación* de cada píxel en la imagen.
    
1. En el gráfico, deberías poder identificar un grupo de puntos de datos del mismo color que la línea en el suelo. Del gráfico, toma nota del rango de valores de Matiz y Saturación dentro de los que residen estos puntos.
    
    <figure markdown>
      ![](./lab2/line_following/hsv_plot.png){width=500px}
    </figure>

1. Una vez que hayas hecho esto, cierra la figura haciendo clic en el ícono :material-close-circle: en la esquina superior derecha, y también cierra la ventana de RViz. Esto debería liberar **TERMINAL 3** y **TERMINAL 4**.

##### Parte B: Implementar el Control Proporcional (Seguir la Línea) {#ex3b}

1. En VS Code, haz clic en el archivo `ex3_line_following.py` en el Explorador de Archivos para mostrarlo en el editor.

1. Revisa el código y trata de entender qué está pasando. Aquí hay algunos puntos para comenzar:

    1. Una vez más, el control de velocidad se maneja de la misma manera que en el ejercicio anterior, usando la clase `#!py Motion()` y llamadas a `#!py self.motion.move_at_velocity()` y `#!py self.motion.stop()`.
    
    1. Los datos de la cámara del robot son manejados una vez más por una clase separada (muy similar a `Lidar` en el ejercicio anterior). Esta (instanciada en la línea 15) se llama `Camera`:

        ```python
        self.camera = Camera(self)
        ```

        Veremos cómo usarla en breve...
    
1. La parte *"principal"* del código está nuevamente controlada por un temporizador y una función de "callback".
    
    !!! info "Cuestionario Post-lab"

        * ¿Cuál es el nombre de la función de callback (también conocida como el método de control "principal")?
        * ¿A qué tasa (en Hz) se ejecutará?

1. Ejecuta el node tal como está, desde **TERMINAL 3**:

    ***
    **TERMINAL 3**:
    ```
    ros2 run amr31001_lab2 ex3_line_following.py
    ```
    ***

    Al principio, el robot no debería hacer nada, pero debería abrirse una ventana que muestre una transmisión en vivo de la cámara del robot. También deberías ver un pequeño círculo azul flotando en algún lugar de la imagen.
    
    Asegúrate de que la línea en el suelo sea visible para el robot antes de continuar.

1. Detén el node con ++ctrl+c++.

1. En VS Code, localiza la línea en el archivo `ex3_line_following.py` que dice:

    ``` { .py .no-copy }
    self.camera.colour_filter()
    ```

    En esta, puedes proporcionar los rangos de Matiz y Saturación que identificaste en la [Parte A](#ex3a):

    ``` { .py .no-copy }
    self.camera.colour_filter(
        hue=[MIN, MAX],
        saturation=[MIN, MAX]
    )
    ```
    
    Reemplaza `MIN` y `MAX` con tus valores superiores e inferiores de matiz y saturación.

1. Ejecuta el código nuevamente. Si tus rangos de Matiz y Saturación son correctos y la línea está visible, ahora debería quedar aislada en la imagen (todos los demás píxeles en la transmisión de la cámara deberían ser negros).

    El pequeño círculo azul también debería estar ubicado aproximadamente en el centro de la línea. Si mueves el robot ahora (manteniendo la línea a la vista) el círculo azul debería moverse con la línea, indicando que la línea está siendo detectada exitosamente por tu filtrado y los algoritmos de procesamiento de imagen.

    <figure markdown>
      ![](./lab2/line_following/line_filtered.png){width=400px}
    </figure>

    Si la línea *no* se aísla exitosamente, [vuelve a la Parte A](#ex3a) y ejecuta el node `ex3_colour_detection.py` nuevamente.

1. El robot ahora puede localizar la posición de la línea en su campo visual, por lo que hemos establecido exitosamente la **Señal de Retroalimentación** para nuestro controlador proporcional. En el código, se puede acceder a esto de la siguiente manera:

    ```py
    self.camera.line_position_pixels
    ```

    Considera la figura de antes, nuevamente:

    <figure markdown>
      ![](./lab2/line_following/overview.png){width=500px}
    </figure>

    En nuestro código, ahora podemos usar esto para calcular el error posicional actual del robot. Localiza las líneas que dicen:

    ``` { .py .no-copy }
    reference_input = self.camera.image_width / 2
    error = 0.0 # TODO
    ```

    ... y edita la línea `#!py error = ...` para calcular correctamente el error posicional del robot basándose en la posición en tiempo real de la línea en su campo visual (`#!py self.camera.line_position_pixels`).

1. La Velocidad Angular es la **Salida de Control** de nuestro Controlador P, calculada (una vez más) según:
    
    $$
    u(t)=K_{P} e(t)
    $$

    Esto se refleja en el código por la línea que dice:

    ```py
    ang_vel = kp * error
    ```

    Modifica la línea `#!py self.motion.move_at_velcity()` en el código para aplicar esta velocidad angular al robot junto con una velocidad lineal constante (y *moderada*) también.

1. Finalmente, sintoniza el Controlador P identificando una ganancia proporcional `kp` apropiada para que el robot siga la línea de manera suave y consistente.

    !!! info "Post-lab"
        Como se discutió anteriormente, ¡tu completitud de este ejercicio será evaluada como parte del post-lab!

Si has terminado con tiempo de sobra, continúa con el Ejercicio 4 a continuación. Si no tienes tiempo, dirígete a la sección [Cierre](#wrapping-up).

#### :material-pen: (Opcional) Ejercicio 4: Navegación basada en Odometría {#ex4}

De nuestro trabajo en el [Ejercicio 1](#ex1) sabemos sobre el sistema de odometría del robot y qué nos dice. Veamos cómo esto podría usarse como señal de retroalimentación para informar la navegación del robot. Recordarás que cuando estuviste aquí por última vez para el [Lab 1](lab1.md) creaste un Node de ROS para hacer que tu robot siguiera una trayectoria cuadrada en el suelo. Sin embargo, esto estaba basado en tiempo: para una velocidad de movimiento dada (girando o avanzando), ¿cuánto tiempo tardaría el robot en moverse la distancia requerida? Habiendo determinado esto, luego usamos temporizadores para controlar la ejecución de dos estados de movimiento diferentes: avanzar y girar sobre sí mismo, para generar la trayectoria cuadrada (aproximadamente).

En teoría, sin embargo, podemos hacer todo esto de manera mucho más efectiva con datos de odometría, así que intentémoslo ahora...

1. Regresa a VS Code y abre el archivo `ex4.py` en el editor.

1. Revisa el código y trata de entender qué está pasando. Aquí hay algunos puntos para comenzar:

    1. El control de velocidad se maneja de la misma manera que en el ejercicio anterior:

        1. Para hacer que el robot se mueva con una velocidad lineal de `x` (m/s) y/o una velocidad angular de `y` (rad/s):

            ```py
            self.motion.move_at_velocity(
                linear = x, angular = y
            )
            ```

        1. Para hacer que el robot se detenga:

            ```py
            self.motion.stop()
            ```

    1. Obtener los datos de Odometría del robot está nuevamente manejado por una clase Python separada similar a `Lidar` y `Camera` en los ejercicios anteriores. Esta se llama `Pose`, y se instancia en la línea 16:

        ```python
        self.pose = Pose(self)
        ```

        Luego podemos llamar al objeto `#!py self.pose` para acceder a los datos de odometría del robot, llamando al atributo apropiado cuando lo necesitemos:

        1. `#!py self.pose.posx` para obtener la posición actual del robot (en metros) en el eje `X`.
        1. `#!py self.pose.posy` para obtener la posición actual del robot (en metros) en el eje `Y`.
        1. `#!py self.pose.yaw` para obtener la orientación actual del robot (en grados) alrededor del eje `Z`.

1. Ejecuta el código en **TERMINAL 3** y observa qué sucede:

    ***
    **TERMINAL 3**:
    ```bash
    ros2 run amr31001_lab2 ex4.py
    ```
    ***

    El robot debería comenzar a girar sobre sí mismo, y deberías ver información interesante imprimiéndose en la terminal. Después de haber girado 45°, el robot debería detenerse.

1. Detén el Node presionando ++ctrl+c++ en **TERMINAL 3** y luego ejecútalo nuevamente si perdiste lo que sucedió la primera vez.

1. **Lo que necesitas hacer**:

    1. La parte *"principal"* del código está nuevamente controlada por un temporizador:
    
        ```py
        self.create_timer(
            timer_period_sec=0.05,
            callback=self.move_square,
        )
        ```

    1. El método de clase `move_square()` es esencialmente la parte principal de nuestro código: una serie de operaciones que se llamarán repetidamente a una tasa especificada.

        Dentro de este hay una instrucción `#!py if` que controla si el robot debe girar o avanzar:
    
        ```python
        if self.turn:
            # Estado de Giro
            ...
        else:
            # Avanzando 
            ...
        ```

        ... donde `#!py self.turn` es un booleano cuyo valor puede ser `#!py True` o `#!py False`.
        
    1. Dentro de esto, mira qué sucede en el `Estado de Giro`. Considera cómo se monitorea y actualiza el ángulo de yaw del robot mientras gira. Luego, mira cómo se controla el ángulo de giro. Ve si puedes adaptar esto para asegurarte de que el robot gire 90°.

    1. En última instancia, después de que el robot ha girado el ángulo deseado, necesita avanzar 0.5m para lograr una trayectoria cuadrada de 0.5x0.5m.
        
        El avance se maneja en el estado `Avanzando`.

        Ve si puedes adaptar el código dentro de este bloque para hacer que el robot avance la cantidad requerida (0.5 metros) entre cada giro. <a name="the_hint"></a>
        
        ??? note "Pista"
            Considera cómo se monitorea y actualiza el ángulo de giro mientras gira (`current_yaw`), y adopta un enfoque similar con el desplazamiento lineal (`current_distance`). Ten en cuenta que necesitarás considerar la *distancia euclidiana*, que necesitarás calcular basándote en la posición del robot tanto en el eje `x` como en el `y`.
        
            <figure markdown>
              ![](./lab2/euclidean_distance.png){width=500px}
            </figure>

        ??? tip "Consejos de Python"

            Necesitarás hacer un poco de matemáticas aquí (consulta [la "Pista" anterior](#the_hint)). Así es como implementar un par de funciones matemáticas en Python:

            1. **A la potencia de X**:
                
                Usa `**` para elevar un número a la potencia de otro número (es decir, $2^{3}$):

                ```py
                >>> 2**3
                8
                ``` 

                O usa el método `#!py pow()`:

                ```py
                >>> pow(2, 3)
                8
                ```

            1. **Raíz Cuadrada**:
                
                Para calcular la raíz cuadrada de un número (es decir, $\sqrt{4}$):

                ```py
                >>> sqrt(4)
                2.0 
                ```        

## Cierre

Antes de irte, por favor apaga todo correctamente:

1. Presiona ++ctrl+c++ en cualquier terminal que todavía esté activa.
1. Apaga tu robot ingresando el siguiente comando en **TERMINAL 1**:

    ***
    **TERMINAL 1**:
    ``` { .bash .no-copy }
    waffle NUM off
    ```
    ... reemplazando `NUM` con el número del robot con el que has estado trabajando hoy.
    ***

    Necesitarás ingresar `y` y luego presionar ++enter++ para confirmar.

1. Luego apaga la laptop, lo cual puedes hacer haciendo clic en el ícono de batería en la parte superior derecha del escritorio y seleccionando la opción "Power Off / Log Out" en el menú desplegable.

<figure markdown>
  ![](../images/laptops/ubuntu_poweroff.svg){width=300px}
</figure>

<center>

**¡Lab 2 de Industry 4.0 Completado!**

</center>
