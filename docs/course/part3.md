---  
title: "Parte 3: Más Allá de los Fundamentos"  
description: Ejecuta aplicaciones ROS de manera más eficiente usando launch files, y aprende cómo modificar el comportamiento de los nodes durante la ejecución usando parameters. Aprende sobre el sensor LiDAR, los datos que genera, y observa los beneficios de esto para herramientas como "SLAM".
---

## Introducción

:material-pen: **Ejercicios**: 5  
:material-timer: **Tiempo Estimado de Finalización**: 3 horas  
:material-gauge: **Nivel de Dificultad**: Intermedio  

### Objetivos

En esta parte del curso exploraremos algunos conceptos más avanzados de ROS, y examinaremos otro de los sensores a bordo de nuestro robot: el sensor LiDAR. A partir del trabajo que realizaste en la Parte 2, es posible que hayas comenzado a apreciar las limitaciones asociadas con el uso de datos de odometría como única señal de retroalimentación al intentar controlar la posición de un robot en su entorno. El sensor LiDAR puede proporcionar información adicional sobre el entorno, mejorando así el conocimiento y las capacidades del robot. Sin embargo, primero veremos cómo lanzar aplicaciones ROS de forma más eficiente con *launch files*, y cómo el comportamiento de los nodes puede modificarse dinámicamente usando *parameters*. 

### Resultados de Aprendizaje Esperados

Al finalizar esta sesión serás capaz de:

1. Crear launch files para permitir la ejecución simultánea de múltiples ROS Nodes con `ros2 launch`.
1. Usar parameters para influir en el comportamiento de los nodes en tiempo real, sin necesidad de reprogramarlos.
1. Aprender sobre el sensor LiDAR del robot y las mediciones que se obtienen de él.
1. Interpretar los datos `LaserScan` que se publican en el topic `/scan` y usar las herramientas existentes de ROS para visualizarlos.
1. Realizar análisis numérico sobre arreglos de datos (usando la librería Python `numpy`) para procesar datos `LaserScan` y usarlos en aplicaciones ROS.
1. Usar herramientas existentes de ROS para implementar SLAM y construir un mapa de un entorno. 

### Enlaces Rápidos

#### Ejercicios

* [Ejercicio 1: Creando un Launch File](#ex1)
* [Ejercicio 2: Usando parameters para cambiar el comportamiento del robot en tiempo real](#ex2)
* [Ejercicio 3: Usando RViz para Visualizar Datos LaserScan](#ex3)
* [Ejercicio 4: Construyendo una Función Callback para LaserScan](#ex4)
* [Ejercicio 5: Construyendo un mapa de un entorno con SLAM](#ex5)

#### Recursos Adicionales

* [Un Node Subscriber Básico para `LaserScan` (para el Ejercicio 4)](./part3/lidar_subscriber.md){target="_blank"}

## Primeros Pasos

**Paso 1: Inicia tu Entorno ROS**

Si aún no lo has hecho, inicia tu entorno ROS ahora:

1. **Sandbox del Laboratorio (Recomendado)**: inicia una sesión en [rigsa.io](https://rigsa.io) — sin instalación local, acceso directo desde el navegador.
1. **Usando WSL-ROS2 en una computadora del laboratorio**: sigue [las instrucciones aquí para iniciarlo](../software/using-wsl-ros/man-win.md).
1. **[Ejecutando WSL-ROS2 en tu propia máquina](../software/installing-wsl-ros2.md)**: inicia el Windows Terminal para acceder a una instancia de terminal WSL-ROS2.
1. **Usuarios de Docker**: sigue [los pasos correspondientes](../software/docker-ros2.md) para iniciar una instancia de terminal con tu instalación local de ROS.

Ahora deberías tener acceso a una instancia de terminal Linux, a la cual nos referiremos como **TERMINAL 1**.

**Paso 2: Restaura tu trabajo (SOLO para usuarios de escritorio administrado con WSL-ROS2)**

Recuerda que cualquier trabajo que realices dentro del entorno WSL-ROS2 no se preservará entre sesiones ni entre diferentes computadoras del laboratorio. Al [final de la Parte 2](./part2.md#backup) deberías haber ejecutado la herramienta `wsl_ros` para respaldar tu directorio de inicio en tu unidad `U:\`. Una vez que WSL-ROS2 esté en funcionamiento, se te pedirá que lo restaures:

``` { .txt .no-copy }
It looks like you already have a backup from a previous session:
  U:\wsl-ros\ros2-backup-XXX.tar.gz
Do you want to restore this now? [y/n]
```

Ingresa ++y+enter++ para restaurar tu trabajo de la sesión anterior. También puedes restaurar tu trabajo en cualquier momento usando el siguiente comando:

```bash
wsl_ros restore
```

**Paso 3: Inicia VS Code**  

También conviene iniciar VS Code ahora, para que esté listo cuando lo necesites más adelante. 

??? warning "Usuarios de WSL..."
        
    Es importante iniciar VS Code dentro de tu entorno ROS usando la extensión "WSL". Recuerda siempre verificar esto: 
    
    <figure markdown>
      ![](../software/figures/code-wsl-ext-on.svg){width=400px}
    </figure>

**Paso 4: Asegúrate de que el Repositorio del Curso esté Actualizado**

En la Parte 1 deberías haber [descargado e instalado el Repositorio del Curso](./part1.md#course-repo) en tu entorno ROS. Esperamos que ya lo hayas hecho, pero si no es así, regresa y hazlo ahora (lo necesitarás para algunos ejercicios aquí). Si ya lo hiciste, vale la pena asegurarte de que esté actualizado, así que ejecuta el siguiente comando ahora:

```bash
cd ~/ros2_ws/src/rigsa_ros/ && git pull
```

Luego ejecuta `colcon build` 

```bash
cd ~/ros2_ws/ && colcon build --packages-up-to rigsa_ros
```

Y finalmente, recarga tu entorno:

```bash
source ~/.bashrc
```

!!! warning "Recuerda"
    Si tienes otras instancias de terminal abiertas, también deberás ejecutar `#!bash source ~/.bashrc` en ellas para que los cambios se propaguen correctamente.

## Launch Files

Hasta ahora (en las Partes 1 y 2) hemos usado el comando `ros2 run` para ejecutar una variedad de ROS nodes, como `teleop_keyboard`, así como varios nodes que hemos creado nosotros mismos. También habrás notado que hemos usado el comando `ros2 launch` en algunas ocasiones, principalmente para lanzar simulaciones Gazebo de nuestro robot. Pero, ¿por qué tenemos estos dos comandos y cuál es la diferencia entre ellos?

Las aplicaciones ROS complejas típicamente requieren la ejecución de múltiples nodes al mismo tiempo. El comando `ros2 run` solo nos permite ejecutar un único node, lo que no es conveniente para aplicaciones complejas donde tendríamos que abrir múltiples terminales, usar `ros2 run` varias veces *y* asegurarnos de ejecutar todo en el orden correcto sin olvidar nada. `ros2 launch`, por otro lado, proporciona una forma de lanzar múltiples ROS nodes *simultáneamente* al definir exactamente lo que queremos lanzar dentro de los *launch files*. Esto hace que la ejecución de aplicaciones complejas sea más confiable, repetible y más fácil para que otros las lancen correctamente. 

### :material-pen: Ejercicio 1: Creando un Launch File {#ex1}

Para entender cómo funcionan los launch files, ¡vamos a crear algunos!

En la Parte 1 creamos los nodes `publisher.py` y `subscriber.py` que podían comunicarse entre sí a través de un topic llamado `/my_topic`. Los lanzamos de forma independiente usando el comando `ros2 run` en dos terminales separadas. ¿No sería conveniente poder lanzarlos ambos al mismo tiempo, desde la *misma terminal*?

Para empezar, vamos a crear otro nuevo package, esta vez llamado `part3_beyond_basics`. 

1. En **TERMINAL 1**:
    
    1. Ve a la carpeta `src` del workspace de ROS 2:

        ```bash
        cd ~/ros2_ws/src/
        ```
       
    1. Clona el Plantilla de Package ROS 2:

        ```bash
        git clone https://github.com/tom-howard/ros2_pkg_template.git
        ```
    
    1. Ejecuta el script `init_pkg.sh` desde dentro de esta plantilla para inicializar un package con el nombre "part3_beyond_basics":

        ```bash
        ./ros2_pkg_template/init_pkg.sh part3_beyond_basics
        ```
    
    1. Y navega hasta la *raíz* de este nuevo package usando `cd`:

        ```bash
        cd ./part3_beyond_basics/
        ```

1. Los launch files deben ubicarse en un directorio `launch` en la raíz del directorio del package, así que usa `mkdir` para crearlo:

    ```bash
    mkdir launch
    ```

1. Usa el comando `cd` para entrar a la carpeta `launch` que acabas de crear:
    
    ```bash
    cd launch
    ```

    ...y luego usa el comando `touch` para crear un nuevo archivo vacío llamado `pubsub.launch.py`:

    ```bash
    touch pubsub.launch.py
    ```
    
1. Abre este launch file en VS Code e ingresa lo siguiente:

    ```py title="pubsub.launch.py"
    from launch import LaunchDescription # (1)!
    from launch_ros.actions import Node # (2)!

    def generate_launch_description(): # (3)!
        return LaunchDescription([ # (4)!
            Node( # (5)!
                package='part1_pubsub', # (6)!
                executable='publisher.py', # (7)!
                name='my_publisher' # (8)!
            )
        ])
    ```

    1. Todo lo que queremos ejecutar con un launch file debe estar encapsulado dentro de un `LaunchDescription`, que se importa aquí desde el módulo `launch`.
    2. Para ejecutar un *node* desde un launch file necesitamos definirlo usando la clase `Node` de `launch_ros.actions` (¡no confundir con el *método de comunicación* ROS Action que se cubre en la Parte 5!).
    3. Encapsulamos una *Launch Description* dentro de una función `generate_launch_description()`.
    4. Aquí definimos todo lo que queremos que ejecute este launch file: en este caso una *lista* Python `[]` que contiene un único elemento `Node()` (por ahora).
    5. Aquí describimos el node que queremos lanzar.
    6. El nombre del package al que pertenece el node.
    7. El nombre del node actual que queremos lanzar desde el package anterior.
    8. Un nombre para registrar este node en la red ROS. Aunque esto también se define dentro del node mismo: 
        
        ``` { .py .no-copy }
        super().__init__("simple_publisher")
        ```
        
        ...podemos sobreescribirlo aquí con otro nombre. 


1. Necesitamos asegurarnos de informarle a `colcon` sobre nuestro nuevo directorio `launch`, para que pueda compilar los launch files dentro de él cuando ejecutemos `colcon build`. Para esto, debemos agregar una instrucción de instalación de *directorio* al `CMakeLists.txt` de nuestro package:

    Abre el archivo `CMakeLists.txt` y agrega el siguiente texto **justo arriba** de la línea `ament_package()` al final del archivo:

    ```txt title="part3_beyond_basics/CMakeLists.txt"
    install(DIRECTORY
      launch
      DESTINATION share/${PROJECT_NAME}
    )
    ```

1. Ahora, compilemos el package usando el **proceso de tres pasos** que ya deberías ir conociendo bien... <a name="colcon-build"></a>

    1. Navega de regreso a la raíz del workspace de ROS 2:

        ```bash
        cd ~/ros2_ws/
        ```
    
    1. Ejecuta `colcon build` solo en tu nuevo package:

        ```bash
        colcon build --packages-select part3_beyond_basics --symlink-install
        ``` 

    1. Y finalmente, recarga el `.bashrc`:

        ```bash
        source ~/.bashrc
        ```
        
1. Usa `ros2 launch` para lanzar este archivo y probarlo tal como está:

    ```bash
    ros2 launch part3_beyond_basics pubsub.launch.py
    ```
        
1. El código (tal como está) lanzará el node `publisher.py` del package `part1_pubsub`, pero no el node `subscriber.py`. Por lo tanto, necesitamos agregar otro objeto `Node()` a nuestra `LaunchDescription`:

    ```py title="pubsub.launch.py"
    from launch import LaunchDescription 
    from launch_ros.actions import Node

    def generate_launch_description():
        return LaunchDescription([
            Node(
                package='part1_pubsub',
                executable='publisher.py',
                name='my_publisher'
            ),
            Node(
                # TODO: define the subscriber.py node...
            )
        ])
    ```

    Usando los mismos métodos anteriores, agrega las definiciones necesarias para el node `subscriber.py` en tu launch file.

1. Una vez que hayas realizado estos cambios, [necesitarás ejecutar `colcon build` nuevamente](#colcon-build).

    !!! warning

        Necesitarás ejecutar `colcon build` *cada vez* que realices cambios en un launch file, incluso si usas la opción `--symlink-install` (ya que esta solo aplica a los nodes en el directorio `scripts`)
        
1. Una vez que hayas completado esto, debería ser posible lanzar tanto el publisher como el subscriber nodes (de tu package `part1_pubsub`) con `ros2 launch` y el archivo `pubsub.launch.py`. Verifica esto en **TERMINAL 1** ejecutando el launch file:

    <figure markdown>
      ![](./part3/pubsub.gif){width=600px}
    </figure>

1. Podemos verificar esto adicionalmente en una nueva terminal (**TERMINAL 2**), usando comandos que hemos usado en las Partes 1 y 2 para *listar* todos los nodes y topics activos en nuestra red ROS:

    ```bash
    ros2 node list
    ```
    ```bash
    ros2 topic list
    ```

    ¿Ves lo que esperabas ver en la salida de estos dos comandos?

!!! tip "Launch Files: Avanzado"
    Para técnicas más avanzadas de launch files, **[consulta aquí](./extras/launch-files.md)**!


## Parameters

Los parameters se usan para configurar nodes, y también pueden usarse para cambiar su comportamiento dinámicamente durante la ejecución. 

### :material-pen: Ejercicio 2: Usando parameters para cambiar el comportamiento del robot en tiempo real {#ex2}

Pensemos de nuevo en nuestro node `move_circle.py` de la Parte 2 para ver para qué podría usarse esto. El node que construimos originalmente haría que un robot se moviera en un círculo de 0.5 metros de radio, ¡indefinidamente! ¿No sería conveniente poder *cambiar* el radio del círculo mientras el node está en ejecución?

1. Cierra tu archivo `pubsub.launch.py` en **TERMINAL 1** si aún está en ejecución.

1. Ahora, crearemos una nueva versión del node `move_circle.py` de la Parte 2 con la que podemos experimentar. Primero, ve al directorio `scripts` de tu package `part3_beyond_basics` en **TERMINAL 1**:

    ```bash
    cd ~/ros2_ws/src/part3_beyond_basics/scripts/
    ```
    
1. Crea un nuevo node llamado `param_circle.py`:
    
    ```bash
    touch param_circle.py
    ``` 

    y dale permisos de *ejecución*:

    ```bash
    chmod +x param_circle.py
    ```

1. Declara esto como un ejecutable del package abriendo el `CMakeLists.txt` de tu package en VS Code y agregando `param_circle.py` como se muestra a continuación:

    ```txt title="CMakeLists.txt"
    # Install Python executables
    install(PROGRAMS
      scripts/basic_velocity_control.py
      scripts/stop_me.py
      scripts/param_circle.py
      DESTINATION lib/${PROJECT_NAME}
    )
    ```

1. Recompila tu package con `colcon` (aunque `param_circle.py` todavía esté vacío en este punto):

    1. Primero:

        ```bash
        cd ~/ros2_ws/
        ```
    
    1. Luego:

        ```bash
        colcon build --packages-select part3_beyond_basics --symlink-install
        ```
    
    1. Y finalmente:

        ```bash
        source ~/.bashrc
        ```

1. Después de haber completado los Ejercicios 4 y 5 de la Parte 2, deberías tener un node `move_circle.py` funcional con un procedimiento de apagado adecuado. Copia el código y pégalo en tu nuevo archivo `param_circle.py`. Alternativamente, si no lograste terminar esos ejercicios anteriormente, **[puedes acceder a un ejemplo resuelto aquí](./part3/move_circle.md){target="_blank"}**.

1. Ahora, modifiquemos el código:

    1. Primero, en el método `__init__()`, cambia el nombre del node:
        
        ```py
        super().__init__("param_circle")
        ```

        Al lanzarse, el node quedará registrado en la red ROS con el nombre `"param_circle"`.

    1. Luego, directamente debajo de esto (aún dentro del método `__init__()`), agrega las siguientes líneas nuevas:

        ```py 
        self.declare_parameter(
            name="radius", 
            value=0.5 # meters
        )
        ```
    
        Aquí estamos declarando un ROS parameter llamado `radius` y asignándole un valor predeterminado de `0.5`, para representar el radio deseado del círculo (en metros).
    
    1. En algún lugar del método `timer_callback()`, deberías estar definiendo el radio deseado del círculo. *Modifica* esto de la siguiente manera:

        ```py 
        radius = self.get_parameter("radius").get_parameter_value().double_value
        ```

        El radio del círculo en el que se moverá el robot ahora se basa en el valor del *parameter* `radius`, en lugar de un valor estático. 

    1. Finalmente, modifica tu declaración `get_logger().info()` (al final del método `timer_callback()`) para incluir información sobre el radio objetivo:

        ```py
        self.get_logger().info( 
            f"Moving with radius: {radius:.2f} [m]\n"
            f"Linear Velocity: {topic_msg.twist.linear.x:.2f} [m/s], "
            f"Angular Velocity: {topic_msg.twist.angular.z:.2f} [rad/s].",
            throttle_duration_sec=1, 
        )
        ```

1. Para probar esto, primero inicia la simulación *Empty World* en **TERMINAL 1**:

    ```bash
    ros2 launch turtlebot3_gazebo empty_world.launch.py 
    ```
    
1. Luego, en **TERMINAL 2**, ejecuta el node `param_circle.py`:

    ```bash
    ros2 run part3_beyond_basics param_circle.py
    ```

    El robot debería comenzar a moverse en un círculo. Al principio, el radio de este círculo debería ser de 0.5 metros, basado en el valor predeterminado que asignamos al parameter en nuestro código.

1. A continuación, abre otra instancia de terminal (**TERMINAL 3**) y ejecuta el siguiente comando para listar todos los parameters que están activos/disponibles actualmente en nuestra red ROS:
    
    ```bash
    ros2 param list
    ```

    Esta puede ser una lista bastante extensa. Los parameters se listan bajo los nodes que los definen, así que para filtrar la lista, proporciona también el nombre del node:

    ```bash
    ros2 param list /param_circle
    ```

    Ahora debería haber solo un pequeño número de parameters listados, incluyendo `radius`. 

1. Ahora podemos cambiar el valor de este parameter mientras nuestro node `param_circle.py` está en ejecución, y por lo tanto cambiar el tamaño del círculo que el robot está siguiendo actualmente. Podemos hacer esto desde la línea de comandos, sin tener que detener nuestro node `param_circle.py` ni realizar ningún cambio en él. Nuevamente, en **TERMINAL 3**: 

    ```txt
    ros2 param set /param_circle radius 1.2
    ```

    ¡Prueba establecer una variedad de valores diferentes y observa cómo cambia el comportamiento del robot en el mundo simulado!

1. Una vez que hayas terminado, cierra el node `param_circle.py` y la simulación Gazebo ingresando ++ctrl+c++ en los terminales **1** y **2** respectivamente.

## Resumen

Los parameters nos permiten cambiar el comportamiento de las cosas durante la ejecución. También exploraremos otros usos para ellos en la siguiente parte de este curso (Parte 4).

También hemos aprendido algunas técnicas clave de launch files, así que avancemos hacia otro tema más avanzado y muy importante...

## Datos de Desplazamiento Láser y el Sensor LiDAR {#lidar}

Como recordarás de la Parte 2, la odometría es muy importante para la navegación de robots, pero puede estar sujeta a deriva y error acumulado a lo largo del tiempo. Es posible que hayas observado esto en la simulación durante el [Ejercicio 5 de la Parte 2](./part2.md#ex5), y definitivamente lo notarías si hicieras lo mismo en un robot real. Afortunadamente, el robot de simulación tiene otro sensor a bordo que proporciona información aún más rica sobre el entorno, y podemos usarlo para complementar la información de odometría y mejorar las capacidades de navegación del robot.

### Introduciendo la Interfaz LaserScan

#### :material-pen: Ejercicio 3: Usando RViz para Visualizar Datos LaserScan {#ex3}

<a name="rviz"></a>Ahora vamos a colocar el robot en un entorno más interesante que el "empty world" con el que hemos estado trabajando hasta ahora...

1. En **TERMINAL 1** ingresa el siguiente comando para lanzarlo:

    ```bash
    ros2 launch turtlebot3_gazebo turtlebot3_world.launch.py
    ```

    Ahora debería lanzarse una simulación Gazebo con el robot de simulación en un nuevo entorno:

    <figure markdown>
      ![](../images/gz/tb3_world.png){width=600px}
    </figure>

1. En **TERMINAL 2** ingresa lo siguiente:

    ```bash
    ros2 launch rigsa_tb3_tools rviz.launch.py environment:=sim
    ```
    
    Al ejecutar el comando debería abrirse una nueva ventana:

    <figure markdown>
      ![](../images/rviz/tb3.png){width=600px}
    </figure>

    Esto es *RViz*, una herramienta de ROS que nos permite *visualizar* los datos que está midiendo un robot en tiempo real. 
    
    Los puntos verdes dispersos alrededor del robot representan *datos de desplazamiento láser* medidos por el sensor LiDAR ubicado en la parte superior del robot, lo que le permite medir la *distancia* a cualquier obstáculo en sus alrededores. 
    
    El sensor LiDAR gira continuamente, emitiendo pulsos láser mientras lo hace. Estos pulsos láser son reflejados por los objetos y devueltos al sensor. La distancia puede determinarse entonces basándose en el tiempo que tardan los pulsos en completar el recorrido completo (desde el sensor, al objeto, y de regreso), mediante un proceso llamado *"tiempo de vuelo"* (*time of flight*). Dado que el sensor LiDAR gira y realiza este proceso continuamente, se puede generar un escaneo completo de 360&deg; del entorno.
    
    En este caso (ya que estamos trabajando en simulación) los datos representan los objetos que rodean al robot en su *entorno simulado*, así que deberías notar que los puntos verdes producen un contorno que se parece a los objetos del mundo que se está simulando en Gazebo (o al menos parcialmente).
    
1. Los datos de desplazamiento láser del sensor LiDAR son publicados por el robot en el topic `/scan`. Podemos usar el comando `ros2 topic info` para obtener más información sobre los nodes que publican y se suscriben a este topic, así como el *tipo de interfaz* utilizado para transmitir los datos de este topic. En **TERMINAL 3** ingresa lo siguiente:

    ```bash
    ros2 topic info /scan
    ```
    ```{ .txt .no-copy }
    Type: sensor_msgs/msg/LaserScan
    Publisher count: 1
    Subscription count: 0
    ```

1. Como podemos ver arriba, los datos del topic `/scan` son del tipo `sensor_msgs/msg/LaserScan`, y podemos obtener más información sobre esta interfaz usando el comando `ros2 interface show`:

    ```bash
    ros2 interface show sensor_msgs/msg/LaserScan
    ```
    ```{ .txt .no-copy }
    # Single scan from a planar laser range-finder

    std_msgs/Header header # timestamp in the header is the acquisition time of
            builtin_interfaces/Time stamp
                    int32 sec
                    uint32 nanosec
            string frame_id
                                 # the first ray in the scan.
                                 #
                                 # in frame frame_id, angles are measured around
                                 # the positive Z axis (counterclockwise, if Z is up)
                                 # with zero angle being forward along the x axis

    float32 angle_min            # start angle of the scan [rad]
    float32 angle_max            # end angle of the scan [rad]
    float32 angle_increment      # angular distance between measurements [rad]

    float32 time_increment       # time between measurements [seconds] - if your scanner
                                 # is moving, this will be used in interpolating position
                                 # of 3d points
    float32 scan_time            # time between scans [seconds]

    float32 range_min            # minimum range value [m]
    float32 range_max            # maximum range value [m]

    float32[] ranges             # range data [m]
                                 # (Note: values < range_min or > range_max should be discarded)
    float32[] intensities        # intensity data [device-specific units].  If your
                                 # device does not provide intensities, please leave
                                 # the array empty.
    ```

### Interpretando los Datos LaserScan

La interfaz `LaserScan` es una interfaz de mensaje ROS estandarizada (del package `sensor_msgs`) que cualquier robot ROS puede usar para publicar los datos que obtiene de un sensor de desplazamiento láser como el LiDAR del robot de simulación.  

`ranges` es un arreglo de valores `float32` (los tipos de datos de arreglo tienen el sufijo `[]`). Esta es la parte del mensaje que contiene todas las *mediciones de distancia reales* que está obteniendo el sensor LiDAR (en metros).

<a name="fig_lidar"></a>Considera un ejemplo simplificado aquí, tomado de un robot de simulación en un entorno diferente:

<figure markdown>
  ![](../images/rviz/lidar_illustrated.png)
</figure>

<a name="echo_scan_variables"></a>Como se ilustra en la figura, podemos asociar cada punto de datos del arreglo `ranges` a una *posición angular* usando los valores `angle_min`, `angle_max` y `angle_increment` que también se proporcionan dentro del mensaje `LaserScan`. Podemos usar el comando `ros2 topic echo` para averiguar cuáles son sus valores:

```{ .txt .no-copy }
$ ros2 topic echo /scan --field angle_min --once
0.0
---
```
```{ .txt .no-copy }
$ ros2 topic echo /scan --field angle_max --once
6.28000020980835
---
```
```{ .txt .no-copy }
$ ros2 topic echo /scan --field angle_increment --once
0.01749303564429283
---
```

!!! question
    ¿Qué representan estos valores? (Compáralos con [la figura anterior](#fig_lidar))

!!! tip 
    ¿Notaste cómo pudimos acceder a *variables específicas* dentro de los datos del topic `/scan` usando el flag `--field`, y pedirle al comando que solo nos proporcionara un único mensaje usando `--once`?

El arreglo `ranges` contiene 360 valores en total, es decir, una medición de distancia cada 1&deg; (un `angle_increment` de 0.0175 radianes) alrededor del robot. El primer valor del arreglo `ranges` (`ranges[0]`) es la distancia al objeto más cercano directamente frente al robot (es decir, en &theta; = 0 radianes, o `angle_min`). El último valor del arreglo `ranges` (`ranges[359]`) es la distancia al objeto más cercano a 359&deg; (es decir, &theta; = 6.283 radianes, o `angle_max`) desde el frente del robot, es decir: 1 grado a la *derecha* del eje X. `ranges[65]`, por ejemplo, representaría la distancia al objeto más cercano a un ángulo de 65&deg; (1.138 radianes) desde el frente del robot (*en sentido antihorario*), como se muestra en [la figura](#fig_lidar).

<a name="range_max_min"></a>El mensaje `LaserScan` también contiene los parámetros `range_min` y `range_max`, que representan las distancias *mínima* y *máxima* (nuevamente, en metros) que puede detectar el sensor LiDAR, respectivamente. Usa el comando `ros2 topic echo` para reportar estos directamente también.  

!!! question "Preguntas"
    1. ¿Cuál es el rango máximo y mínimo del sensor LiDAR? Usa [la misma técnica que usamos anteriormente](#echo_scan_variables) para averiguarlo.
    1. Considera la nota junto a `ranges` en la salida de `ros2 interface show` anterior:

        ``` { .txt .no-copy }
        float32[] ranges    # range data [m]
                            # (Note: values < range_min or > range_max should be discarded)
        ```

        (esto puede valer la pena tenerlo en cuenta).

Finalmente, usa el comando `ros2 topic echo` nuevamente para mostrar la porción `ranges` de los datos `LaserScan`. Hay mucha información aquí (¡360 puntos de datos por mensaje, como ya sabes!):

```txt
ros2 topic echo /scan --field ranges
```

Ahora omitimos la opción `--once`, para poder ver los datos tal como llegan, en *tiempo real*. Es posible que necesites expandir la ventana del terminal para poder ver todos los puntos de datos; los datos estarán delimitados por corchetes `[]`, y debería haber un `---` al final de cada mensaje para ayudarte a confirmar que estás viendo el mensaje completo.

Lo principal que notarás aquí es que hay mucha información, ¡y cambia rápidamente! Sin embargo, como ya has visto, son los números que aparecen aquí los que están representados por los puntos verdes en RViz. Regresa a la pantalla de RViz para echar otro vistazo ahora. Como sin duda estarás de acuerdo, esta es una forma mucho más útil de visualizar los datos `ranges`, e ilustra cuán útil puede ser RViz para interpretar lo que tu robot puede *ver* en tiempo real.

También puedes notar varios valores `inf` dispersos por el arreglo. Estos representan lecturas del sensor que están fuera del rango de medición del sensor (es decir, *mayores que* `range_max` o *menores que* `range_min`), por lo que el sensor no puede reportar una medición de distancia en esos casos. Recuerda lo mencionado anteriormente: 

``` { .txt .no-copy }
(Note: values < range_min or > range_max should be discarded)
```

!!! note
    ¡Este comportamiento es diferente en los robots reales! **¡Ten esto en cuenta cuando desarrolles código para robots reales!**

Detén el comando `ros2 topic echo` en la ventana del terminal ingresando ++ctrl+c++ en **TERMINAL 3**. También cierra el proceso RViz que se ejecuta en **TERMINAL 2** ahora, pero deja la simulación (en **TERMINAL 1**) en funcionamiento. 

#### :material-pen: Ejercicio 4: Construyendo una Función Callback para LaserScan {#ex4}

Los datos LaserScan nos presentan un nuevo desafío: procesar grandes conjuntos de datos. En este ejercicio veremos algunos enfoques básicos que se pueden tomar para trabajar con estos datos y obtener algo significativo que pueda usarse en tus aplicaciones robóticas.

1. En **TERMINAL 2**, navega a la carpeta `scripts` de tu package `part3_beyond_basics`:

    ```bash
    cd ~/ros2_ws/src/part3_beyond_basics/scripts/
    ```

1. Crea un nuevo archivo llamado `lidar_subscriber.py` (usando `touch`), hazlo ejecutable (usando `chmod`) y luego decláralo como ejecutable del package en tu archivo `CMakeLists.txt` (si necesitas ayuda con alguno de estos pasos, consulta el ejercicio anterior).

1. Abre el archivo en VS Code, luego consulta a continuación las instrucciones sobre cómo construirlo:
    
    <center>[:material-file-code-outline: Construyendo un Subscriber para `LaserScan`](./part3/lidar_subscriber.md){ .md-button target="_blank"}</center> 

1. Regresa al terminal y compila con `colcon`:

    ```bash
    cd ~/ros2_ws/
    ```
    
    ```bash
    colcon build --packages-select part3_beyond_basics --symlink-install
    ```

    ```bash
    source ~/.bashrc
    ```

1. Con todo eso hecho, estás listo para comenzar. Ejecuta el node usando `ros2 run`:

    ```bash
    ros2 run part3_beyond_basics lidar_subscriber.py
    ```

1. Abre otra terminal (para que aún puedas ver las salidas de tu node `lidar_subscriber.py`). Lanza el node `teleop_keyboard`, conduce el robot alrededor y observa cómo cambian las salidas de tu node `lidar_subscriber.py` mientras lo haces.

1. Cierra todo ahora (incluida la simulación en **TERMINAL 1**). Luego lanza la simulación "empty world" nuevamente:

    ```bash
    ros2 launch turtlebot3_gazebo empty_world.launch.py
    ```

1. Regresa a **TERMINAL 2** y lanza tu node `lidar_subscriber.py` nuevamente:

    ```bash
    ros2 run part3_beyond_basics lidar_subscriber.py
    ```

    ¿Qué salida ves ahora?

    Deberías notar que tu node `lidar_subscriber.py` reporta `nan meters` ahora. Esto se debe a que no hay nada en el entorno para que el sensor LiDAR detecte, por lo que *todas* las lecturas están fuera de rango y, por tanto, nuestro análisis del arco de 40&deg; de lecturas LiDAR en la parte frontal del robot ha filtrado *todo* y por ello devuelve `nan` (no es un número).

1. Usa la **herramienta Box** en Gazebo para colocar una caja en el entorno. 

    <figure markdown>
      ![](../images/gz/toolbars_antd.png){width=500px}
    </figure>

1. Haz clic en la **herramienta Translate** para mover la caja hasta que el node `lidar_subscriber.py` devuelva algunas lecturas que *no* sean `nan`.

1. Mueve la caja un poco más para observar qué puede detectar nuestro análisis de los datos `LaserScan`, y dónde la caja queda fuera del rango detectable.

1. Piensa en cómo podrías adaptar la función callback del node `lidar_subscriber.py` para que detecte más de un subconjunto de `LaserScan`, de modo que pueda detectar situaciones como esta (por ejemplo):

    <figure markdown>
      ![](./part3/lidar_subscriber_adv.png){width=500px}
    </figure>


## Localización y Mapeo Simultáneo (SLAM) {#slam}

En conjunto, los datos del sensor LiDAR y la odometría del robot (específicamente la *pose* del robot) son muy poderosos, y permiten extraer conclusiones muy útiles sobre el entorno en el que opera un robot. Una de las aplicaciones clave de estos datos es la *"Localización y Mapeo Simultáneo"* (*Simultaneous Localisation and Mapping*), o *SLAM*. Esta es una herramienta integrada en ROS que permite a un robot construir un mapa de su entorno y localizarse dentro de ese mapa al mismo tiempo. ¡Ahora veremos cuán fácil es aprovechar esto en ROS!

### :material-pen: Ejercicio 5: Construyendo un mapa de un entorno con SLAM {#ex5}

1. Cierra todos los procesos ROS que estén en ejecución ahora ingresando ++ctrl+c++ en cada terminal. 

1. Ahora vamos a lanzar nuestro robot en *otro* nuevo entorno simulado, ¡del cual crearemos un mapa usando SLAM! Para lanzar la simulación ingresa el siguiente comando en **TERMINAL 1**:

    ```bash
    ros2 launch rigsa_simulations nav_world.launch.py
    ```

    El entorno que se lanza debería verse así:

    <figure markdown>
      ![](./part3/nav_world.png){width=800px}
    </figure>

1. Ahora lanza SLAM para comenzar a construir un mapa de este entorno. En **TERMINAL 2**, lanza SLAM de la siguiente manera:
        
    ```bash
    ros2 launch rigsa_tb3_tools slam.launch.py environment:=sim
    ```

    Esto lanzará RViz nuevamente, donde deberías ver una vista desde arriba de un entorno con un modelo del robot, rodeado de algunos puntos que representan los datos LiDAR en tiempo real. 
    
    <figure markdown>
      ![](./part3/cartographer_rviz1.png){width=600px}
    </figure>

    SLAM ya ha comenzado a construir un mapa de los límites que actualmente son visibles para el robot, basándose en su posición inicial en el entorno. 

    Si dejas esto por un minuto, las paredes del espacio comenzarán a hacerse visibles en RViz, y el suelo comenzará a tornarse de un gris más claro. A medida que pase el tiempo, los algoritmos SLAM se volverán más seguros sobre lo que se está observando en el entorno, lo que permitirá definir los límites y el espacio libre.

    <figure markdown>
      ![](./part3/cartographer_rviz2.png){width=600px}
    </figure>

1. En **TERMINAL 3** lanza el node `teleop_keyboard` ([ya deberías saber cómo hacer esto](./part2.md#teleop)). Reorganiza y redimensiona tus ventanas para que puedas ver Gazebo, RViz *y* las instancias de terminal del `teleop_keyboard` al mismo tiempo.

1. Conduce el robot alrededor del espacio lentamente, usando el node `teleop_keyboard`, y observa cómo el mapa se actualiza y expande constantemente en la ventana de RViz mientras lo haces. 

1. Mientras haces esto, abre *otra* instancia de terminal (**TERMINAL 4**) y ejecuta el node `odom_subscriber.py` que creaste en la Parte 2:
    
    ```bash
    ros2 run part2_navigation odom_subscriber.py
    ```
    
    Esto te proporcionará las coordenadas `X` e `Y` del robot (en metros) dentro del entorno mientras lo conduces, y puedes usar esto para determinar las coordenadas del centro de los cuatro círculos (A, B, C y D) que están marcados en el suelo del espacio. 
    
    Conduce tu robot hacia cada una de estas zonas circulares y detén el robot dentro de ellas.    

    <a name="goal_coords"></a>Registra las coordenadas de cada marcador de zona en una tabla como la siguiente.

    <center>

    | Zona | Posición X (m) | Posición Y (m) |
    | :---: | :---: | :---: |
    | START | 0.5   | -0.04 |
    | A     |       |       |
    | B     |       |       |
    | C     |       |       |
    | D     |       |       |

    </center>

1. Continúa conduciendo el robot hasta que se haya generado un mapa completo del entorno.
    
    <figure markdown>
      ![](./part3/slam_steps.png){width=800px}
    </figure>

1. Una vez que hayas construido un mapa completo del entorno (y hayas obtenido las coordenadas de todos los círculos), puedes guardar tu mapa para usarlo más adelante. Para esto usamos el package `map_server` de ROS. Primero, detén el robot presionando ++s++ en **TERMINAL 3** y luego ingresa ++ctrl+c++ para cerrar el node `teleop_keyboard`.

1. Luego, permaneciendo en **TERMINAL 3**, navega a la raíz del directorio de tu package `part3_beyond_basics` y crea una nueva carpeta llamada `maps`:

    ```bash
    cd ~/ros2_ws/src/part3_beyond_basics/
    ```
    ```bash
    mkdir maps
    ```

1. Navega hacia este nuevo directorio:

    ```bash
    cd maps/
    ```
    
1. Luego, ejecuta el node `map_saver_cli` del package `map_server` para guardar una copia de tu mapa: <a name="map-saver-cli"></a>

    ```{ .bash .no-copy }
    ros2 run nav2_map_server map_saver_cli -f MAP_NAME
    ```
    Reemplazando `MAP_NAME` con un nombre de tu elección. 

    Esto creará dos archivos: un archivo `MAP_NAME.pgm` y un archivo `MAP_NAME.yaml`, ambos con datos relacionados al mapa que acabas de crear. El archivo `.pgm` contiene un *Mapa de Cuadrícula de Ocupación* (*Occupancy Grid Map, OGM*), que se usa para la *navegación autónoma* en ROS. Observa el mapa lanzándolo en una aplicación de visualización de imágenes llamada `eog`:
    
    ```{ .bash .no-copy }
    eog MAP_NAME.pgm
    ```

    Debería abrirse una nueva ventana con el mapa que acabas de crear con SLAM y el node `map_saver_cli`: 
    
    <figure markdown>
      ![](part3/slam_map.png){width=300px}
    </figure>

    Las regiones blancas representan el área que tu robot ha determinado como espacio abierto en el que puede moverse libremente. Las regiones negras, por otro lado, representan límites u objetos que han sido detectados. Cualquier área gris en el mapa representa regiones que permanecen sin explorar o que eran inaccesibles para el robot.
    
1. Compara el mapa generado por SLAM con el entorno simulado real (en Gazebo). 

    !!! question "Preguntas"
        * ¿Con qué precisión mapeó tu robot el entorno?
        * ¿Qué podría afectar esto al trabajar en un entorno del mundo real?
    
1. Cierra la imagen usando el botón :material-close-circle: en el lado derecho de la ventana *eog*.

### Resumen de SLAM

¿Ves qué fácil fue mapear un entorno en el ejercicio anterior? Esto funciona igual de bien en un robot real en un entorno real también (como observarás en el laboratorio). 

Esto ilustra el poder de ROS: tener acceso a herramientas como SLAM, integradas en el framework ROS, hace que sea muy rápido y fácil para un ingeniero en robótica comenzar a desarrollar aplicaciones robóticas sobre esta base. Nuestro trabajo fue aún más fácil aquí ya que usamos algunos packages pre-configurados para ayudarnos a lanzar SLAM con las configuraciones correctas para el robot de simulación en particular. Si estuvieras desarrollando un robot por tu cuenta, o trabajando con un tipo diferente de robot, podrías necesitar hacer un poco más de trabajo para configurar y ajustar las herramientas SLAM para que funcionen con tu propia aplicación.

## Conclusión

Como aprendimos en la Parte 2, la odometría de un robot se determina mediante la estimación por avance (*dead-reckoning*) y los algoritmos de control basados únicamente en esto (como el node `move_square.py`) pueden estar sujetos a deriva y error acumulado. 

En última instancia, un robot necesita información adicional para determinar con precisión su ubicación dentro de un entorno, y así mejorar su capacidad para navegar de manera efectiva y evitar colisiones.

Esta información adicional puede provenir de un sensor LiDAR, del cual hablamos anteriormente. Exploramos dónde se publican estos datos, cómo accedemos a ellos y qué nos dicen sobre el entorno inmediato de un robot. Luego analizamos algunas formas en que los datos de odometría y desplazamiento láser pueden combinarse para realizar funciones robóticas avanzadas, como el mapeo de un entorno. Todo esto es complicado, pero usando ROS podemos aprovechar estas herramientas con relativa facilidad, lo que ilustra cuán poderoso puede ser ROS para desarrollar aplicaciones robóticas de manera rápida y efectiva, ¡sin tener que reinventar la rueda!

### ¡Guarda tu trabajo! {#backup}

!!! info "Sandbox del Laboratorio (rigsa.io)"
    Tu código se guarda en `/home/student/ros2_ws/src` dentro de la sesión.
    Antes de cerrar la sesión, descárgalo para no perderlo:

    1. En VS Code, haz clic derecho sobre la carpeta `src` en el explorador de archivos → **Descargar…**
    2. O desde la terminal integrada:
    ```bash
    zip -r ~/mi_codigo_parte3.zip ~/ros2_ws/src && echo "¡Listo! ✓"
    ```
    Luego descarga el archivo `mi_codigo_parte3.zip` desde el explorador de VS Code.

!!! note "WSL-ROS2 (Computadoras del laboratorio con escritorio administrado)"
    Ejecuta el siguiente script en cualquier instancia de terminal WSL-ROS2 que no esté en uso:

    ```bash
    wsl_ros backup
    ```

    Esto exportará tu directorio de inicio a tu unidad `U:\`, lo que te permitirá restaurarlo en otra computadora del laboratorio la próxima vez que inicies WSL-ROS2.
