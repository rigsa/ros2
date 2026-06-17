---
title: "Launch Files (Avanzado)"
---

Como sabemos por el trabajo que hemos realizado en este curso, las aplicaciones de ROS pueden ejecutarse de dos formas diferentes:  

1. Usando el comando `ros2 run`:

    ``` { .bash .no-copy }
    ros2 run {Nombre del Package} {Nombre del Node}
    ```

1. Usando el comando `ros2 launch`:

    ``` { .bash .no-copy }
    ros2 launch {Nombre del Package} {Launch file}
    ```

El comando `ros2 launch`, usado en combinación con *launch files*, ofrece algunas ventajas sobre `ros2 run`, por ejemplo:

1. **Múltiples nodes** pueden ejecutarse **simultáneamente**.
1. Desde dentro de un launch file, podemos llamar a *otros* launch files.
1. Podemos pasar **argumentos adicionales** para lanzar cosas condicionalmente, o para cambiar el comportamiento de nuestras aplicaciones de ROS *dinámicamente*.

El punto 1 anterior se explora en la [Parte 3 del Curso de ROS 2](../part3.md) (Ejercicio 1). En esta sección exploraremos los Puntos 2 y 3 con más detalle[^more].

[^more]: Para características más avanzadas de launch files, [echa un vistazo a esta guía](https://github.com/MetroRobots/rosetta_launch){target="_blank"}.

!!! note
    ¡Asegúrate de [verificar si hay actualizaciones del repositorio del curso](./course-repo.md#actualización) antes de continuar!

## Identificar Argumentos de Launch

Podemos usar la opción `-s` con `ros2 launch` para descubrir los argumentos adicionales que se pueden suministrar a cualquier launch file dado. Tomemos el launch file `waffle.launch.py` de `tuos_simulations`, por ejemplo:

```bash
ros2 launch tuos_simulations waffle.launch.py -s
```

Deberías ver una serie de argumentos aquí, comenzando con:

``` { .txt .no-copy }
$ ros2 launch tuos_simulations waffle.launch.py -s
Arguments (pass arguments as '<name>:=<value>'):
urdf_file_name : turtlebot3_waffle.urdf

    'with_gui':
        Select whether to launch Gazebo with or without Gazebo Client (i.e. the GUI).
        (default: 'true')
```

Desplázate hasta el *final* de la lista, y deberías ver lo siguiente:

``` { .txt .no-copy }
    'x_pose':
        Starting X-position of the robot
        (default: '0.0')

    'y_pose':
        Starting Y-position of the robot
        (default: '0.0')

    'yaw':
        Starting orientation of the robot (radians)
        (default: '0.0')
```

Usando estos argumentos, podemos controlar la posición y orientación del Waffle cuando aparece en el mundo simulado. Prueba esto:

```txt
ros2 launch tuos_simulations waffle.launch.py x_pose:=1 y_pose:=0.5
```

El robot debería aparecer en un mundo vacío, pero en la posición de coordenadas $x=1.0$, $y=0.5$, en lugar de $x=0$, $y=0$, como sería normalmente el caso.

## ¡Lanzar Launch Files desde Launch Files!

Como se mencionó arriba, aprendimos cómo crear un launch file básico en la [Parte 3 del Curso de ROS](../part3.md#ex1). Usando lo que aprendimos aquí, podemos desarrollar launch files para ejecutar tantos nodes como queramos en una red de ROS simultáneamente. *Otra* cosa que podemos hacer con los launch files es lanzar *otros* launch files. 

Recuerda el [Ejercicio 2 de la Parte 3](../part3.md#ex2), donde exploramos los **Parámetros de ROS 2**. Para explorar esto, creamos un node `param_circle.py` (basado en el node `move_circle.py` de la Parte 2) que haría que el robot se moviera en un círculo con un radio dictado por el parámetro de ROS `radius`.

En última instancia, para que este node haga *algo*, primero debemos tener una simulación del robot en funcionamiento, por ejemplo: 

``` { .bash .no-copy }
ros2 launch turtlebot3_gazebo empty_world.launch.py
```

De hecho, podríamos envolver la ejecución de la simulación *y* nuestro node `param_circle.py` dentro de un único launch file, para que todo pueda lanzarse junto usando un único comando `ros2 launch`...

!!! warning "Nota"
    
    Este ejercicio es solo con fines ilustrativos.

    **NO** incluyas descripciones de launch para simulaciones en ningún trabajo que entregues para las tareas del curso. 

1. En un terminal de ROS 2, regresa al directorio `launch` del package `part3_beyond_basics`. Primero, navega a la raíz del package:

    ```bash
    cd ~/ros2_ws/src/part3_beyond_basics
    ```

    ... y luego al directorio `launch` desde allí:

    ```bash
    cd launch/
    ```

1. Crea un nuevo launch file aquí, llamado `circle.launch.py`:

    ```bash
    touch circle.launch.py
    ```

1. Ábrelo en VS Code e ingresa lo siguiente:

    ```py title="circle.launch.py"
    from launch import LaunchDescription
    from launch_ros.actions import Node

    from launch.actions import IncludeLaunchDescription
    from launch.launch_description_sources import PythonLaunchDescriptionSource
    from launch.substitutions import PathJoinSubstitution
    from launch_ros.substitutions import FindPackageShare

    def generate_launch_description():
        return LaunchDescription([
            IncludeLaunchDescription( # (1)!
                PythonLaunchDescriptionSource( # (2)!
                    PathJoinSubstitution([ # (3)!
                        FindPackageShare("turtlebot3_gazebo"), # (4)!
                        "launch", 
                        "empty_world.launch.py" 
                    ])
                )
            )
        ])
    ``` 

    1. Para incluir otro launch file en una descripción de launch, usamos una instancia de la clase `IncludeLaunchDescription()` (importada de un módulo llamado `launch.actions`).
    2. Queremos lanzar la simulación "Empty World" del package `turtlebot3_gazebo`, lo cual (como sabemos) puede hacerse *desde un terminal* con el siguiente comando:

        ``` { .bash .no-copy }
        ros2 launch turtlebot3_gazebo empty_world.launch.py
        ```

        Basándonos en lo anterior, sabemos que el launch file en sí es un launch file de *Python*, debido a la extensión de archivo `.py` al final.

        Como tal, la descripción de launch que queremos incluir es una descripción de launch de *Python*, que por lo tanto debe definirse usando una instancia de `PythonLaunchDescriptionSource()` (importada de un módulo llamado `launch.launch_description_sources`)
        
    3. La clase `PathJoinSubstitution()` (de la biblioteca `launch.substitutions`) puede usarse para construir rutas de archivos a partir de una *lista* de componentes individuales (otras rutas de archivos, nombres de carpetas y nombres de launch files).
        
        Aquí la usamos para construir una ruta de archivo completa al launch file que queremos ejecutar.

        ... pero *¿cómo sabemos cuál es?* Consulta a continuación para más información...
    
    4. Necesitamos conocer la *ruta completa* al launch file que queremos ejecutar. No siempre sabemos dónde está este archivo en nuestro sistema de archivos (por ejemplo, launch files que están fuera del workspace de ROS 2, que no hemos creado nosotros mismos).
    
        Podemos usar otra clase llamada `FindPackageShare()` (de otra biblioteca llamada `launch_ros.substitutions`). Esta nos proporciona la ruta a la *raíz* del directorio de este package.

        Los packages de ROS instalados (incluidos los que creamos nosotros mismos) siempre se encuentran en — y se ejecutan desde — un directorio *"share"*, de ahí `FindPackageShare()`. Habrá múltiples directorios *share* en nuestro sistema:
            
        * `/opt/ros/jazzy/share/`
        * `~/ros2_ws/install/part3_beyond_basics/share/`
        
            ... por ejemplo.
            
    
    Actualmente, este launch file solo contiene la descripción del launch file `empty_world.launch.py` del package `turtlebot3_gazebo`. Hay algunas cosas nuevas que se han introducido aquí para lograr esto, así que haz clic en los iconos :material-plus-circle: en el código anterior para descubrir qué hacen todas estas cosas.

1. Ahora, agrega un elemento `Node()` a la descripción de launch para que el node `param_circle.py` (de tu package `part3_beyond_basics`) se lance *después* de que se haya lanzado la simulación "Empty World".

    Consulta el [Ejercicio 1 de la Parte 3](../part3.md#ex1) como recordatorio de cómo hacer esto.

1. [Ejecuta `colcon build` en tu package](../part3.md#colcon-build) para *compilar* este nuevo launch file.


1. Finalmente, cuando estés listo, ejecuta tu nuevo launch file `circle.launch.py`:

    ```bash
    ros2 launch part3_beyond_basics circle.launch.py
    ```

Si has hecho esto correctamente, al lanzar el comando anterior la simulación Gazebo Empty World debería iniciarse y, una vez cargada, el robot debería comenzar a moverse en un círculo inmediatamente.

## Pasar Argumentos de Launch

¿Cómo pasamos un argumento a un launch file (`tuos_simulations/waffle.launch.py`, por ejemplo) que está declarado dentro de *otro* launch file? 

Siguiendo el mismo enfoque anterior, una descripción de launch básica para la simulación `tuos_simulations/waffle.launch.py` se vería así:

```py title="launch_args_example.launch.py"
from launch import LaunchDescription
from launch_ros.actions import Node

from launch.actions import IncludeLaunchDescription
from launch.launch_description_sources import PythonLaunchDescriptionSource
from launch.substitutions import PathJoinSubstitution
from launch_ros.substitutions import FindPackageShare

def generate_launch_description():
    return LaunchDescription([
        IncludeLaunchDescription(
            PythonLaunchDescriptionSource(
                PathJoinSubstitution([
                    FindPackageShare("tuos_simulations"),
                    "launch", 
                    "waffle.launch.py" 
                ])
            )
        )
    ])
```

Para lanzar esto *y* también suministrar los argumentos de launch `x_pose` e `y_pose`, necesitamos agregar lo siguiente a la definición de `PythonLaunchDescriptionSource()`:

```py
IncludeLaunchDescription(
    PythonLaunchDescriptionSource(
        PathJoinSubstitution([
            FindPackageShare("tuos_simulations"), 
            "launch", 
            "waffle.launch.py"
        ])
    ),
    launch_arguments={ # (1)!
        'x_pose': '1.0',
        'y_pose': '0.5' # (2)!
    }.items()
)
```

1. Los argumentos se pasan al launch file a través de la opción `launch_arguments` de `IncludeLaunchDescription()`.
2. Los argumentos se pasan como un diccionario, que puede contener múltiples pares clave-valor separados por comas: `#!py dict = {key1:value1, key2:value2, ... }`. 
    
    En este caso, las *claves* son los nombres de los argumentos de launch que se pasarán al launch file `waffle.launch.py`, y los **valores** son los valores reales que queremos asignar a esos argumentos (y que pueden cambiarse según sea necesario).

## Argumentos de Línea de Comandos para Launch Files

Para crear argumentos para nuestros propios launch files y poder pasar estos argumentos a nuestros propios Nodes, necesitamos usar **parámetros**. Una vez más, aprendimos sobre estos en la [Parte 3 del curso](../part3.md#ex2) (en el Ejercicio 2), donde creamos el node `param_circle.py` que ya hemos discutido anteriormente.

Si tienes una simulación ejecutándose, ciérrala ahora. Para el resto de esta sección, debes lanzar un mundo vacío manualmente, desde un terminal separado, cuando lo necesites (tanto el mundo `tuos_simulations/waffle.launch.py` como `turtlebot3_gazebo/empty_world.launch.py` serían apropiados).

### Declarar Argumentos de Línea de Comandos para Launch Files

Vamos a crear ahora un launch file muy básico llamado `cli_example.launch.py` para lanzar solo este node (¡una vez más, por qué no crearlo en tu package `part3_beyond_basics` donde ya habrás acumulado una buena colección de launch files!):

```py title="cli_example.launch.py"
from launch import LaunchDescription 
from launch_ros.actions import Node 

def generate_launch_description(): 
    return LaunchDescription([ 
        Node( 
            package='part3_beyond_basics', 
            executable='param_circle.py', 
            name='my_param_circle_node' 
        )
    ])
```

Como sabemos, este node usa un parámetro de ROS 2 llamado `radius` para controlar el tamaño del círculo que seguirá el robot. Podemos declarar un valor para este en tiempo de ejecución desde dentro de este launch file y establecer su valor mediante un argumento de línea de comandos pasado al propio launch file. 

Para hacer esto, primero usamos la acción `DeclareLaunchArgument`, que debe incluirse como un elemento en el `LaunchDescription`:

```py title="cli_example.launch.py"
from launch import LaunchDescription 
from launch_ros.actions import Node 
from launch.actions import DeclareLaunchArgument # (1)!

def generate_launch_description(): 
    return LaunchDescription([ 
        DeclareLaunchArgument(
            name='circle_radius', 
            description="Sets the desired radius of the circle (in meters).",
            default_value='1.0'
        ), # (2)!
        Node( 
            package='part3_beyond_basics', 
            executable='param_circle.py', 
            name='my_param_circle_node' 
        )
    ])
```

1. Necesitamos importar `DeclareLaunchArgument` para poder usarlo en el launch file.
2. ¡No olvides la coma para separar los dos elementos de la descripción de launch: `DeclareLaunchArgument()` y `Node()`! 

Estamos definiendo **tres cosas** al declarar el argumento de launch:

1. `name`: El **nombre** del argumento.
2. `description`: Una descripción de para qué se usa este argumento.
3. `default_value`: Un valor que se asignará si no proporcionamos uno al ejecutar el launch file.

### Pasar Argumentos de Launch Files a Nodes de Python (mediante Parámetros)

Definimos un argumento de launch en el paso anterior, pero (actualmente) este argumento no se está pasando realmente a nuestro node `param_circle.py`. Para hacer esto, podemos agregar un argumento al elemento de descripción de launch `Node()`:

```py title="cli_example.launch.py"
from launch import LaunchDescription 
from launch_ros.actions import Node 
from launch.actions import DeclareLaunchArgument
from launch.substitutions import LaunchConfiguration # (1)!

def generate_launch_description(): 
    return LaunchDescription([ 
        DeclareLaunchArgument(
            name='circle_radius', 
            description="Sets the desired radius of the circle (in meters).",
            default_value='1.0'
        ),
        Node( 
            package='part3_beyond_basics', 
            executable='param_circle.py', 
            name='my_param_circle_node',
            parameters=[{'radius': LaunchConfiguration('circle_radius')}] 
        )
    ])
```

1. ¡Otra nueva importación aquí!

Recuerda que nuestro node `param_circle.py` usa un parámetro llamado `radius`, y lo estamos pasando a *este launch file* usando el valor suministrado por el argumento del *launch file* `circle_radius`. Entonces, si llamamos a este launch file *sin* suministrar el argumento `circle_radius`, se establecerá un valor predeterminado de `1.0` (en lugar del valor predeterminado de `0.5` establecido por el propio node). Prueba esto ejecutando este launch file sin pasar un valor para el argumento `circle_radius` primero:

```txt
ros2 launch part3_beyond_basics cli_example.launch.py
```

Deberías ver mensajes regulares impresos en el terminal para indicar el radio que el node está intentando alcanzar:

``` { .txt .no-copy}
...
[param_circle.py-1] [INFO] [###] [my_param_circle_node]: Moving with radius: 1.00 [m]
...
```

Ahora, haz esto de nuevo pero esta vez especificando un valor para `circle_radius`:

```txt
ros2 launch part3_beyond_basics cli_example.launch.py circle_radius:=0.3
```

Esta vez, los mensajes de estado regulares (y el movimiento del robot) deberían haber cambiado:

``` { .txt .no-copy}
...
[param_circle.py-1] [INFO] [###] [my_param_circle_node]: Moving with radius: 0.30 [m]
...
```

### Resumen

En las dos secciones anteriores hemos visto cómo podemos construir un launch file que acepta un argumento de línea de comandos, y cómo podemos pasar el *valor* de ese argumento de línea de comandos a un node de ROS.