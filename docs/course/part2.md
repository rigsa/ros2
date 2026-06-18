---  
title: "Parte 2: Odometría y Navegación"  
description: Aprende sobre la odometría - posición y orientación del robot en su entorno - y aplica métodos de control de velocidad en lazo abierto y cerrado a un robot diferencial.
---

## Introducción

:material-pen: **Ejercicios**: 6  
:material-timer: **Tiempo Estimado de Completación**: 3 horas  
:material-gauge: **Nivel de Dificultad**: Intermedio  

### Objetivos

En la Parte 2 aprenderemos cómo controlar la **posición** y la **velocidad** de un robot ROS tanto desde la línea de comandos como mediante Nodes de ROS. También aprenderemos a interpretar los datos que nos permiten monitorear la posición de un robot en su entorno físico (odometría). Los temas cubiertos aquí forman la base de la navegación de robots en ROS, desde métodos simples de lazo abierto hasta control en lazo cerrado más avanzado (ambos los exploraremos).

### Resultados de Aprendizaje Esperados

Al finalizar esta sesión serás capaz de:

1. Interpretar los datos de Odometría publicados por un Robot ROS e identificar las partes de estos mensajes de interfaz que son relevantes para un robot de accionamiento diferencial de dos ruedas.
1. Desarrollar nodes de Python para obtener datos de Odometría desde una red ROS activa y *traducir* esto en información útil sobre la *pose* de un robot de forma conveniente y legible para humanos.
1. Implementar *control de velocidad en lazo abierto* de un robot usando herramientas de línea de comandos de ROS.
1. Desarrollar nodes de Python que usen métodos de control de velocidad en lazo abierto para hacer que un robot siga una trayectoria de movimiento predefinida.
1. Combinar los métodos de comunicación de publisher *y* subscriber en un único node de Python para implementar control de velocidad en lazo cerrado (basado en odometría) de un robot.
1. Explicar las limitaciones de los métodos de control de movimiento basados en Odometría. 

### Enlaces Rápidos

#### Ejercicios

* [Ejercicio 1: Explorando los Datos de Odometría](#ex1)
* [Ejercicio 2: Creando un Node de Python para Procesar Datos de Odometría](#ex2)
* [Ejercicio 3: Controlando la Velocidad con el CLI de ROS 2](#ex3)
* [Ejercicio 4: Creando un Node de Python para Hacer que un Robot Se Mueva en Círculo](#ex4)
* [Ejercicio 5: Implementando un Procedimiento de Apagado](#ex5)
* [Ejercicio 6: Haciendo que Nuestro Robot Siga una Trayectoria Cuadrada](#ex6)

#### Recursos Adicionales

* [Un Node Subscriber de Odometría](./part2/odom_subscriber.md){target="_blank"}
* [Un Node Simple de Control de Velocidad (Move Circle)](./part2/move_circle.md){target="_blank"}
* [Navegación Basada en Odometría (Move Square)](./part2/move_square.md){target="_blank"}

## Primeros Pasos

**Paso 1: Inicia tu Entorno ROS 2**

Si aún no lo has hecho, inicia tu entorno ROS ahora:

1. **WSL-ROS2 en una computadora del laboratorio**: sigue [las instrucciones aquí para iniciarlo](../software/using-wsl-ros/man-win.md).
1. **[Ejecutando WSL-ROS2 en tu propia máquina](../software/installing-wsl-ros2.md)**: inicia el Terminal de Windows para acceder a una instancia de terminal WSL-ROS2.
1. **Usuarios de Docker**: sigue [las instrucciones](../software/docker-ros2.md).

Ahora deberías tener acceso a ROS 2 a través de una instancia de terminal Linux. Nos referiremos a esta instancia de terminal como **TERMINAL 1**.

**Paso 2: Restaura tu trabajo (SOLO Usuarios de Escritorio Administrado WSL-ROS2)**

Recuerda que [cualquier trabajo que realices dentro del Entorno WSL-ROS2 no se conservará entre sesiones o en diferentes computadoras del laboratorio](../software/using-wsl-ros/man-win.md#backing-up-and-restoring-your-data). Al [final de la Parte 1](./part1.md#backup) deberías haber ejecutado la herramienta `wsl_ros` para respaldar tu directorio home en tu Unidad `U:\`. Una vez que WSL-ROS2 esté funcionando, se te pedirá que lo restaures:

``` { .txt .no-copy }
It looks like you already have a backup from a previous session:
  U:\wsl-ros\ros2-backup-XXX.tar.gz
Do you want to restore this now? [y/n]
```

Ingresa ++y+enter++ para restaurar tu trabajo de la última vez. También puedes restaurar tu trabajo en cualquier momento usando el siguiente comando:

```bash
wsl_ros restore
```

**Paso 3: Inicia VS Code** 

También vale la pena iniciar VS Code ahora, para que esté listo cuando lo necesites más adelante. 

??? warning "Usuarios de WSL..."
        
    Es importante iniciar VS Code dentro de tu entorno WSL usando la extensión "WSL". Recuerda siempre verificar esto:

    <figure markdown>
      ![](../software/figures/code-wsl-ext-on.svg){width=400px}
    </figure>

**Paso 4: Asegúrate de que el Repositorio del Curso Esté Actualizado**

<a name="course-repo"></a>

En la Parte 1 deberías haber [descargado e instalado el Repositorio del Curso](./part1.md#course-repo) en tu entorno ROS. Si aún no lo has hecho, regresa y hazlo ahora. Si *ya* lo hiciste, vale la pena asegurarse de que esté actualizado, así que ejecuta el siguiente comando en **TERMINAL 1** ahora:

```bash
cd ~/ros2_ws/src/rigsa_ros/ && git pull
```

Luego compila con Colcon: 

```bash
cd ~/ros2_ws/ && colcon build --packages-up-to rigsa_ros
```

Y finalmente, recarga tu entorno:

```bash
source ~/.bashrc
```

!!! warning
    Si tienes otras instancias de terminal abiertas, deberás ejecutar `source ~/.bashrc` en estas también, para que cualquier cambio realizado por el proceso de compilación de Colcon se propague a estas.

**Paso 5: Inicia la Simulación del Robot**

En **TERMINAL 1** ingresa el siguiente comando para iniciar una simulación del robot en un mundo vacío:  
        
```bash
ros2 launch turtlebot3_gazebo empty_world.launch.py
```

Se debería abrir una ventana de simulación Gazebo y dentro de ella deberías ver el robot de simulación en espacio vacío:

<figure markdown>
  ![](../images/gz/tb3_empty_world_mid.png){width=700px}
</figure>

## Topics e Interfaces de ROS (de la Parte 1)

En la Parte 1 aprendimos sobre los Topics de ROS, y sobre cómo el node `teleop_keyboard` puede usarse para publicar mensajes a un topic particular con el fin de controlar la velocidad del robot (y así cambiar su *posición*).

!!! question "Preguntas"
    1. ¿Qué *topic* se usa para controlar la velocidad del robot?
    1. ¿Qué *interfaz* usa este topic?

    [Regresa aquí si necesitas un recordatorio sobre cómo encontrar las respuestas a estas preguntas](./part1.md#ex3).

Recuerda que los Topics son clave para hacer que las cosas sucedan en un robot: los datos se transmiten entre los Nodes en una red ROS a través de Topics usando estructuras de datos estandarizadas llamadas Interfaces de Mensajes, lo que permite a cada uno de estos nodes tomar decisiones y realizar las tareas necesarias para dar vida al robot.

Habiendo investigado el topic `/cmd_vel` en la Parte 1, veamos ahora otro topic: `/odom`, y consideremos qué significa la información aquí y para qué se usa.

## Odometría {#odometry}

La Odometría es un proceso de monitoreo de la *posición* y *orientación* de un robot en un entorno, lo cual (como aprenderemos) es esencial para la navegación de robots. La posición y orientación de un robot se denomina su *pose*. La pose de un robot es tridimensional, y por lo tanto se define en términos de tres *"Ejes Principales"*: `X`, `Y` y `Z`. En el contexto de nuestro robot de simulación, estos ejes y el movimiento a su alrededor se definen de la siguiente manera:

<a name="principal-axes"></a>

<figure markdown>
  ![Ejes principales del robot diferencial](../images/waffle/principal_axes.svg){width=800}
</figure>

No todas las posiciones y orientaciones anteriores aplican a nuestro robot de simulación, y exploraremos esto más adelante.

### La Odometría en Acción

Recuerda de la Parte 1 el comando que podemos usar para listar *todos* los topics disponibles en nuestro robot:

```bash
ros2 topic list
```

Deberías ver `/odom` en esta lista, que es donde se publican los datos de Odometría de nuestro robot. Ejecuta el comando `ros2 topic` nuevamente, pero esta vez con una opción adicional `-t`:

```bash
ros2 topic list -t
```

Busca `/odom` nuevamente en la lista, y *ahora* notarás que la definición de interfaz se proporciona entre corchetes junto al nombre del topic:

``` { .txt .no-copy }
/odom [nav_msgs/msg/Odometry]
```

!!! question "Preguntas"
    1. ¿A qué package pertenece esta interfaz?
    1. ¿Qué *tipo* de interfaz es?
    1. ¿Cuál es su nombre?

    [Ve aquí para un recordatorio sobre cómo interpretar una definición de interfaz](./part1.md#msg-interface-struct).

Habiendo establecido la estructura de datos, exploremos los datos reales ahora, usando `rqt`.

#### :material-pen: Ejercicio 1: Explorando los Datos de Odometría {#ex1}

1. En una nueva instancia de terminal (**TERMINAL 2**) usa el siguiente comando para iniciar el *Monitor de Topics RQT*:

    ```bash
    ros2 run rqt_topic rqt_topic 
    ```

    El *Monitor de Topics* debería iniciarse con una lista de topics activos que coincidan con la lista de topics del comando `ros2 topic list` que ejecutaste anteriormente.

1. Marca la casilla junto a `/odom` y haz clic en la flecha junto a él para expandir el topic y revelar cuatro *campos base*.

1. Expande el campo `pose`, y luego el campo `pose` adicional dentro de él. Esto debería revelar dos campos adicionales: **`position`** y **`orientation`**. 

    Expande ambos para revelar los datos que se publican en los *tres* valores de posición (`x`, `y` y `z`) y los *cuatro* valores de orientación (`x`, `y`, `z` y `w`).

    <figure markdown>
      ![](../images/rqt/topic_monitor.png){width=600}
    </figure>

1. A continuación, inicia una nueva instancia de terminal, la llamaremos **TERMINAL 3**. Colócala junto a la ventana de `rqt`, para que puedas verlas ambas una al lado de la otra.

1. En **TERMINAL 3** inicia el node `teleop_keyboard` [como lo hiciste en la Parte 1](./part1.md#teleop): <a name="teleop"></a>

    ```bash
    ros2 run turtlebot3_teleop teleop_keyboard
    ```

1. Presiona ++a++ un par de veces para hacer que el robot rote en el lugar. Observa cómo cambian los datos de odometría en el Monitor de Topics.

    !!! question
        ¿Qué campos de `pose` están cambiando?

1. Ahora presiona la tecla ++s++ para detener el robot, luego presiona ++w++ un par de veces para hacer que el robot avance.

    !!! question
        ¿Qué campos de `pose` están cambiando *ahora*? ¿Cómo se relaciona esto con la posición del robot en el mundo simulado?

1. Ahora presiona ++d++ un par de veces y tu robot debería comenzar a moverse en círculo.

    !!! question
        ¿Qué está pasando con los datos de `pose` ahora? ¿Cómo están cambiando estos datos mientras tu robot se mueve en una trayectoria circular?
    
1. Presiona ++s++ en **TERMINAL 3** para detener el robot (pero deja corriendo el node `teleop_keyboard`). Luego, presiona ++ctrl+c++ en **TERMINAL 2** para cerrar `rqt`. 

1. Veamos los datos de Odometría de otra manera ahora. Con el robot estacionario, usa `ros2 run` (en **TERMINAL 2**) para ejecutar un node de Python del package `rigsa_examples`: 

    ```bash
    ros2 run rigsa_examples robot_pose.py
    ```
        
1. Ahora (usando el node `teleop_keyboard` en **TERMINAL 3**) conduce tu robot de nuevo, prestando atención a las salidas que imprime el node `robot_pose.py` en **TERMINAL 2** mientras lo haces.

    La salida del node `robot_pose.py` te muestra cómo la *posición* y *orientación* (es decir, *"pose"*) del robot están cambiando en tiempo real mientras mueves el robot. La columna `"initial"` nos indica la pose del robot cuando el node se inició por primera vez, y la columna `"current"` nos muestra cuál es su pose actualmente. La columna `"delta"` muestra entonces la diferencia entre ambas.
    
    !!! question
        ¿Qué parámetros de pose *no* han cambiado, y ¿es esto lo que esperarías (considerando [los ejes principales del robot, como se ilustra arriba](#principal-axes))?
    
1. Presiona ++ctrl+c++ en **TERMINAL 2** y **TERMINAL 3**, para detener los nodes `robot_pose.py` y `teleop_keyboard`. 

### La Odometría Explicada

Esperamos que estés empezando a entender qué es la Odometría ahora, pero profundicemos un poco más usando algunas herramientas clave de la línea de comandos de ROS nuevamente. En **TERMINAL 2**:

```bash
ros2 topic info /odom
```

Esto proporciona información sobre la interfaz usada por este topic:

``` { .txt .no-copy }
Type: nav_msgs/msg/Odometry
```

Podemos obtener más información sobre esta interfaz usando el comando `ros2 interface show`:

```bash
ros2 interface show nav_msgs/msg/Odometry
```

Mira a lo largo del lado izquierdo para identificar los cuatro *campos base* de la interfaz (los campos que no tienen sangría):

<a name="odom-base-fields"></a>

<center>

| # | *Nombre* del Campo | *Tipo* del Campo |
| :---: | :---: | :---: |
| 1 | `header` | `std_msgs/Header` |
| 2 | `child_frame_id` | `string` |
| **3** | **`pose`** | **`geometry_msgs/PoseWithCovariance`** |
| 4 | `twist` | `geometry_msgs/TwistWithCovariance` |

</center>

Vimos todos estos en `rqt` anteriormente. Como antes, es el elemento 3 el que más nos interesa...

#### Pose

``` { .txt .no-copy }
# Estimated pose that is typically relative to a fixed world frame.
geometry_msgs/PoseWithCovariance pose
        Pose pose
                Point position
                        float64 x
                        float64 y
                        float64 z
                Quaternion orientation
                        float64 x
                        float64 y
                        float64 z
                        float64 w
        float64[36] covariance
```

Dentro del campo base `pose` tenemos dos subcampos: `pose` y `covariance`:

<center>

| # | *Nombre* del Campo | *Tipo* del Campo |
| :---: | :---: | :---: |
| **1** | **`pose`** | **`Pose`** |
| 2 | `covariance` | `float64[36]` |

</center>

Es el subcampo `pose` el que más nos interesa aquí, que contiene dos subcampos *adicionales* llamados `position` y `orientation`: 

<center>

| # | *Nombre* del Campo | *Tipo* del Campo |
| :---: | :---: | :---: |
| 1 | `position` | `Point` |
| 2 | `orientation` | `Quaternion` |

</center>

1. `position`
    
    Nos dice dónde está ubicado nuestro robot en el espacio tridimensional. Se expresa en unidades de **metros**.

1. `orientation`

    Nos dice en qué dirección apunta nuestro robot en su entorno. Se expresa en unidades de **Cuaterniones**, que es una forma matemáticamente conveniente de almacenar datos relacionados con la orientación de un robot (sin embargo, es un poco difícil para nosotros los humanos entender y visualizar esto, así que hablaremos sobre cómo convertirlo a un formato diferente más adelante).

La Pose se define en relación a un punto de referencia arbitrario, típicamente donde estaba el robot cuando fue encendido, o el origen de un mundo simulado. En robots de accionamiento diferencial como el de simulación, se determina a partir de:

* Datos de la Unidad de Medición Inercial (IMU) en la tarjeta OpenCR
* Datos de los encoders de la rueda izquierda y derecha
* Un *modelo cinemático* del robot

Toda la información anterior puede usarse entonces para calcular (y mantener un seguimiento de) la distancia recorrida por el robot desde su punto de referencia predefinido usando un proceso llamado *"dead-reckoning."*

#### ¿Qué son los Cuaterniones?

Los Cuaterniones representan la orientación de algo en el espacio tridimensional[^quaternions], como podemos observar en la estructura de la interfaz ROS `nav_msgs/msg/Odometry`, hay **cuatro campos** asociados con esto:

[^quaternions]: [Los Cuaterniones se explican muy bien aquí](https://automaticaddison.com/how-to-convert-a-quaternion-to-a-rotation-matrix/#What_is_a_Quaternion){target="_blank"}, si deseas aprender más.

``` { .txt .no-copy }
Quaternion orientation
        float64 x
        float64 y
        float64 z
        float64 w
```

Para nosotros, es más fácil pensar en la orientación de nuestro robot en una representación de *"Ángulos de Euler"*, que nos indican el grado de rotación alrededor de los *tres ejes principales* ([como se discutió anteriormente](#principal-axes)):

* $\theta_{x}$: La posición angular alrededor del eje **X**, también conocida como **"Roll"**
* $\theta_{y}$: La posición angular alrededor del eje **Y**, también conocida como **"Pitch"**
* $\theta_{z}$: La posición angular alrededor del eje **Z**, también conocida como **"Yaw"**

Afortunadamente, la matemática involucrada en la conversión entre estos dos formatos de orientación es bastante sencilla. La posición angular alrededor del eje Z (también conocida como "Yaw"), por ejemplo, se calcula de la siguiente manera: 

$$
\theta_{z} = \operatorname{atan2}\left( 2(wz + xy), 1 - 2(y^2 + z^2) \right)
$$

Donde $\theta_{z}$ es el ángulo de yaw (en radianes), y $w$, $x$, $y$ y $z$ son los componentes de cuaternión de la orientación de un robot ($w$ siendo la parte escalar (real) y $x$, $y$ y $z$ siendo las partes vectoriales)[^auto-addison].

[^auto-addison]: Tomado de [esta publicación del blog Automatic Addison](https://automaticaddison.com/how-to-convert-a-quaternion-into-euler-angles-in-python/){target="_blank"}.

### ¿Qué Valores de Pose Aplican a Nuestro Robot?

Refiriéndonos de nuevo a los tres *ejes principales* de antes: 

<figure markdown>
  ![Ejes principales del robot diferencial](../images/waffle/principal_axes.svg){width=500}
</figure>

Como puedes ver, el robot de simulación tiene dos motores que le permiten moverse. Como resultado de esto, solo puede moverse en un plano 2D y por lo tanto su pose puede representarse completamente con solo 3 términos de odometría en total: 

* $x$ & $y$: las coordenadas 2D del robot en el plano **X**-**Y**
* $\theta_{z}$: el ángulo del robot alrededor del eje **Z** (*yaw*)

(¡desafortunadamente, no puede volar!)

### Los Datos de Odometría como Señal de Retroalimentación

Los datos de Odometría pueden ser muy útiles para la navegación de robots, permitiéndonos rastrear dónde está un robot, cómo se mueve y cómo volver a donde empezamos. Por lo tanto, necesitamos saber cómo usar estos datos eficazmente dentro de nuestros nodes de Python, y lo exploraremos ahora.

#### :material-pen: Ejercicio 2: Creando un Node de Python para Procesar Datos de Odometría {#ex2}

En la Parte 1 aprendimos cómo crear un package y construir nodes simples de Python para publicar y suscribirse a mensajes en un topic. En este ejercicio construiremos un nuevo node subscriber, muy parecido a lo que hicimos anteriormente, pero este se suscribirá al topic `/odom` del que hemos estado hablando. ¡También crearemos un nuevo package llamado `part2_navigation` para que viva este node!

1. Primero, dirígete al directorio `src` de tu workspace de ROS 2 en **TERMINAL 2**:

    ```bash
    cd ~/ros2_ws/src/
    ```

1. Clona la Plantilla de Package ROS 2:

    ```bash
    git clone https://github.com/tom-howard/ros2_pkg_template.git
    ```

1. Ejecuta el script `init_pkg.sh` dentro de este para inicializar ese package con el nombre "part2_navigation":

    ```bash
    ./ros2_pkg_template/init_pkg.sh part2_navigation
    ```

1. Luego navega hacia el nuevo package usando `cd`:

    ```bash
    cd ./part2_navigation/
    ```

1. El subscriber que construiremos aquí tendrá una estructura similar al subscriber que construimos en la Parte 1. Como punto de partida, copia el archivo `subscriber.py` de tu package `part1_pubsub` usando el comando `cp` (es decir, **c**o**p**iar):

    ```bash
    cp ../part1_pubsub/scripts/subscriber.py ./scripts/odom_subscriber.py
    ```

    ??? info "Información: Copiar archivos en un terminal"
        Cuando usamos el comando `cp` para copiar cosas, necesitamos proporcionar dos piezas clave de información (al menos): 

        ``` { .txt .no-copy }
        cp SOURCE DEST
        ```

        Es decir: copiar el archivo `SOURCE` al destino `DEST`.
        
        Recuerda que estamos ubicados en la carpeta raíz del package `part2_navigation` cuando ejecutamos esto, y las rutas de archivos que estamos usando aquí son todas *relativas* a esa ubicación.

        Por lo tanto, `..` significa "retroceder un directorio," así que al definir el archivo `SOURCE` que queremos copiar, le estamos diciendo a `cp` que *salga* del directorio `part2_navigation` (de vuelta a `~/ros2_ws/src/`), y luego que *entre* al directorio `part1_pubsub` desde allí (y continúe hacia `scripts`).

        `.` significa "este directorio actual," así que al definir dónde queremos copiar el `subscriber.py` *hacia* (`DEST`), le estamos diciendo a `cp` que empiece desde donde estamos actualmente en el sistema de archivos (es decir, `~/ros2_ws/src/part2_navigation/`) y lo copie al directorio `scripts` desde allí (mientras también lo renombra a `odom_subscriber.py`).

1. A continuación, dirígete a la siguiente página para obtener instrucciones paso a paso sobre cómo construir el subscriber de odometría:

    <center>[:material-file-code-outline: Construyendo el node `odom_subscriber.py`](./part2/odom_subscriber.md){ .md-button target="_blank"}</center> 

1. Ahora, declara el node `odom_subscriber.py` como un ejecutable en el `CMakeLists.txt`:

    ```txt title="CMakeLists.txt"
    # Install Python executables
    install(PROGRAMS
      scripts/basic_velocity_control.py
      scripts/stop_me.py
      scripts/odom_subscriber.py
      DESTINATION lib/${PROJECT_NAME}
    )
    ```

1. Regresa al terminal y usa Colcon para compilar el package (incluyendo el nuevo node `odom_subscriber.py`). Este es un **proceso de tres pasos**, que siempre debes seguir:

    1. Navega a la **raíz** del workspace de ROS 2:

        ```bash
        cd ~/ros2_ws/
        ```
    
    1. Compila tu package usando `colcon`:

        ```bash
        colcon build --packages-select part2_navigation --symlink-install
        ```

    1. Y finalmente, recarga el `.bashrc`:

        ```bash
        source ~/.bashrc
        ```

1. ¡Ahora estamos listos para ejecutar esto! Hazlo usando `ros2 run` y observa qué hace:

    ```bash
    ros2 run part2_navigation odom_subscriber.py
    ```

1. Habiendo seguido todos los pasos, la salida de tu node debería ser similar a la que se muestra a continuación:
    
    <figure markdown>
      ![](./part2/odom_subscriber.gif){width=700px}
    </figure>

1. Observa cómo cambia la salida (los datos de odometría formateados) mientras mueves el robot usando el node `teleop_keyboard` en **TERMINAL 3**.
1. Detén tu node `odom_subscriber.py` en **TERMINAL 2** y el node `teleop_keyboard` en **TERMINAL 3** ingresando ++ctrl+c++ en cada una de las terminales.

## Navegación Básica: Control de Velocidad en Lazo Abierto {#velocity}

Para cambiar la pose de nuestro robot, necesitamos aplicar velocidad para hacerlo mover. Aprendimos sobre esto en la Parte 1, pero veámoslo todo con un poco más de detalle ahora.

Sabemos que podemos usar el topic `/cmd_vel` para publicar comandos de velocidad a nuestro robot. Recordemos cómo deben estructurarse estos comandos de velocidad:

```bash
ros2 topic info /cmd_vel
```

Esto nos dice que los datos transmitidos en el topic `/cmd_vel` son del tipo de interfaz `geometry_msgs/msg/TwistStamped`.  

También aprendimos cómo obtener más información sobre esta interfaz particular (usando el comando `ros2 interface show`): 

```bash
ros2 interface show geometry_msgs/msg/TwistStamped
```

<a name="twist-stamped-struct"></a>

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

Hay dos campos base en esta estructura de datos:

<center>

| # | Nombre del Campo | Tipo de Dato |
| :---: | :---: | :---: |
| 1 | `header` | `std_msgs/Header` |
| 2 | `twist` | `Twist` |

</center>

Cada uno de estos campos base está compuesto por subcampos adicionales. Es el campo `twist` el que más nos interesa, y este comprende dos subcampos adicionales:

<center>

| # | Nombre del Campo | Tipo de Dato |
| :---: | :---: | :---: |
| 1 | `linear` | `Vector3` |
| 2 | `angular` | `Vector3` |

</center>

Cada uno de *estos* contiene 3 subcampos *adicionales*: `x`, `y` y `z`:

<center>

| # | Nombre del Campo | Tipo de Dato |
| :---: | :---: | :---: |
| 1 | `x` | `float64` |
| 2 | `y` | `float64` |
| 3 | `z` | `float64` |

</center>

### Comandos de Velocidad

Por lo tanto, hay **seis** *campos* de velocidad que podemos asignar valores cuando enviamos comandos de velocidad a un robot ROS: **dos** *tipos* de velocidad, cada uno con **tres** *componentes* de velocidad: 

<center>

| Tipo de Velocidad | Componente 1 | Componente 2 | Componente 3 |
| :--- | :---: | :---: | :---: |
| `linear` | `x` | `y` | `z` |
| `angular` | `x` | `y` | `z` |

</center>

Estos se relacionan con los **seis grados de libertad** (DOFs) de un robot, y los comandos de velocidad están formateados para dar a un Programador de ROS la capacidad de *solicitar* a un robot que se mueva en cualquiera de sus seis DOFs. 

<center>

| Componente (Eje) | Velocidad Lineal | Velocidad Angular | 
| :---: | :---: | :---: |
| **X** | "Adelante/Atrás" | "Roll" |
| **Y** | "Izquierda/Derecha" | "Pitch" |
| **Z** | "Arriba/Abajo" | "Yaw" |

</center>

### Los Grados de Libertad del Robot

Recuerda (de nuevo) los *"Ejes Principales"* del robot y el movimiento a su alrededor:

<figure markdown>
  ![Ejes principales del robot diferencial](../images/waffle/principal_axes.svg){width=500}
</figure>

Como se discutió anteriormente, el robot de simulación solo tiene dos motores. Estos dos motores pueden controlarse de forma independiente (en lo que se conoce como una configuración de *"accionamiento diferencial"*), lo que en última instancia le proporciona un total de **dos grados de libertad** en general, como se destaca a continuación.

<figure markdown>
  ![Velocidades del robot diferencial](../images/waffle/velocities.svg){width=800}
</figure>

Al emitir comandos de velocidad al robot, por lo tanto, solo dos (de los seis) campos de comando de velocidad son aplicables: velocidad **lineal** en el eje **x** (*Adelante/Atrás*) y velocidad **angular** alrededor del eje **z** (*Yaw*).

<center>

| Eje Principal | Velocidad Lineal | Velocidad Angular | 
| :---: | :---: | :---: |
| **X** | **"Adelante/Atrás"** | ~~"Roll"~~ |
| **Y** | ~~"Izquierda/Derecha"~~ | ~~"Pitch"~~ |
| **Z** | ~~"Arriba/Abajo"~~ | **"Yaw"** |

</center>

<a name="velocity_limits"></a>

!!! note "Límites Máximos de Velocidad"
    Ten en cuenta (mientras estamos en el tema de la velocidad) que el robot de simulación tiene **límites máximos de velocidad**:

    <center>

    | Componente de Velocidad | Límite Superior | Unidades |
    | :--- | :---: | :--- |
    | *Lineal (en el eje X)* | 0.26 | m/s |
    | *Angular (alrededor del eje Z)* | 1.82 | rad/s |

    </center>


#### :material-pen: Ejercicio 3: Controlando la Velocidad con el CLI de ROS 2 {#ex3}

!!! warning
    ¡Asegúrate de haber detenido el node `teleop_keyboard` antes de comenzar este ejercicio!

<a name="rostopic_pub"></a>Podemos usar el comando `ros2 topic pub` para *publicar* datos a un topic desde un terminal usando el comando de la siguiente manera:

``` { .bash .no-copy }
ros2 topic pub {topic_name} {interface_type} {data}
```

Como se discutió anteriormente, el topic `/cmd_vel` espera mensajes de interfaz que contengan datos de velocidad *lineal* y *angular*, cada uno con valores `x`, `y` y `z` asociados. Podemos componer estos mensajes en un terminal y publicarlos con el comando `ros2 topic pub`, siempre que tengamos cuidado de formatear los mensajes correctamente para cumplir con la estructura de datos `geometry_msgs/msg/TwistStamped`.

1. En **TERMINAL 3** ingresa lo siguiente, esto terminará siendo un comando bastante largo, así que analicémoslo un poco:

    1. Comienza con el subcomando deseado de `ros2 topic`:

        ``` { .txt .no-copy }
        ros2 topic pub
        ```

    1. A continuación viene el *nombre del topic* al que queremos publicar: 

        ``` { .txt .no-copy }
        ros2 topic pub /cmd_vel
        ```

    1. A continuación, definimos el tipo de interfaz que usa este topic. Comienza a escribirlo y luego presiona la tecla ++tab++ donde se indica, y debería autocompletarse:

        ``` { .txt .no-copy }
        ros2 topic pub /cmd_vel geom[TAB]
        ```

        Lo que debería autocompletar el tipo de interfaz por ti:

        ``` { .txt .no-copy }
        ros2 topic pub /cmd_vel geometry_msgs/msg/TwistStamped
        ```
        
        !!! tip 
            ¡Puedes usar ++tab++ para autocompletar muchos comandos de terminal, experimenta con ello - te ahorrará mucho tiempo! 
        
    1. Finalmente, proporciona los valores a publicar, que **deben** estar formateados según la definición de interfaz ([como establecimos anteriormente](#twist-stamped-struct)):

        ```txt
        ros2 topic pub /cmd_vel geometry_msgs/msg/TwistStamped \
        "{header: auto, \
          twist: { \
            linear: {x: 0.0, y: 0.0, z: 0.0}, \
            angular: {x: 0.0, y: 0.0, z: 0.0} \
          } \
        }"
        ```

1. Desplázate hacia atrás en el mensaje usando la tecla ++left++ en tu teclado y luego edita los valores de los distintos campos, según corresponda.

    Primero, define algunos valores que harían que el robot **rote en el lugar**.  
    
1. Ingresa ++ctrl+c++ en **TERMINAL 3** para dejar de publicar el mensaje.

    Observa que **el robot sigue moviéndose** incluso cuando detienes el proceso `ros2 topic pub`...

    Para que el robot *realmente* se detenga, necesitamos publicar un *nuevo* mensaje que contenga comandos de velocidad alternativos.

1. En **TERMINAL 3** presiona la tecla ++up++ en tu teclado para recuperar el comando anterior, ¡pero no presiones ++enter++ todavía! Ahora presiona la tecla ++left++ para retroceder en el mensaje y cambiar los valores del campo de velocidad a `0.0` para ahora hacer que el robot **se detenga**.

1. Una vez más, ingresa ++ctrl+c++ en **TERMINAL 3** para detener al publisher de publicar nuevos mensajes activamente, y luego sigue los mismos pasos que arriba para componer *otro* nuevo mensaje para ahora hacer que el robot **se mueva en círculo**.

1. Ingresa ++ctrl+c++ para volver a dejar de publicar el mensaje, publica un nuevo mensaje adicional para detener el robot, y luego compón (y publica) un mensaje que haga que el robot **avance en línea recta**.

1. Finalmente, ¡**detén** el robot de nuevo!

#### :material-pen: Ejercicio 4: Creando un Node de Python para Hacer que un Robot Se Mueva en Círculo {#ex4}

Controlar un robot desde el terminal (o usando el node `teleop_keyboard`) está bien, pero ¿qué pasa si necesitamos implementar un control más avanzado o *autonomía*?

Ahora aprenderemos cómo controlar la velocidad de nuestro robot *programáticamente*, desde un Node de Python. Comenzaremos con un ejemplo simple para lograr un perfil de velocidad simple (un círculo), pero esto nos proporcionará la base sobre la cual podemos construir algoritmos de control de velocidad más complejos (que veremos en el siguiente ejercicio).

En la Parte 1 construimos [un node publisher simple](./part1/publisher.md), y este funcionará de la misma manera, pero esta vez, sin embargo, necesitamos publicar mensajes de tipo `Twist` al topic `/cmd_vel` en su lugar... 

1. En **TERMINAL 2**, asegúrate de estar ubicado dentro de la carpeta `scripts` de tu package `part2_navigation` (puedes usar `pwd` para verificar tu directorio de trabajo actual).

    Si no estás ubicado aquí, navega a este directorio usando `cd`.

1. Crea un nuevo archivo llamado `move_circle.py`:

    ```bash
    touch move_circle.py
    ```
    ... y haz este archivo ejecutable usando el comando `chmod` ([como hicimos en la Parte 1](./part1.md#chmod)).

1. La tarea es hacer que el robot se mueva en un **círculo** con un **radio** de trayectoria de aproximadamente **0.5 metros**.

    Sigue las instrucciones en la siguiente página para construir esto:

    <center>[:material-file-code-outline: Construyendo el node `move_circle.py`](./part2/move_circle.md){ .md-button target="_blank"}</center>

1. A continuación (¡esperamos que ya estés captando la idea!), declara el node `move_circle.py` como un ejecutable en el archivo `part2_navigation/CMakeLists.txt`:

    ```txt title="CMakeLists.txt"
    # Install Python executables
    install(PROGRAMS
      scripts/basic_velocity_control.py
      scripts/stop_me.py
      scripts/odom_subscriber.py
      scripts/move_circle.py
      DESTINATION lib/${PROJECT_NAME}
    )
    ```

1. Finalmente, regresa a **TERMINAL 2** y usa Colcon para compilar el nuevo node junto con todo lo demás en el package, usando el mismo **proceso de tres pasos** que antes:

    1. Primero: 

        ```bash
        cd ~/ros2_ws/
        ```

    1. Luego:
    
        ```bash
        colcon build --packages-select part2_navigation --symlink-install
        ```
    
    1. Y finalmente, recarga de nuevo:

        ```bash
        source ~/.bashrc
        ```

1. Ejecuta este node ahora, usando `ros2 run` y observa qué sucede:

    ```bash
    ros2 run part2_navigation move_circle.py
    ```

    ¡Regresa a la simulación Gazebo y observa cómo el robot se mueve en círculo con un radio de 0.5 metros!

1. Una vez que hayas terminado, ingresa ++ctrl+c++ en **TERMINAL 2** para detener el node `move_circle.py`. 

    !!! question
        ¿Qué le pasa al robot cuando presionas ++ctrl+c++ para detener el node `move_circle.py`?

        **Respuesta**: ¡Sigue moviéndose :open_mouth:!

        Puedes ejecutar otro node desde dentro de tu package para detenerlo realmente:
        
        ```bash
        ros2 run part2_navigation stop_me.py
        ```

#### :material-pen: Ejercicio 5: Implementando un Procedimiento de Apagado {#ex5}

Claramente, nuestro trabajo en el node `move_circle.py` no está del todo terminado. Cuando terminamos nuestro node esperaríamos que el robot dejara de moverse, pero (actualmente) este no es el caso. 

También es posible que hayas notado (con todos los nodes que hemos creado hasta ahora) un rastreo de error en el terminal, cada vez que presionamos ++ctrl+c++. 

Nada de esto es muy bueno, y lo abordaremos ahora modificando el archivo `move_circle.py` para incorporar un procedimiento de apagado adecuado (y *seguro*).

1. Regresa al archivo `move_circle.py` en VS Code. 

1. Primero, necesitamos agregar una importación a nuestro Node:

    ```py
    from rclpy.signals import SignalHandlerOptions
    ```

    Pronto verás para qué sirve esto...

1. Luego pasa al método `__init__()` de tu clase `Circle()`.

    Agrega aquí una bandera booleana llamada `shutdown`:

    ```py
    self.shutdown = False
    ```

    ... para comenzar, queremos que esto esté establecido en `False`.

1. A continuación, agrega un nuevo método a tu clase `Circle()`, llamado `on_shutdown()`:

    ```py
    def on_shutdown(self):
        self.get_logger().info(
            "Stopping the robot..."
        )
        self.my_publisher.publish(TwistStamped()) # (1)!
        self.shutdown = True # (2)!
    ```

    1. Todas las velocidades dentro de la clase de mensaje `Twist(Stamped)` se establecen en cero por defecto, por lo que podemos publicar esto tal como está, para pedirle al robot que se detenga.
    2. Establece la bandera `shutdown` en verdadero para indicar que ahora se ha publicado un mensaje de PARADA.

1. Finalmente, dirígete a la función `#!py main()` del script. Aquí es donde se deben realizar la mayoría de los cambios...

    ```py
    def main(args=None):
        rclpy.init(
            args=args,
            signal_handler_options=SignalHandlerOptions.NO
        ) # (1)!
        move_circle = Circle()
        try:
            rclpy.spin(move_circle) # (2)!
        except KeyboardInterrupt: # (3)!
            print(
                f"{move_circle.get_name()} received a shutdown request (Ctrl+C)."
            )
        finally: 
            move_circle.on_shutdown() # (4)!
            while not move_circle.shutdown: # (5)!
                continue
            move_circle.destroy_node() # (6)!
            rclpy.shutdown()
    ```
    
    1. Al inicializar `rclpy`, estamos solicitando que nuestro node `move_circle.py` maneje las *"señales"* (es decir, eventos como un ++ctrl+c++), en lugar de dejar que `rclpy` las maneje por nosotros. Aquí estamos usando el objeto `SignalHandlerOptions` que importamos de `rclpy.signals` anteriormente.

    2. Ahora configuramos nuestro node para que gire dentro de un bloque Try-Except, para que podamos capturar una `#!py KeyboardInterrupt` (es decir, un ++ctrl+c++) y actuar en consecuencia cuando esto suceda.

    3. Al detectar la `#!py KeyboardInterrupt` imprimimos un mensaje en el terminal. Después de esto, el código pasará al bloque `#!py finally`...

    4. Llama al método `on_shutdown()` que definimos anteriormente. Esto asegurará que se publique un comando de PARADA al robot (a través de `/cmd_vel`).

    5. Este bucle `#!py while` continuará iterando hasta que nuestra bandera booleana `shutdown` se haya vuelto `True`, para indicar que el mensaje de PARADA ha sido publicado.

    6. El resto es igual que antes...
    
        ... destruye el node y luego apaga `rclpy`.

1. Con todo esto en su lugar, ejecuta el node nuevamente ahora (`ros2 run ...`).
    
    Ahora, cuando presionas ++ctrl+c++ deberías encontrar que el robot realmente se detiene. ¡Ah, mucho mejor!

## Navegación Basada en Odometría

A lo largo de los dos ejercicios anteriores hemos creado un node de Python para hacer que nuestro robot se mueva usando *control en lazo abierto*. Para lograr esto publicamos comandos de velocidad al topic `/cmd_vel` para hacer que el robot siguiera una trayectoria de movimiento circular.

!!! question "Preguntas"
    1. ¿Cómo sabemos si nuestro robot realmente logró la trayectoria de movimiento que solicitamos?
    1. En un entorno del *mundo real*, ¿qué factores externos podrían resultar en que el robot *no* logre su trayectoria deseada?

Anteriormente también aprendimos sobre la [Odometría del Robot](#odometry), que es usada por el robot para rastrear su **posición** y **orientación** (también conocida como **Pose**) en el entorno. Como se explicó anteriormente, esto se determina mediante un proceso llamado *"dead-reckoning,"* que es solo una aproximación, pero es bastante buena en cualquier caso, y podemos usar esto como una señal de retroalimentación para entender si nuestro robot se mueve de la manera que esperamos.

Por lo tanto, podemos construir sobre las técnicas que usamos en el ejercicio `move_circle.py`, y ahora también incorporar la capacidad de *suscribirse* a un topic y obtener *retroalimentación en tiempo real*. Para hacer esto, necesitaremos suscribirnos al topic `/odom`, y usar esto para implementar algún *control en lazo cerrado* básico.

#### :material-pen: Ejercicio 6: Haciendo que Nuestro Robot Siga una Trayectoria Cuadrada {#ex6}

1. Asegúrate de que tu node `move_circle.py` ya no esté corriendo en **TERMINAL 2**, deteniéndolo con ++ctrl+c++ si es necesario.

1. Asegúrate de que **TERMINAL 2** todavía esté ubicado dentro de tu package `part2_navigation`.
        
1. Navega al directorio `scripts` del package y usa el comando Linux `touch` para crear un nuevo archivo llamado `move_square.py`:
    
    ```bash
    touch move_square.py
    ```

1. Luego haz este archivo ejecutable usando `chmod`:

    ```bash
    chmod +x move_square.py
    ```

1. Define `move_square.py` como un ejecutable del package en tu archivo `CMakeLists.txt` (ya deberías saber cómo hacer esto, pero si no, consulta el Ejercicio 2 o el Ejercicio 4). 

1. Usa el Explorador de Archivos de VS Code para navegar a este archivo `move_square.py` y ábrelo, listo para editar.
1. Hay una plantilla a continuación para ayudarte con este ejercicio. 

    <center>[:material-file-code-outline: Accede a la plantilla de `move_square.py` aquí](./part2/move_square.md){ .md-button target="_blank"}</center>

    Copia y pega el código de la plantilla en tu nuevo archivo `move_square.py` para comenzar. 

1. Vuelve a compilar tu package `part2_navigation`, para incluir tu nuevo node `move_square.py`, siguiendo ese **proceso de compilación de tres pasos** una vez más:

    Paso 1:

    ```bash
    cd ~/ros2_ws/
    ```
    
    Paso 2:

    ```bash
    colcon build --packages-select part2_navigation --symlink-install
    ```

    Paso 3:

    ```bash
    source ~/.bashrc
    ```

1. Ejecuta el código tal como está para ver qué sucede... <a name="blank-2"></a>

    !!! warning "¡Completa el Espacio en Blanco!"
        ¿Algo no funciona como se esperaba? ¿[Olvidamos algo muy crucial](./part1/publisher.md#shebang) en **la primera línea** de la plantilla de código?!

1. Completa el espacio en blanco según sea necesario y luego adapta el código para hacer que tu robot siga una trayectoria de movimiento **cuadrada** de dimensiones de **1 x 1 metro**.

    Después de seguir una trayectoria de movimiento cuadrada algunas veces, tu robot *debería* regresar a la misma ubicación desde la que comenzó.

    !!! tip "Función avanzada"
        Adapta el node para hacer que el robot se detenga automáticamente una vez que haya realizado dos vueltas completas.

## Conclusión

En esta sesión hemos aprendido cómo controlar la velocidad y posición de un robot tanto desde la línea de comandos (usando herramientas de línea de comandos de ROS) como desde Nodes de ROS publicando mensajes correctamente formateados al topic `/cmd_vel`.  

También hemos aprendido sobre la *Odometría*, que es publicada por nuestro robot al topic `/odom`. Los datos de odometría nos indican las velocidades lineales y angulares actuales de nuestro robot en relación con sus 3 ejes principales. Además de esto, también nos indica dónde en el espacio físico está ubicado y orientado nuestro robot, lo cual se determina en base al *dead-reckoning*. 

!!! question "Preguntas" 
    1. ¿Qué información (datos de sensores/actuadores) se usa para hacer esto?
    1. ¿Ves alguna limitación potencial de esto?
    
En el ejercicio final exploramos el desarrollo del control basado en odometría para hacer que un robot siga una trayectoria de movimiento *cuadrada*. Es probable que hayas observado cierto grado de error en esto, que podría deberse al hecho de que los datos de Odometría se determinan mediante dead-reckoning y por lo tanto están sujetos a deriva y error acumulado. Considera cómo otros factores también pueden afectar la precisión del control.

!!! question "Preguntas"
    1. ¿Qué papel podría jugar la frecuencia con la que se muestrean los datos de odometría?
    1. ¿Con qué rapidez puede tu robot recibir nuevos comandos de velocidad, y con qué rapidez puede responder?

Ten en cuenta que todo esto lo hicimos en simulación también. De hecho, en un entorno del mundo real, este tipo de navegación podría ser *menos efectiva*, ya que cosas como el ruido de medición y los errores de calibración también pueden tener un impacto considerable. Tendrás la oportunidad de experimentar esto de primera mano en el laboratorio.

En última instancia, hemos visto aquí un requisito de información adicional para proporcionar más confianza sobre la ubicación de un robot en su entorno, con el fin de mejorar su capacidad de navegar eficazmente y evitar chocar con las cosas. Exploraremos esto más adelante en este curso.

### Usuarios de Escritorio Administrado WSL-ROS2: ¡Guarda tu trabajo! {#backup}

Recuerda, ¡el trabajo que has realizado en el entorno WSL-ROS2 durante esta sesión **no se conservará** para sesiones futuras o en diferentes máquinas del laboratorio automáticamente! Para guardar el trabajo que has realizado hoy debes ejecutar el siguiente script en cualquier instancia de Terminal WSL-ROS2 inactiva:

```bash
wsl_ros backup
```

Esto exportará tu directorio home a tu Unidad `U:\`, lo que te permitirá restaurarlo en otra computadora del laboratorio la próxima vez que inicies WSL-ROS2.
