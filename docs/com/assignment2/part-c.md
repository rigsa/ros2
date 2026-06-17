---  
title: "Asignación #2 Parte C (tarea individual avanzada)"  
description: "En Simulación, programa un Waffle para buscar un entorno, detectar un objeto de color y navegar hacia él."
---  

Los estudiantes que deseen completar esta tarea adicional individual como parte de la Asignación #2 pueden hacerlo. La distribución general de puntos para la Asignación #2 es la siguiente:

<center>

| Parte | Descripción | Ponderación de Asignación #2 | Entrega |
| :---: | :---  | :---: | :---: |
| **A** | **[Tareas 1 y 2](./part-a/README.md)**<br />Entrega de equipo | 30% | Viernes de la Semana 6 a las 6pm |
| **B** | **[Tarea 3 y Viva de Equipo](./part-b/README.md)**<br />Entrega de equipo | 45% | Viernes de la Semana 12 a las 6pm |
| **C** | **[Tarea de Búsqueda, Detección y Balizamiento](#overview)**<br />Entrega individual (evaluada en simulación) | 25% | Viernes de la Semana 12 a las 6pm |

</center>

Como se indicó arriba, la **fecha límite para la Parte C** es la Semana 12, viernes a las 6pm.

## Descripción General {#overview}

Desarrolla nodes de ROS que permitan a un TurtleBot3 Waffle buscar un entorno, detectar un objeto de color y navegar hacia él, ¡deteniéndose en su proximidad sin chocar contra él!

Esta es una asignación **individual**, que será evaluada **en simulación** ^^NO^^ en un robot real.

## La Tarea

Para esta tarea, tu robot será colocado en una *"Arena de Búsqueda"* que contiene varios objetos de diferentes colores (*"balizas"*). Partiendo de los comportamientos de exploración que habrás desarrollado en tu equipo para las Tareas de la Asignación #2, el robot necesitará buscar en el arena una baliza de un *"Color Objetivo"* particular (cada baliza en el arena tendrá un color único). El arena contendrá tres *"Zonas de Inicio"*: **A**, **B** y **C** (también de colores únicos) y tu robot estará ubicado en una de estas tres zonas para comenzar (seleccionada al azar). El color de la Zona de Inicio indica el Color Objetivo para la tarea de búsqueda (es decir, el color de la baliza que el robot necesita encontrar). Una vez que se haya detectado el objeto objetivo, el robot necesitará moverse hacia él (es decir, *"balizamiento"*) y detenerse dentro de una *"Zona de Parada"* impresa en el suelo alrededor de él. ¡El robot debe detenerse en la Zona de Parada sin tocar la baliza!

Lo primero que tu robot necesitará hacer en esta tarea es detectar el color de la zona en la que empieza. Aprendiste sobre la detección de objetos basada en color en la [Parte 6 del Curso de ROS 2](../../course/part6.md#ex2), donde usaste OpenCV para analizar las imágenes publicadas en el topic `/camera/image_raw`. Usa lo que hiciste aquí, así como el trabajo adicional que hiciste en el [Ejercicio 3 de la Parte 6](../../course/part6.md#ex3), como punto de partida para lograr el comportamiento deseado para esta parte inicial de la tarea. Ten en cuenta que en los ejercicios de la Parte 6 desarrollaste algoritmos para detectar un objeto de cierto color, pero aquí necesitas trabajar de la manera opuesta y realmente establecer el color del objeto, por lo que tendrás que invertir la lógica un poco.

Luego necesitarás explorar el arena para encontrar el objeto objetivo. Recuerda que tanto la zona de inicio como el objeto objetivo compartirán el mismo color, ¡así que ten cuidado de no detectar la zona de inicio como la baliza! La odometría podría ser útil aquí para informar a tu robot de dónde comenzó, para que sepa descartar cualquier cosa en esa zona como posible objetivo.

Habiendo localizado el objeto objetivo dentro del entorno, tu robot entonces necesitará moverse hacia él y detenerse dentro de la zona de parada asignada. Esta técnica se conoce como *Balizamiento*, y algunas estrategias para esto se discuten en los materiales del curso. Quizás podrías considerar una implementación del Vehículo 3a de Braitenberg como una forma de controlar la trayectoria y el enfoque de tu robot hacia el objeto objetivo.

El concepto de *Orientación Visual* también podría valer la pena considerar como método para controlar la posición y trayectoria de un robot basándose en las imágenes de su cámara. Las mediciones de distancia del sensor LiDAR también podrían ser útiles para esto.

## Crear un Paquete

Necesitarás crear tu propio paquete de ROS individual para esta asignación. Esta es una *asignación individual*, y es completamente separada del proyecto de equipo de la Asignación #2 (Partes A y B), por lo que debes crear tu propio repositorio de paquetes de ROS individual para esto. Sigue los pasos a continuación para hacerlo:

### Crear tu Repositorio de Paquete Individual (en GitHub)

1. Asegúrate de haber iniciado sesión en tu cuenta de GitHub, luego ve al [repositorio `ros2_pkg_template`](https://github.com/tom-howard/ros2_pkg_template){target="_blank"}.
1. Haz clic en el botón verde `Use this template` y luego selecciona `Create a new repository` del menú desplegable.

    <figure markdown>
      ![](../assignment2/getting-started/ros2_pkg_template.png){width=700px}
    </figure>

    Luego deberías ver una pantalla de **Create a new repository**.

1. Introduce un nombre para tu repositorio en el cuadro `Repository name`. Este nombre **debe** estar formateado de la siguiente manera:

    ``` { .txt .no-copy }
    ros2_lab_individual_XXXXX
    ```

    ... donde `XXXXX` debe reemplazarse con tu **nombre de usuario** o identificador.

    !!! warning "Importante"
        Todos los caracteres deben estar en **minúsculas**

1. Selecciona `Private` para **hacer el repositorio privado**, luego haz clic en el botón verde `Create repository`.

1. Serás dirigido a la página principal de tu repositorio. Desde aquí, haz clic en `Settings`, luego en `Access` haz clic en `Collaborators` (es posible que se te solicite 2FA).

1. En el área `Manage access`, haz clic en el botón verde `Add people` y agrega a los miembros del equipo docente según te indiquen.

### Registrar tu Paquete de ROS

Habiendo creado tu paquete, deberás informarnos tu nombre de usuario de GitHub y la URL de GitHub de tu repositorio. Hay un formulario que **debes completar** para hacer esto. El formulario está disponible a través del enlace que te compartirá el equipo docente (también disponible en la plataforma del curso).

### Inicializar tu Paquete

Debes hacerlo desde dentro de tu propia instalación de ROS (por ejemplo, WSL-ROS2). [Consulta aquí para más detalles sobre cómo acceder a un entorno de ROS](../../software/README.md).

1. En GitHub, regresa a la página principal de tu repositorio haciendo clic en la pestaña `<> Code` en la parte superior izquierda.

1. Haz clic en el botón verde `Code` y luego, del menú desplegable, haz clic en el botón :octicons-copy-16: para copiar la URL **HTTPS** remota de tu repositorio.
    
1. Desde tu instalación local de ROS, abre una instancia de terminal y navega al directorio `src` del Espacio de Trabajo de ROS:

    ```bash
    cd ~/ros2_ws/src
    ```

1. Clona tu repositorio aquí usando la URL HTTPS remota:

    ``` { .bash .no-copy }
    git clone REMOTE_HTTPS_URL
    ```

    Luego se te pedirá que ingreses tu nombre de usuario de GitHub, seguido de una contraseña. Necesitarás [generar un token de acceso personal](https://docs.github.com/en/authentication/keeping-your-account-and-data-secure/creating-a-personal-access-token#creating-a-personal-access-token-classic){target="_blank"} y usarlo aquí (o [usar claves SSH](https://docs.github.com/en/authentication/connecting-to-github-with-ssh){target="_blank"} en su lugar).

1. Navega al directorio de tu paquete usando el comando `cd`:

    ``` { .bash .no-copy }
    cd ros2_lab_individual_XXXXX
    ```
    
    ...reemplazando `XXXXX` según corresponda.

1. Luego, ejecuta el script `init_pkg.sh` para configurar tu paquete de ROS apropiadamente:

    ```bash
    ./init_pkg.sh
    ``` 

### Publicar tus Cambios Locales en GitHub {#git-push}

Deberás asegurarte de que Git esté configurado correctamente con tu nombre y dirección de correo en tu instalación local de ROS antes de hacer esto. [Consulta aquí para detalles](./getting-started.md#git).

1. Desde la misma terminal que antes, usa el comando `git status` para ver todos los cambios realizados en el repositorio durante el proceso de inicialización:

    ```bash
    git status
    ```

1. Usa `git add` para *preparar* todos estos cambios para un commit inicial:

    ```bash
    git add .
    ```

1. Luego realiza el commit:

    ```bash
    git commit -m "ROS package initialisations complete."
    ```

1. Finalmente, *publica* los cambios locales de vuelta al repositorio "remoto" en GitHub:

    ```bash
    git push origin main
    ```

    Luego se te pedirá que ingreses tu nombre de usuario y contraseña de GitHub nuevamente. (¡Recuerda que **no** es la contraseña de tu cuenta de GitHub... Usa el token de acceso personal que creaste anteriormente!)

## Detalles

El arena utilizado para esta tarea será de 5.0 m x 5.0 m y las balizas que buscarás serán cajas o cilindros de colores, todos entre 200 mm y 400 mm de altura. La *Zona de Parada* que rodea cada baliza será 500 mm más grande que las dimensiones de la baliza en los ejes `X` e `Y`.

Solo hay **seis** colores objetivo posibles que se usarán en esta tarea, por lo que tu aplicación de ROS solo necesitará acomodar estos seis. Los colores se enumeran a continuación, y también hay un entorno de simulación en el paquete `tuos_task_sims` llamado `beacon_colours` para ilustrarlos[^update-course-repo].

[^update-course-repo]: Asegúrate de tener [la versión más actualizada del Repositorio del Curso](../../course/extras/course-repo.md#updating).

```bash
ros2 launch tuos_task_sims beacon_colours.launch.py
```

<figure markdown>
  ![](./part-c/beacon_colours_table.png){width=600px}
  <figcaption>El rango de posibles colores de balizas que podrían usarse en esta asignación.</figcaption>
</figure>

En cuanto a la tarea en sí:

1. Tu robot primero necesitará determinar el *"Color Objetivo"* analizando la *"Zona de Inicio"* en la que ha sido colocado dentro del arena simulado (ver abajo).
1. El arena contendrá tres Zonas de Inicio, cada una de un color diferente, y tu robot podría lanzarse en cualquiera de ellas (seleccionada al azar).
1. Una vez que el robot haya determinado el color de la zona de inicio, un Mensaje de Log de ROS 2 con severidad `INFO` **debe** imprimirse en la terminal para indicar qué color de baliza se buscará. Este mensaje de log **debe** estar formateado *exactamente* de la siguiente manera:

    <a name="target_beacon"></a>

    ``` { .txt .no-copy }
    SEARCH INITIATED: The target beacon colour is {}.
    ```

    Donde `{}` es reemplazado por el *nombre* del color objetivo tal como se define en la tabla de la figura anterior.

    !!! note
        Debes usar llamadas al método `#!py get_logger().info()` dentro de tu node para imprimir **TODOS** los mensajes de log para esta asignación.

1. El robot entonces necesita navegar por el arena, evitando el contacto con cualquiera de los objetos ubicados dentro de él mientras busca la baliza del color correcto.
1. Una vez detectada la baliza objetivo, otro Mensaje de Log con severidad `INFO` **debe** imprimirse en la terminal para indicar que esto ha sucedido. El mensaje de terminal debe ser claramente visible y legible, y *el robot debe estar mirando hacia la baliza objetivo cuando se imprima*. Este Mensaje de Log debe estar formateado de la siguiente manera:

    <a name="beacon_detected"></a>

    ``` { .txt .no-copy }
    TARGET DETECTED: Beaconing initiated.
    ```

    !!! note "Recuerda"
        Usa llamadas al método `#!py get_logger().info()` dentro de tu node para imprimir este mensaje de log con severidad `INFO`.

1. El robot entonces necesita comenzar a moverse hacia la baliza, deteniéndose cuando esté suficientemente cerca para estar dentro de la zona de parada que la rodea, pero no tan cerca como para realmente hacer contacto. Como se discutió anteriormente, la zona de parada que rodea cada objeto será 500 mm más grande que las dimensiones de la baliza en el plano `X-Y`.
1. Debe imprimirse un Mensaje de Log adicional con severidad `INFO` en la terminal para indicar que el robot se ha detenido exitosamente e *intencionalmente* dentro del área designada. Este mensaje de terminal debe estar formateado de la siguiente manera:

    <a name="beaconing_complete"></a>

    ``` { .txt .no-copy }
    BEACONING COMPLETE: The robot has now stopped.
    ```

    !!! note "Recuerda"
        ¡Usa `#!py get_logger().info()`!

1. El robot tendrá un máximo de 90 segundos para completar esta tarea.

    *El tiempo se determinará usando el indicador "Sim Time" en Gazebo*.

1. Tu paquete de ROS debe contener un archivo de lanzamiento llamado `part_c.launch.py`, de modo que la funcionalidad que desarrolles pueda lanzarse desde tu paquete mediante el comando:

    ``` { .bash .no-copy }
    ros2 launch ros2_lab_individual_XXXXX part_c.launch.py
    ```

    El robot ya habrá sido lanzado en el entorno simulado antes de que intentemos ejecutar tu archivo de lanzamiento.

## Recursos de Simulación

Dentro del paquete `tuos_task_sims` hay un entorno llamado `beaconing`, que puede usarse para desarrollar y probar tus nodes de ROS para esta tarea:

```bash
ros2 launch tuos_task_sims beaconing.launch.py
```

El arena contiene tres zonas de inicio: **A**, **B** y **C**; cada una de un color diferente, así como varias balizas de colores únicos. ¡Hay una baliza en el arena para coincidir con cada una de las tres zonas de inicio, más un par más para actuar como señuelos!

<figure markdown>
  ![](./part-c/beaconing.png){width=600px}
  <figcaption>El arena de "balizamiento".</figcaption>
</figure>

Puedes lanzar el robot en cualquiera de las tres zonas de inicio suministrando un argumento opcional `start_zone` al archivo `beaconing.launch.py`, como se ilustra a continuación:

```bash
ros2 launch tuos_task_sims beaconing.launch.py start_zone:={}
```

...donde `{}` puede reemplazarse por `a`, `b` o `c` para seleccionar la zona de inicio en la que quieres que esté ubicado el robot cuando se lance la simulación. Por lo tanto, puedes desarrollar y probar tus algoritmos de balizamiento en tres escenarios únicos.

!!! note
    1. Se usará el mismo arena para evaluar tu entrega para esta asignación.
    1. El color de las zonas de inicio y balizas cambiará, pero la forma, tamaño y ubicación de todos los objetos permanecerán iguales.
    1. Una vez más, la zona de inicio en la que se lanza tu robot para la evaluación será seleccionada al azar.

## Marcación

Hay **15 puntos** disponibles para esta tarea en total, otorgados según los criterios a continuación. No se otorgará crédito parcial a menos que se indique específicamente en alguno de los criterios.

<centre>

| Criterio | Puntos | Detalles |
| :--- | :---: | :--- |
| **A**: Identificar el color objetivo | 2/15 | Mientras el robot todavía está ubicado dentro de la zona de inicio, un node de ROS dentro de tu paquete debe imprimir un **Mensaje de Log** en la terminal para indicar el color objetivo que ha sido determinado y que se usará posteriormente para identificar la baliza objetivo. Recibirás los puntos completos disponibles aquí siempre que el mensaje se presente usando una llamada al método `#!py get_logger().info()`, **y** [esté formateado como se especifica aquí](#target_beacon). |
| **B**: Detectar la baliza correcta | 3/15 | Recibirás los puntos completos disponibles aquí por imprimir un **Mensaje de Log** en la terminal para indicar que la baliza objetivo ha sido identificada dentro del entorno. El mensaje debe presentarse nuevamente usando una llamada al método `#!py get_logger().info()`, debe estar [formateado como se especifica aquí](#beacon_detected), **y** el robot debe estar mirando directamente a la baliza cuando se imprima este mensaje. | 
| **C**: Detenerse en la zona de parada correcta | 5/15 | Tu robot debe **detenerse** dentro de la zona de parada correcta dentro del límite de tiempo de 90 segundos **y** un **Mensaje de Log** debe imprimirse en la terminal para indicar que esto se ha hecho intencionalmente. Recibirás los puntos completos disponibles aquí siempre que esto se logre exitosamente, y el mensaje de log (nuevamente usando una llamada `#!py get_logger().info()`) esté [formateado como se especifica aquí](#beaconing_complete). Si tu robot logra detenerse, pero parte de su cuerpo queda fuera de la zona de parada, se te otorgarán la mitad de los puntos. |
| **D**: Una "ejecución sin incidentes" | 5/15 | Si tu robot completa la tarea (o transcurren los 90 segundos) sin hacer contacto con nada en el arena, se te otorgará el máximo de puntos aquí. Se deducirán puntos por cualquier contacto realizado, a un mínimo de 0 (es decir, sin calificación negativa). ¡Tu robot debe estar moviéndose dentro del arena continuamente para ser elegible para estos puntos; simplemente girar sobre sí mismo durante 90 segundos no es suficiente! |

</center>

## Entrega

Tu trabajo será obtenido de GitHub en la fecha límite indicada arriba, por lo que es importante que registres tu paquete de ROS con el equipo docente para que puedan acceder a él.

Tu trabajo debe estar ubicado en la rama `main` del repositorio de tu paquete.
