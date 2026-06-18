---  
title: "Waffle (& ROS) Básico"  
---

# Waffle (& ROS) Básico

Habiendo completado los pasos de [la página anterior](./launching-ros.md), tu robot y laptop ya deben estar emparejados y ROS debe estar en funcionamiento (en el robot). ¡Ahora estás listo para darle vida al robot!

En esta página encontrarás una serie de ejercicios para trabajar, ver cómo funcionan los robots, explorar algunos conceptos fundamentales de ROS y utilizar herramientas clave de ROS, en caso de que aún no hayas tenido la oportunidad de explorarlas en simulación.

### Enlaces Rápidos

* [Ejercicio 1: Hacer que el Robot se Mueva](#exMove)
* [Ejercicio 2: Ver los Sensores en Acción](#exViz)
* [Ejercicio 3: Visualizar la Red de ROS](#exNet)
* [Ejercicio 4: Explorar Topics e Interfaces de ROS](#exTopicMsg)
* [Ejercicio 5: Un Nodo de Control de Velocidad en Python](#exSimpleVelCtrl)
* [Ejercicio 6: Usar SLAM para crear un mapa del entorno](#exSlam)

## Control Manual

#### :material-pen: Ejercicio 1: Hacer que el Robot se Mueva {#exMove}

Existe una aplicación ROS ya lista muy útil llamada `teleop_keyboard` (del paquete `turtlebot3_teleop`) que usaremos para conducir un Waffle. ¡Este nodo funciona exactamente de la misma manera tanto en simulación como en el mundo real!

1. Ya deberías tener dos instancias de terminal activas:

    * **TERMINAL 1**: La terminal del *robot* con los procesos de *"bringup"* en ejecución ([Lanzando ROS, Paso 3](./launching-ros.md#step3))
    * **TERMINAL 2**: La terminal de la *laptop* con el nodo `rmw_zenohd` en ejecución ([Lanzando ROS, Paso 4](./launching-ros.md#step4))

1. Abre una nueva instancia de terminal en la laptop usando el atajo de teclado ++ctrl+alt+t++ o haciendo clic en el ícono de la aplicación Terminal; la llamaremos **TERMINAL 3**. En esta terminal, ingresa el siguiente comando `ros2 run` para iniciar el nodo `teleop_keyboard`:

    ```bash
    ros2 run turtlebot3_teleop teleop_keyboard
    ```
    
1. Sigue las instrucciones que aparecen en la terminal para conducir el robot utilizando teclas específicas del teclado:

    <figure markdown>
      ![](../images/cli/teleop_keymap.svg)
    </figure>

    !!! warning 
        ¡Ten cuidado de evitar obstáculos y otras personas en el laboratorio mientras haces esto!

2. Una vez que hayas pasado un tiempo con esto, cierra la aplicación ingresando ++ctrl+c++ en **TERMINAL 3**.

## Paquetes y Nodos

Las aplicaciones ROS se organizan en *paquetes*. Los paquetes son básicamente carpetas que contienen scripts, configuraciones y archivos de lanzamiento (formas de iniciar esos scripts y configuraciones).

Los *scripts* le indican al robot qué hacer y cómo actuar. En ROS, estos scripts se llaman *nodos*. Los *Nodos de ROS* son programas ejecutables que realizan tareas y operaciones específicas del robot. Típicamente están escritos en C++ o Python, aunque también es posible escribir Nodos de ROS en otros lenguajes de programación.

Hay dos formas principales de lanzar aplicaciones ROS:

1. `ros2 launch`
1. `ros2 run`

Recuerda que acabamos de usar el comando `ros2 run` en el Ejercicio 1 para lanzar el nodo `teleop_keyboard`. Este comando tiene la siguiente estructura:

``` { .bash .no-copy }
ros2 run {[1] Nombre del paquete} {[2] Nombre del nodo}
```    

La **Parte [1]** especifica el nombre del *paquete de ROS* que contiene la funcionalidad que queremos ejecutar. La **Parte [2]** se usa para especificar un *único* script dentro de ese paquete que queremos ejecutar. Por lo tanto, usamos comandos `ros2 run` para lanzar **ejecutables individuales** (también conocidos como *Nodos*) en la red ROS (en el Ejercicio 1, por ejemplo, lanzamos el nodo `teleop_keyboard`).

El comando `ros2 launch` tiene una estructura *similar*:

``` { .bash .no-copy }
ros2 launch {[1] Nombre del paquete} {[2] Archivo de lanzamiento}
```

Aquí, la **Parte [1]** es igual que en el comando `ros2 run`, pero la **Parte [2]** es ligeramente diferente: `{[2] Archivo de lanzamiento}`. En este caso, la **Parte [2]** es un archivo dentro de ese paquete que especifica cualquier número de Nodos que queremos lanzar en la red ROS. Por lo tanto, podemos lanzar *múltiples* nodos al mismo tiempo desde un único archivo de lanzamiento.

## Sensores y Herramientas de Visualización

Nuestros Waffles tienen sensores bastante sofisticados que les permiten "ver" el mundo a su alrededor. Ahora veamos lo que nuestro robot percibe, usando algunas herramientas útiles de ROS.

#### :material-pen: Ejercicio 2: Ver los Sensores en Acción {#exViz}

1. No debería haber nada ejecutándose en **TERMINAL 3** ahora, después de que cerraste el nodo `teleop_keyboard` (usando ++ctrl+c++) al final del ejercicio anterior. Regresa a esta terminal e ingresa el siguiente comando:

    ```bash
    ros2 launch rigsa_tb3_tools rviz.launch.py
    ```
    
    Esto lanzará una aplicación llamada *RViz*, una herramienta muy útil que nos permite *visualizar* los datos de todos los sensores a bordo de nuestros robots. Cuando RViz se abra, deberías ver algo similar a lo siguiente:

    <figure markdown>
      ![](../images/laptops/waffle_rviz.png){width=700px}
    </figure>

    Haz clic en la casilla junto a *"Camera"* en la lista de *"Displays"* para habilitar la suscripción a la cámara. Luego debería aparecer una transmisión en vivo de la cámara del robot en el panel *Camera* en la parte inferior izquierda.
    
1. En el panel principal de RViz deberías ver un modelo digital del robot, rodeado por muchos puntos verdes. Esta es una representación de los *datos de desplazamiento láser* provenientes del sensor LiDAR (el dispositivo negro en la parte superior del robot). El sensor LiDAR gira continuamente, enviando pulsos láser al entorno mientras lo hace. Cuando un pulso alcanza un objeto, se refleja de vuelta al sensor, y el tiempo que tarda este proceso se usa para calcular a qué distancia está el objeto.
    
    El sensor LiDAR gira y realiza este proceso de forma continua, por lo que se puede generar un escaneo completo de 360&deg; del entorno. Por lo tanto, estos datos son muy útiles para cosas como *evasión de obstáculos* y *mapeo*.

1. Coloca tu mano frente al robot y observa si la posición de los puntos verdes cambia para coincidir con la ubicación de tu mano. Mueve tu mano hacia arriba y hacia abajo y considera a qué altura el sensor LiDAR puede detectarla.

1. Luego, acerca y aleja tu mano y observa cómo los puntos verdes se mueven para reflejar esto.

1. Abre una nueva instancia de terminal (**TERMINAL 4**) y lanza el nodo `teleop_keyboard` como lo hiciste en el Ejercicio 1. Observa cómo cambian los datos en la pantalla de RViz mientras conduces el robot.

#### :material-pen: Ejercicio 3: Visualizar la Red de ROS {#exNet}

Al usar `ros2 run` y `ros2 launch` como hemos hecho hasta ahora, es fácil terminar con muchos procesos o *Nodos de ROS* diferentes ejecutándose en la red, algunos de los cuales interactuaremos con ellos, pero otros pueden simplemente estar ejecutándose en segundo plano. A menudo es útil saber exactamente qué *está* ejecutándose en la red ROS, y hay varias formas de hacer esto.

1. Abre una nueva instancia de terminal ahora (**TERMINAL 5**) y desde aquí usa el comando `ros2 node` para *listar* los nodos que están ejecutándose actualmente:

    ```bash
    ros2 node list
    ```
    
    Como *mínimo*, deberías ver la siguiente lista: 
    
    ``` { .txt .no-copy }
    /camera
    /diff_drive_controller
    /hlds_laser_publisher
    /robot_state_publisher
    /tb3_status_node
    /turtlebot3_node
    ```

2. Podemos visualizar las conexiones entre los nodos activos usando un nodo de ROS llamado `rqt_graph`. En la misma terminal, inícialo de la siguiente manera:

    ```bash
    rqt
    ```
    
    Debería abrirse una ventana:

    <figure markdown>
      ![](../images/rqt/main.png){width=600}
    </figure>

1. Desde aquí, queremos cargar el plugin *Node Graph*. En el menú superior selecciona `Plugins` > `Introspection` > `Node Graph`.

    ??? tip "Atajo"
        También puedes lanzar el nodo `rqt_graph` directamente con `ros2 run`:
        
        ```bash
        ros2 run rqt_graph rqt_graph
        ```

1. En la ventana que se abre, selecciona `Nodes/Topics (active)` en el menú desplegable de la parte superior izquierda.

    Lo que deberías ver entonces es un mapa de todos los nodos de la lista anterior (como óvalos) y flechas que ilustran el flujo de información entre ellos. ¡Esta es una representación visual de la red ROS!

    <figure markdown>
      ![](../images/rqt/graph_waffle.png){width=600px}
    </figure>
    
    Los elementos con borde rectangular son *ROS Topics*. Los ROS Topics son esencialmente canales de comunicación, y los Nodos de ROS pueden leer (*suscribirse*) o escribir (*publicar*) en estos topics para acceder a datos de sensores, pasar información por la red y hacer que sucedan cosas.

    Si el Nodo `teleop_keyboard` aún está activo (en **TERMINAL 4**), el gráfico debería mostrarnos que este nodo está publicando mensajes en un topic llamado `/cmd_vel`, al cual a su vez se suscribe `turtlebot3_node`.

    <figure markdown>
      ![](../images/rqt/graph_waffle_teleop.png){width=600px}
    </figure>

    Este nodo se ejecuta en el robot y controla su velocidad. Le enviamos instrucciones (publicando en el topic `/cmd_vel`) para hacer que el robot se mueva.

Un Robot ROS podría tener cientos de nodos individuales ejecutándose simultáneamente para llevar a cabo todas sus operaciones y acciones necesarias. Cada nodo se ejecuta de forma independiente, pero utiliza *métodos de comunicación de ROS* para comunicarse y compartir datos con los demás nodos en la Red ROS.

## Publishers y Subscribers: Un *Método de Comunicación de ROS*

Los ROS Topics son fundamentales para hacer que las cosas sucedan en un robot. Los Nodos pueden publicar (*escribir*) y/o suscribirse (*leer*) a ROS Topics para compartir datos en la red ROS. Los datos se publican en los topics a través de *interfaces de tipo mensaje*.

Veamos esto con un poco más de detalle...

#### :material-pen: Ejercicio 4: Explorar Topics e Interfaces de ROS {#exTopicMsg}

Al igual que el comando `ros2 node list`, podemos usar `ros2 topic list` para listar todos los *topics* que están actualmente activos en la red ROS.

1. Cierra la ventana de RQT Graph si aún no lo has hecho. Esto liberará **TERMINAL 5** para que podamos ingresar comandos en ella nuevamente. Regresa a esta ventana de terminal e ingresa lo siguiente:

    ```bash
    ros2 topic list
    ```
    
    Ahora debería imprimirse una nueva lista de elementos en la terminal. Intenta identificar el elemento `/cmd_vel` en la lista.
    
    Como aprendimos antes, este topic se usa para controlar la velocidad del robot (*'velocidad de comando'*).

1. Obtengamos más información sobre esto usando el comando `ros2 topic info`.

    ```bash
    ros2 topic info /cmd_vel
    ```
    
    Esto debería proporcionar una salida similar a la siguiente: 
    
    ``` { .txt .no-copy }
    Type: geometry_msgs/msg/TwistStamped
    Publisher count: 1
    Subscription count: 1
    ```

    Esto nos dice que el *tipo* de datos que se comunican en el topic `/cmd_vel` se llama: `geometry_msgs/msg/TwistStamped`.
    
    La descripción de la interfaz tiene tres partes:

    1. `geometry_msgs`: El nombre del paquete de ROS al que pertenece esta interfaz.
    1. `msg`: El tipo de interfaz. En este caso *mensaje*, pero también hay otros tipos.
    1. `TwistStamped`: El nombre de la interfaz de mensaje.

    Así, acabamos de aprender que si queremos hacer que el robot se mueva, necesitamos publicar mensajes `TwistStamped` en el topic `/cmd_vel`.

1. Podemos usar el comando `ros2 interface` para obtener más información sobre el mensaje `TwistStamped`:

    ```bash
    ros2 interface show geometry_msgs/msg/TwistStamped
    ```
    
    Con esto deberíamos obtener lo siguiente:

    ``` { .txt .no-copy }
    std_msgs/Header header
            builtin_interfaces/Time stamp
                    int32 sec
                    uint32 nanosec
            string frame_id
    Twist twist
            Vector3  linear
                    float64 x
                    float64 y
                    float64 z
            Vector3  angular
                    float64 x
                    float64 y
                    float64 z
    ```

    Aquí tenemos una lista de campos, subcampos y tipos de datos. La interfaz tiene dos *campos base* (indicados por las líneas que no están indentadas):

    <center>

    | # | *Nombre* del Campo | *Tipo* del Campo |
    | :---: | :---: | :---: |
    | 1 | `header` | `std_msgs/Header` |
    | 2 | `twist` | `Twist` |
    
    </center>
    
    De los anteriores, nos interesa principalmente el *Campo 2*, que contiene dos subcampos adicionales:
    
    <center>

    | # | *Nombre* del Campo | *Tipo* del Campo |
    | :---: | :---: | :---: |
    | 1 | `linear` | `Vector3` |
    | 2 | `angular` | `Vector3` |
    
    </center>

    Cada uno de *estos* contiene 3 *subcampos adicionales*: `x`, `y` y `z`:

    <center>

    | # | Nombre del Campo | Tipo de Dato |
    | :---: | :---: | :---: |
    | 1 | `x` | `float64` |
    | 2 | `y` | `float64` |
    | 3 | `z` | `float64` |

    </center>

    Veamos qué significa todo esto...

## Control de Velocidad

El movimiento de cualquier robot móvil puede definirse en términos de sus tres *ejes principales*: `X`, `Y` y `Z`. En el contexto de nuestro TurtleBot3 Waffle, estos ejes (y el movimiento en torno a ellos) se definen de la siguiente manera:

<figure markdown>
  ![](../images/waffle/principal_axes.svg){width=600}
</figure>

En teoría, un robot puede moverse *linealmente* o *angularmente* en cualquiera de estos tres ejes, como se muestra con las flechas en la figura. Eso son seis *Grados de Libertad* (GDL) en total, logrados según el diseño del robot y los actuadores con que cuenta. Vuelve a mirar la salida de `ros2 interface show` mostrada anteriormente. Esperamos que ahora quede más claro que el subcampo `twist` de la interfaz `TwistStamped` está formateado para darle a un programador de ROS la capacidad de *pedirle* a un robot que se mueva en cualquiera de sus seis GDL.

``` { .txt .no-copy }
Vector3  linear
        float64 x  <-- Adelante (o Atrás)
        float64 y  <-- Izquierda (o Derecha)
        float64 z  <-- Arriba (o Abajo)
Vector3  angular
        float64 x  <-- "Balanceo" (Roll)
        float64 y  <-- "Cabeceo" (Pitch)
        float64 z  <-- "Guiñada" (Yaw)
```

¡Nuestro robot TurtleBot3 solo tiene dos motores, por lo que en realidad no tiene seis GDL! Los dos motores pueden controlarse de forma independiente, lo que le da lo que se llama una configuración de *"tracción diferencial"*, pero aun así solo le permite moverse con **dos grados de libertad** en total, como se ilustra a continuación.

<figure markdown>
  ![](../images/waffle/velocities.svg){width=600}
</figure>

Por lo tanto, solo puede moverse **linealmente** en el **eje x** (*Adelante/Atrás*) y **angularmente** en el **eje z** (*Guiñada*).

#### :material-pen: Ejercicio 5: Un Nodo de Control de Velocidad en Python {#exSimpleVelCtrl}

!!! important
    Antes de comenzar, asegúrate de que no haya nada ejecutándose en **TERMINAL 3**, **4** ni **5** (ingresa ++ctrl+c++ en cada una de estas terminales para detener cualquier proceso que pueda estar ejecutándose allí).

Como hemos visto, hacer que un robot se mueva con ROS es simplemente publicar los datos correctos (`geometry_msgs/msg/TwistStamped`) en el topic de ROS correcto (`/cmd_vel`). Anteriormente usamos el nodo `teleop_keyboard` para conducir el robot, un poco como un auto de control remoto. En el fondo, lo que realmente ocurría era que el nodo convertía las pulsaciones de teclas del teclado en comandos de velocidad y los publicaba en el topic `/cmd_vel`.

En la realidad, los robots necesitan ser capaces de navegar entornos complejos de forma autónoma, lo cual es una tarea bastante difícil y requiere que construyamos aplicaciones a medida. Podemos construir estas aplicaciones usando Python, y veremos los conceptos fundamentales detrás de esto ahora, construyendo un nodo simple que le permitirá a nuestro robot ser un poco más "autónomo". ¡Lo que haremos aquí forma la base de las aplicaciones más complejas que aprenderás durante el curso de laboratorio!

1. Anteriormente hablamos de cómo los Nodos de ROS deben estar contenidos dentro de paquetes, así que creemos uno ahora usando un script auxiliar que ya hemos preparado. (Esto se cubre con más detalle en el curso de ROS, pero para los propósitos de este ejercicio, simplemente ejecuta el script sin preocuparte demasiado por él.)

    En **TERMINAL 3**, navega al *Espacio de Trabajo de ROS2* en la laptop:

    ```bash
    cd ~/ros2_ws/src/
    ```

1. Desde aquí, usa `git` para *clonar* nuestra *"Plantilla de Paquete ROS 2"* desde GitHub:

    ```bash
    git clone https://github.com/tom-howard/ros2_pkg_template.git
    ```
    
1. Esta plantilla de paquete contiene un script llamado `init_pkg.sh`, que puede ejecutarse para convertir la plantilla en un paquete de ROS 2 real. Ejecuta el script de la siguiente manera, lo que convertirá la plantilla en un paquete de ROS 2 llamado `waffle_demo`:

    ```bash
    ./ros2_pkg_template/init_pkg.sh waffle_demo
    ```

1. Navega al directorio de este nuevo paquete (usando `cd`):

    ```bash
    cd waffle_demo/ 
    ```

1. Este paquete contiene un subdirectorio llamado `scripts`, y dentro de él hay dos nodos básicos para comenzar:

    ```bash
    tree scripts/
    ```
    ``` { .txt .no-copy}
    scripts/
    ├── basic_velocity_control.py
    └── stop_me.py
    ```

1. Abramos nuestro paquete ahora en *Visual Studio Code* (VS Code).

    ```bash
    code .
    ```

    !!! note
        ¡No olvides incluir el `.` al final, es importante!

    
1. A continuación, en el explorador de archivos de VS Code, abre el directorio `scripts`, encuentra el archivo `basic_velocity_control.py` y haz clic en él para abrirlo en el editor.

    <a name="timedSquareCode"></a>

    Este es un Nodo Python de ROS 2 (bastante) básico que controlará la velocidad del robot. Analicemos su contenido:
    
    1. Primero, tenemos algunas importaciones:

        ``` { .py .no-copy }
        import rclpy # (1)!
        from geometry_msgs.msg import TwistStamped # (2)!
        import time # (3)!
        ```

        1. `rclpy` es la biblioteca cliente de ROS para Python. La necesitamos para que nuestro nodo Python pueda interactuar con ROS.
        2. Sabemos de antes que para hacer que un robot se mueva necesitamos publicar mensajes en el topic `/cmd_vel`, y que este topic usa una estructura de datos (o Interfaz) llamada `geometry_msgs/msg/TwistStamped`. Así es como importamos la interfaz a nuestro nodo Python para poder crear comandos de velocidad para nuestro robot (a lo cual llegaremos en breve...).
        3. Usaremos esto para controlar el tiempo en nuestro nodo.

        Haz clic en los íconos :material-plus-circle: para revelar más información sobre cada línea del código.

    1. Luego, declaramos algunas variables que podemos usar y adaptar durante la ejecución principal de nuestro código:

        ``` { .py .no-copy }
        state = 1 # (1)!
        vel = TwistStamped() # (2)!
        ```

        1. Dentro del bucle `#!py while` (explicado en breve) definimos dos estados operativos diferentes para el robot, y podemos controlar cuál está activo cambiando este valor de `1` a `2` (y viceversa).
        2. Aquí estamos instanciando un mensaje de Interfaz `TwistStamped` y lo llamamos `vel`. Le asignaremos valores de velocidad en el bucle `#!py while` más adelante.
            
            Recuerda que un mensaje `TwistStamped` contiene seis componentes diferentes a los que podemos asignar valores. [¿Cuáles *dos* son relevantes para nuestro robot?](#control-de-velocidad)

    1. Luego configuramos algunas cosas importantes relacionadas con ROS:

        ``` { .py .no-copy }
        rclpy.init(args=None) # (1)!
        node = rclpy.create_node("basic_velocity_control")  # (2)!
        vel_pub = node.create_publisher(TwistStamped, "cmd_vel", 10)  # (3)!
        ```

        1. Inicializa `rclpy` y todas las comunicaciones de ROS necesarias para nuestro nodo.
        2. Inicializa este script Python como un nodo de ROS real, proporcionando un nombre con el que se registrará en la red ROS ("basic_velocity_control" en este caso).
        3. Aquí configuramos un publisher al topic `/cmd_vel` para que el nodo pueda enviar comandos de velocidad al robot (usando datos `TwistStamped`).

    1. Después de esto, definimos otra variable:

        ``` { .py .no-copy }
        timestamp = node.get_clock().now().nanoseconds # (1)!
        ```

        1. ¿Qué hora es ahora mismo? Esto nos indica el "Tiempo de ROS" actual (en nanosegundos), que será útil para comparar en el bucle while.

    1. Ahora entramos en un bucle `#!py while`, donde nuestro código pasará la mayor parte de su tiempo una vez que esté en funcionamiento:

        ``` { .py .no-copy }
        while rclpy.ok(): # (1)!
            time_now = node.get_clock().now().nanoseconds # (2)!
            elapsed_time = (time_now - timestamp) * 1e-9 # (3)!

            ...

        ```

        1. Esto retorna `#!py True` mientras el nodo esté activo, por lo que todo el código dentro del bucle `#!py while` continuará ejecutándose mientras esto sea así.
        2. ¿Qué hora es *ahora*? Verifica el tiempo al inicio de cada iteración del bucle `#!py while` y asígnalo a una variable llamada `time_now`.
        3. Determina cuánto tiempo ha transcurrido (en segundos) desde que se actualizó por última vez el `timestamp`.

        <a name="break"></a>

        1. Una sentencia `#!py if` controla ahora el estado de operación de nuestro robot.
            
            1. En el estado `1` establecemos velocidades que harán que el robot se mueva hacia adelante (solo velocidad lineal en X) durante cierta cantidad de tiempo y luego se detenga. ¿Cuánto tiempo se moverá el robot hacia adelante y a qué velocidad?

                ``` { .py .no-copy }
                if state == 1: 
                    if elapsed_time < 2: # (1)!
                        vel.twist.linear.x = 0.05 # (2)!
                        vel.twist.angular.z = 0.0
                    else: # (3)!
                        vel.twist.linear.x = 0.0 # (4)!
                        vel.twist.angular.z = 0.0
                        state = 2 # (5)!
                        timestamp = node.get_clock().now().nanoseconds # (6)!
                ```

                1. Si el tiempo transcurrido es menor a 2 segundos...
                2. Establece una velocidad lineal para que el robot se mueva hacia adelante.
                3. Si el tiempo transcurrido ha *superado* los 2 segundos...
                4. Establece las velocidades del robot a `0.0` para que se detenga.
                5. En la siguiente iteración del bucle, pasa al estado 2.
                6. Reinicia el timestamp para empezar a contar de nuevo.

            2. En el estado `2` establecemos velocidades que harán que el robot gire en el lugar (solo velocidad angular en Z) durante cierta cantidad de tiempo y luego se detenga. ¿Cuánto tiempo lo hará y a qué velocidad?
                
                ``` { .py .no-copy }
                elif state == 2:
                    if elapsed_time < 4: # (1)!
                        vel.twist.linear.x = 0.0
                        vel.twist.angular.z = 0.2 # (2)!
                    else: # (3)!
                        vel.twist.linear.x = 0.0 # (4)!
                        vel.twist.angular.z = 0.0 
                        state = 1 # (5)!
                        timestamp = node.get_clock().now().nanoseconds # (6)!
                ```

                1. Mientras el tiempo transcurrido sea menor a 4 segundos...
                2. Aplica una velocidad angular al robot para que gire en el lugar.
                3. Una vez que el tiempo transcurrido haya *superado* los 4 segundos...
                4. Regresa las velocidades del robot a `0.0` para que se detenga.
                5. En la siguiente iteración del bucle, regresa al estado 1 (avanzar).
                6. Reinicia el timestamp una vez más.

        1. Y después de la sentencia `#!py if`:

            ``` { .py .no-copy }
            node.get_logger().info( # (1)!
                f"\n[State = {state}] Publishing velocities:\n"
                f"  - linear.x: {vel.twist.linear.x:.2f} [m/s]\n"
                f"  - angular.z: {vel.twist.angular.z:.2f} [rad/s].",
                throttle_duration_sec=1,
            )
            vel_pub.publish(vel) # (2)!
            ```

            1. Esto (y las siguientes 5 líneas) imprimirá un mensaje en la terminal para proporcionarnos actualizaciones regulares sobre en qué estado se encuentra actualmente el nodo y qué velocidades se han establecido (en la sentencia `#!py if` anterior).
            2. Esta línea es crucial: esta operación publica los comandos de velocidad en el topic `/cmd_vel` para que el robot actúe en base a nuestras instrucciones.

                Independientemente de lo que ocurra en los estados del `if` anteriores, *siempre* publicamos un comando de velocidad en el topic `/cmd_vel` aquí (en cada iteración del bucle).


1. Ahora estamos listos para compilar nuestro paquete y poder ejecutarlo. Usamos una herramienta llamada "Colcon" para esto, pero **DEBE** ejecutarse desde la raíz del Espacio de Trabajo de ROS 2 (es decir, `~/ros2_ws/`), así que naveguemos allí ahora usando `cd`. Regresa a **TERMINAL 3** y ejecuta lo siguiente:

    ```bash
    cd ~/ros2_ws/ 
    ```

    Luego, usa el comando `colcon build` para compilar tu paquete:

    ```bash
    colcon build --packages-select waffle_demo --symlink-install
    ```
    
    Y finalmente, "recarga" el entorno:

    ```bash
    source ~/.bashrc
    ```
    
1. Ahora podemos ejecutar el código.

    !!! note
        ¡Asegúrate de que el robot esté en el suelo y tenga suficiente espacio para moverse antes de hacer esto!
    
    ``` { .bash .no-copy }
    ros2 run waffle_demo basic_velocity_control.py
    ```
    
    Observa qué hace el robot. Cuando hayas visto suficiente, ingresa ++ctrl+c++ para detener el nodo.

    !!! warning
        ¡El robot continuará moviéndose incluso después de que hayas detenido el nodo! Ejecuta el siguiente comando para detenerlo:
        
        ```bash
        ros2 run waffle_demo stop_me.py
        ```
    
5. Ahora es el momento de **adaptar el código**:
    
    El objetivo aquí es hacer que el robot siga una trayectoria cuadrada. Lo que puede que hayas observado al ejecutar el código es que el robot ¡en realidad no hace eso! Estamos usando un enfoque basado en tiempo para que el robot alterne entre dos estados diferentes de forma continua:
    
    1. Avanzando hacia adelante
    2. Girando en el lugar
    
    Observa el código para determinar cuánto tiempo pasará el robot actualmente en cada estado.
    
    Queremos que el robot siga una trayectoria cuadrada de **0.5m x 0.5m**. Para lograrlo correctamente tendrás que ajustar los tiempos, la velocidad del robot, o ambos. ¡Edita el código para que el robot siga realmente una **trayectoria cuadrada de 0.5m x 0.5m**!

## SLAM

El Mapeo y Localización Simultáneos (SLAM, por sus siglas en inglés: *Simultaneous Localisation and Mapping*) es una sofisticada herramienta integrada en ROS. Usando datos del sensor LiDAR del robot, más el conocimiento de cuánto se ha movido el robot[^odom], un robot es capaz de crear un mapa de su entorno *y* mantener un seguimiento de su ubicación dentro de ese entorno al mismo tiempo. En el ejercicio que sigue verás lo fácil que es implementar SLAM con el Waffle.

[^odom]: Aprenderás mucho más sobre "Odometría del Robot" en el curso de laboratorio.

#### :material-pen: Ejercicio 6: Usar SLAM para crear un mapa del entorno {#exSlam}

1. En **TERMINAL 3** ingresa el siguiente comando para lanzar todos los nodos de SLAM necesarios:

    ```bash
    ros2 launch rigsa_tb3_tools slam.launch.py environment:=real
    ```
    
    ??? tip
        ¡En la laptop, este comando también está disponible como un alias: `tb3_slam`!

    Esto lanzará una nueva instancia de RViz, mostrando una vista aérea del entorno y puntos de varios colores que representan los datos en tiempo real del LiDAR.
    
    <figure markdown>
      ![](../images/waffle/slam_step0.png){width=600px}
    </figure>

    SLAM ya habrá comenzado a procesar estos datos para empezar a construir un mapa de los límites actualmente visibles para el Waffle según su ubicación en el entorno.

1. Regresa ahora a **TERMINAL 4** y lanza el nodo `teleop_keyboard`. Comienza a conducir el robot *despacio* y *con cuidado* para construir un mapa completo del área.
    
    !!! tip
        Es mejor hacerlo despacio y realizar múltiples circuitos del área para construir un mapa más preciso.

    <a name="slam-steps"></a>

    <figure markdown>
      ![](../images/waffle/slam_step1.png){width=500px}
      ![](../images/waffle/slam_step2.png){width=500px}
      ![](../images/waffle/slam_step3.png){width=500px}
    </figure>

1. Una vez que estés satisfecho con el mapa que ha construido tu robot de su entorno, puedes guardarlo usando el nodo `map_saver_cli` del paquete `nav2_map_server`:

    1. Primero, crea un nuevo directorio dentro de tu paquete de ROS en la laptop. Regresa a **TERMINAL 5** y navega a la raíz del paquete `waffle_demo` que creaste anteriormente:

        ```bash
        cd ~/ros2_ws/src/waffle_demo
        ```
        
    1. Crea un directorio aquí llamado `maps`: 
        
        ```bash
        mkdir maps
        ```
        
    1. Navega a este directorio:

        ```bash
        cd maps/
        ```
        
    1. Luego, usa `ros2 run` para ejecutar el nodo `map_saver_cli` y guardar una copia del mapa de tu robot:

        ``` { .bash .no-copy }
        ros2 run nav2_map_server map_saver_cli -f NOMBRE_MAPA
        ```
        
        Reemplaza `NOMBRE_MAPA` con un nombre apropiado para tu mapa. Esto creará dos archivos:
        
        1. un `NOMBRE_MAPA.pgm` 
        2. un archivo `NOMBRE_MAPA.yaml`
        
        ...ambos contienen datos relacionados con el mapa que acabas de crear.

    1. El archivo `.pgm` se puede abrir usando una aplicación llamada `eog` en la laptop:
    
        ``` { .bash .no-copy }
        eog NOMBRE_MAPA.pgm
        ```
        
1. Regresa a **TERMINAL 3** y cierra SLAM presionando ++ctrl+c++. El proceso debería detenerse y RViz debería cerrarse.

1. Cierra también el nodo `teleop_keyboard` en **TERMINAL 4**, si aún está en ejecución.

## Próximos Pasos

Habiendo dominado los conceptos básicos, debes asegurarte de revisar algunas **[Consideraciones Esenciales](./essentials.md)** antes de avanzar mucho más en este curso; estas destacarán algunos desafíos que los estudiantes enfrentan comúnmente al trabajar con los robots. Conocerlos con anticipación puede marcar una gran diferencia y ahorrarte muchos dolores de cabeza en el laboratorio.

... y cuando hayas terminado con tu robot al final de cada sesión de laboratorio, asegúrate de **[apagarlo correctamente](./shutdown.md)**.
