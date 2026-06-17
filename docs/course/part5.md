---  
title: "Parte 5: Actions"  
description: Aprende sobre otro método de comunicación clave de ROS que es similar a un ROS Service, pero con algunas ventajas clave y casos de uso alternativos.
---

## Introducción

:material-pen: **Ejercicios**: 6 (5 *básicos*, 1 *avanzado*)  
:material-timer: **Tiempo Estimado de Finalización**: 3 horas (solo ejercicios básicos)  
:material-gauge-full: **Nivel de Dificultad**: Avanzado 

### Objetivos

En esta parte del curso aprenderemos sobre un tercer método de comunicación disponible en ROS: los *Actions*. Los Actions son esencialmente una versión avanzada de los Services, y veremos exactamente en qué difieren estos dos y por qué podrías elegir emplear un action en lugar de un service para ciertas tareas.

### Resultados de Aprendizaje Esperados

Al finalizar esta sesión podrás:

1. Reconocer cómo los ROS Actions difieren de los ROS Services y explicar dónde este método podría ser útil en aplicaciones robóticas.
1. Explicar la estructura de las interfaces de Action e identificar la información relevante dentro de ellas, permitiéndote construir Action Servers y Clients.
1. Implementar nodes Python Action *Client* que puedan manejar *feedback* y *results* y también puedan *cancelar* un action a mitad de camino.
1. Desarrollar nodes Action Server y Client que podrían usarse como base para una estrategia de exploración robótica.

### Enlaces Rápidos

#### Ejercicios

* [Ejercicio 1: Lanzar un Action Server y llamarlo desde la línea de comandos](#ex1)
* [Ejercicio 2: Construir un Node Python Action Client](#ex2)
* [Ejercicio 3: Crear una Interface de Action](#ex3)
* [Ejercicio 4: Construir el Action Server "ExploreForward"](#ex4)
* [Ejercicio 5: Construir un Client Básico "ExploreForward"](#ex5)
* [Ejercicio 6 (Avanzado): Implementar una Estrategia de Exploración](#ex6)

#### Recursos Adicionales

* [Un Action Client Mínimo (para el Ejercicio 2)](./part5/minimal_action_client.md){target="_blank"}
* [La Plantilla del Explore Server (para el Ejercicio 4)](./part5/explore_server.md){target="_blank"}

## Primeros Pasos

**Paso 1: Lanza tu Entorno de ROS**

Lanza tu entorno de ROS ahora para que tengas acceso a una instancia de terminal Linux (también conocida como **TERMINAL 1**).

**Paso 2: Restaura tu trabajo (Solo para Usuarios de Computadoras del Laboratorio con WSL-ROS2)**

Recuerda que cualquier trabajo que realices dentro del Entorno WSL-ROS2 no se conservará entre sesiones ni en diferentes computadoras del laboratorio, por lo que debes hacer una copia de seguridad de tu trabajo en tu unidad `U:\` regularmente. Cuando se te solicite (al primer lanzamiento de WSL-ROS2 en **TERMINAL 1**) ingresa `Y` para restaurarlo[^1].

[^1]: Recuerda: también puedes usar el comando `wsl_ros restore` en cualquier momento.

**Paso 3: Lanza VS Code**  

*Usuarios de WSL* [recuerda verificar esto](../software/using-wsl-ros/vscode.md#verify).

**Paso 4: Asegúrate de que el Repositorio del Curso esté Actualizado**

Verifica que el Repositorio del Curso esté actualizado antes de comenzar con estos ejercicios. [Consulta aquí cómo instalar y/o actualizar](./extras/course-repo.md).

## Llamar a un Action Server

Antes de hablar sobre qué son realmente los actions, vamos a ir directo al grano y ver uno en *action* (perdona el juego de palabras).

<!-- As you may remember from Part 3, you actually used a ROS Action to make your robot navigate autonomously in [Exercise 3](./part3.md#ex3), by calling an action server from the command-line. We will do a similar thing now, in a different context, and this time we'll also look at what's going on in a bit more detail. -->

#### :material-pen: Ejercicio 1: Lanzar un Action Server y llamarlo desde la línea de comandos {#ex1}

Vamos a jugar un pequeño juego aquí. Vamos a lanzar nuestro TurtleBot3 Waffle en un *entorno misterioso* ahora, y lo haremos lanzando Gazebo en modo *headless*, es decir, Gazebo se ejecutará en segundo plano, pero no habrá Interfaz Gráfica de Usuario (GUI) para mostrarnos cómo es realmente el entorno. Luego, usaremos un *action server* para hacer que nuestro robot escanee el entorno y tome fotos por nosotros, ¡para revelar su entorno!

1. Para lanzar el TurtleBot3 Waffle en este *entorno misterioso*, usa el siguiente comando `ros2 launch` en **TERMINAL 1**:

    ```bash
    ros2 launch tuos_simulations mystery_world.launch.py
    ```
    
    ... ¡aparentemente no ocurrirá *nada* (por ahora)!

1. A continuación, abre una nueva terminal (**TERMINAL 2**) y echa un vistazo a todos los topics que están actualmente activos en la red de ROS (¡ya deberías saber exactamente cómo hacer esto!).

    La salida de esto debería confirmar que ROS y nuestro robot están efectivamente activos...

    ??? question "¿Cómo?"
        Cuando el robot está activo, la salida del comando `ros2 topic list` debería proporcionar una larga lista de topics, varios de los cuales hemos estado trabajando a lo largo de este curso, como `cmd_vel`, `odom`, `scan`, y así sucesivamente. Si la simulación del Waffle *no* está activa, se nos presentaría una lista mucho más pequeña, que contiene solo los topics básicos de ROS:

        ***
        **TERMINAL 2:**
        ``` { .bash .no-copy }
        $ ros2 topic list
        /parameter_events
        /rosout
        ```
        ***

1. A continuación (aún en **TERMINAL 2**), ejecuta el siguiente comando para lanzar un *Action Server* en la red:

    ```bash
    ros2 run tuos_examples camera_sweep_action_server.py
    ```
    
1. Ahora, abre *otra* nueva instancia de terminal (**TERMINAL 3**), de manera que puedas ver esta y la **TERMINAL 2** lado a lado. Ingresa el siguiente comando para *listar* todos los actions que están activos en la red de ROS:

    ```bash
    ros2 action list
    ```

    Debería haber un elemento aquí llamado `/camera_sweep`. Usa el comando `info` para obtener más información sobre este:

    ```bash
    ros2 action info /camera_sweep
    ```

    Esto nos indica el *nombre* del action: `Action: /camera_sweep`, así como el número de nodes client y server que tiene este action. Actualmente, el action debería tener 0 *clients* y 1 *server*, y el node que actúa como servidor aquí debería aparecer como `/camera_sweep_action_server_node` (el node que acabamos de lanzar con el comando `ros2 run` en **TERMINAL 2**).
    
    Finalmente, llama al comando `ros2 action info` nuevamente, pero esta vez proporcionando un argumento adicional:
    
    ```
    ros2 action info -t /camera_sweep
    ```

    ```
    Action: /camera_sweep
    Action clients: 0
    Action servers: 1
        /camera_sweep_action_server [tuos_interfaces/action/CameraSweep]
    ```

    El argumento `-t` muestra adicionalmente el *tipo* de action frente al node servidor, indicándonos el tipo de *interface* utilizada por el servidor.

1. Ahora busquemos más información sobre la interface en sí. Al igual que con cualquier interface (mensaje, service o action) podemos usar el comando `ros2 interface` para esto. En **TERMINAL 3** ingresa lo siguiente:

    ```bash
    ros2 interface show tuos_interfaces/action/CameraSweep
    ```
    
    Lo cual debería presentarnos lo siguiente:

    ```txt
    --8<-- "https://raw.githubusercontent.com/tom-howard/tuos_ros/refs/heads/jazzy/tuos_interfaces/action/CameraSweep.action"
    ```
    
    Hay tres partes en una interface de action, y hablaremos sobre estas con más detalle en breve, pero por ahora, todo lo que necesitamos saber es que para *llamar* a un action, necesitamos enviar al action server un **Goal**.

    ??? info "Comparación con ROS Services"
        Esto es un poco como enviar una **Request** a un ROS Service Server, como hicimos en la sesión anterior.
    
1. Podemos emitir un goal a un action server desde la línea de comandos usando el comando `ros2 action` nuevamente. Vamos a intentarlo en **TERMINAL 3**.
    
    Primero, identifiquemos el sub-comando correcto de `ros2 action`:

    ```bash
    ros2 action --help
    ```

    ``` { .txt .no-copy}
    Commands:
      info       Print information about an action
      list       Output a list of action names
      send_goal  Send an action goal
    ```

    Como se muestra arriba, hay tres sub-comandos para elegir, ¡y ya hemos usado los dos primeros! Claramente, el comando `send_goal` es el que necesitamos ahora.

    Obtengamos ayuda sobre este:

    ```bash
    ros2 action send_goal --help
    ```
    
    A partir de esto, aprendemos que hay tres *argumentos posicionales*, que deben suministrarse en el orden correcto:
    
    ``` { .bash .no-copy }
    ros2 action send_goal <action_name> <action_type> <goal>
    ```

    Sabemos por nuestra investigación anterior con los comandos `ros2 action list`, `info` y `ros2 interface show` cómo proporcionar los datos correctos aquí:
    
    1. `action_name`: `/camera_sweep`
    1. `action_type`: `tuos_interfaces/action/CameraSweep`
    1. `goal`: un paquete de datos (en formato YAML) que contiene dos parámetros:
        1. `sweep_angle`: el ángulo (en grados) que el robot rotará en su lugar (es decir, el 'barrido')
        1. `image_count`: el número de imágenes que capturará desde su cámara frontal mientras realiza el 'barrido'
    
1. Ahora, de nuevo en **TERMINAL 3**, intenta usar el comando `ros2 action send_goal`, pero vigila la **TERMINAL 2** mientras lo haces:

    ``` { .bash .no-copy }
    ros2 action send_goal /camera_sweep tuos_interfaces/action/CameraSweep \
        "{sweep_angle: 0, image_count: 0}"
    ```

    Después de llamar al action, se te debería presentar un mensaje (en **TERMINAL 3**) indicando que el `Goal was rejected.` En **TERMINAL 2** (donde se está ejecutando el action server), deberíamos ver información adicional sobre por qué fue así. Lee esto y luego regresa a **TERMINAL 3** e intenta de nuevo enviar un goal al action server, ¡esta vez suministrando entradas válidas!

    Una vez que se hayan suministrado parámetros de goal válidos, el action server (en **TERMINAL 2**) responderá para informarte de lo que va a hacer. Luego deberás esperar a que complete su tarea...

1. Una vez que el action haya completado (podría tardar hasta 20 segundos), debería aparecer un mensaje en **TERMINAL 3** para informarnos del resultado:
        
    ``` { .txt .no-copy }
    Result:
        image_paths: 
    - ~/ros_action_examples/img01.jpg
    - ~/ros_action_examples/img02.jpg
    - ~/ros_action_examples/img03.jpg
    - ...

    Goal finished with status: SUCCEEDED
    ```

    Adicionalmente, también deberíamos ver algo más de texto en **TERMINAL 2**:

    ``` { .txt .no-copy }
    [INFO] [#####] [camera_sweep_action_server_node]: camera_sweep_action_server_node completed successfully:
      - Angular sweep = # degrees
      - Images captured = #
      - Time taken = # seconds
    ```

    1. El *result* del action (presentado en **TERMINAL 3**) es una serie de rutas de archivos, que ilustran las imágenes que han sido capturadas y dónde se han guardado en el sistema de archivos. Navega a este directorio en **TERMINAL 3** (usando `cd`) y echa un vistazo al contenido usando `ll` (un alias útil para el comando `ls`):

        ```bash
        cd ~/ros_action_examples
        ```

        ```bash
        ll
        ```
            
        Deberías ver el mismo número de archivos de imagen que el solicitado con el parámetro `image_count`.
    
    1. Lanza `eog` en este directorio y navega por todas las imágenes para revelar el *entorno misterioso* de tu robot:

        ```bash
        eog .
        ```

1. Hagamos esto una vez más. Cierra la ventana de `eog`, regresa a **TERMINAL 3** y emite el comando `ros2 action send_goal` nuevamente, pero esta vez usa el flag opcional `-f`: <a name="send_goal_cli"></a>

    ```bash
    ros2 action send_goal -f /camera_sweep tuos_interfaces/action/CameraSweep \
        "{sweep_angle: 0, image_count: 0}" 
    ```

    !!! tip
        ¡No olvides suministrar nuevamente parámetros de goal válidos!

    *Ahora*, además de recibir un result una vez que el action haya completado, ¡*también* recibimos algunas actualizaciones regulares mientras el action está en progreso (también conocido como *"feedback"*)!

1. Para terminar, cierra el action server en **TERMINAL 2** y el proceso de Gazebo headless en **TERMINAL 1** ingresando ++ctrl+c++ en cada terminal.

## ¿Qué es un ROS Action?

En el ejercicio anterior lanzamos un action server y luego lo llamamos desde la línea de comandos usando el sub-comando `ros2 action send_goal`. De la misma manera que un ROS Service, el action también nos proporcionó un **result** una vez que la tarea se completó.

Usando el flag `-f` pudimos pedir al servidor que nos proporcionara *feedback en tiempo real* sobre cómo iba (en **TERMINAL 3**). El **Feedback** es una de las características clave que diferencia a un ROS Action de un ROS Service: un Action Server proporciona **feedback** a intervalos regulares mientras trabaja hacia su **goal**. Otra característica de los ROS Actions es que pueden *cancelarse* a mitad de camino (con lo que jugaremos en breve).

<figure markdown>
  ![](./part5/action_interface.png){width=400px}
</figure>

En última instancia, los Actions usan una combinación de comunicación basada tanto en Topics *como* en Services, para crear un protocolo de mensajería más avanzado. Basándose en los ROS Services, los *Actions* están diseñados para ser usados en **tareas de larga duración**, debido a la provisión de *feedback* y la capacidad de *cancelar* un proceso a mitad de camino. Puedes leer más sobre Actions en [la documentación oficial de ROS 2 aquí](https://docs.ros.org/en/jazzy/Tutorials/Beginner-CLI-Tools/Understanding-ROS2-Actions/Understanding-ROS2-Actions.html){target="_blank"} (que también incluye una animación muy buena para explicar cómo funcionan).

### El Formato de las Interfaces de Action

Al igual que los Services, las Interfaces de Action tienen múltiples partes, y necesitamos saber qué formato tienen estos mensajes de action para poder usarlos.

Ejecutamos `ros2 interface show` en el ejercicio anterior, para interrogar la interface de action utilizada por el action server `/camera_sweep`:

```txt
ros2 interface show tuos_interfaces/action/CameraSweep
```

``` { .txt .no-copy }
--8<-- "https://raw.githubusercontent.com/tom-howard/tuos_ros/refs/heads/jazzy/tuos_interfaces/action/CameraSweep.action"
```

Como sabemos del Ejercicio 1, para llamar a este action server necesitamos enviar un **goal**, y (en este caso) hay **dos** parámetros de goal que deben proporcionarse:

1. `sweep_angle`: un valor de punto flotante de 32 bits
1. `image_count`: un entero de 32 bits

!!! question "Preguntas"
    * ¿Cuáles son los nombres de los parámetros de interface de **result** y **feedback**? (Hay tres en total.)
    * ¿Qué tipos de datos usan estos parámetros?

Aprenderás cómo usamos esta información para desarrollar nodes Python Action Server y Client en los siguientes ejercicios.

## Creación de Python Action Clients

En el ejercicio anterior *llamamos* a un Action Server preexistente desde la línea de comandos, enviándole un goal. Veamos ahora cómo podemos hacer esto desde dentro de un node Python de ROS.

### :material-pen: Ejercicio 2: Construir un Node Python Action Client {#ex2}

1. En **TERMINAL 1** lanza la simulación del *mundo misterioso* nuevamente, pero esta vez con un argumento adicional:

    ```txt
    ros2 launch tuos_simulations mystery_world.launch.py with_gui:=true
    ```

    Con el switch `with_gui` configurado en `true`, ahora deberíamos poder *ver* realmente el mundo simulado esta vez.

    <figure markdown>
      ![](../images/gz/coloured_pillars.png){width=600px}
    </figure>
    <center>*(¡No es muy emocionante que digamos!)*</center>

1. Luego, en **TERMINAL 2**, lanza el Camera Sweep Action Server nuevamente:

    ```bash
    ros2 run tuos_examples camera_sweep_action_server.py
    ```

#### Parte 1: Un Action Client Mínimo

1. Ahora, en **TERMINAL 3**, crea un nuevo paquete llamado `part5_actions` usando [el enfoque que hemos estado usando para crear paquetes a lo largo de este curso](part1.md#ex4).

1. Navega a la carpeta `scripts` de tu paquete usando el comando `cd`:

    ```bash
    cd ~/ros2_ws/src/part5_actions/scripts/
    ```

1. Aquí, crea un nuevo archivo Python llamado `camera_sweep_action_client.py` (usando el comando `touch`) y hazlo ejecutable ([usando `chmod`](./part1.md#chmod)).

1. Luego, declara esto como un ejecutable en el `CMakeLists.txt` del paquete:

    ```txt title="CMakeLists.txt"
    # Install Python executables
    install(PROGRAMS
      scripts/basic_velocity_control.py
      scripts/stop_me.py
      scripts/camera_sweep_action_client.py
      DESTINATION lib/${PROJECT_NAME}
    )
    ```

1. Como *mínimo absoluto*, el Action Client puede construirse de la siguiente manera:

    <center>[:material-file-code-outline: El Node `camera_sweep_action_client.py`](./part5/minimal_action_client.md){ .md-button target="_blank"}</center>

1. Construyamos el Node ahora, para poder ejecutarlo. Regresa a **TERMINAL 3** y usa Colcon para construir el paquete: <a name="colcon"></a>

    ```bash
    cd ~/ros2_ws/ 
    ```

    ```bash
    colcon build --packages-select part5_actions --symlink-install
    ```

1. Vuelve a cargar el `.bashrc`:

    ```bash
    source ~/.bashrc
    ```

1. Ejecuta tu node con `ros2 run`:

    ```
    ros2 run part5_actions camera_sweep_action_client.py
    ```

    Con el comando anterior tal como está, el servidor rechazará el goal (vuelve a **TERMINAL 2** para averiguar por qué). ¿Cómo puedes modificar el comando anterior (agregando algunos argumentos adicionales), para que el node `camera_sweep_action_client.py` envíe realmente un goal válido?[^goal_params]

    [^goal_params]: Necesitas establecer explícitamente los parámetros `goal_images` y `goal_angle` en tiempo de ejecución, [de manera similar a como lo hicimos aquí con el service client `number_game_client.py`](./part4.md#ex5).

1. Habiendo modificado el comando `ros2 run` para enviar exitosamente un *goal* válido al action server `camera_sweep`, el robot debería comenzar a girar, capturando imágenes a medida que avanza.

    El Client que hemos creado aquí hace una llamada al action server y luego termina, ¡ni siquiera espera a que el servidor complete su tarea! La única manera de saber si el action fue exitoso sería vigilar **TERMINAL 2**, para ver al *server* del action responder al goal que se le envió... El client en sí no proporciona feedback durante el action, ni el result al final. Veamos cómo incorporar eso ahora...

#### Parte 2: Manejo de un Result

1. Regresa al archivo `camera_sweep_action_client.py` en VS Code.

1. Para poder manejar el result que se envía desde un action server, primero necesitamos manejar la respuesta que el servidor envía al goal en sí.

    Dentro del método `send_goal()` de la clase `CameraSweepActionClient()`, encuentra la línea que dice:

    ```py
    return self.actionclient.send_goal_async(goal)
    ```

    y cámbiala a:

    ```py
    self.send_goal_future = self.actionclient.send_goal_async(goal)
    self.send_goal_future.add_done_callback(self.goal_response_callback)
    ```

    Este método ya no retorna el *future* que se envía desde `send_goal_async()`, sino que ahora lo maneja y le agrega un callback: `goal_response_callback`. Este callback ahora puede usarse para informar al client de si el servidor ha *aceptado* el goal o no.

1. Por lo tanto, necesitamos definir este callback ahora. Defínelo como un *nuevo* método de clase de la clase `CameraSweepActionClient()` (es decir, debajo del método de clase `send_goal()` que ya ha sido definido)...

    ```py
    def goal_response_callback(self, future):
        goal_handle = future.result()
        if not goal_handle.accepted:
            self.get_logger().warn("The goal was rejected by the server.")
            return

        self.get_logger().info("The goal was accepted by the server.")

        self.get_result_future = goal_handle.get_result_async()
        self.get_result_future.add_done_callback(self.get_result_callback)
    ```

    La *entrada* a este método será el *future* que crea la llamada `send_goal_async()`. Lo asignamos a un atributo llamado `goal_handle` aquí, y podemos usarlo para dos propósitos:

    1. Verificar si el goal que enviamos fue aceptado por el servidor.
    1. Si *fue* aceptado, entonces podemos obtener el result (usando `get_result_async()`) y podemos adjuntar *otro* callback para procesar realmente ese result: `get_result_callback`.

1. Ahora también necesitamos definir este callback. Define `get_result_callback` como otro nuevo método de la clase `CameraSweepActionClient()` (es decir, debajo del método de clase `goal_response_callback()` que acabamos de definir)...

    ```py
    def get_result_callback(self, future):
        result = future.result().result
        self.get_logger().info(
            f"The action has completed.\n"
            f"Result (Image Paths):\n  "
            + "\n  ".join(result.image_paths)
        )
        rclpy.shutdown()
    ``` 

    La entrada a *este* método de clase es otro objeto future que contiene el result real enviado desde el servidor. Lo asignamos a `result` y usamos una llamada `get_logger().info()` para imprimirlo en el terminal cuando el action haya finalizado.

    Como sabemos de nuestro trabajo anterior, la interface de Action `CameraSweep` contiene un parámetro de *Result* llamado `image_paths`.

1. Finalmente, en el método `main`, cambia esto:

    ```py
    future = action_client.send_goal()
    ```
    a solo esto:
    ```py
    action_client.send_goal()
    ```
    (porque `#!py send_goal()` ya no retorna un `future`)

1. Y luego también cambia:
    ```py
    rclpy.spin_until_future_complete(action_client, future)
    ```

    a esto:

    ```py
    rclpy.spin(action_client)
    ```

1. ¡Guarda todos tus cambios!

1. Ejecuta este node nuevamente ahora (con el comando `ros2 run`) y observa los cambios en acción.

    Nuestro node client ahora nos presenta el *result* que envía el servidor al completarse el action, pero ¿no sería bueno poder ver el *feedback* en tiempo real mientras el action tiene lugar? Agreguemos esto ahora...

#### Parte 3: Manejo de Feedback

1. Regresa al archivo `camera_sweep_action_client.py` en VS Code.

1. Para poder manejar el feedback que se envía desde un action server, ¡necesitamos agregar otro callback! Regresa al método `send_goal()` y a la línea donde realmente estamos enviando el goal al servidor:

    ```py
    self.send_goal_future = self.actionclient.send_goal_async(goal)
    ```

    Tal como está, todo lo que hacemos aquí es enviar el goal, pero también podemos agregar un *feedback callback* a esto:

    ```py
    self.send_goal_future = self.actionclient.send_goal_async(
        goal=goal, 
        feedback_callback=self.feedback_callback
    )
    ```

    El `feedback_callback` se ejecutará cada vez que se reciba un nuevo mensaje de feedback del servidor.

1. Para definir qué queremos hacer con estos mensajes de feedback, necesitamos agregar *otro nuevo* método a la clase `CameraSweepActionClient()`. Debajo del método de clase `get_result_callback()` que definimos antes, agrega también este nuevo:

    ```py
    def feedback_callback(self, feedback_msg):
        feedback = feedback_msg.feedback
        fdbk_current_angle = feedback.current_angle
        fdbk_current_image = feedback.current_image
        self.get_logger().info(
            f"\nFEEDBACK:\n"
            f"  - Current angular position = {fdbk_current_angle:.1f} degrees.\n"
            f"  - Image(s) captured so far = {fdbk_current_image}."
        )
    ``` 

    Como sabemos de nuestro trabajo anterior, la interface `CameraSweep` contiene dos parámetros de *feedback*: `current_angle` y `current_image`.

1. Guarda todos tus cambios nuevamente, ejecuta el node nuevamente con el comando `ros2 run` y observa los cambios en acción.

    El node que hemos construido ahora puede enviar un *goal* a un action server, procesar el *feedback* devuelto por el servidor mientras el action está en progreso, y presentarnos el *result* una vez que todo esté completo.
    
    Como se discutió anteriormente, la *otra* característica clave de los Actions es la capacidad de *cancelarlos* a mitad de camino. Veamos también cómo incorporar esto ahora.

#### Parte 4: Cancelar un Action

1. Primero, crea una copia de tu node `camera_sweep_action_client.py` y llámala `cancel_camera_sweep.py`. Asegúrate de que **TERMINAL 3** esté ubicada en el directorio `scripts` de tu paquete `part5_actions` antes de ejecutar lo siguiente:

    ```bash
    cp camera_sweep_action_client.py cancel_camera_sweep.py
    ```
    
1. No olvides declarar esto como un ejecutable *adicional* en el `CMakeLists.txt` del paquete. También necesitarás reconstruir el paquete con `colcon build` ([regresa para un recordatorio](#colcon)).

1. Abre el archivo `cancel_camera_sweep.py` en VS Code.

1. Queremos que este client pueda cancelar el goal en dos circunstancias diferentes:

    1. El client en sí es apagado por el usuario (mediante un ++ctrl+c++ en el terminal).
    1. Un evento condicional que ocurre mientras el action está en curso.

    Para abordar el punto 1 primero, necesitamos recurrir a parte del trabajo que hicimos en la Parte 2 en [la implementación de *procedimientos de apagado seguro*](part2.md#ex5)...

1. Como esperamos que recuerdes, primero necesitamos importar `SignalHandlerOptions` en nuestro node, así que agrega esto como una importación adicional al comienzo del código:

    ```py
    from rclpy.signals import SignalHandlerOptions
    ```

    Luego, en la función del node `main()`, modifica la llamada `#!py rclpy.init()`:

    ```py
    rclpy.init(
        args=args,
        signal_handler_options=SignalHandlerOptions.NO
    )
    ```

1. Dentro del método `#!py __init__()` de nuestra clase `CameraSweepActionClient()` ahora necesitamos agregar algunos flags adicionales:

    ```py
    self.goal_succeeded = False
    self.goal_cancelled = False
    self.stop = False
    ```

    En el método de clase `get_result_callback()`, podemos entonces asegurarnos de que el flag `self.goal_succeeded` se establezca en `True` cuando se recibe un result. En este método de clase, localiza la línea `#!py rclpy.shutdown()` y agrega la siguiente línea *adicional* justo encima de ella:

    ```py
    self.goal_succeeded = True
    ```

1. Los Actions pueden cancelarse usando un método `cancel_goal_async()` del `goal_handle` que se obtiene del `goal_response_callback()`. Por ello, necesitamos hacerlo accesible en toda nuestra clase `CameraSweepActionClient()`. Localiza el método de clase `goal_response_callback()` y agrega esta línea al final como la última línea del método `goal_response_callback()`:

    ```py
    self.goal_handle = goal_handle
    ```

    Esto hace que `goal_handle` sea accesible en toda la clase `CameraSweepActionClient()` como `#!py self.goal_handle`.

1. Solo podemos intentar cancelar un Action cuando está en progreso, por lo tanto, el *feedback callback* es el mejor lugar para activar esto. Localiza el método de clase `feedback_callback()` y coloca lo siguiente al final de él:

    ```py
    if self.stop:
        future = self.goal_handle.cancel_goal_async()
        future.add_done_callback(self.cancel_goal)
    ```

    Aquí, llamamos al método `cancel_goal_async()` desde `self.goal_handle` y agregamos otro nuevo callback (`cancel_goal()`) a él (es decir, para encapsular lo que queremos que suceda cuando el action sea cancelado).

1. Ahora, definamos esto como otro nuevo (¡y final!) método de clase:

    ```py
    def cancel_goal(self, future):
        cancel_response = future.result()
        if len(cancel_response.goals_canceling) > 0:
            self.get_logger().info('Goal successfully canceled')
            self.goal_cancelled = True
        else:
            self.get_logger().info('Goal failed to cancel')
    ```

    La entrada a este callback es otro *future*, que podemos usar para determinar si el goal ha sido cancelado (como se muestra arriba). Si *lo ha sido*, entonces establecemos nuestro flag `self.goal_cancelled` en `True`.

1. **Finalmente**, regresa a la función `main()` del node. Vamos a reemplazar la línea `#!py rclpy.spin(action_client)` ahora, con un `#!py rclpy.spin_once()`, envuelto dentro de un `#!py try` - `#!py except`, ¡envuelto dentro de un loop `#!py while`!
    
    ```py
    while not action_client.goal_succeeded:
        try:
            rclpy.spin_once(action_client)
            if action_client.goal_cancelled:
                break
        except KeyboardInterrupt:
            print("Ctrl+C")
            action_client.stop = True
    ```

    El loop `#!py while` se ejecutará hasta que el action complete exitosamente, *o* hasta que el goal sea *cancelado*, *o* apaguemos el node con una interrupción ++ctrl+c++.

    Revisa el node para ver cómo todo esto fluirá a través de tu clase.

1. Es posible que deseemos cancelar un goal *condicionalmente* si, por ejemplo, ha transcurrido demasiado tiempo desde que se realizó la llamada, o si el caller ha sido informado de algo más que ha ocurrido mientras tanto (¡quizás nos estamos quedando sin espacio de almacenamiento en el robot y no podemos guardar más imágenes!).

    Para los propósitos de este ejercicio, queremos modificar nuestro node para que el action siempre sea cancelado después de que se hayan capturado un total de **5 imágenes**. Esto puede hacerse realizando una modificación bastante pequeña al `feedback_callback()`. **Intenta implementar esto ahora**.

    * Intenta ahora introducir una llamada condicional al método `cancel_goal()` una vez que se hayan capturado un total de **5 imágenes**.
    * Podrías usar el atributo `current_image` del mensaje `CameraSweepFeedback` para activar esto.

### Un Resumen de los ROS Actions

Los ROS Actions funcionan de manera muy similar a los ROS Services, pero tienen las siguientes diferencias clave:

1. Pueden **cancelarse**: Si algo tarda demasiado, o si ha ocurrido algo más, entonces un Action Client puede cancelar un Action cuando lo necesite.
1. Proporcionan **feedback**: para que un client pueda monitorear lo que está sucediendo y actuar en consecuencia (es decir, cancelar el action, si es necesario).

Por lo tanto, este mecanismo es útil para operaciones que pueden tardar mucho en ejecutarse, y donde podría ser necesaria una intervención.

## Creación de tus Propios Action Servers, Clients e Interfaces

!!! info "Importante"
    Cancela *todos* los procesos activos que puedas tener en ejecución antes de continuar.

Hasta ahora hemos visto cómo llamar a un action server preexistente, pero ¿qué pasa si realmente queremos configurar el nuestro propio, y también usar nuestras propias Interfaces de Action personalizadas?

Para empezar, echa un vistazo al Action Server con el que has estado trabajando en los ejercicios anteriores. Has estado lanzándolo con el siguiente comando:

``` { .bash .no-copy }
ros2 run tuos_examples camera_sweep_action_server.py
```

!!! question "Preguntas"
    * ¿A qué *paquete* pertenece el node del action server?
    * ¿Dónde (en el directorio de ese paquete) es probable que esté ubicado este node?

Una vez que hayas identificado el nombre y la ubicación del código fuente, ábrelo en VS Code y revísalo para ver cómo funciona todo. No te preocupes demasiado por todo el contenido relacionado con la obtención y manipulación de imágenes de cámara, aprenderemos más sobre esto en [la siguiente parte de este curso](./part6.md). En cambio, enfócate en la estructura general del código y en la manera en que se implementa el action server.

Algunas cosas a revisar:

1. La manera en que el servidor se inicializa y los numerosos callbacks que se le adjuntan:
    
    ```py
    self.actionserver = ActionServer(
        node=self, 
        action_type=CameraSweep,
        action_name="camera_sweep",
        execute_callback=self.server_execution_callback, # (1)!
        callback_group=ReentrantCallbackGroup(), # (2)!
        goal_callback=self.goal_callback, # (3)!
        cancel_callback=self.cancel_callback # (4)!
    )
    ```

    1. Este callback contiene todo el código que ejecutará el servidor una vez que se le envíe un goal válido (es decir, la funcionalidad principal del Action).
    2. Este node servidor se configura como un *Executor Multi-hilo* (consulta la configuración en `main()`), para controlar la ejecución de los diversos callbacks que necesitamos. Aquí, asignamos el Action Server a un *Reentrant Callback Group*, permitiendo que todos sus callbacks se ejecuten en paralelo, así como otros callbacks de subscriber también.
    3. Este callback se usa para verificar los parámetros del goal que se han enviado al servidor, para decidir si aceptar o rechazar una solicitud.
    4. Este callback contiene todo lo que necesita suceder en caso de que el Action sea *cancelado* a mitad de camino.


1. Echa un vistazo a los diversos callbacks de Action para ver qué sucede en cada uno:

    1. ¿Cómo se verifican los parámetros de **goal** y, consecuentemente, se aceptan o rechazan?
    1. ¿Cómo se implementan las **cancelaciones** y cómo se monitorea esto en el `server_execution_callback()` principal?
    1. ¿Cómo se maneja y publica el **feedback**?
    1. ¿Cómo se maneja y publica también el **result**?

1. Finalmente, considera las operaciones de apagado.

### Implementación de una Estrategia de "Exploración" usando el Marco de Actions {#explore}

Una estrategia de exploración permite a un robot navegar autónomamente por un entorno desconocido mientras simultáneamente evita colisiones. Una manera de lograr esto es utilizar dos estados de movimiento distintos: moverse hacia adelante y girar en su lugar, alternando repetidamente entre ellos. El *Movimiento Browniano* y el *Levy Flight* son ejemplos de este tipo de enfoque. Aleatorizar el tiempo pasado en uno o ambos de estos dos estados resultará en una estrategia de navegación que permite al robot explorar lenta y aleatoriamente un entorno. El movimiento hacia adelante podría realizarse hasta que, por ejemplo, se haya recorrido cierta distancia, haya transcurrido un tiempo determinado o algo se interponga en el camino. De manera similar, la dirección, velocidad y/o duración del giro también podría aleatorizarse para lograr esto.

En los próximos ejercicios construiremos nuestra propia Interface de Action, y nodes Server y Client con el objetivo de crear la *base* para un comportamiento de exploración básico. Habiendo completado estos ejercicios tendrás algo que, con mayor desarrollo, podría convertirse en un tipo de comportamiento de exploración como el descrito arriba.

#### :material-pen: Ejercicio 3: Crear una Interface de Action {#ex3}

En el Ejercicio 2 creamos el paquete `part5_actions`. Dentro de este paquete ahora definiremos una *Interface* de Action para ser usada por el Action Server y Client subsiguientes que crearemos en los ejercicios posteriores.

1. Las interfaces de action deben definirse dentro de una carpeta `action` en la raíz del directorio del paquete, así que vamos a crearla ahora en **TERMINAL 1**:

    1. Primero, navega a tu paquete:

        ```bash
        cd ~/ros2_ws/src/part5_actions
        ```
    
    1. Luego usa `mkdir` para crear un nuevo directorio:

        ```bash
        mkdir action
        ```

1. Aquí ahora definiremos una Interface de Action llamada `ExploreForward`:

    ```bash
    touch action/ExploreForward.action
    ```

1. Ábrela en VS Code y define la estructura de datos de la Interface de la siguiente manera:

    ```txt title="ExploreForward.action"
    #goal
    float32 fwd_velocity               # The speed at which the robot should move forwards (m/s)
    float32 stopping_distance          # Minimum distance of an approaching obstacle before the robot stops (meters) 
    ---
    #result
    float32 total_distance_travelled   # Total distance travelled during the action (meters)
    float32 closest_obstacle           # LaserScan distance to the closest detected obstacle up ahead (meters)
    ---
    #feedback
    float32 current_distance_travelled # Distance travelled so far during the action (meters)
    ```

    Esta interface tiene por lo tanto **dos** parámetros de goal, **uno** de feedback y **dos** de result:

    **Goal**:

    1. `fwd_velocity`: La velocidad (en m/s) a la que el robot debe moverse hacia adelante cuando se llama al action server.
    1. `stopping_distance`: La distancia (en metros) a la que el robot debe detenerse frente a cualquier objeto o pared límite que esté delante de él (estos datos provendrán de los datos `LaserScan` del sensor LiDAR del robot).
    
    **Feedback**:

    1. `current_distance_travelled`: La distancia recorrida (en metros) desde que se inició el action actual (basada en datos de `Odometry`).

    **Result**:

    1. `total_distance_travelled`: La distancia *total* recorrida (en metros) durante el transcurso del action (basada en datos de `Odometry`).
    1. `closest_obstacle`: La distancia al obstáculo más cercano por delante del robot cuando el action se completa.

1. Ahora, declara esta interface en el archivo `CMakeLists.txt` del paquete, para que se pueda crear el código Python necesario:

    ```txt title="CMakeLists.txt"
    find_package(rosidl_default_generators REQUIRED)
    rosidl_generate_interfaces(${PROJECT_NAME}
      "action/ExploreForward.action" 
    )
    ```

1. También modifica el archivo `package.xml` (encima de la línea `#!xml <export>`) para incluir las dependencias `rosidl` necesarias:

    ```xml title="package.xml"
    <buildtool_depend>rosidl_default_generators</buildtool_depend>
    <exec_depend>rosidl_default_runtime</exec_depend>
    <member_of_group>rosidl_interface_packages</member_of_group>
    ```

1. Ahora ejecuta `colcon` para generar el código fuente necesario para esta nueva interface: <a name="colcon-build-steps"></a>

    1. Primero, **siempre** asegúrate de estar en la raíz del Workspace:
        
        ```bash
        cd ~/ros2_ws/
        ```
    
    1. Luego ejecuta `colcon build`:

        ```bash
        colcon build --packages-select part5_actions --symlink-install 
        ```
    
    1. Y finalmente vuelve a cargar el `.bashrc`:

        ```bash
        source ~/.bashrc
        ```

1. Ahora podemos verificar que funcionó.

    1. Usa `ros2 interface` para listar todos los tipos de interface disponibles, pero usa la opción `-a` para mostrar solo las interfaces de tipo action:

        ```bash
        ros2 interface list -a
        ```

        Busca un mensaje con el prefijo "`part5_actions`".

    1. A continuación, *muestra* la estructura de datos de la interface:

        ```bash
        ros2 interface show part5_actions/action/ExploreForward
        ```

        Esto debería coincidir con el contenido del archivo `part5_actions/action/ExploreForward.action` que creamos arriba.

#### :material-pen: Ejercicio 4: Construir el Action Server "ExploreForward" {#ex4}

1. En **TERMINAL 1** navega a la carpeta `scripts` de tu paquete `part5_actions`, luego:
    
    1. Crea un script Python llamado `explore_server.py`
    1. Hazlo ejecutable
    1. Decláralo como un ejecutable en `CMakeLists.txt`

1. Abre el archivo en VS Code.

1. La tarea del node Server es la siguiente:

    * El action server debe hacer que el robot se mueva hacia adelante hasta detectar un obstáculo por delante.
    * Debe usar la Interface `ExploreForward.action` que creamos en el ejercicio anterior.
    * El Server deberá configurarse para aceptar dos parámetros de **goal**:
        
        1. La velocidad (en m/s) a la que el robot debe moverse hacia adelante cuando se llama al action server.
        1. La distancia (en metros) a la que el robot debe detenerse frente a cualquier objeto o pared límite que esté delante de él.
            
            Para hacer esto necesitarás suscribirte al topic `/scan`. Ten en cuenta que un objeto no estará necesariamente directamente frente al robot, por lo que puede que necesites monitorear un rango de puntos de datos de `LaserScan` (dentro del arreglo `ranges`) para que la evasión de colisiones sea efectiva (recuerda el [ejemplo de callback de LaserScan de la Parte 3](./part3/lidar_subscriber.md)).
    
    * Asegúrate de hacer algunas verificaciones de errores en los parámetros del goal para garantizar que se realice una solicitud válida. Esto se hace adjuntando un `goal_callback` al Action Server.

        * `fwd_velocity`: Debe ser una velocidad moderada, dentro de [los límites de velocidad del robot](./part2.md#velocity_limits).
        * `stopping_distance`: Debe ser mayor que el [límite mínimo detectable del Sensor LiDAR](./part3.md#range_max_min), lo suficientemente grande para evitar colisiones de manera segura.

    * Mientras tu servidor realiza su tarea debe proporcionar el siguiente **feedback** a un Client:

        1. La distancia recorrida (en metros) desde que se inició el action actual.

            Para hacer esto necesitarás suscribirte al topic `/odom`. Recuerda el trabajo que hiciste en la Parte 2 sobre esto.
            
            !!! tip "Consejos" 
            
                * La orientación del robot no debería cambiar durante el transcurso de una sola llamada al action, solo sus posiciones `linear.x` y `linear.y` deberían variar.
                * Ten en cuenta, sin embargo, que el robot no necesariamente se moverá a lo largo del eje `X` o `Y`, por lo que necesitarás considerar la distancia total recorrida en el plano `X-Y`.
                * Hicimos esto en el [ejercicio `move_square` de la Parte 2](./part2.md#ex6), así que consúltalo si necesitas un recordatorio.

    * Finalmente, al completarse el action, tu servidor debe estar configurado para proporcionar los siguientes **dos** parámetros de *result*:
        1. La distancia *total* recorrida (en metros) durante el transcurso del action.
        1. La distancia al obstáculo que hizo que el robot se detuviera (si el action server ha hecho su trabajo correctamente, esto debería ser muy similar al `stopping_distance` que proporcionó el Action Client en el **goal**).

1. Hay código de plantilla para ayudarte con esto:

    <center>[:material-file-code-outline: La Plantilla `explore_server.py`](./part5/explore_server.md){ .md-button target="_blank"}</center>
    
    También puede que quieras echar un vistazo al código de `camera_sweep_action_server.py` de los ejercicios anteriores para ayudarte a construir esto: muchas de las técnicas usadas aquí serán similares (excluyendo todo lo relacionado con la cámara).

**Pruebas**

Cuando quieras probar las cosas, ¿por qué no usar el entorno *Nav World* de la Parte 3 (en **TERMINAL 1**)?:

```bash
ros2 launch tuos_simulations nav_world.launch.py
```

<figure markdown>
  ![](./part3/nav_world.png){width=600px}
</figure>

No olvides que para lanzar el servidor necesitarás haber construido todo con `colcon` siguiendo [el proceso habitual de **tres etapas**](#colcon-build-steps).

Haz esto en **TERMINAL 2** y luego podrás ejecutarlo:

```bash
ros2 run part5_actions explore_server.py
```

Además, no olvides que **no necesitas haber desarrollado un Node Python Client para probar el servidor**. Usa la herramienta CLI `ros2 action send_goal` para hacer llamadas al servidor (como lo hicimos en el [Ejercicio 1](#send_goal_cli)).

#### :material-pen: Ejercicio 5: Construir un Client Básico "ExploreForward" {#ex5}

1. En **TERMINAL 3** navega a la carpeta `scripts` de tu paquete `part5_actions`, crea un script Python llamado `explore_client.py`, hazlo ejecutable y agrégalo a tu `CMakeLists.txt`.

1. Ejecuta `colcon build` ahora, para que no tengas que preocuparte por ello más tarde (de nuevo, siguiendo el [proceso de **tres etapas** como arriba](#colcon-build-steps))...

    Aquí está de nuevo, por si acaso:

    1. Paso 1:
    
        ```bash
        cd ~/ros2_ws
        ```

    1. Paso 2:

        ```bash
        colcon build --packages-select part5_actions --symlink-install
        ```

    1. Paso 3:

        ```bash
        source ~/.bashrc
        ```
    
1. Abre el archivo `explore_client.py` en VS Code.

1. La tarea del Action Client es la siguiente:

    * El client necesita emitir un **goal** correctamente formateado al servidor.
    * El client debe programarse para monitorear los datos de **feedback** del Server. Si detecta (a partir del feedback) que el robot ha recorrido una distancia *mayor de 2 metros* sin detectar un obstáculo, entonces debe **cancelar** la llamada al action actual.

1. Usa las técnicas que usamos en el node Client del [Ejercicio 2](#ex2) como guía para ayudarte con esto.

    <!-- There's also [a code template here](./part5/search_client.md) to help you get started. <a name="ex4c_ret"></a> -->

1. Una vez que tengas todo en su lugar, lanza el action client con `ros2 run` como se muestra a continuación:

    ```bash
    ros2 run part5_actions explore_client.py
    ```

    Si todo está bien, este node client debería llamar al action server, que (a su vez) hará que el robot se mueva hacia adelante hasta que esté a cierta distancia de un obstáculo por delante (`stopping_distance`), momento en el que el robot se detendrá, y tu node client también debería detenerse. Una vez que esto suceda, reorienta tu robot (usando el node `teleop_keyboard`) y lanza el node client nuevamente para asegurarte de que esté deteniéndose de manera robusta frente a los obstáculos repetidamente, y cuando se aproxime desde diferentes ángulos.

    !!! warning "Importante"
        Asegúrate de que tu funcionalidad de cancelación también funcione correctamente, garantizando que:
            
        1. El robot nunca se mueva más de 2 metros durante una llamada al action determinada.
        1. Un action se aborta a mitad de camino si el node client se apaga con ++ctrl+c++.

#### :material-pen: Ejercicio 6 (Avanzado): Implementar una Estrategia de Exploración {#ex6}

Hasta ahora, tu node Action Client debería tener la capacidad de llamar al servidor `ExploreForward.action` para hacer que el robot se mueva hacia adelante 2 metros, o hasta que llegue a un obstáculo (lo que ocurra primero), pero *podrías* construir sobre esto ahora y convertirlo en un comportamiento de exploración completo:

* Entre llamadas al action, tu node *client* podría hacer que el robot gire en su lugar para enfrentar una dirección diferente y luego emitir otra llamada al action para hacer que el robot se mueva hacia adelante nuevamente.
* El proceso de giro podría hacerse aleatoriamente (*idealmente*), o en una cantidad fija cada vez.
* Programando tu node client para repetir este proceso una y otra vez, el robot (de manera algo aleatoria) recorrería su entorno de forma segura, deteniéndose antes de chocar con cualquier obstáculo y reorientándose cada vez que deje de moverse hacia adelante.

<!-- !!! success "Assignment #2 Checkpoint"
    Having completed Assignment #1 up to this point, you should have everything you need to tackle [Assignment #2 Task 2](../assignment2/parta/task2.md). -->

<!-- #### :material-pen: Advanced Exercise 2: Autonomous Navigation using waypoint markers {#adv_ex2}

In Part 3 you used SLAM to construct a map of an environment ([Exercise 2](./part3.md#ex2)) and then issued navigation requests to the `move_base` action server, via the command-line, ([Exercise 3](./part3.md#ex3)) to make your robot move to a zone marker, based on coordinates that you had established beforehand. Now that you know how to build Action Client Nodes in Python you could return to your `part2_navigation` package and build a new node that makes the robot move sequentially between each zone marker programmatically.

* Your node could cycle through the coordinates of all four of the zone markers (or "waypoints") that you established whilst using SLAM to build a map of the environment ([as per Exercise 2](./part3.md#ex2)).
* Your node could monitor the status of the `move_base_simple` action call to know when the robot has reached a zone marker, so that it knows when to issue a further action call to move on to the next one.
* You could refer to [the launch file that you created in Part 3](./part3.md#launch_file) to launch all the navigation processes that need to be running in order to enable and configure the ROS Navigation Stack appropriately for the TurtleBot3 robot. -->

## Conclusión

En la Parte 5 de este curso has aprendido:

* Cómo funcionan los ROS Actions y por qué pueden ser útiles.
* Cómo desarrollar Action Client Nodes en Python que pueden monitorear el action en tiempo real (a través de *feedback*), y que también pueden *cancelar* el action solicitado, si es necesario.
* Cómo usar las herramientas estándar de ROS para interrogar interfaces de action, permitiéndonos así construir clients para llamarlas.
* Cómo construir action servers, clients e interfaces personalizados.
* Cómo aprovechar este marco para implementar una *estrategia de exploración*.

### Topics, Services o Actions: *¿Cuál Elegir?*

Ahora deberías haber desarrollado una buena comprensión de los tres métodos de comunicación disponibles dentro de ROS para facilitar la comunicación entre ROS Nodes:

1. Mensajería basada en Topics.
1. ROS Services.
1. ROS Actions.

A través de este curso has adquirido algo de experiencia práctica usando los tres, pero puede que aún te preguntes cómo seleccionar el apropiado para cierta tarea robótica...

[Esta página web de ROS.org](https://docs.ros.org/en/jazzy/How-To-Guides/Topics-Services-Actions.html){target="_blank"} resume todo esto muy bien (y brevemente), así que deberías leerla para asegurarte de saber qué es qué. En resumen:

* **Topics**: Son más apropiados para transmitir flujos de datos continuos como datos de sensores e información del estado del robot, y para publicar datos que probablemente sean requeridos por una variedad de Nodes en una red de ROS.
* **Services**: Son más apropiados para procedimientos muy cortos como cálculos *rápidos* (cinemática inversa, etc.) y para realizar acciones discretas cortas que es poco probable que salgan mal o que no necesitarán intervención (p. ej., encender un LED de advertencia cuando la batería está baja).
* **Actions**: Son más apropiados para tareas de larga duración (como mover un robot), o para operaciones donde *podríamos* necesitar cambiar de opinión y hacer algo diferente o cancelar un comportamiento invocado a mitad de camino.
    
### Usuarios de Computadoras del Laboratorio con WSL-ROS2: ¡Guarda tu trabajo! {#backup}

Recuerda guardar el trabajo que has realizado en WSL-ROS2 durante esta sesión para poder restaurarlo en una máquina diferente en una fecha posterior. Ejecuta el siguiente script en cualquier instancia de Terminal WSL-ROS2 inactiva ahora:

```bash
wsl_ros backup
```

Luego podrás restaurarlo en un entorno WSL-ROS2 nuevo la próxima vez que lo inicies (`wsl_ros restore`).
