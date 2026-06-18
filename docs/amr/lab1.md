---  
title: "Lab 1: Robótica Móvil"
---  

!!! info 
    Deberías poder completar los ejercicios 1 al 7 de esta página dentro de una sesión de laboratorio de dos horas.

## Introducción

En este primer lab del curso *'Industry 4.0'* aprenderás a usar ROS 2 (la versión más reciente de [el Robot Operating System](https://www.ros.org/){target="_blank"}) para controlar el movimiento de un robot.

ROS 2 es un framework de programación robótica de código abierto y estándar industrial, utilizado en una variedad de industrias como la agricultura, la automatización de almacenes y fábricas, y la manufactura avanzada.

ROS 2 nos permite programar robots utilizando diferentes lenguajes de programación (incluyendo C++, Java, MATLAB, etc.), pero usaremos Python en estos laboratorios. Además, ROS 2 se ejecuta sobre un sistema operativo Linux llamado *'Ubuntu'*, por lo que también aprenderemos un poco sobre cómo usarlo.

Trabajaremos con un robot diferencial de simulación. Para más información sobre los robots del laboratorio, visita la [página de robots](../about/robots.md).

!!! warning "Trabajo previo al laboratorio"
    Debes haber completado el test previo al laboratorio antes de comenzar. Este está disponible en la plataforma del curso.

### Objetivos

En este laboratorio aprenderás a usar ROS 2 para hacer que un robot se mueva, y también veremos cómo crear nuestro propio script básico de ROS 2 (o *'Node'*), usando Python.

De aquí en adelante, nos referiremos a ROS 2 simplemente como *"ROS"* por comodidad.

### Resultados de Aprendizaje

Al finalizar esta sesión serás capaz de:

1. Controlar un robot de simulación desde una laptop usando ROS.
1. Lanzar aplicaciones ROS en la laptop y el robot usando `ros2 launch` y `ros2 run`.
1. Interrogar una red ROS usando herramientas *de línea de comandos* y *gráficas*.
1. Usar métodos de comunicación de ROS para publicar mensajes.
1. Usar un sistema operativo Linux y trabajar dentro de una terminal Linux.

### Acceso rápido

* [Ejercicio 1: Lanzar ROS y hacer mover al robot](#ex1)
* [Ejercicio 2: ¡Los sensores del robot en acción!](#ex2)
* [Ejercicio 3: Visualizar la red ROS](#ex3)
* [Ejercicio 4: Explorar Topics y Mensajes de ROS](#ex4)
* [Ejercicio 5: Publicar comandos de velocidad en el topic `/cmd_vel`](#ex5)
* [Ejercicio 6: Crear un paquete ROS](#ex6)
* [Ejercicio 7: Un node de Python para hacer mover al robot](#ex7)
* [Ejercicio 8 (Avanzado): Trayectorias de movimiento alternativas](#ex8)

## El Laboratorio

!!! info "Evaluación"
    Este laboratorio es **evaluado de forma sumativa**.

    1. Existe un **cuestionario post-lab** que deberás completar después de esta sesión, el cual será publicado en la plataforma del curso.
    1. También serás evaluado por el trabajo que realices **en el laboratorio** para el [Ejercicio 7](#ex7).

### Primeros pasos

Antes de hacer cualquier cosa, necesitarás poner en marcha tu robot y asegurarte de que ROS esté funcionando.

#### :material-pen: Ejercicio 1: Lanzar ROS y hacer mover al robot {#ex1}

Ya deberías tener un robot y una laptop disponibles (¡de hecho, probablemente ya estés leyendo esto en la laptop!)

1. Primero, identifica el robot que tienes asignado. Cada uno de nuestros robots tiene un nombre único: `robot-X`, donde `X` es el *'Número de Robot'*. Revisa la etiqueta impresa en la parte superior del robot para saber cuál te corresponde.

1. Abre una instancia de terminal en la laptop, ya sea presionando las teclas ++ctrl+alt+t++ simultáneamente, o haciendo clic en el ícono de la aplicación Terminal en la barra de favoritos del escritorio:
    
    <figure markdown>
      ![](../images/laptops/terminal_icon.svg?width=60px)
    </figure>
        
    Nos referiremos a esta terminal como **TERMINAL 1**.
    
1. En **TERMINAL 1** escribe el siguiente comando para *vincular* la laptop y el robot, de modo que puedan trabajar juntos:

    ***
    
    **TERMINAL 1:**
    ``` { .bash .no-copy }
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
    ``` { .bash .no-copy }
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
    ros2 launch rigsa_tb3_tools ros.launch.py enable_depth:=true
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

    No necesitarás interactuar con esta instancia de terminal, pero la pantalla te proporcionará información en tiempo real sobre el estado del robot. Déjala abierta en segundo plano y revisa el indicador de `Battery` de vez en cuando:

    ``` { .txt .no-copy } 
    Battery: 12.40V [100%]
    ```

    !!! info "Batería baja :material-battery-low:"

        **¡La batería del robot no durará una sesión completa de 2 horas!**

        Cuando el indicador de capacidad llegue a alrededor del 15%, comenzará a emitir pitidos, y cuando llegue al ~10%, dejará de funcionar por completo. Informa a un miembro del equipo de enseñanza cuando la batería esté baja y la reemplazarán. (Es más fácil hacerlo cuando llega al 15%, en lugar de esperar hasta que baje del 10%.)

    ¡ROS ya está funcionando en el robot y estamos listos para comenzar!

    Deja **TERMINAL 1** como está, ejecutándose en segundo plano durante el resto del laboratorio.

1. El siguiente **paso crucial** es conectar la laptop a la red ROS que acabamos de establecer en el robot. Los dos dispositivos se comunicarán entre sí a través de la red inalámbrica, pero se requiere un paso más para vincularlos.

    Abre **una nueva instancia de terminal** en la laptop (ya sea con el atajo ++ctrl+alt+t++ o haciendo clic en el ícono de la terminal) e ingresa el siguiente comando:

    ***
    **TERMINAL 2:**

    ```bash
    ros2 run rmw_zenoh_cpp rmw_zenohd
    ```
    ***

    Deja ambas terminales ejecutándose en segundo plano **en todo momento** mientras trabajas con tu robot.

1. A continuación, abre una *nueva instancia de terminal* en la laptop (presionando ++ctrl+alt+t++ o haciendo clic en el ícono de la terminal). La llamaremos **TERMINAL 3**.

1. En **TERMINAL 3** ingresa el siguiente comando:
    
    ***
    **TERMINAL 3:**
    ```bash
    ros2 run turtlebot3_teleop teleop_keyboard
    ```
    ***

1. Sigue las instrucciones proporcionadas en la terminal para conducir el robot usando las teclas del teclado:

    <figure markdown>
      ![](../images/cli/teleop_keymap.svg)
    </figure>

1. Presiona ++ctrl+c++ en **TERMINAL 3** para detener el node Teleop cuando hayas terminado.
    
### Paquetes y Nodes

Las aplicaciones ROS se organizan en *paquetes*. Los paquetes son básicamente carpetas que contienen scripts, configuraciones y archivos de lanzamiento (formas de ejecutar esos scripts y configuraciones).

Los *scripts* le dicen al robot qué hacer y cómo actuar. En ROS, estos scripts se llaman *nodes*. Los *ROS Nodes* son programas ejecutables que realizan tareas y operaciones específicas del robot. Generalmente se escriben en C++ o Python, aunque es posible escribir ROS Nodes en otros lenguajes de programación también.

En el Ejercicio 1 lanzaste una amplia variedad de nodes en la red ROS usando los comandos `ros2 launch` y `ros2 run`:

1. `ros2 launch rigsa_tb3_tools ros.launch.py ...` (en el *robot*, en **TERMINAL 1**)
1. `ros2 run rmw_zenoh_cpp rmw_zenohd` (en la *laptop*, en **TERMINAL 2**)
1. `ros2 run turtlebot3_teleop teleop_keyboard` (en la *laptop*, en **TERMINAL 3**)

El primero de los anteriores fue un comando ROS `launch`, que tiene las siguientes partes clave (después de la parte `ros2 launch`):

``` { .bash .no-copy }
ros2 launch {[1] Nombre del paquete} {[2] Archivo de lanzamiento} {[3] Argumentos (opcional)}
```

Los primeros **dos** son los más importantes:

**Parte [1]** especifica el nombre del *paquete ROS* que contiene la funcionalidad que queremos ejecutar.  
**Parte [2]** es un archivo dentro de ese paquete que le dice a ROS exactamente qué scripts (*'nodes'*) queremos lanzar. Podemos lanzar múltiples nodes al mismo tiempo desde un solo archivo de lanzamiento.

El segundo y tercer comando fueron comandos ROS `run`: <a name="ros2-run"></a>

``` { .bash .no-copy }
ros2 run {[1] Nombre del paquete} {[2] Nombre del node}
```    

Aquí, **la Parte [1]** es igual que el comando `ros2 launch`, pero **la Parte [2]** es ligeramente diferente: `{[2] Nombre del node}`. Aquí especificamos directamente un solo script que queremos ejecutar. Por lo tanto, usamos `ros2 run` si solo queremos lanzar **un único node** en la red ROS (por ejemplo, `teleop_keyboard`, que es un script de Python).

!!! info "Post-lab"
    ¿Cuáles fueron los nombres de los tres paquetes que invocamos en el Ejercicio 1?

#### :material-pen: Ejercicio 2: ¡Los sensores del robot en acción! {#ex2}

Nuestros Waffles tienen sensores bastante sofisticados que les permiten "ver" el mundo a su alrededor. No los utilizaremos mucho durante este laboratorio, pero este ejercicio te permitirá ver cómo los datos de estos dispositivos podrían usarse para que nuestros robots hagan cosas muy avanzadas (¡con una programación inteligente, por supuesto!)

##### Parte 1: La Cámara

1. No debería haber nada ejecutándose en **TERMINAL 3** ahora, después de haber cerrado el node `teleop_keyboard` al final del ejercicio anterior (++ctrl+c++). Regresa a esta terminal y lanza el node `rqt_image_view`:

    ***
    **TERMINAL 3:**
    ```bash
    ros2 run rqt_image_view rqt_image_view
    ```
    ***

    !!! info "Post-lab"
        1. Estamos usando `ros2 run` de nuevo aquí, ¿qué significa esto?
        1. ¿Por qué tuvimos que escribir `rqt_image_view` dos veces?
    
1. Debería abrirse una nueva ventana. Maximízala (si aún no lo está) y selecciona `/camera/color/image_raw` del menú desplegable en la parte superior izquierda de la ventana de la aplicación.
1. ¡Las imágenes en vivo de la cámara del robot deberían ser visibles ahora! Pon tu cara frente a la cámara y verte aparecer en la pantalla de la laptop.
1. Cierra la ventana cuando hayas visto suficiente (presiona ++ctrl+c++ en **TERMINAL 3**). Esto debería liberar **TERMINAL 3** para que puedas ingresar comandos nuevamente.

    La cámara del robot es un dispositivo bastante inteligente. Dentro de la unidad hay dos sensores de imagen separados, lo que le da efectivamente un ojo izquierdo y un ojo derecho. El dispositivo combina los datos de ambos sensores y usa la información combinada para inferir también la profundidad de las imágenes. Veamos eso en acción ahora...

1. En **TERMINAL 3** ingresa el siguiente comando:

    ***
    **TERMINAL 3:**
    ```bash
    ros2 launch rigsa_tb3_tools rviz.launch.py
    ```
    ***
    
    Esto lanzará una aplicación llamada *RViz*, que es una herramienta útil que nos permite *visualizar* los datos de todos los sensores a bordo de nuestros robots. Cuando se abra RViz, deberías ver algo similar a lo siguiente:

    <figure markdown>
      ![](../images/laptops/waffle_rviz.png){width=700px}
    </figure>

    En el menú "Displays" del lado izquierdo, haz clic en la casilla junto al elemento "DepthCloud".

    <figure markdown>
      ![](../images/laptops/waffle_rviz_depth_cloud.png){width=600px}
    </figure>

    La extraña hoja ondulante de colores que debería aparecer frente al robot es la transmisión de imágenes en vivo de la cámara con profundidad aplicada al mismo tiempo. La cámara puede determinar qué tan lejos está cada píxel de imagen del objetivo de la cámara y luego usa eso para generar esta representación tridimensional.

1. Nuevamente, coloca tu mano o tu cara frente a la cámara y mantén la posición durante unos segundos (puede haber algo de retraso ya que todos estos datos se transmiten a través de la red WiFi). ¡Deberías verte renderizado en 3D frente al robot!

##### Parte 2: El Sensor LiDAR

En RViz es posible que también hayas notado muchos puntos verdes dispersos alrededor del robot. Esta es una representación de los *datos de desplazamiento* provenientes del sensor LiDAR (el dispositivo negro en la parte superior del robot). El sensor LiDAR gira continuamente, enviando pulsos láser al entorno a medida que lo hace. Cuando un pulso golpea un objeto, se refleja de vuelta al sensor, y el tiempo que tarda en ocurrir esto se usa para calcular qué tan lejos está el objeto.
    
El sensor LiDAR gira y realiza este proceso continuamente en incrementos de 1°, por lo que se puede generar un escaneo completo de 360° del entorno. Por lo tanto, estos datos son muy útiles para cosas como la *evasión de obstáculos* y la *cartografía*. Echemos un vistazo rápido a esto último ahora.

1. Cierra RViz (haz clic en el botón "Close without saving" si se te solicita).

1. Regresa a **TERMINAL 3** y ejecuta el siguiente comando:

    ***
    **TERMINAL 3:**
    ```bash
    ros2 launch rigsa_tb3_tools slam.launch.py
    ```
    ***

    Se abrirá una nueva pantalla de RViz, esta vez mostrando el robot desde una vista superior, y con los datos del LiDAR representados por puntos multicolores.

    <figure markdown>
      ![](../images/laptops/waffle_slam.png){width=700px}
    </figure>

    Debajo de los puntos del LiDAR deberías notar que se está formando un mapa, con líneas negras que representan objetos fijos en el entorno y áreas blancas que representan espacio libre por el que el robot podría desplazarse. ROS está usando un proceso llamado *SLAM* (Localización y Cartografía Simultáneas) para generar un mapa del entorno utilizando los datos del sensor LiDAR.

1. Abre una nueva instancia de terminal, la llamaremos **TERMINAL 4**. Lanza el node `teleop_keyboard` en esta, de la misma forma que lo hiciste antes:

    ***
    **TERMINAL 4:**
    ```bash
    ros2 run turtlebot3_teleop teleop_keyboard
    ```
    ***

1. Conduce el robot un poco y observa cómo el mapa en RViz se actualiza a medida que el robot explora nuevas partes del entorno.

1. Presiona ++ctrl+c++ en **TERMINAL 4** para detener el node `teleop_keyboard`.

1. Cierra la ventana de RViz, o presiona ++ctrl+c++ en **TERMINAL 3** para detenerla también.

Ya hemos usado tanto `ros2 launch` como `ros2 run` para lanzar aplicaciones ROS. Estas son *herramientas de línea de comandos* de ROS, y hay muchas más a nuestra disposición.

Al usar `ros2 run` y `ros2 launch` como hemos hecho hasta ahora, es fácil terminar con muchos procesos o *ROS Nodes* diferentes ejecutándose en la red, algunos de los cuales interactuaremos directamente, pero otros pueden simplemente estar ejecutándose en segundo plano. A menudo es útil saber exactamente qué *está* ejecutándose en la red ROS, y hay varias formas de hacerlo.

#### :material-pen: Ejercicio 3: Visualizar la red ROS {#ex3}

1. No debería haber nada ejecutándose en **TERMINAL 3** ahora, así que regresa a esta terminal y usa el comando `ros2 node` para *listar* los nodes que están actualmente en ejecución en el robot:

    ***
    **TERMINAL 3:**
    ```bash
    ros2 node list
    ```
    ***

    Deberías ver una lista de 6 elementos.

1. Podemos visualizar las conexiones entre los nodes activos usando un node ROS llamado `rqt_graph`. Lánzalo de la siguiente manera:

    ***
    **TERMINAL 3:**
    ```bash
    ros2 run rqt_graph rqt_graph
    ```
    ***
    
1. En la ventana que se abre, selecciona `Nodes/Topics (active)` del menú desplegable en la parte superior izquierda.

    Lo que deberías ver es un mapa de todos los nodes de la lista anterior (como óvalos), y flechas para ilustrar el flujo de información entre ellos. ¡Esta es una representación visual de la red ROS!

    <figure markdown>
      ![](../images/rqt/graph_waffle.png){width=600px}
    </figure>
    
    Los elementos con un borde rectangular son *ROS Topics*. Los Topics de ROS son esencialmente canales de comunicación, y los nodes ROS pueden leer (*suscribirse*) o escribir (*publicar*) en estos topics para acceder a datos de sensores, pasar información por la red y hacer que sucedan cosas.

1. Regresa a **TERMINAL 4** y lanza el node `teleop_keyboard` nuevamente:

    ***
    **TERMINAL 4:**
    ```bash
    ros2 run turtlebot3_teleop teleop_keyboard
    ```
    ***

1. Regresa a la ventana de RQT Graph y presiona el ícono de actualización (a la izquierda del menú desplegable `Nodes/Topics (active)`).

    <figure markdown>
      ![](../images/rqt/graph_waffle_teleop.png){width=600px}
    </figure>

    !!! info "Post-lab"
        ¿Qué ha cambiado? Asegúrate de saber cómo interpretar estos gráficos.

Un robot ROS podría tener cientos de nodes individuales ejecutándose simultáneamente para llevar a cabo todas sus operaciones y acciones necesarias. Cada node se ejecuta de forma independiente, pero usa *métodos de comunicación ROS* para comunicarse y compartir datos con los otros nodes en la red ROS.

### Publicadores y Suscriptores: Un *Método de Comunicación ROS*

Los topics de ROS son clave para hacer que las cosas sucedan en un robot. Los nodes pueden publicar (*escribir*) y/o suscribirse a (*leer*) topics de ROS para compartir datos en la red ROS. Debemos usar estructuras de datos estandarizadas en ROS para que todo esto funcione. Diferentes topics usan diferentes estructuras de datos, y hay muchos *tipos* de estructuras de datos disponibles para usar (incluso podemos definir las nuestras propias, pero esto va más allá del alcance de esta sesión de laboratorio). Echemos un vistazo más detallado a los topics y sus estructuras de datos ahora...

#### :material-pen: Ejercicio 4: Explorar Topics e Interfaces de ROS {#ex4}

Al igual que el comando `ros2 node list`, podemos usar `ros2 topic list` para listar todos los *topics* que están actualmente activos en la red.

1. Cierra la ventana `rqt_graph` si aún no lo has hecho. Esto liberará **TERMINAL 3** para que podamos ingresar comandos en ella nuevamente. Deja el node `teleop_keyboard` en **TERMINAL 4** ejecutándose. Regresa a **TERMINAL 3** e introduce lo siguiente:

    ***
    **TERMINAL 3:**
    ```bash
    ros2 topic list
    ```
    ***

    Ahora debería imprimirse en la terminal una lista mucho más grande de elementos. Ve si puedes encontrar `/cmd_vel` en la lista.
    
    Este topic se usa para controlar la velocidad del robot (*'command velocity'*).

1. Averigüemos más sobre esto usando el comando `ros2 topic info`.

    ***
    **TERMINAL 3:**
    ```bash
    ros2 topic info /cmd_vel
    ```
    ***

    Esto debería proporcionar una salida similar a la siguiente:
    
    ``` { .txt .no-copy }
    Type: geometry_msgs/msg/TwistStamped
    Publisher count: 1
    Subscription count: 1
    ```

    Esto nos dice varias cosas: <a name="rostopic_info_explained"></a>
    
    1. El topic `/cmd_vel` actualmente tiene 1 publicador (es decir, 1 node escribiendo datos en el topic).
    1. También hay 1 *suscriptor* (es decir, otro node leyendo los datos que se escriben en el topic).
    1. Si pensamos en `rqt_graph` (del ejercicio anterior), sabemos que el publicador es el node `/teleop_keyboard`, y el suscriptor es un node llamado `/turtlebot3_node`. Este node convierte los datos del topic en comandos de motor, resultando en el movimiento real de las ruedas del robot.
    1. El *tipo* de estructura de datos que usa el topic `/cmd_vel` se define como:  
        
        <center>`geometry_msgs/msg/TwistStamped`</center>
        
        Esta es una *"Interface"* de ROS.

        **Interfaces**
    
        Las estructuras de datos en ROS 2 se llaman *Interfaces*.
        
        De la salida anterior, `Type` se refiere al *tipo* de estructura de datos (es decir, el tipo de interface). La definición de `Type` tiene tres partes: `geometry_msgs`, `msg` y `TwistStamped`:
        
        1. `geometry_msgs` es el nombre del paquete ROS al que pertenece esta interface (estructura de datos).
        1. `msg` nos indica que es una interface de *mensaje* de topic (en lugar de otro tipo de interface).
        1. `TwistStamped` es el *nombre* de la interface de mensaje.

        Hemos aprendido entonces que, si queremos hacer que el robot se mueva, necesitamos publicar mensajes de interface `TwistStamped` al topic `/cmd_vel`.

1. Podemos usar el comando `ros2 interface` para encontrar más información sobre el mensaje `TwistStamped`:

    ***
    **TERMINAL 3:**
    ```bash
    ros2 interface show geometry_msgs/msg/TwistStamped
    ```
    ***

    De esto, la parte inferior es la que más nos interesa: <a name="show-twist"></a>

    ``` { .txt .no-copy }
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

    Hmm, esto parece complicado. Averigüemos qué significa todo esto...

### Control de Velocidad

El movimiento de cualquier robot móvil se puede definir en términos de sus tres *ejes principales*: `X`, `Y` y `Z`. En el contexto del robot de simulación, estos ejes (y el movimiento alrededor de ellos) se definen de la siguiente manera:

<figure markdown>
  ![](../images/waffle/principal_axes.svg){width=700px}
</figure>

En teoría, un robot puede moverse *linealmente* o *angularmente* alrededor de cualquiera de estos tres ejes, como se muestra por las flechas en la figura. Eso son seis *Grados de Libertad* (DOFs) en total, logrados según el diseño del robot y los actuadores con los que está equipado. Vuelve a ver la salida de `ros2 interface show` en **TERMINAL 3**. Esperemos que ahora esté más claro que estos mensajes de topic están formateados para darle a un programador de ROS la capacidad de *pedirle* a un robot que se mueva en cualquiera de sus seis DOFs.

``` { .txt .no-copy }
Vector3  linear
        float64 x  <-- Adelante (o Atrás)
        float64 y  <-- Izquierda (o Derecha)
        float64 z  <-- Arriba (o Abajo)
Vector3  angular
        float64 x  <-- "Alabeo" (Roll)
        float64 y  <-- "Cabeceo" (Pitch)
        float64 z  <-- "Guiñada" (Yaw)
```

¡Nuestro TurtleBot3 solo tiene dos motores, así que en realidad no tiene seis DOFs! Estos dos motores pueden controlarse de forma independiente, en una configuración de *"accionamiento diferencial"*, pero esto aún solo le permite moverse con **dos grados de libertad** en total, como se ilustra a continuación.

<figure markdown>
  ![](../images/waffle/velocities.svg){width=700px}
</figure>

Por lo tanto, la velocidad solo puede aplicarse **linealmente** en el **eje x** (*Adelante/Atrás*) y **angularmente** en el **eje z** (*Guiñada/Yaw*).

!!! info "Post-lab"
    Toma nota de todo esto, ¡puede haber una pregunta sobre ello!

#### :material-pen: Ejercicio 5: Publicar comandos de velocidad en el topic "cmd_vel" {#ex5}

1. Detén el node `teleop_keyboard` ahora presionando ++ctrl+c++ en **TERMINAL 4**. Vamos a usar otra herramienta gráfica para ayudarnos a publicar mensajes en el topic `/cmd_vel` *directamente*.
1. Regresa a **TERMINAL 3** e ingresa el siguiente comando para lanzar el node *RQT Message Publisher*:

    ***
    **TERMINAL 3:**
    ```bash
    ros2 run rqt_publisher rqt_publisher
    ```
    ***

    <figure markdown>
      ![](../images/rqt/msg_pub.png){width=600px}
    </figure>

1. En el menú desplegable "**Topic**" selecciona `/cmd_vel`.

1. Muévete hacia la derecha e ingresa un valor de `10` en el cuadro junto a la etiqueta "**Freq.**".

1. Más a la derecha, haz clic en el cuadro :material-plus-box: para añadir esto como publicador a la *"Tabla de Publicadores"* principal.

1. En la Tabla de Publicadores, haz clic en el :octicons-triangle-right-16: junto a `/cmd_vel` para expandir el elemento y revelar dos elementos adicionales: `header` y `twist`:

    <figure markdown>
      ![](../images/rqt/msg_pub_cmd_vel.png){width=600px}
    </figure>

1. Haz clic en el ícono :octicons-triangle-right-16: junto a `twist`, y luego en los íconos :octicons-triangle-right-16: subsiguientes junto a los elementos `linear` y `angular` que aparecen debajo. Finalmente, verás algunos valores en la columna "**expression**":

    <figure markdown>
      ![](../images/rqt/msg_pub_cmd_vel_values.png){width=600px}
    </figure>

    ¿Se parece esto a [la definición de la interface que vimos en la terminal antes](#show-twist)?

1. Usando lo que aprendimos anteriormente sobre la forma en que el robot puede moverse, cambia **uno** de los seis valores en la columna "expression" que creas que podría hacer que el robot ***gire sobre sí mismo***. Antes de hacerlo, vale la pena tener en cuenta lo siguiente:
    
    1. La unidad de velocidad *lineal* es metros por segundo (m/s).
    1. La unidad de velocidad *angular* es radianes por segundo (rad/s).
    1. Nuestros robots Waffle pueden moverse con una **velocidad lineal máxima** de 0.26 m/s y una **velocidad angular máxima** de 1.82 rad/s.

1. Una vez que hayas ingresado un valor, haz clic en la casilla de verificación a la izquierda de `/cmd_vel` para comenzar a publicar estos valores en el topic. ¡Observa qué hace tu robot!

1. Vuelve el valor a `0.0` y presiona ++enter++ para detener el robot.

1. A continuación, encuentra un valor de velocidad alternativo que puedas configurar para hacer que el robot ***avance***. (No olvides volver el valor a `0.0` para detener el robot nuevamente después.)

1. Finalmente, introduce una *combinación* de valores de velocidad para hacer que el robot ***se mueva en círculo***.

1. Una vez que hayas terminado, vuelve todas las velocidades a `0.0`, asegúrate de que el robot ya no se esté moviendo, y luego desmarca la casilla junto a `/cmd_vel` para dejar de publicar mensajes. Haz clic en el botón :material-close-circle: en la esquina superior derecha de la ventana del Message Publisher para cerrarlo.

Con suerte ya puedes ver que, para hacer mover a un robot, simplemente se trata de publicar el Interface Message de ROS correcto (`TwistStamped`) en el topic de ROS correcto (`/cmd_vel`). Al principio del laboratorio usamos el node `teleop_keyboard` para conducir el robot, un poco como un carro de control remoto. En el fondo, todo lo que realmente estaba sucediendo era que el node convertía las pulsaciones de teclas de nuestro teclado en comandos de velocidad y los publicaba en el topic `/cmd_vel`. En el ejercicio anterior examinamos esto con más detalle aplicando directamente valores a los atributos correctos del mensaje y usando el RQT Message Publisher para publicarlos. Sin embargo, hay un límite en lo que podemos lograr trabajando de esta manera (¡el movimiento circular y en línea recta es básicamente todo!)

En realidad, los robots necesitan poder moverse por entornos complejos de forma autónoma, lo cual es una tarea bastante difícil y requiere que construyamos aplicaciones específicas. Podemos construir estas aplicaciones usando Python, y veremos los conceptos básicos detrás de esto en los siguientes ejercicios, comenzando por construir un Node simple que nos permita hacer que nuestro robot sea un poco más "autónomo". Lo que haremos aquí forma la base de los enfoques más complejos utilizados por los ingenieros de robótica para realmente dar vida a los robots.

#### :material-pen: Ejercicio 6: Crear un paquete ROS {#ex6}

Como aprendimos antes, todos los nodes ROS deben estar contenidos dentro de *paquetes*, por lo que para crear nuestro propio node, primero necesitamos crear nuestro propio paquete.

1. En **TERMINAL 3** ejecuta el siguiente comando para navegar a una carpeta llamada el *"Espacio de Trabajo ROS"* usando el comando `cd` ("cambiar directorio"):

    ```bash
    cd ~/ros2_ws/src
    ```

1. A continuación, ejecuta el siguiente comando para copiar una plantilla de paquete de GitHub en la carpeta del Espacio de Trabajo ROS:

    ```bash
    git clone https://github.com/tom-howard/ros2_pkg_template.git
    ```

1. Ahora, ejecuta un script desde dentro de esta plantilla para inicializar el paquete:

    ```bash
    ./ros2_pkg_template/init_pkg.sh robotics_lab1
    ```

1. Abriremos este paquete en un editor de texto llamado *Visual Studio Code* (también conocido como "VS Code") ahora, para que podamos empezar a hacer cambios:

    ```bash
    code ./robotics_lab1
    ```

1. Cuando se abra VS Code, deberías ver un *Explorador de Archivos* en el lado izquierdo que te permite acceder a todos los archivos y carpetas dentro de tu paquete.
    
    <figure markdown>
      ![](./lab1/vscode_explorer_package_xml.png){width=400px}
    </figure>

    Busca un archivo llamado `package.xml` aquí y haz clic en él. Esto abrirá este archivo en la ventana principal de VS Code para que puedas editarlo.

1. Busca las siguientes líneas en el archivo `package.xml`:

    ``` title="package.xml"
    <maintainer email="nombre.apellido1@institucion.edu">Nombre 1</maintainer>
    <maintainer email="nombre.apellido2@institucion.edu">Nombre 2</maintainer>
    ```

    Cambia `Nombre 1` a tu nombre completo, y `nombre.apellido1@institucion.edu` a tu correo institucional. Haz lo mismo para el otro miembro de tu grupo en la línea inferior. (Si están trabajando en un grupo de más de 2 personas, pueden agregar líneas adicionales debajo de esta para los demás miembros del grupo.)

    !!! warning "Post-lab"
        **¡Esto es importante para el post-lab!**

        Evaluaremos tu trabajo aquí como parte del post-lab, por lo que es importante que podamos identificar a cada miembro de tu grupo. Si algún miembro del grupo no está listado aquí, ¡no recibirá calificación por esto!

        Al ingresar los nombres, asegúrate de proporcionar nombres **Y** apellidos para cada miembro del grupo.

1. Regresa a **TERMINAL 3** ahora y ejecuta los siguientes tres comandos:

    1. Primero: 
        
        ```bash
        cd ~/ros2_ws
        ```
    
    1. Luego:

        ```bash
        colcon build --symlink-install --packages-select robotics_lab1
        ```

    1. Y finalmente:

        ```bash
        source ~/.bashrc
        ```

Bien, **la creación del paquete ya está completa**, así que estamos listos para comenzar con la programación en Python...

#### :material-pen: Ejercicio 7: Un node de Python para hacer mover al robot {#ex7}

Regresa a VS Code ahora, y (en el Explorador de Archivos) busca una carpeta llamada `scripts`. Haz clic en el ícono :material-chevron-right: junto a esta para expandir la carpeta y revelar su contenido. Se debería revelar un archivo llamado `basic_velocity_control.py`. Haz clic en él para abrirlo en la ventana principal del editor.

<figure markdown>
  ![](./lab1/vscode_explorer_scripts.png){width=400px}
</figure>

Este es un Node de Python de ROS 2 (bastante) básico que controlará la velocidad del robot. Analicémoslo:
    
1. Primero, tenemos algunas importaciones:

    ```py
    import rclpy # (1)!
    from geometry_msgs.msg import TwistStamped # (2)!
    import time # (3)!
    ```

    1. `rclpy` es la biblioteca cliente de ROS para Python. La necesitamos para que nuestro node de Python pueda interactuar con ROS.
    2. [Sabemos de antes](#ex4) que para hacer mover a un robot necesitamos publicar mensajes en el topic `/cmd_vel`, y que este topic usa una estructura de datos (o Interface) llamada `geometry_msgs/msg/TwistStamped`. Así es como importamos la interface en nuestro node de Python para poder crear comandos de velocidad para nuestro robot (a lo que llegaremos en breve...).
    3. Usaremos esto para controlar el tiempo en nuestro node.

    Haz clic en los íconos :material-plus-circle: de arriba para revelar más información sobre cada línea del código.

1. A continuación, declaramos algunas variables que podemos usar y adaptar durante la ejecución principal de nuestro código:

    ```py
    state = 1 # (1)!
    vel = TwistStamped() # (2)!
    ```

    1. Dentro del bucle `#!py while` (explicado próximamente) definimos dos estados operativos diferentes para el robot, y podemos controlar cuál está activo cambiando este valor de `1` a `2` (y viceversa).
    2. Estamos instanciando un mensaje de Interface `TwistStamped` aquí y lo llamamos `vel`. Asignaremos valores de velocidad a esto en el bucle `#!py while` más adelante.
        
        Recuerda que un mensaje `TwistStamped` contiene seis componentes diferentes a los que podemos asignar valores. [¿Cuáles *dos* son relevantes para nuestro robot?](#velocity-control)

1. A continuación, configuramos algunas cosas importantes relacionadas con ROS:

    ```py
    rclpy.init(args=None) # (1)!
    node = rclpy.create_node("basic_velocity_control")  # (2)!
    vel_pub = node.create_publisher(TwistStamped, "cmd_vel", 10)  # (3)!
    ```

    1. Inicializa `rclpy` y todas las comunicaciones ROS necesarias para nuestro node.
    2. Inicializa este script de Python como un node ROS real, proporcionando un nombre para que se registre en la red ROS ("basic_velocity_control" en este caso).
    3. Aquí estamos configurando un publicador en el topic `/cmd_vel` para que el node pueda enviar comandos de velocidad al robot (usando datos `TwistStamped`).

1. Después de esto, definimos otra variable:

    ```py
    timestamp = node.get_clock().now().nanoseconds # (1)!
    ```

    1. ¿Qué hora es ahora mismo? Esto nos indica el "Tiempo ROS" actual (en nanosegundos), que será útil para comparar en el bucle while.

1. Ahora, entramos en un bucle `#!py while`, donde nuestro código pasará la mayor parte de su tiempo una vez que esté en ejecución:

    ```py
    while rclpy.ok(): # (1)!
        time_now = node.get_clock().now().nanoseconds # (2)!
        elapsed_time = (time_now - timestamp) * 1e-9 # (3)!

        ...

    ```

    1. Esto devuelve `#!py True` mientras el node esté vivo, por lo que todo el código dentro del bucle `#!py while` continuará ejecutándose mientras ese sea el caso.
    2. ¿Qué hora es *ahora*? Verifica la hora al comienzo de cada iteración del bucle `#!py while` y asígnala a una variable llamada `time_now`.
    3. Determina cuánto tiempo ha transcurrido (en segundos) desde que se actualizó por última vez el `timestamp`.

    Todo lo que está sangrado debajo de la línea `#!py while rclpy.ok():` continuará ejecutándose una y otra vez hasta que le pidamos que nuestro node se detenga. El código se ejecutará línea por línea de arriba a abajo dentro de este bucle `#!py while`, y luego regresará al principio y lo repetirá todo una y otra y *otra* vez. Cada repetición se llama una *"iteración"*.

    1. Una instrucción `#!py if` ahora controla el estado de operación para nuestro robot.
        
        1. En el estado `1` establecemos velocidades que harán que el robot avance (solo velocidad lineal X) durante un cierto tiempo y luego se detenga. ¿Cuánto tiempo avanzará el robot y a qué velocidad?

            ```py
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
            2. Establece una velocidad lineal para que el robot avance.
            3. Si el tiempo transcurrido ha *superado* los 2 segundos...
            4. Establece las velocidades de nuestro robot a `0.0` para detenerlo.
            5. En la próxima iteración del bucle, pasa al estado 2.
            6. Reinicia el timestamp para comenzar a contar de nuevo.

        2. En el estado `2` establecemos velocidades que harán que el robot gire sobre sí mismo (solo velocidad angular Z) durante un cierto tiempo y luego se detenga. ¿Durante cuánto tiempo hará esto y a qué velocidad?
            
            ```py
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
            2. Aplica una velocidad angular al robot para que gire sobre sí mismo.
            3. Una vez que el tiempo transcurrido haya *superado* los 4 segundos...
            4. Vuelve las velocidades del robot a `0.0` para detenerlo.
            5. En la próxima iteración del bucle, vuelve al estado 1 (avanzar).
            6. Reinicia el timestamp una vez más.

    1. Y después de la instrucción `#!py if`:

        ```py
        node.get_logger().info( # (1)!
            f"\n[State = {state}] Publishing velocities:\n"
            f"  - linear.x: {vel.twist.linear.x:.2f} [m/s]\n"
            f"  - angular.z: {vel.twist.angular.z:.2f} [rad/s].",
            throttle_duration_sec=1,
        )
        vel_pub.publish(vel) # (2)!
        ```

        1. Esto (y las siguientes 5 líneas) imprimirá un mensaje en la terminal para proporcionarnos actualizaciones regulares sobre el estado actual del node y qué velocidades se han establecido (en la instrucción `#!py if` anterior).
        2. Esta línea es crucial: esta operación publica los comandos de velocidad en el topic `/cmd_vel`, para que el robot actúe según nuestras instrucciones.

            Independientemente de lo que suceda en los estados `if` anteriores, *siempre* publicamos un comando de velocidad en el topic `/cmd_vel` aquí (cada iteración del bucle).


1. Regresa a **TERMINAL 3** ahora, ejecuta el código y observa lo que sucede. *¡Asegúrate de que el robot esté en el suelo y tenga suficiente espacio para moverse antes de hacer esto!*
    
    ***
    **TERMINAL 3:**
    ```bash
    ros2 run robotics_lab1 basic_velocity_control.py
    ```
    ***
    
    Presiona ++ctrl+c++ en **TERMINAL 3** para detener el node cuando hayas visto suficiente.
    
    !!! warning
        ¡El robot seguirá moviéndose incluso después de que hayas detenido el node! Ejecuta el siguiente comando para detenerlo:
        
        ```bash
        ros2 run robotics_lab1 stop_me.py
        ```
    
1. **Tu tarea**:
    
    El objetivo aquí es hacer que el robot siga una **trayectoria cuadrada** de dimensiones **0.5m x 0.5m**. Sin embargo, tal como está, el node `basic_velocity_control.py` no hace esto aún, ¡y necesitas arreglarlo!
        
    ¡Edita el código para que el robot siga realmente una **trayectoria cuadrada de 0.5m x 0.5m**!

    !!! info "Post-lab"
        Como se discutió anteriormente, ¡tu completitud de este ejercicio será evaluada como parte del post-lab!

#### :material-pen: Ejercicio 8 (Avanzado): Trayectorias de movimiento alternativas {#ex8}

*Si tienes tiempo, inténtalo ahora...*

¿Cómo podrías adaptar el código para lograr perfiles de movimiento más interesantes?

1. Primero, regresa a **TERMINAL 3** y asegúrate de estar en la ubicación correcta del sistema de archivos:

    ```bash
    cd ~/ros2_ws/src/robotics_lab1/scripts
    ```

1. Luego, haz una copia del código `basic_velocity_control.py` usando el comando `cp` (**c**o**p**iar):

    ```bash
    cp basic_velocity_control.py alt_velocity_control.py
    ```
    Esto creará una copia llamada `alt_velocity_control.py`

1. Usa el siguiente comando para abrir un archivo de texto en VS Code:

    ```bash
    code ../CMakeLists.txt
    ```

1. En este archivo, ubica las líneas (cerca del final del archivo) que dicen:

    ``` { .txt .no-copy}
    # Install Python executables
    install(PROGRAMS
      scripts/basic_velocity_control.py
      scripts/stop_me.py
      DESTINATION lib/${PROJECT_NAME}
    )
    ```

    Inserta una nueva línea debajo de la que dice `scripts/basic_velocity_control.py`, de modo que ahora se vea así:

    ``` { .txt .no-copy }
    # Install Python executables
    install(PROGRAMS
      scripts/basic_velocity_control.py
      scripts/alt_velocity_control.py
      scripts/stop_me.py
      DESTINATION lib/${PROJECT_NAME}
    )
    ```

    Acabas de agregar `alt_velocity_control.py` como un nuevo node dentro de tu paquete.

    Guarda el archivo y ciérralo.

1. Regresa a **TERMINAL 3** y ejecuta los siguientes 3 comandos nuevamente, en orden:

    1. Primero: 
        
        ```bash
        cd ~/ros2_ws
        ```
    
    1. Luego:

        ```bash
        colcon build --symlink-install --packages-select robotics_lab1
        ```

    1. Y finalmente:

        ```bash
        source ~/.bashrc
        ```

1. Regresa a VS Code y encuentra tu nuevo archivo `alt_velocity_control.py`. Haz clic en él para abrirlo en el editor.
    
1. **AHORA** intenta editarlo para lograr alguno de los perfiles de movimiento más complejos ilustrados a continuación.

    <figure markdown>
      ![](./lab1/move_alt.png)
    </figure>

    1. **Perfil (a):** El robot necesita seguir una trayectoria en forma de *figura ocho*, donde un comando de velocidad lineal y angular se establece simultáneamente para generar movimiento circular. Se deberán definir velocidades para lograr **un diámetro de trayectoria de 1m** para cada uno de los dos bucles. Habiendo establecido las velocidades apropiadamente, necesitarás calcular cuánto tiempo tardaría el robot en completar cada bucle, para poder determinar cuándo el robot habrá regresado a su punto de partida. En ese momento necesitarás cambiar la dirección de giro, para que el robot pase del giro en sentido antihorario al giro en sentido horario.
    1. **Perfil (b):** El robot necesita comenzar y terminar en la misma posición, pero moverse por los puntos intermedios 1-7, en secuencia, para generar el perfil de *cuadrados apilados* como se muestra. Cada uno de los dos cuadrados debe ser de **1m x 1m**, por lo que necesitarás encontrar los pares correctos de velocidad y duración para avanzar y girar. ¡También necesitarás cambiar la dirección de giro cuando el robot llegue al Punto 3, y luego nuevamente en el Punto 7!

1. Para ejecutar el archivo y probarlo, necesitarás usar `ros2 run ...`. ¿Cómo formatearías este comando ([recuerda esto](#ros2-run))?[^run-alt]

    Siempre que necesites detener el node, presiona ++ctrl+c++ en la terminal.

    [^run-alt]: `#!bash ros2 run robotics_lab1 alt_velocity_control.py`

    !!! warning "Recuerda"
        ¡El robot seguirá moviéndose incluso después de que hayas detenido el node! Ejecuta el siguiente comando para detenerlo cuando lo necesites:
        
        ```bash
        ros2 run robotics_lab1 stop_me.py
        ```

## Cierre

Antes de irte, ¡por favor apaga tu robot! Introduce el siguiente comando en **TERMINAL 3** para hacerlo:

***
**TERMINAL 3:**
``` { .bash .no-copy }
waffle X off
```
... nuevamente, reemplazando `X` con el número del robot con el que has estado trabajando hoy.
***

Necesitarás ingresar `y` y luego presionar ++enter++ para confirmar.

Luego apaga la laptop, lo cual puedes hacer haciendo clic en el ícono de batería en la parte superior derecha del escritorio, haciendo clic en el ícono de energía y seleccionando "Power Off..." en el menú.

<figure markdown>
  ![](../images/laptops/ubuntu_poweroff.svg){width=300px}
</figure>

<center>

**¡Lab 1 de Industry 4.0 Completado!**  
*¡Nos vemos en el Lab 2!*

</center>
