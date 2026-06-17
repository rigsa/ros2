---
title: "Parte 1: Primeros pasos con ROS 2" 
description: Aprende los fundamentos de ROS 2 y familiarízate con algunas herramientas y principios clave, lo que te permitirá programar robots y trabajar con aplicaciones ROS 2 de manera efectiva. 
---

## Introducción

:material-pen: **Ejercicios**: 8  
:material-timer: **Tiempo estimado de finalización**: 2 horas  
:material-gauge-low: **Nivel de dificultad**: Principiante 

### Objetivos

En la primera parte de este laboratorio aprenderás los fundamentos de ROS 2 y te familiarizarás con algunas herramientas y principios clave del framework, lo que te permitirá programar robots y trabajar con aplicaciones ROS 2 de manera efectiva.

A lo largo de este curso, y de aquí en adelante, nos referiremos a ROS 2 simplemente como "ROS" para facilitar las cosas.

En su mayor parte, interactuarás con ROS usando la *línea de comandos de Linux*, por lo que también te familiarizarás con algunas herramientas clave de la línea de comandos de Linux que te serán de ayuda. Finalmente, aprenderás cómo crear algunos Nodes básicos de ROS usando Python y tendrás un primer vistazo de cómo funciona la comunicación a través de ROS Topics e Interfaces.

### Resultados de Aprendizaje Esperados

Al finalizar esta sesión serás capaz de:  

1. Controlar un robot TurtleBot3, en simulación, usando ROS.
1. Lanzar aplicaciones ROS usando `ros2 launch` y `ros2 run`.
1. Consultar aplicaciones ROS en ejecución usando herramientas clave de la línea de comandos de ROS.
1. Crear un package de ROS compuesto por múltiples nodes y programar estos nodes (en Python) para que se comuniquen entre sí usando los métodos de comunicación de ROS.
1. Crear una interfaz de mensaje personalizada de ROS y crear Nodes Python para usarla.
1. Navegar por un sistema de archivos Linux y aprender a realizar diversas operaciones del sistema de archivos desde una terminal Linux.

### Accesos Rápidos

#### Ejercicios

* [Ejercicio 1: Lanzar una simulación y hacer mover un robot](#ex1)
* [Ejercicio 2: Visualizar la Red ROS](#ex2)
* [Ejercicio 3: Explorar ROS Topics y Mensajes](#ex3)
* [Ejercicio 4: Crear tu propio package de ROS](#ex4)
* [Ejercicio 5: Crear un node publisher](#ex5)
* [Ejercicio 6: Crear un node subscriber](#ex6)
* [Ejercicio 7: Definir nuestro propio mensaje](#ex7)
* [Ejercicio 8: Usar un mensaje ROS personalizado](#ex8)

#### Recursos Adicionales

* [Un Publisher Python simple (para el Ejercicio 5)](./part1/publisher.md){target="_blank"}
* [Un Subscriber Python simple (para el Ejercicio 6)](./part1/subscriber.md){target="_blank"}
* [El Publisher del mensaje `Example` (para el Ejercicio 8)](./part1/custom_msg_pub.md){target="_blank"}

## Primeros Pasos

### Paso 1: Acceder a un entorno ROS 2 para este curso

Si aún no lo has hecho, consulta aquí todos los detalles sobre [cómo instalar o acceder a un entorno ROS para este curso](../software/README.md).

### Paso 2: Lanzar ROS

Inicia tu entorno ROS.

1. Si estás usando WSL-ROS2 en una computadora del laboratorio, sigue [las instrucciones aquí para iniciarlo](../software/using-wsl-ros/man-win.md).
1. Si estás [ejecutando WSL-ROS2 en tu propia computadora](../software/installing-wsl-ros2.md), necesitarás abrir la Terminal de Windows para acceder a una instancia de terminal WSL-ROS2.
1. Si estás usando Docker, puedes encontrar [más instrucciones aquí](../software/docker-ros2.md). 

De cualquier manera, ahora deberías tener acceso a ROS 2 a través de una instancia de terminal Linux, y nos referiremos a esta instancia de terminal como **TERMINAL 1**.

### Paso 3: Descargar el Repositorio del Curso

<a name="course-repo"></a>

Hemos preparado algunos packages de ROS específicamente para este curso. Todos se encuentran en [este repositorio de GitHub](https://github.com/tom-howard/tuos_ros/tree/jazzy){target="_blank"}, y deberás descargarlo e instalarlo en tu entorno ROS ahora, antes de continuar.

1. En **TERMINAL 1**, navega hacia el *"ROS Workspace"* usando el comando `cd`[^ros2_ws]:

    [^ros2_ws]: ¿Qué es un ROS 2 Workspace? [Puedes encontrar más información aquí](https://docs.ros.org/en/jazzy/Tutorials/Beginner-Client-Libraries/Creating-A-Workspace/Creating-A-Workspace.html#background){target="_blank"}. 

    ```bash
    cd ~/ros2_ws/src/
    ```

1. Luego, ejecuta el siguiente comando para clonar el repositorio del curso desde GitHub:

    ```bash
    git clone https://github.com/tom-howard/tuos_ros.git -b jazzy
    ```

1. Una vez hecho esto, necesitarás compilarlo usando una herramienta llamada *"Colcon"*[^colcon]:

    [^colcon]: ¿Qué es **Colcon**? [Descubre más aquí](https://docs.ros.org/en/jazzy/Tutorials/Beginner-Client-Libraries/Colcon-Tutorial.html#background){target="_blank"}.

    ```bash
    cd ~/ros2_ws/ && colcon build --packages-up-to tuos_ros && source ~/.bashrc
    ```

No te preocupes demasiado por lo que acabas de hacer por ahora. Lo cubriremos con más detalle a lo largo del curso. Por el momento es suficiente; más adelante empezaremos a usar algunos de los packages que acabamos de instalar.

## :material-pen: Ejercicio 1: Lanzar una simulación y hacer mover un robot {#ex1}

Ahora que todo está en marcha, lancemos ROS y pongamos en funcionamiento una simulación de nuestro robot TurtleBot3 Waffle...

1. En **TERMINAL 1** ingresa el siguiente comando para lanzar una simulación de un TurtleBot3 Waffle en un *mundo vacío*:  
        
    ```bash
    ros2 launch turtlebot3_gazebo empty_world.launch.py
    ```    

1. Se debería abrir una ventana de *Gazebo Sim*:

    <figure markdown>
      ![](../images/gz/tb3_empty_world_top.png){width=800}
    </figure>

    1. **Acercar y alejar** usando la rueda de desplazamiento del mouse.  
    1. **Rotar la vista de la cámara** presionando y manteniendo simultáneamente el botón izquierdo del mouse y la tecla ++shift++ de tu teclado, y luego moviendo el mouse.
    
    Usando ambos métodos deberías poder obtener una mejor vista del robot, que es una representación aproximada de [nuestros robots reales](../about/robots.md#our-waffles).

    <figure markdown>
      ![](../images/gz/tb3_empty_world_close.png){width=700px}
    </figure> 

1. Con la simulación de Gazebo en funcionamiento, regresa a tu terminal y abre una *segunda* instancia de terminal (**TERMINAL 2**)
   
1. En esta nueva instancia de terminal ingresa el siguiente comando:<a name="teleop"></a>

    ```bash
    ros2 run turtlebot3_teleop teleop_keyboard
    ```

1. Sigue las instrucciones proporcionadas en la terminal para controlar el robot usando teclas específicas de tu teclado:

    <figure markdown>
      ![](../images/waffle/teleop_keymap.svg)
    </figure>

### Resumen

Acabas de lanzar varias aplicaciones diferentes en una red ROS usando dos comandos diferentes de ROS: `ros2 launch` y `ros2 run`: 

1. `ros2 launch turtlebot3_gazebo empty_world.launch.py`
1. `ros2 run turtlebot3_teleop teleop_keyboard`

Estos dos comandos tienen una estructura similar, pero funcionan de manera ligeramente diferente.

El primer comando que usaste fue un comando `launch`, que tiene las siguientes dos partes (después de la parte `launch`):

``` { .bash .no-copy }
ros2 launch {[1] Nombre del package} {[2] Archivo launch}
```

La **Parte [1]** es el nombre del *package de ROS* que contiene la funcionalidad que queremos ejecutar. La **Parte [2]** es un archivo dentro de ese package que le indica a ROS exactamente qué scripts (*'nodes'*) queremos lanzar. *Podemos lanzar múltiples nodes al mismo tiempo desde un único archivo launch*.

El segundo comando fue un comando `run`, que tiene una estructura similar a `launch`:

``` { .bash .no-copy }
ros2 run {[1] Nombre del package} {[2] Nombre del node}
```    

Aquí, la **Parte [1]** es la misma que en el comando `launch`, pero la **Parte [2]** es ligeramente diferente: `{[2] Nombre del node}`. Aquí estamos especificando directamente un único script que queremos ejecutar. Por lo tanto, usamos `ros2 run` si solo queremos lanzar un **único node** en la red ROS: el node `teleop_keyboard` (un script Python), en este caso.

## Packages y Nodes de ROS

### Packages

Las aplicaciones ROS se organizan en *packages*. Los packages son básicamente colecciones que contienen scripts, configuraciones y archivos launch (formas de lanzar esos scripts y configuraciones), todos relacionados con alguna funcionalidad robótica común. ROS usa packages como una manera de organizar todos los programas que se ejecutan en un robot.

!!! info  
    El sistema de packages es un concepto fundamental en ROS y todos los programas de ROS se organizan de esta manera.

Crearás varios packages a lo largo de este curso, cada uno conteniendo diferentes nodes, archivos launch y otras cosas más. Comenzaremos a explorar esto más adelante.

### Nodes

Los *Nodes* de ROS son ejecutables que realizan tareas y operaciones específicas del robot. Antes (por ejemplo) usamos `ros2 run` para ejecutar un node llamado `teleop_keyboard`, que nos permitió controlar remotamente (o *"teleop"*) el robot.

!!! question
    ¿Cuál era el nombre del *package* de ROS que contenía el node `teleop_keyboard`? (Recuerda: `ros2 run {[1] Nombre del package} {[2] Nombre del node}`)

Un robot ROS podría tener cientos de nodes individuales ejecutándose simultáneamente para llevar a cabo todas sus operaciones y acciones necesarias. Cada node se ejecuta de forma independiente, pero usa *métodos de comunicación de ROS* para compartir datos con los demás nodes en la red ROS.

## La Red ROS

Podemos usar el comando `ros2 node` para ver todos los nodes que están actualmente activos en una red ROS.

#### :material-pen: Ejercicio 2: Visualizar la Red ROS {#ex2}

Actualmente deberías tener dos instancias de terminal activas: la primera en la que lanzaste la simulación de Gazebo (**TERMINAL 1**) y la segunda con tu node `teleop_keyboard` activo (**TERMINAL 2**).

1. Abre una nueva instancia de terminal ahora (**TERMINAL 3**).
1. Usa el siguiente comando para ver qué nodes están actualmente activos en la red:

    ```bash
    ros2 node list
    ```

    Solo debería aparecer una pequeña cantidad de nodes:

    ``` { .bash .no-copy }
    /robot_state_publisher
    /ros_gz_bridge
    /ros_gz_image
    /teleop_keyboard
    ```

1. Podemos visualizar las conexiones entre los nodes activos usando una aplicación llamada *RQT*. RQT es una colección de herramientas gráficas que nos permiten interactuar e interrogar la red ROS. Lanza la aplicación principal de RQT ingresando `rqt` en **TERMINAL 3** (es posible que veas algunas advertencias en la terminal al hacerlo, pero no te preocupes por ellas):

    ```bash
    rqt
    ```

    Debería abrirse una ventana:

    <figure markdown>
      ![](../images/rqt/main.png){width=600}
    </figure>

1. Desde aquí, queremos cargar el plugin *Node Graph*. Desde el menú superior selecciona `Plugins` > `Introspection` > `Node Graph`.

1. Selecciona `Nodes/Topics (all)` del menú desplegable superior izquierdo, y en la sección **`Hide`** desmarca todo excepto `Debug` y `Params` (puede que necesites presionar el botón de actualizar):

    <figure markdown>
      ![](../images/rqt/node_graph.png){width=600}
      <figcaption>(Haz clic en la imagen para ampliarla.)</figcaption>
    </figure>

    Aquí, los *nodes* están representados por elipses y los *topics* por rectángulos (pasa el cursor sobre una región del gráfico para activar el resaltado de color).

    Esta herramienta nos muestra que (entre otras cosas) el node `/teleop_keyboard` se está comunicando con otro node llamado `/ros_gz_bridge`. La dirección de la flecha nos indica que `/teleop_keyboard` es un *Publisher* y `/ros_gz_bridge` es un *Subscriber*. Los dos nodes se comunican a través de un **ROS Topic** llamado `/cmd_vel`. 

## Publishers y Subscribers: Un *Método de Comunicación de ROS* 

Los ROS Topics son fundamentales para hacer que las cosas sucedan en un robot. Los nodes pueden publicar (*escribir*) y/o subscribirse a (*leer*) ROS Topics para compartir datos a través de la red ROS. Los datos se publican en los topics usando *ROS Messages*. Como acabamos de aprender, el node `teleop_keyboard` estaba publicando mensajes en un topic (`/cmd_vel`) para hacer mover el robot.

Veamos esto con un poco más de detalle...

#### :material-pen: Ejercicio 3: Explorar ROS Topics y Mensajes {#ex3}

Podemos encontrar más información sobre el topic `/cmd_vel` usando el comando `ros2 topic`.

1. Abre *otra* nueva instancia de terminal (**TERMINAL 4**) y escribe lo siguiente:

    ```bash
    ros2 topic list
    ```

    Esto nos muestra todos los topics que están actualmente disponibles en la red ROS (muchos de los cuales vimos en el Node Graph de RQT arriba):

    ``` { .txt .no-copy }
    /camera/camera_info
    /camera/image_raw
    /camera/image_raw/compressed
    /camera/image_raw/compressedDepth
    /camera/image_raw/theora
    /camera/image_raw/zstd
    /clock
    /cmd_vel
    /imu
    /joint_states
    /odom
    /parameter_events
    /robot_description
    /rosout
    /scan
    /tf
    /tf_static
    ```

    Averiguemos un poco más sobre `/cmd_vel`...

1. Usa el comando `topic info` ahora:

    ```bash
    ros2 topic info /cmd_vel
    ```
    
    Esto debería proporcionar la siguiente salida:
    
    ``` { .txt .no-copy }
    Type: geometry_msgs/msg/TwistStamped
    Publisher count: 1
    Subscription count: 1
    ```

    Ahora hemos establecido la siguiente información sobre `/cmd_vel`: <a name="msg-interface-struct"></a>
    
    1. El topic tiene 1 publisher *escribiendo* datos en él (el node `/teleop_keyboard`, como se estableció a partir del RQT Graph)
    1. El topic también tiene 1 subscriber *leyendo* estos datos (el node `ros_gz_bridge`)
    1. Los datos se transmiten en el topic `/cmd_vel` usando una [Interface](https://docs.ros.org/en/jazzy/Concepts/Basic/About-Interfaces.html){target="_blank"}. Esta interface particular se define como: `geometry_msgs/msg/TwistStamped`. 

        **Definiciones de Interfaces**

        Las **Interfaces** son *estructuras de datos estandarizadas* que se usan para transmitir datos a través de la red ROS. La definición de interface anterior (y, de hecho, *toda* definición de interface) tiene tres partes:
        
        1. `geometry_msgs`: el nombre del package de ROS al que pertenece esta interface.
        1. `msg`: indica que esto es un *topic message* en lugar de otro tipo de interface (hay **tres** tipos de interface, y aprenderemos sobre los otros dos más adelante en este curso).
        1. `TwistStamped`: el nombre real de la interface

        En resumen, hemos establecido que si queremos hacer mover el robot necesitamos publicar mensajes `TwistStamped` en el topic `/cmd_vel`.

1. Todavía en **TERMINAL 4**, usa el comando `ros2 interface` para mostrarnos la estructura de datos (estandarizada) usada por la Interface `TwistStamped`:

    ```bash
    ros2 interface show geometry_msgs/msg/TwistStamped
    ```

    De esto, obtenemos lo siguiente:

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

    Aprenderemos más sobre lo que esto significa en la Parte 2.

1. Para finalizar, ingresa ++ctrl+c++ en cada una de las tres terminales que actualmente deberían tener procesos ROS en ejecución (Terminales **1**, **2** y **3**). Las ventanas de Gazebo y del Node Graph de RQT deberían cerrarse como resultado de esto también.

    !!! tip
        Siempre que necesites detener cualquier proceso ROS usa ++ctrl+c++ en la terminal donde está ejecutándose. 

## Creando tus Primeras Aplicaciones ROS

En breve crearemos algunos nodes simples de publisher y subscriber en Python y enviaremos datos simples entre ellos. Como aprendimos antes, los nodes de ROS siempre deben vivir dentro de *packages*, por lo que necesitamos crear un package primero para poder comenzar a crear nuestros propios nodes de ROS.

Es importante trabajar en una ubicación específica del sistema de archivos cuando creamos y trabajamos en nuestros propios packages de ROS. Estos se llaman *"Workspaces"* y ya deberías tener uno listo para usar dentro de tu entorno ROS local llamado `ros2_ws`[^workspaces], con un subdirectorio dentro de él llamado `src`:

``` { .bash .no-copy }
~/ros2_ws/src/
```

**¡Todos los nuevos packages ^^DEBEN^^ estar ubicados dentro de la carpeta `src` del workspace!**

!!! note 
    `~` es un alias para tu directorio home. Entonces `cd ~/ros2_ws/src/` es lo mismo que escribir `cd /home/{tu nombre de usuario}/ros2_ws/src/`.

[^workspaces]: `ros2_ws` es un nombre común utilizado para un ROS 2 workspace en muchos tutoriales en línea, el nombre no importa realmente, podría llamarse de cualquier manera. [Puedes aprender más sobre los ROS 2 Workspaces aquí](https://docs.ros.org/en/jazzy/Tutorials/Beginner-Client-Libraries/Creating-A-Workspace/Creating-A-Workspace.html#background){target="_blank"}. 

#### :material-pen: Ejercicio 4: Crear tu propio package de ROS {#ex4}

La interfaz de línea de comandos (CLI) `ros2` que hemos estado usando hasta ahora incluye una herramienta para crear nuevos packages de ROS: `ros2 pkg create`[^ros2-pkg-create]. Sin embargo, para este curso adoptaremos un enfoque ligeramente diferente para la creación de packages, para brindarnos un poco más de flexibilidad y facilidad de uso (especialmente para cosas que haremos más adelante)[^cpp-py-pkg]. Por lo tanto, hemos creado nuestra propia [Plantilla de Package ROS 2](https://github.com/tom-howard/ros2_pkg_template){target="_blank"} (en GitHub), y ahora veremos cómo usarla para crear nuevos packages...

[^ros2-pkg-create]: Puedes aprender más sobre todo esto en los [Tutoriales Oficiales de ROS 2](https://docs.ros.org/en/jazzy/Tutorials/Beginner-Client-Libraries/Creating-Your-First-ROS2-Package.html){target="_blank"} (si te interesa).

[^cpp-py-pkg]: El enfoque que adoptamos está basado en [este tutorial (cortesía de Robotics Backend)](https://roboticsbackend.com/ros2-package-for-both-python-and-cpp-nodes/){target="_blank"}, así que no dudes en revisarlo si deseas obtener más información.

1. Navega hacia el directorio `ros2_ws/src` usando el comando `cd` de Linux (**c**ambiar **d**irectorio). En **TERMINAL 1** ingresa lo siguiente:

    ```bash
    cd ~/ros2_ws/src/
    ```

1. Desde aquí, usa `git` para *clonar* nuestra *Plantilla de Package ROS 2* desde GitHub:

    ```bash
    git clone https://github.com/tom-howard/ros2_pkg_template.git
    ```
    
1. Esta plantilla de package contiene un script llamado `init_pkg.sh`, que usaremos para convertir la plantilla en nuestro primer package de ROS 2. Ejecuta el script de la siguiente manera, para convertir la plantilla en un package de ROS 2 llamado `part1_pubsub`:

    ```bash
    ./ros2_pkg_template/init_pkg.sh part1_pubsub
    ```

    Como resultado de hacer esto, el directorio `ros2_pkg_template` ha sido renombrado a `part1_pubsub`, y varias otras cosas dentro del package también han sido actualizadas, para inicializar el package con el nombre que especificamos.

1. Navega hacia el directorio del package (usando `cd`):

    ```bash
    cd part1_pubsub/
    ```

1. `tree` es un **comando de Linux** que nos muestra el contenido del directorio actual en un formato de árbol. Usa `tree` ahora para mostrar el contenido actual del directorio `part1_pubsub`:

    ```bash
    tree
    ```

    ...lo que debería mostrar:

    ``` { .txt .no-copy }
    .
    ├── CMakeLists.txt
    ├── package.xml
    ├── part1_pubsub_modules
    │   ├── __init__.py
    │   └── tb3_tools.py
    └── scripts
        ├── basic_velocity_control.py
        └── stop_me.py

    3 directories, 6 files
    ```

    * `scripts`: es un *directorio* que contendrá todos los Nodes Python que crearemos (notarás que ya hay un par allí).
    * `part1_pubsub_modules`: es un *directorio* que podemos usar para almacenar *módulos* Python, que luego podemos importar en nuestros nodes Python principales
        
        (`#!py from part1_pubsub_modules.tb3_tools import ...`, por ejemplo)
    
    * `package.xml` y `CMakeLists.txt`: son ambos *archivos* que definen nuestro package y cómo debe compilarse (usando `colcon build`). Los exploraremos más en breve... 

#### :material-pen: Ejercicio 5: Crear un node publisher {#ex5}

1. Desde la raíz de tu package `part1_pubsub`, navega hacia la carpeta `scripts` usando el comando `cd`.

    ```bash
    cd scripts
    ```

1. `touch` es un **comando de Linux** que podemos usar para crear un archivo vacío. Úsalo para crear un archivo vacío llamado `publisher.py`, al que añadiremos contenido en breve:

    ```bash
    touch publisher.py
    ```

1. Usa `ls` para verificar que el archivo ha sido creado, pero usa la opción `-l` con esto, para que el comando muestre su salida en *"formato de lista larga"*:

    ```bash
    ls -l
    ```

    Esto debería mostrar algo similar a lo siguiente: <a name="no-exec-perms"></a>

    ``` { .txt .no-copy }
    -rwxr-xr-x 1 student student 1500 MMM DD HH:MM minimal_node.py
    -rw-r--r-- 1 student student    0 MMM DD HH:MM publisher.py
    -rwxrwxr-x 1 student student  816 MMM DD HH:MM stop_me.py
    ```

    Esto confirma que el archivo `publisher.py` existe, y el `0` en esa línea indica que el archivo está vacío (es decir, su tamaño actual es de 0 bytes), lo cual es lo esperado.

1. Por lo tanto, ahora necesitamos abrir el archivo y añadirle contenido. Recomendamos usar Visual Studio Code (VS Code) como IDE para este curso. Lanza VS Code y accede a tu entorno ROS 2 (cómo hacerlo variará según cómo tengas ROS instalado en tu computadora).

1. Usando el Explorador de Archivos de VS Code, localiza el archivo `publisher.py` vacío que acabas de crear (`~/ros2_ws/src/part1_pubsub/scripts/`) y haz clic en el archivo para abrirlo en el editor principal.

1. El código de `publisher.py` se proporciona aquí:

    <center>[:material-file-code-outline: El código de `publisher.py`](./part1/publisher.md){ .md-button target="_blank"}</center><a name="pub_ret"></a>

    Échale un vistazo y ten en cuenta el siguiente contenido adicional de esta página también:
    
    * Haz clic en los íconos :material-plus-circle: para expandir las anotaciones en el código. **Es importante que entiendas cómo funciona el código, ¡así que asegúrate de leer estas anotaciones!**
    * Hay una sección adicional debajo del código llamada **"Definición de Dependencias del Package"**. ¡Asegúrate de seguir también los pasos descritos allí!

1. Una vez que hayas revisado el código, toma una copia de él, pégalo en tu archivo `publisher.py` y guárdalo.

1. Ahora, necesitamos añadir nuestro archivo `publisher.py` como un ejecutable al `CMakeLists.txt` de nuestro package. Esto asegurará que se compile cuando ejecutemos `colcon build` (en el siguiente paso).

    En VS Code, abre el archivo `CMakeLists.txt` que está en la raíz del directorio de tu package `part1_pubsub` (`ros2_ws/src/part1_pubsub/CMakeLists.txt`). Localiza las líneas (cerca del final del archivo) que dicen:

    ``` { .txt .no-copy}
    # Install Python executables
    install(PROGRAMS
      scripts/basic_velocity_control.py
      scripts/stop_me.py
      DESTINATION lib/${PROJECT_NAME}
    )
    ```
    
    Añade el Node `publisher.py` de la siguiente manera:

    ``` { .txt .no-copy }
    # Install Python executables
    install(PROGRAMS
      scripts/basic_velocity_control.py
      scripts/stop_me.py
      scripts/publisher.py
      DESTINATION lib/${PROJECT_NAME}
    )
    ```

1. Ahora, usa `colcon` para compilar tu package.
    
    1. **DEBES** ejecutar esto desde la **raíz** de tu Colcon Workspace (es decir: `~/ros2_ws/`), **NO** el directorio `src` (`~/ros2_ws/src/`), así que navega allí ahora usando `cd`:

        ```bash
        cd ~/ros2_ws/
        ```

    1. Luego, usa el siguiente comando `colcon` para compilar tu package:

        ```bash
        colcon build --packages-select part1_pubsub --symlink-install
        ```

        !!! info "¿Qué hacen los argumentos adicionales anteriores?"

            * `--packages-select`: Compila *únicamente* el package `part1_pubsub`, nada más (sin esto, `colcon` intentaría compilar *cada* package en el workspace).
            * `--symlink-install`: Asegura que no tengas que volver a ejecutar `colcon build` cada vez que realices un cambio en los ejecutables de tu package (es decir, tus nodes Python en el directorio `scripts`).
    
    1. Finalmente, "re-sourcea" tu `bashrc`[^source-bashrc]:

        [^source-bashrc]: ¿Qué hace `source ~/.bashrc`? [Consulta aquí para una explicación](https://devconnected.com/source-command-on-linux-explained/#Source_to_update_your_current_shell_environment_bashrc){target="_blank"}.

        ```bash
        source ~/.bashrc
        ```

1. Ahora deberíamos poder ejecutar este node usando el comando `ros2 run`.
    
    Recuerda: `ros2 run {nombre del package} {nombre del script}`, entonces:

    ```bash
    ros2 run part1_pubsub publisher.py
    ```

    ... ¿Hmm, algo no está del todo bien? Si escribiste el comando exactamente como arriba y luego intentaste ejecutarlo, probablemente acabas de recibir el siguiente error:

    ``` { .txt .no-copy }
    No executable found
    ``` 

    <a name="chmod"></a>

    Cuando creamos un archivo usando `touch`, se le asignan ciertos *permisos* por defecto. Recuerda la salida del comando `ls -l` que ejecutamos antes ([haz clic aquí para volver a esto como recordatorio](#no-exec-perms)):

    ``` { .txt .no-copy }
    -rw-r--r-- 1 student student   0 MMM DD HH:MM publisher.py
    ```
        
    La primera parte nos indica sobre los permisos que actualmente están asignados al archivo `publisher.py`:  
    
    <center>`-rw-r--r--`</center>  
    
    Esto nos indica *quién* tiene permiso para hacer *qué* con este archivo y (actualmente) la primera parte: `-rw-`, nos indica que tenemos permiso para **l**eer o **e**scribir en él. Sin embargo, hay una *tercera* opción que también podemos configurar, que es el permiso de *ejecución*, y podemos configurarlo usando el **comando de Linux** `chmod`...

1. Usa `cd` para navegar de vuelta al directorio `scripts` de nuestro package (donde se encuentra el archivo `publisher.py`):

    ```bash
    cd ~/ros2_ws/src/part1_pubsub/scripts/
    ```

    Luego ejecuta el comando `chmod` de la siguiente manera para dar al archivo `publisher.py` permisos de *ejecución*:

    ```bash
    chmod +x publisher.py
    ```

1. Ahora, ejecuta `ls -l` nuevamente para ver qué ha cambiado:
    
    ```bash
    ls -l
    ```

    Ahora hemos otorgado permiso para que el archivo también sea e**j**ecutado:
    
    ``` { .txt .no-copy }
    -rwxr-xr-x 1 student student 1195 MMM DD HH:MM publisher.py
    ```

1. Bien, ahora usa `ros2 run` nuevamente para (*¡con suerte!*) ejecutar el node `publisher.py` (recuerda: `ros2 run {nombre del package} {nombre del script}`).
    
    Si ves un mensaje en la terminal similar al siguiente, entonces el node se ha lanzado exitosamente:
        
    ``` { .txt .no-copy }
    [INFO] [#####] [simple_publisher]: The 'simple_publisher' node is initialised.
    ```

    ¡Genial!

1. Podemos verificar adicionalmente que nuestro node publisher está en ejecución usando varias herramientas diferentes. Intenta ejecutar los siguientes comandos en **TERMINAL 2**:

    1. `ros2 node list`: Esto proporcionará una lista de todos los *nodes* que están actualmente activos en el sistema. Verifica que el nombre de nuestro node publisher sea visible en esta lista (¡probablemente es el *único* elemento en la lista en este momento!).
    1. `ros2 topic list`: Esto proporcionará una lista de los *topics* que actualmente están siendo usados por los nodes del sistema. Verifica que el nombre del topic al que nuestro publisher está publicando mensajes (`/my_topic`) esté presente en esta lista.

### Interrogando ROS Topics {#rostopic}

Hasta ahora hemos usado el comando ROS `ros2 topic` con dos argumentos adicionales:

* `list`: para proporcionarnos una *lista* de todos los topics que están activos en nuestro sistema ROS, y
* `info`: para proporcionarnos *información* sobre un topic de interés en particular.

Podemos averiguar qué otros *sub-comandos* están disponibles para usar con `ros2 topic` solicitando *ayuda*. Ejecuta lo siguiente en **TERMINAL 2**:

```bash
ros2 topic --help
```

Lo que debería proporcionarnos una lista de todas las opciones:

``` { .txt .no-copy }
Commands:
  bw     Display bandwidth used by topic
  delay  Display delay of topic from timestamp in header
  echo   Output messages from a topic
  find   Output a list of available topics of a given type
  hz     Print the average publishing rate to screen
  info   Print information about a topic
  list   Output a list of available topics
  pub    Publish a message to a topic
  type   Print a topic's type

  Call `ros2 topic <command> -h` for more detailed usage.
```

Hablemos de algunos de estos:

* `ros2 topic hz {nombre del topic}` proporciona información sobre la frecuencia (en Hz) a la que se están publicando mensajes en un topic:

    ```bash
    ros2 topic hz /my_topic
    ```

    Esto debería decirnos que nuestro node publisher está publicando mensajes en el topic `/my_topic` a (o cerca de) 1 Hz, que es exactamente lo que solicitamos en el archivo `publisher.py` (en la parte `__init__` de nuestra clase `Publisher`). Ingresa ++ctrl+c++ para detener este comando.

* `ros2 topic echo {nombre del topic}` muestra los mensajes que se están publicando en un topic:

    ```bash
    ros2 topic echo /my_topic
    ```

    Esto proporcionará un flujo en vivo de los mensajes que nuestro node `publisher.py` está publicando en el topic `/my_topic`. Ingresa ++ctrl+c++ para detener esto.

* Podemos ver algunas opciones adicionales para el comando `echo` viendo la documentación de ayuda para este también:

    ```bash
    ros2 topic echo --help
    ```

    Desde aquí, por ejemplo, podemos aprender que si solo quisiéramos imprimir el primer mensaje que se recibió podríamos usar la opción `--once`, por ejemplo:

    ```bash
    ros2 topic echo /my_topic --once
    ```

#### :material-pen: Ejercicio 6: Crear un node subscriber {#ex6}

Para ilustrar cómo se puede pasar información de un node a otro (a través de topics y mensajes) ahora crearemos otro node para *subscribirse* al topic al que nuestro node publisher está transmitiendo mensajes.

1. En **TERMINAL 2** usa los comandos del sistema de archivos que se introdujeron antes (`cd`, `ls`, etc.) para navegar hacia la carpeta `scripts` de tu package `part1_pubsub`.

1. Usa el mismo procedimiento que antes para crear un nuevo archivo Python vacío llamado `subscriber.py` ¡y recuerda hacerlo ejecutable! <a name="sub_ret"></a>

1. Luego, abre este archivo `subscriber.py` recién creado en VS Code.

1. El código del archivo `subscriber.py` se proporciona aquí:

    <center>[:material-file-code-outline: El código de `subscriber.py`](./part1/subscriber.md){ .md-button target="_blank"}</center>
    
    Una vez más, es importante que entiendas cómo funciona este código, ¡así que **asegúrate de leer las anotaciones del código**!

    !!! warning "¡Completa el `{BLANK}`!"
        ¡Este código no funcionará *de inmediato*! Busca un `{BLANK}`, que es una indicación para que reemplaces este texto con algo más. 

1. Ahora necesitamos añadir esto como un ejecutable *adicional* del package.

    Abre el archivo `CMakeLists.txt` en la raíz del directorio de tu package `part1_pubsub` nuevamente, regresa a la sección `# Install Python executables` y añade el archivo `subscriber.py` como se ilustra a continuación:

    ``` { .txt .no-copy }
    # Install Python executables
    install(PROGRAMS
      scripts/basic_velocity_control.py
      scripts/stop_me.py
      scripts/publisher.py
      scripts/subscriber.py
      DESTINATION lib/${PROJECT_NAME}
    )
    ```

1. Ahora necesitamos ejecutar `colcon build` nuevamente.
    
    1. Asegúrate de estar en la **raíz** del Colcon Workspace:

        ```bash
        cd ~/ros2_ws/
        ```

    1. Ejecuta `colcon build` solo en el package `part1_pubsub`:

        ```bash
        colcon build --packages-select part1_pubsub --symlink-install
        ```

    1. Y luego re-sourcea el `bashrc`:

        ```bash
        source ~/.bashrc
        ```

1. Usa `ros2 run` (en **TERMINAL 2**) para ejecutar tu node `subscriber.py` recién creado (recuerda: `ros2 run {nombre del package} {nombre del script}`). Si tus nodes publisher y subscriber están funcionando correctamente deberías ver una salida como esta:
    
    <figure markdown>
      ![](part1/subscriber_output.gif){width=700px}
    </figure>

1. Interroga tu red ROS:

    1. Como antes, podemos saber qué nodes están ejecutándose en nuestro sistema usando el comando `ros2 node list`. Ejecuta esto en **TERMINAL 3**, deberías ver tanto tu node publisher *como* tu node subscriber listados allí.

    1. Usa el comando `ros2 topic` para *listar* todos los topics que están disponibles en la red. Deberías ver `/my_topic` listado allí.

    1. Usa el comando `ros2 topic` nuevamente para encontrar más *info* sobre `my_topic`.
    
    1. Usa el comando `ros2 interface` para *mostrar* qué tipo de datos se están enviando entre los dos nodes.

1. Finalmente, cierra tus nodes publisher y subscriber ingresando ++ctrl+c++ en las terminales donde están ejecutándose (deberían ser 1 y 2).

#### :material-pen: Ejercicio 7: Definir nuestro propio mensaje {#ex7}

Acabamos de crear un publisher y un subscriber que pudieron comunicarse entre sí a través de un topic.

<figure markdown>
  ![](./part1/pub_sub_rosgraph.png)
</figure>

Los datos que el publisher enviaba al topic eran muy simples: un mensaje de tipo `example_interfaces/msg/String`.

``` { .txt .no-copy }
ros2 topic info /my_topic

Type: example_interfaces/msg/String
Publisher count: 1
Subscription count: 1
```


Este mensaje solo tiene un *campo* llamado `data` de tipo `string`:

``` { .txt .no-copy }
ros2 interface show ros2 topic info -t /my_topic

string data
```

Los mensajes ROS generalmente serán más complejos que esto, típicamente conteniendo varios campos en un solo mensaje. Ahora definiremos nuestro propio mensaje personalizado, esta vez con dos campos, para que puedas ver cómo funcionan las cosas con estructuras de datos *un poco* más complejas.

1. Las interfaces de mensajes deben definirse dentro de una carpeta `msg` en la raíz de nuestro directorio del package, así que vamos a crear esta carpeta ahora en **TERMINAL 1**:

    1. Primero, navega hacia tu package:

        ``` bash
        cd ~/ros2_ws/src/part1_pubsub
        ```
    
    1. Luego usa `mkdir` para crear un nuevo directorio:

        ```bash
        mkdir msg
        ```

1. Crearemos un mensaje llamado `Example`, y para hacerlo necesitaremos crear un nuevo archivo llamado `Example.msg` dentro de la carpeta `msg`:

    ```bash
    touch msg/Example.msg
    ```

1. Para definir la estructura de datos de este mensaje, ahora necesitamos abrir el archivo y añadir el siguiente contenido:

    ```txt title="Example.msg"
    string info
    int32 time
    ```

    El mensaje tendrá por lo tanto dos campos:

    <center>

    | # | Nombre del Campo | Tipo de Dato |
    | :---: | :---: | :---: |
    | 1 | `info` | `string` |
    | 2 | `time` | `int32` |

    </center>

    Podemos dar a nuestros campos cualquier nombre que queramos, pero los tipos de datos deben ser [tipos incorporados](https://docs.ros.org/en/jazzy/Concepts/Basic/About-Interfaces.html#field-types){target="_blank"} u otras interfaces ROS preexistentes.

1. Ahora necesitamos declarar este mensaje en el archivo `CMakeLists.txt` de nuestro package, para que el código Python necesario pueda ser creado (por `colcon build`) y nos permita importar este mensaje en nuestros propios archivos Python.

    Añade las siguientes líneas a tu archivo `part1_pubsub/CMakeLists.txt`, encima de la línea `ament_package()`:

    ```txt title="CMakeLists.txt"
    find_package(rosidl_default_generators REQUIRED)
    rosidl_generate_interfaces(${PROJECT_NAME}
      "msg/Example.msg" 
    )
    ```

1. También necesitamos modificar nuestro archivo `package.xml`. Añade las siguientes líneas a este, justo encima de la línea `#!xml <export>`:

    ```xml title="package.xml"
    <buildtool_depend>rosidl_default_generators</buildtool_depend>
    <exec_depend>rosidl_default_runtime</exec_depend>
    <member_of_group>rosidl_interface_packages</member_of_group>
    ```

1. Ahora podemos usar Colcon para generar el código fuente necesario para el mensaje:

    1. Primero, asegúrate de estar en la raíz del ROS 2 Workspace:
        
        ```bash
        cd ~/ros2_ws/
        ```
    
    1. Luego ejecuta `colcon build`:

        ```bash
        colcon build --packages-select part1_pubsub --symlink-install 
        ```
    
    1. Y finalmente re-sourcea el `.bashrc`:

        ```bash
        source ~/.bashrc
        ```

1. Ahora podemos verificar que esto funcionó con más herramientas de línea de comandos de `ros2`:

    1. Primero, *lista* todos los mensajes ROS que están disponibles para nosotros en nuestro sistema:

        ```bash
        ros2 interface list -m
        ```

        Desplázate por esta lista y comprueba si puedes encontrar nuestro mensaje allí (estará listado como `part1_pubsub/msg/Example`)

    1. Luego, *muestra* la estructura de datos de la interface:

        ```bash
        ros2 interface show part1_pubsub/msg/Example
        ```

        Esto debería coincidir con cómo lo definimos en nuestro archivo `part1_pubsub/msg/Example.msg`.

#### :material-pen: Ejercicio 8: Usar un mensaje ROS personalizado {#ex8}

1. Crea una copia del archivo `publisher.py` del [Ejercicio 5](#ex5). También hagamos esto desde la línea de comandos (en **TERMINAL 1**):

    1. Navega hacia la carpeta `scripts` de tu package:

        ```bash
        cd ~/ros2_ws/src/part1_pubsub/scripts
        ```
    
    1. Y usa el comando `cp` para hacer una copia del archivo `publisher.py` y llamar a este nuevo archivo `custom_msg_publisher.py`:

        ```bash
        cp publisher.py custom_msg_publisher.py
        ```
    
    1. También hagamos una copia del archivo `subscriber.py`, ya que estamos aquí:

        ```bash
        cp subscriber.py custom_msg_subscriber.py
        ```

1. Declara estos dos nuevos archivos como ejecutables adicionales en nuestro `CMakeLists.txt`:

    ```txt title="CMakeLists.txt"
    # Install Python executables
    install(PROGRAMS
      scripts/basic_velocity_control.py
      scripts/stop_me.py
      scripts/publisher.py
      scripts/subscriber.py
      scripts/custom_msg_publisher.py  # AÑADIR ESTO 
      scripts/custom_msg_subscriber.py # Y ESTO
    DESTINATION lib/${PROJECT_NAME}
    )
    ```

1. Ejecuta Colcon nuevamente (¡última vez!):

    1. Primero:
        ```bash
        cd ~/ros2_ws
        ```
    1. Luego:
        ```bash
        colcon build --packages-select part1_pubsub --symlink-install
        ```
    1. Y finalmente:
        ```bash
        source ~/.bashrc
        ```

1. Ahora modifica tu archivo `custom_msg_publisher.py` según el código proporcionado a continuación:

    <center>[:material-file-code-outline: El código de `custom_msg_publisher.py`](./part1/custom_msg_pub.md){ .md-button target="_blank"}</center>
    
1. **Tarea Final**:

    Modifica el node `custom_msg_subscriber.py` ahora para adaptarlo a los nuevos mensajes de interface que se están publicando en `/my_topic`.

## Conclusión

En esta sesión hemos cubierto los fundamentos de ROS, y aprendido sobre algunos conceptos clave como *Packages*; *Nodes*; y cómo enviar datos a través de una red ROS usando *Topics*, *Messages* y el *Método de Comunicación Publisher-Subscriber*.

Hemos aprendido cómo usar algunos comandos clave de `ros2`:

* `launch`: para lanzar múltiples Nodes de ROS a través de archivos launch.
* `run`: para ejecutar ejecutables dentro de un package de ROS.
* `node`: para mostrar información sobre los Nodes de ROS activos.
* `topic`: para mostrar información sobre los topics de ROS activos.
* `interface`: para mostrar información sobre *todas* las Interfaces de ROS que están disponibles para usar en una aplicación ROS.

También hemos aprendido cómo trabajar en la Terminal de Linux y navegar por un sistema de archivos Linux usando comandos clave como:

* `ls`: lista los archivos en el directorio actual.
* `cd`: cambiar directorio para moverse por el sistema de archivos.
* `mkdir`: crear un nuevo directorio (`mkdir {nueva_carpeta}`).
* `chmod`: modificar permisos de archivos (es decir, para añadir permisos de ejecución a un archivo para todos los usuarios: `chmod +x {archivo}`).
* `touch`: crear un archivo sin ningún contenido.

Además de esto, también hemos aprendido cómo crear un package de ROS 2, y cómo crear nodes Python simples que pueden *publicar* y *subscribirse* a topics en una red ROS.

Hemos trabajado con mensajes ROS prefabricados para hacer esto y también hemos creado nuestra propia interface de mensaje personalizada para ofrecer una funcionalidad más avanzada.

### Usuarios de WSL-ROS2 con Computadoras del Laboratorio: ¡Guarda tu trabajo! {#backup}

Recuerda, el trabajo que has realizado en el entorno WSL-ROS2 durante esta sesión **no se preservará** automáticamente para futuras sesiones o en diferentes computadoras del laboratorio. Para guardar el trabajo que has realizado hoy deberías ejecutar ahora el siguiente script en cualquier instancia de Terminal WSL-ROS2 inactiva:

```bash
wsl_ros backup
```

Esto exportará tu directorio home a tu unidad `U:\`, permitiéndote restaurarlo en otra computadora del laboratorio la próxima vez que inicies WSL-ROS2.
