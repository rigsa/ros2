---  
title: "Parte 4: Services"  
description: Aprende sobre una forma alternativa en que los nodos de ROS pueden comunicarse a través de una red ROS, y las situaciones en las que esto puede ser útil.  
---

## Introducción

:material-pen: **Ejercicios**: 6  
:material-timer: **Tiempo estimado de finalización**: 2 horas  
:material-gauge: **Nivel de dificultad**: Intermedio  

### Objetivos

En esta parte aprenderás sobre los *Services*: un método de comunicación alternativo que se puede usar para transmitir datos/información o invocar acciones en una red ROS. Aprenderás cómo funciona esto y por qué puede ser útil. También explorarás algunas aplicaciones prácticas de esto.

### Resultados de Aprendizaje Esperados

Al finalizar esta sesión serás capaz de:

1. Reconocer cómo los ROS Services difieren del enfoque estándar de publisher-subscriber basado en topics, e identificar casos de uso apropiados para este tipo de sistema de mensajería.
1. Identificar los services disponibles en una red ROS, y usar las herramientas de línea de comandos de ROS para interrogarlos y *llamarlos*.
1. Desarrollar Nodos Python de tipo Service Client.
1. Invocar diferentes services usando diversas interfaces de tipo service.

### Enlaces Rápidos

#### Ejercicios

* [Ejercicio 1: Usar Herramientas de Línea de Comandos para Interrogar un Service y su Interface](#ex1)
* [Ejercicio 2: Jugar el Juego de Números (desde la Línea de Comandos)](#ex2)
* [Ejercicio 3: Crear una Interface de Service](#ex3)
* [Ejercicio 4: Adaptar el Server del Juego de Números](#ex4)
* [Ejercicio 5: Crear un Python Service Client](#ex5)
* [Ejercicio 6: Desarrollar un Map Saver Service Client](#ex6)

#### Recursos Adicionales

* [El Nodo `number_game_client.py` (para el Ejercicio 5)](./part4/number_game_client.md){target="_blank"}

## Primeros Pasos

**Paso 1: Iniciar tu Entorno ROS2**

Si aún no lo has hecho, inicia tu entorno ROS ahora. Una vez hecho esto, deberías tener acceso a una instancia de terminal de Linux (también conocida como **TERMINAL 1**).

**Paso 2: Restaurar tu trabajo (Solo para Usuarios de Escritorio Administrado WSL-ROS2)**

Recuerda que cualquier trabajo que realices dentro del Entorno WSL-ROS2 no se conservará entre sesiones ni en diferentes computadoras del laboratorio, por lo que debes hacer copias de seguridad de tu trabajo en tu unidad `U:\` regularmente. Cuando se te solicite (al primer inicio de WSL-ROS2 en **TERMINAL 1**) ingresa ++y+enter++ para restaurar tus datos[^1].

``` { .txt .no-copy }
It looks like you already have a backup from a previous session:
  U:\wsl-ros\ros2-backup-XXX.tar.gz
Do you want to restore this now? [y/n]
```

[^1]: Recuerda: también puedes usar el comando `wsl_ros restore` en cualquier momento.

**Paso 3: Iniciar VS Code**  

También vale la pena iniciar VS Code ahora. 

??? warning "Usuarios de WSL..."
        
    Es importante iniciar VS Code dentro de tu entorno ROS usando la extensión "WSL". Recuerda siempre verificar esto: 
    
    <figure markdown>
      ![](../software/figures/code-wsl-ext-on.svg){width=400px}
    </figure>

**Paso 4: Asegurarse de que el Repositorio del Curso Esté Actualizado**

Una vez más, vale la pena verificar rápidamente que el Repositorio del Curso esté actualizado antes de comenzar con los ejercicios de la Parte 4. Vuelve a la [Parte 1](./part1.md#course-repo) si aún no lo has instalado (¿en serio?!) o, alternativamente, [consulta aquí cómo actualizarlo](./extras/course-repo.md#updating).

## Introducción a los Services

Hasta ahora, hemos aprendido sobre los *topics* de ROS y las interfaces de tipo *message* que usamos para transmitir datos en ellos. También hemos aprendido cómo los nodos individuales pueden acceder a datos de un robot simplemente *suscribiéndose* a topics en los que otro nodo de la red ROS está publicando mensajes. Además, sabemos que cualquier nodo puede *publicar* mensajes en cualquier topic, lo que transmite datos a través de la red ROS, poniéndolos a disposición de cualquier otro nodo de la red que desee acceder a ellos.

Otra forma de pasar datos entre Nodos ROS es usando *Services*. Estos se basan en un tipo de comunicación de *llamada y respuesta*:

* Un **Client** de Service envía una **Request** a un **Server** de Service.
* El **Server** de Service procesa esa request y envía de vuelta una **Response**.

<figure markdown>
  ![La diferencia entre la mensajería basada en topics y el protocolo de ROS Service](part4/topic_vs_service.png){width=600px}
</figure>

Esto es similar a una transacción: un nodo solicita algo, y otro nodo cumple esa solicitud y responde. Esto es útil para **tareas rápidas y de corta duración**, por ejemplo:

1. Encender o apagar un dispositivo.
1. Obtener algunos datos y guardarlos en un archivo (un mapa, por ejemplo).
1. Realizar un cálculo y devolver un resultado.
1. Emitir un sonido[^tb3_sound].

[^tb3_sound]: En los Waffles reales, existe un service llamado `/sound`. Échale un vistazo la próxima vez que estés en el laboratorio... Una vez que hayas trabajado toda la Parte 4, sabrás exactamente cómo interrogar este service y aprovechar la funcionalidad que proporciona.

Un único service puede tener muchos clients, pero solo puede haber un *único* Server proporcionando ese service en particular en un momento dado.

<figure markdown>
  ![](part4/service_clients.png)
  <figcaption>Múltiples Clients hacia un único Service Server</figcaption>
</figure>

Veamos ahora cómo funciona todo esto en la práctica, ¡jugando un juego de números! No necesitamos una simulación en ejecución para este, así que en **TERMINAL 1** usa el siguiente comando para iniciar el Service *Adivina el Número*: 

```bash
ros2 run tuos_examples number_game.py
```

Habiendo iniciado el service exitosamente, deberías ver lo siguiente:

``` { .txt .no-copy }
[INFO] [#####] [number_game_service]: The '/guess_the_number' service is active.
[INFO] [#####] [number_game_service]: A secret number has been set... Game on!
```

Ahora necesitamos interrogar esto para averiguar cómo jugar el juego...

## Interrogar un Service

#### :material-pen: Ejercicio 1: Usar Herramientas de Línea de Comandos para Interrogar un Service y su Interface {#ex1}

1.  Abre una nueva instancia de terminal (**TERMINAL 2**) y usa el comando `ros2 service` para listar todos los ROS services activos:

    ```bash
    ros2 service list
    ```

    Habrá algunos elementos en esta lista, la mayoría con el prefijo: `/number_game_service`. Este es el nombre del *nodo* que está proporcionando el service (es decir, el **Server**), y estos elementos son generados automáticamente por ROS. Lo que realmente nos interesa es el service en sí, que debería aparecer en la lista como `/guess_the_number`. 

1. A continuación, necesitamos encontrar el *tipo de interface* utilizado por este service, lo cual podemos hacer de un par de maneras:
   
    1. Usar el subcomando `type`:

        ```
        ros2 service type /guess_the_number
        ```

    1. Usar el subcomando `list` nuevamente, pero con la bandera `-t`:

        ```bash
        ros2 service list -t
        ```

        Este último proporcionará la misma lista de services que antes, pero ahora cada uno tendrá su tipo de interface listado junto a él.

1. Independientemente del método que hayas usado arriba, deberías haber descubierto que el tipo de interface utilizado por el service `/guess_the_number` es:
    
    ``` { .txt .no-copy }
    tuos_interfaces/srv/NumberGame
    ```

    Observa cómo ([de manera muy similar a las interfaces de tipo message usadas por los *topics*](./part1.md#msg-interface-struct)), hay tres campos en esta definición de tipo:
        
    1. `tuos_interfaces`: el nombre del package de ROS al que pertenece esta interface.
    1. `srv`: que esto es una interface de tipo *service*, el segundo tipo de interface que hemos visto (aprenderemos sobre el tercero y último en la Parte 5).
    1. `NumberGame`: la estructura de datos.

    Necesitamos conocer la estructura de datos para poder hacer una llamada al service, así que vamos a identificarla a continuación.

1. Podemos usar el comando `ros2 interface list` para listar *todos* los tipos de interface disponibles en nuestro sistema ROS, ¡pero esto nos dará una lista muy larga!

    1. Podemos usar la bandera `-m` para filtrar por interfaces de tipo *message*, o la bandera `-s` para filtrar por interfaces de tipo *service*. Prueba la última:

        ```bash
        ros2 interface list -s
        ```
    
        <a name="grep"></a>

    1. ¡Todavía hay bastante ahí, verdad!? Filtremos esto aún más con [Grep](https://en.wikipedia.org/wiki/Grep){target="_blank"} para identificar *solo* las interfaces que pertenecen al package `tuos_interfaces`:

        ```bash
        ros2 interface list -s | grep tuos_interfaces
        ```

        Con suerte, la interface `srv/NumberGame` ahora aparece en la lista.

    1. Usa el subcomando `show` para *mostrar* la estructura del mensaje:

        ```bash
        ros2 interface show tuos_interfaces/srv/NumberGame
        ``` 
        
    La estructura de la interface debería mostrarse de la siguiente manera:

    ``` { .txt .no-copy }
    int32 guess
    ---
    int32 guesses
    string hint
    bool success
    ```

## El Formato de las Interfaces de Service

Las interfaces de service tienen dos partes, separadas por tres guiones (`---`). Sobre el separador está la **Request** del Service, y debajo está la **Response** del Service:

``` { .txt .no-copy }
int32 guess      <-- Request
---
int32 guesses    <-- Response (1 de 3)
string hint      <-- Response (2 de 3)
bool success     <-- Response (3 de 3)
```

Para *llamar* a un service, necesitamos proporcionarle datos en el formato especificado en la sección de **Request** de la interface. El *Server* del service enviará datos de vuelta al llamante en el formato especificado en la sección de **Response** de la interface.

La interface de service `tuos_interfaces/srv/NumberGame` tiene solo **un** parámetro de request:

1. `guess`: un `int32` (entero de 32 bits)  
    ...que es lo único que necesitamos enviar al Service Server `/number_game_service` para llamarlo.

Luego hay **tres** parámetros de response:

1. Un *entero de 32 bits* llamado `guesses`
1. Una *cadena de texto* llamada `hint`  
1. Una bandera *booleana* llamada `success`

    ...todos los cuales serán devueltos por el server una vez que haya procesado nuestra request.

#### :material-pen: Ejercicio 2: Jugar el Juego de Números (desde la Línea de Comandos) {#ex2}

Ahora estamos listos para hacer una llamada al service, y podemos hacerlo usando el comando `ros2 service` nuevamente (desde **TERMINAL 2**):

1. Para empezar, enviemos una suposición inicial de `0` y veamos qué sucede:

    ```bash
    ros2 service call /guess_the_number tuos_interfaces/srv/NumberGame "{guess: 0}"
    ```

    La request nos será devuelta como eco, seguida de una response, que probablemente se verá algo así, y que nos muestra el valor de los tres parámetros de response que identificamos arriba:

    ``` { .txt .no-copy }
    response:
    tuos_interfaces.srv.NumberGame_Response(guesses=1, hint='Higher', success=False)
    ```

    1. `guesses`: nos dice cuántas veces hemos intentado adivinar el número en total (solo una vez hasta ahora)
    1. `hint`: nos dice si deberíamos ir "más alto" o "más bajo" en nuestra próxima suposición para acercarnos al *número secreto*
    1. `success`: nos dice si adivinamos el número correcto o no (¡poco probable en el primer intento!)

1. Realiza otra llamada al service, esta vez cambiando el valor de tu `guess`, por ejemplo:
    
    ```bash
    ros2 service call /guess_the_number tuos_interfaces/srv/NumberGame "{guess: 10}"
    ```

1. Intenta hacer una suposición de 500 ahora.

    El service debería responder con el hint `'Error'` ahora. Vuelve a mirar en **TERMINAL 1** (donde el Server está corriendo) para obtener más información sobre esto.

1. Continúa hasta que adivines el número mágico, ¿cuántos intentos te toma?! 

1. Detén el server, ingresando ++ctrl+c++ en **TERMINAL 1**.

## Crear Nuestros Propios Services

A lo largo de los próximos tres ejercicios, aprenderemos cómo crear una interface de service propia, y construir un Server y un Client (en Python) que la usen.

Primero, sin embargo, necesitamos crear un nuevo package, así que sigue el mismo procedimiento que has seguido en las partes anteriores de este curso para crear otro nuevo package llamado `part4_services`.

En **TERMINAL 1**:

1. Dirígete a la carpeta `src` del workspace de ROS 2:

    ```bash
    cd ~/ros2_ws/src/
    ```
       
1. Clona la plantilla del package:

    ```bash
    git clone https://github.com/tom-howard/ros2_pkg_template.git
    ```
    
1. Ejecuta el script `init_pkg.sh` y especifica el nombre de tu package:

    ```bash
    ./ros2_pkg_template/init_pkg.sh part4_services
    ```

#### :material-pen: Ejercicio 3: Crear una Interface de Service {#ex3}

Creemos ahora una interface de service que tenga una estructura *similar* a la usada por el service `/guess_the_number`, pero esta vez con *dos* parámetros de request, en lugar de solo uno...

1. En **TERMINAL 1**, navega hasta la raíz del directorio de tu package `part4_services`:

    ```bash
    cd ~/ros2_ws/src/part4_services/
    ```

1. Crea un nuevo directorio llamado `srv`:

    ```bash
    mkdir srv
    ```

1. Crea un nuevo archivo en este directorio llamado `MyNumberGame.srv`:

    ```bash
    touch srv/MyNumberGame.srv
    ```

    Aquí es donde definiremos la estructura de nuestra propia interface de service `MyNumberGame`.

1. Abre este archivo en VS Code, ingresa el siguiente contenido y guarda el archivo:

    ```txt title="MyNumberGame.srv"
    int32 guess
    bool cheat
    ---
    int32 num_guesses
    string hint
    bool correct
    ```

    La **Request** tendrá por tanto dos campos ahora:

    <center>

    | # | Nombre del Campo | Tipo de Dato |
    | :---: | :---: | :---: |
    | 1 | `guess` | `int32` |
    | 2 | `cheat` | `bool` |

    </center>

1. El resto del proceso es ahora muy similar a crear una interface de tipo *message*, [como hicimos en la Parte 1](./part1.md#ex7). 
    
    Primero, necesitamos declarar la interface en nuestro archivo `CMakeLists.txt`, agregando lo siguiente encima de la línea `ament_package()`:

    ```txt title="part4_services/CMakeLists.txt"
    find_package(rosidl_default_generators REQUIRED)
    rosidl_generate_interfaces(${PROJECT_NAME}
      "srv/MyNumberGame.srv" 
    )
    ```

1. A continuación, necesitamos modificar el archivo `package.xml`. Agrega las siguientes líneas a este, justo encima de la línea `#!xml <export>`:

    ```xml title="package.xml"
    <buildtool_depend>rosidl_default_generators</buildtool_depend>
    <exec_depend>rosidl_default_runtime</exec_depend>
    <member_of_group>rosidl_interface_packages</member_of_group>
    ```

1. Y finalmente, usamos Colcon para generar el código fuente necesario para la interface de service:

    1. Navega hasta la raíz del Workspace de ROS2:
        
        ```bash
        cd ~/ros2_ws/
        ```
    
    1. Ejecuta `colcon build`:

        ```bash
        colcon build --packages-select part4_services --symlink-install 
        ```
    
    1. Y vuelve a cargar el `.bashrc`:

        ```bash
        source ~/.bashrc
        ```

1. Verifiquemos que esto funcionó, usando el CLI de `ros2` (de la misma manera que hicimos antes cuando interrogamos `tuos_interfaces/srv/NumberGame`):

    1. Primero, *lista* todas las interfaces de service de ROS disponibles en el sistema (¡recuerda usar `-s` para filtrar por tipos de interfaces de *service*!):

        ```bash
        ros2 interface list -s
        ```

        Desplázate por esta lista y mira si puedes encontrar `part4_services/srv/MyNumberGame` (o, [usa `grep` nuevamente](#grep)).

    1. Si está ahí, usa el subcomando `show` para *mostrar* la estructura de datos:

        ```bash
        ros2 interface show part4_services/srv/MyNumberGame
        ```

    ¿Coincide con la definición en nuestro archivo `MyNumberGame.srv`?

#### :material-pen: Ejercicio 4: Adaptar el Server del Juego de Números {#ex4}

Vamos a tomar una copia del nodo server `tuos_examples/number_game.py` ahora, y adaptarlo para usar la interface de service que creamos arriba.

1. Todavía en **TERMINAL 1**, navega hasta el directorio `part4_services/scripts`:

    ```bash
    cd ~/ros2_ws/src/part4_services/scripts/
    ```

1. Copia el script `number_game.py` del repositorio del curso aquí, renombrándolo como `my_number_game.py` al mismo tiempo:

    ```bash
    cp ../../tuos_ros/tuos_examples/scripts/number_game.py ./my_number_game.py
    ```

    Este archivo ya debería tener permisos de *ejecución*, pero [siempre vale la pena verificarlo](./part1.md#chmod)...

1. Declara esto como un ejecutable del package volviendo al archivo `CMakeLists.txt` y agregando `my_number_game.py` a tu lista de ejecutables Python:

    ```txt title="CMakeLists.txt"
    # Install Python executables
    install(PROGRAMS
      scripts/basic_velocity_control.py
      scripts/stop_me.py
      scripts/my_number_game.py
      DESTINATION lib/${PROJECT_NAME}
    )
    ```

1. Compila y vuelve a cargar ahora: <a name="colcon-build-steps"></a>

    ```bash
    cd ~/ros2_ws/
    ```
    ```bash
    colcon build --packages-select part4_services --symlink-install
    ```
    ```bash
    source ~/.bashrc 
    ```

1. Ahora, veamos el código y qué necesita ser adaptado:

    1. Abre el nodo `my_number_game.py` en VS Code y revísalo.

    1. Tal como está, el nodo importa la interface de service `NumberGame` de `tuos_interfaces`, así que necesitarás cambiar esto para usar la interface de tu propio package ahora:

        ```py
        from part4_services.srv import MyNumberGame
        ```

        También necesitarás cambiar la definición de `srv_type`, cuando el service se crea en `#!py __init__()`:

        ```py
        self.srv = self.create_service(
            srv_type=MyNumberGame,
            srv_name='guess_the_number',
            callback=self.srv_callback
        )
        ```
    
    1. Todo lo que este service *hace* (cuando se le envía una **Request**) está contenido dentro del método `srv_callback()`. 

        Aquí, los parámetros de `request` son procesados, los parámetros de `response` son definidos y la `response` general es devuelta una vez que las tareas del callback han sido completadas.
    
    1. Es posible que hayas notado que cuando creamos nuestra interface `MyNumberGame` en el ejercicio anterior, los parámetros de **Response** eran *casi* los mismos que los de los Ejercicios 1 y 2, *excepto* que algunos de sus nombres habían cambiado ligeramente.

        Trabaja a través del método `srv_callback()` y asegúrate de que todos los atributos de `response` sean renombrados para coincidir con los nuevos nombres que les hemos dado en nuestra interface `part4_services/srv/MyNumberGame`. 

    1. Recuerda que nuestra interface `MyNumberGame` también tiene un parámetro de **Request** adicional: 

        ``` { .txt .no-copy } 
        bool cheat
        ```

        ... es decir, una bandera *booleana* con el nombre de atributo `cheat`.

        Adapta el método `srv_callback()` aún más ahora para leer este valor también. 
            
        * Si (cuando se realiza una **request** al server) el valor de `cheat` es `True`, el hint que devuelve el server debería contener ¡el número secreto real! Por ejemplo:

            ``` { .txt .no-copy } 
            hint='The answer is 67!'
            ```

        * En tales situaciones, el valor de `response.num_guesses` aún debería incrementarse en uno, y la bandera `correct` aún debería devolver `False`.
    
1. Una vez que hayas adaptado el nodo, pruébalo ejecutándolo:

    ***
    **TERMINAL 1:**
    ```bash
    ros2 run part4_services my_number_game.py
    ```
    ***

    Luego deberías poder hacer llamadas a este desde **TERMINAL 2** usando el subcomando `ros2 service call`, como hicimos en el [Ejercicio 2](#ex2).
    
    !!! hint
        Ahora hay **dos** parámetros de request, así que al enviar una request desde la línea de comandos **ambos** deben ser suministrados. Haz esto incluyéndolos a ambos dentro de las llaves (`{}`) separados por una coma, por ejemplo:

        ```bash
        ros2 service call /guess_the_number part4_services/srv/MyNumberGame "{guess: X, cheat: Y}" 
        ```

#### :material-pen: Ejercicio 5: Crear un Python Service Client {#ex5}

Hasta ahora hemos estado haciendo llamadas a services desde la línea de comandos, pero también podemos llamar services desde dentro de Nodos Python. Cuando un nodo *llama* (es decir, *solicita*) un service, se convierte en un *"Client"* de Service.

1. Asegúrate de que tu nodo `my_number_game.py` siga activo en **TERMINAL 1** para este ejercicio.

1. En **TERMINAL 2**, crea un nuevo archivo en el directorio `part4_services/scripts` llamado `number_game_client.py` (usando el comando `touch`).

1. [Hazlo ejecutable (con `chmod`)](./part1.md#chmod).

1. Agrégalo a la lista de *ejecutables Python* de tu package en el archivo `CMakeLists.txt`:

    ```txt title="CMakeLists.txt"
    # Install Python executables
    install(PROGRAMS
      scripts/basic_velocity_control.py
      scripts/stop_me.py
      scripts/my_number_game.py
      scripts/number_game_client.py
      DESTINATION lib/${PROJECT_NAME}
    )
    ```

1. Vuelve a compilar tu package (como antes), recordando que hay [tres pasos para esto](#colcon-build-steps):

    1. Navega hasta la **raíz** del workspace de ROS2,
    1. Ejecuta `colcon build` (con los argumentos adicionales necesarios), 
    1. Vuelve a cargar tu `~/.bashrc`.

1. Ahora, abre el archivo `number_game_client.py` en VS Code, y luego echa un vistazo a lo siguiente:

    <center>[:material-file-code-outline: El Nodo `number_game_client.py`](./part4/number_game_client.md){ .md-button target="_blank"}</center>

    Revisa el código anterior cuidadosamente (**incluyendo todas las anotaciones**), antes de tomar una copia y pegarlo en tu propio archivo `number_game_client.py`.

1. Ahora deberías poder ejecutar el código con `ros2 run`. Para empezar, usa una llamada estándar de `ros2 run` de la siguiente manera:

    ```bash
    ros2 run part4_services number_game_client.py
    ```
    
    Luego deberías obtener una salida como esta:

    ``` { .txt .no-copy }
    [INFO] [#####] [number_game_client]: Sending the request:
     - guess: 0
     - cheat: False
       Awaiting response...
    [INFO] [#####] [number_game_client]: The server responded with:
     - Incorrect guess :(
     - Number of attempts so far: 1
     - A hint: 'Higher'.
    ```

    ¿Notas cómo los parámetros de request `guess` y `cheat` han tomado los valores predeterminados `0` y `False` respectivamente?

1. La razón principal de usar parámetros en nuestro nodo `number_game_client` es para poder cambiar el valor de la suposición desde la línea de comandos. Podemos hacer esto agregando algunos argumentos adicionales a la llamada de `ros2 run`:

    ``` { .bash .no-copy }
    ros2 run part4_services number_game_client.py --ros-args -p guess:=X
    ```
    
    ... ¡reemplaza `X` con un número real!

1. Intenta hacer trampa también ahora:

    ```bash
    ros2 run part4_services number_game_client.py --ros-args -p cheat:=True
    ```
    
1. También podemos establecer los dos parámetros simultáneamente usando múltiples banderas `-p`:

    ```txt
    ros2 run part4_services number_game_client.py \
        --ros-args -p guess:=99 -p cheat:=True
    ```

    !!! note
        El `\` de arriba nos permite dividir el comando en dos líneas separadas, ¡útil para cuando estas cosas empiezan a ser un poco largas!

## El Map Saver Service

Claramente, los ejemplos con los que hemos estado trabajando hasta ahora han sido bastante triviales: ¡es poco probable que alguna vez necesites programar un robot para jugar el juego de números! Sin embargo, el objetivo ha sido ilustrar cómo funcionan los ROS Services y cómo desarrollar los propios. 

Sin embargo, una aplicación que *puede* resultarte útil es el *guardado de mapas*. En la Parte 3 aprendimos sobre SLAM, donde condujimos un robot por un entorno mientras los algoritmos SLAM trabajaban en segundo plano para generar un mapa del mundo usando datos del sensor LiDAR del robot y su sistema de odometría:

<figure markdown>
  ![](./part3/slam_steps.png){width=500px}
</figure>

Habiendo mapeado el entorno, llamamos al nodo `map_saver_cli` del package `nav2_map_server`, para guardar una copia de ese mapa en un archivo:

``` { .bash .no-copy }
ros2 run nav2_map_server map_saver_cli -f MAP_NAME
```

... ¿no sería conveniente tener una manera de poder hacer esto *programáticamente* (es decir, desde dentro de un nodo Python, por ejemplo) en lugar de tener que ejecutar el comando anterior manualmente? Bueno, hay una manera, ¿y adivina qué? ... ¡*Involucra Services*!

#### :material-pen: Ejercicio 6: Desarrollar un Map Saver Service Client {#ex6}

1. Asegúrate de que todo en **TERMINALES 1** y **2** de los ejercicios anteriores esté cerrado ahora.

1. En **TERMINAL 1**, volvamos a iniciar el *Nav World*, como lo hicimos en la Parte 3:

    ```bash
    ros2 launch tuos_simulations nav_world.launch.py
    ```
    
    <figure markdown>
      ![](./part3/nav_world.png){width=500px}
    </figure>

1. En **TERMINAL 2**, también volvamos a iniciar *Cartographer* (los algoritmos SLAM):

    ```bash
    ros2 launch tuos_tb3_tools slam.launch.py environment:=sim
    ```

    <figure markdown>
      ![](./part3/cartographer_rviz1.png){width=500px}
    </figure>

1. Abre *otra* instancia de terminal ahora (**TERMINAL 3**), y úsala para iniciar el *Map Saver Service* (¿no sería conveniente poder iniciar todos estos launch files a la vez?[^launch-adv]):

    ```bash
    ros2 launch nav2_map_server map_saver_server.launch.py
    ```

    Esto agregará una serie de services `/map_saver` a nuestra red ROS.

    [^launch-adv]: ¡Puedes! Podemos usar launch files para iniciar *otros* launch files, [consulta aquí para más información](./extras/launch-files.md).

1. En *otra* nueva instancia de terminal (**TERMINAL 4**), usa un subcomando de `ros2 service` para identificar todos los services `/map_saver` (como lo hicimos en el [Ejercicio 1](#ex1)).

    !!! question
        ¿Ves un elemento en esta lista que podría estar relacionado con guardar un mapa? (¡Tiene el prefijo `/map_saver`![^save-map])

    [^save-map]: Debería haber uno en la lista llamado `/map_saver/save_map`

1. Usa otro subcomando de `ros2 service` para determinar el tipo de interface utilizada por este service (nuevamente, como lo hicimos en el Ejercicio 1).

1. A continuación, usa un comando `ros2 interface` para descubrir la estructura de esta interface de service.

    !!! question "Preguntas"
        1. ¿Cuántos parámetros de **Request** tiene esta interface?
        1. ¿Cuántos parámetros de **Response** hay también?[^save-map-interface]
        1. ¿Cuáles son sus tipos de datos?
    
    [^save-map-interface]: La Interface de Service `nav2_msgs/srv/SaveMap` tiene **6** Requests (`map_topic`, `map_url`, `image_format`, `map_mode`, `free_thresh`, `occupied_thresh`) y **1** Response (`result`).

1. **Desarrolla un Python Service Client para hacer llamadas a este service**:

    1. Crea un nuevo Nodo en tu package `part4_services` llamado `map_saver_client.py` para esto. 
        
        Cosas a recordar al hacer esto:
        
        * [ ] Créalo en tu directorio `part4_services/scripts`.
        * [ ] Asegúrate de que tenga permisos de *ejecución*.
        * [ ] Declárao como un ejecutable del package en tu `CMakeLists.txt`.
        * [ ] Vuelve a compilar tu package con `colcon`, asegurándote de seguir [el proceso completo de **tres pasos**](#colcon-build-steps) 
    
    1. Usa [el Nodo `number_game_client.py` del Ejercicio 5](./part4/number_game_client.md) como punto de partida al construir tu nuevo nodo `map_saver_client.py`... todos los mismos principios aplicarán aquí, solo los estás aplicando a un service diferente (y por lo tanto necesitas tener en cuenta una interface de service diferente).

    1. *Declara un parámetro para tu nodo* para permitirte especificar un nombre de archivo para tu mapa cuando se llame al nodo `map_saver_client.py`, por ejemplo:
        
        ```txt
        ros2 run part4_services map_saver_client.py \ 
            --ros-args -p map_file:=my_amazing_map
        ```
        
        Sigue el mismo enfoque que en el Ejercicio 5 para esto, y asegúrate de especificar un valor predeterminado, para situaciones en las que el valor del parámetro no se defina explícitamente cuando se llame al nodo.
    
    1. Al construir requests de service, considera los siguientes consejos:
        
        1. Los datos del mapa SLAM (generados por Cartographer) se publican en un topic llamado `/map`. 
        1. Al proporcionar un nombre para el archivo del mapa:
            * No necesitas incluir una extensión de archivo
            * Los nombres de archivo se interpretan en relación con tu directorio home, así que:
                
                 `my_amazing_map` resultaría en un archivo de mapa en `~/my_amazing_map.yaml`
                 
                 `my/amazing/map` resultaría en un archivo de mapa en `~/my/amazing/map.yaml` (¡asumiendo que la estructura de directorios ya existe!)

        1. Para más orientación [consulta aquí para un ejemplo de uso](https://github.com/ros-navigation/navigation2/blob/main/nav2_map_server/README.md#services){target="_blank"}.
        1. El server aplicará [sus propios valores predeterminados a ciertos atributos de la request](https://docs.nav2.org/configuration/packages/map_server/configuring-map-saver.html){target="_blank"}, si no son definidos explícitamente por un client.
    
### Resumen del Map Saver Service

[De regreso en la Parte 3](./part3.md#map-saver-cli) guardamos nuestro mapa SLAM una vez mediante una llamada de línea de comandos después de haber *explorado y mapeado completamente el entorno*:

``` { .bash .no-copy }
ros2 run nav2_map_server map_saver_cli -f MAP_NAME
```

... lo que resultó en algo como:

<figure markdown>
  ![](part3/slam_map.png){width=300px}
  <figcaption>El archivo <code>MAP_NAME.pgm</code></figcaption>
</figure>


Sin embargo, en tareas del mundo real (¡es decir, tareas que podrías necesitar completar en el laboratorio!), tu robot podría estar explorando un entorno *de forma autónoma*, y no necesariamente sabes cuándo se ha explorado el entorno completo, ¡ni siempre estarás ahí para ejecutar el nodo `map_saver_cli` manualmente! Por lo tanto, es posible que desees programar tu robot con la capacidad de guardar un mapa *de forma incremental* y *periódica* a medida que se explora más y más del entorno.

¡El proceso que exploramos en el ejercicio anterior te permite hacer exactamente eso! En el ejemplo, nuestro nodo client fue programado para hacer solo una request al server y luego detenerse. Sin embargo, *podría* ser programado para hacer requests de service regulares (digamos, una vez cada 5 o 10 segundos) para actualizar continuamente su mapa a medida que el robot explora más y más.

Piensa en cómo podrías adaptar el nodo `map_saver_client.py` para lograr esto, apoyándote en otros ejercicios que has trabajado en partes anteriores de este curso.  

## Conclusión

En la Parte 4 hemos aprendido sobre los ROS Services y por qué pueden ser útiles para aplicaciones robóticas:

* Los Services difieren de los métodos de comunicación estándar basados en topics en ROS en que son un tipo de comunicación de *llamada y respuesta*, que tiene lugar entre un nodo y otro.  
* Típicamente, un *Caller* de service hará una **request** a un service, y luego esperará una **response** (aunque es posible hacer otras cosas mientras tanto).
* En general, sin embargo, los Services son útiles para controlar tareas *rápidas*, de *corta duración* o *cálculos*.

### Usuarios de Escritorio Administrado WSL-ROS2: ¡Guarda tu trabajo! {#backup}

Recuerda guardar el trabajo que has realizado en WSL-ROS2 durante esta sesión para poder restaurarlo en una máquina diferente en una fecha posterior. Ejecuta el siguiente script en cualquier Instancia de Terminal WSL-ROS2 inactiva ahora:

```bash
wsl_ros backup
```

Luego podrás restaurarlo a un entorno WSL-ROS2 nuevo la próxima vez que lo inicies (`wsl_ros restore`).
