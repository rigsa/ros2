---  
title: "Tarea 3: Exploración y Búsqueda"  
---  

Desarrolla nodes de ROS para permitir que un robot de simulación explore de manera autónoma la mayor parte posible del arena robótico, mientras busca una baliza y documenta su exploración con un mapa del entorno a medida que avanza.

!!! success "Puntos de Control del Curso"
    
    * Deberías haber completado **las Partes 1-6 de la Asignación #1 ^^en su totalidad^^** para apoyar tu trabajo aquí.

    * **[Entendiendo los robots](../../../waffles/essentials.md)** es *también* esencial para tu éxito en esta tarea, así que asegúrate de haber considerado **TODOS** los siguientes aspectos:
    
        * [ ] [Control de Movimiento y Velocidad](../../../waffles/essentials.md#motion-and-velocity-control)
        * [ ] [Lecturas de Desplazamiento Láser y el Sensor LiDAR](../../../waffles/essentials.md#laser-displacement-readings-and-the-lidar-sensor)
        * [ ] [La Cámara y el Procesamiento de Imagen](../../../waffles/essentials.md#the-camera-and-image-processing)

    * También necesitarás considerar algunos de los [**Conceptos Avanzados de Archivos de Lanzamiento** discutidos aquí](../../../course/extras/launch-files.md).

## Resumen

Esta tarea se basa en lo que hiciste para la Tarea 2. Esta vez, sin embargo, tu robot necesitará navegar por un arena con mayor densidad de obstáculos (es decir, más obstáculos), por lo que habrá menos espacio para navegar libremente y más posibilidades de que ocurran colisiones. Una vez más, el objetivo principal es *explorar de manera segura* la mayor parte del arena posible, pero ahora con un poco más de tiempo para hacerlo. Al mismo tiempo, necesitarás buscar una baliza de un color particular e intentar capturar una imagen de ella. Finalmente, *también* necesitarás documentar la exploración de tu robot construyendo un mapa del entorno (con SLAM) mientras explora, y guardar este mapa para que podamos verlo después.

## Detalles

### El Entorno

Ya estás muy familiarizado con el Arena Robótico, y ¡lo explorarás una vez más! Esto es lo que puedes esperar para la Tarea 3:

<a name="t3-arena-layout"></a>

<figure markdown>
  ![](../figures/task3_arena_layout.png){width=700px}
  <figcaption>Un ejemplo de la configuración del arena para la Tarea 3.</figcaption>
</figure>

<a name="env-vars"></a>

**Lo anterior es solo un ejemplo de cómo podría verse el arena real**, pero lo que podemos decir es esto:

* El arena contendrá varias paredes de madera de 180 mm de altura, 10 mm de grosor y 440 mm *o* 880 mm de longitud (habrá una combinación de ambas longitudes).
* Las paredes se ensamblarán juntas *al menos* en pares (ya que no pueden sostenerse solas), pero un solo ensamblaje de pared podría comprender más de dos paredes, y cualquier combinación de longitudes de pared.
* La ubicación y orientación de los ensamblajes de paredes, así como los ángulos relativos entre las paredes dentro de cada ensamblaje, variarán.
* Los ensamblajes de paredes y/o paredes también podrían variar ligeramente en cantidad (puede haber algunos más, puede haber algunos menos).
* El arena siempre contendrá **cuatro** balizas cilíndricas de 200 mm de diámetro y 250 mm de altura, cada una de un color diferente: una **amarilla**, una **roja**, una **verde** y una **azul**.
* Las balizas también podrían estar ubicadas *en cualquier lugar* del arena.
* Los "corredores" del arena (es decir, los espacios libres para que el robot explore) siempre serán suficientes para que un robot pase con cierta holgura. Sin embargo, debes anticipar que haya algunas *brechas muy pequeñas* entre paredes adyacentes en los ensamblajes de paredes (debido a las bisagras), o las "cuñas" que se forman entre una baliza colocada junto a una pared. Tus algoritmos de exploración deben ser robustos ante estas brechas pequeñas inevitables.
* El robot podría empezar *en cualquier lugar* del arena: cualquier zona, cualquier posición dentro de una zona y en cualquier orientación.

### Exploración

1. Tu robot tendrá **3 minutos (180 segundos) en total** para completar esta tarea.
    
    **Nota**: *El temporizador comenzará tan pronto como el robot empiece a moverse dentro del arena.*

1. El suelo del arena estará marcado en **16 zonas iguales** (cada una de 1 m x 1 m cuadrado). Se te otorgarán puntos por cada zona que tu robot entre dentro del tiempo disponible (excluyendo aquella en la que empieza).

    **Nota**: *Los puntos de exploración solo cuentan cuando el ^^cuerpo completo^^ del robot entra en la zona.*

1. Tu robot necesitará explorar con éxito mientras evita el contacto con *cualquier cosa* en el entorno.
    
    Cualquier contacto que el robot haga con el entorno se cuenta como un *"incidente"*. Una vez que haya ocurrido un incidente, moveremos el robot un poco para que pueda moverse nuevamente, pero después de que hayan ocurrido **cinco** incidentes la evaluación se detendrá, independientemente de cuánto tiempo haya transcurrido.

### Buscar una Baliza

Al igual que con las 2 tareas anteriores, lanzaremos los nodes de ROS desde dentro de tu paquete para esta tarea usando `ros2 launch` ([más detalles abajo](#launch)). Para esta, sin embargo, también suministraremos un argumento adicional cuando lo hagamos:

``` { .bash .no-copy }
ros2 launch ros2_lab_equipoXX task3.launch.py target_beacon:=COLOUR
```

...donde `COLOUR` será reemplazado por `yellow`, `red`, `green` o `blue` (siempre en minúsculas). Este color objetivo será seleccionado al azar. Basándose en esta entrada, tu robot necesitará capturar una imagen de la baliza de ese color.

Por lo tanto, necesitarás definir tu archivo de lanzamiento para acomodar el argumento de línea de comandos `target_beacon`. Además de esto, dentro de tu archivo de lanzamiento también *necesitarás* pasar el *valor* de esto a un node de ROS dentro de tu paquete, para que el node sepa qué baliza buscar realmente (es decir, la baliza *amarilla*, *roja*, *verde* o *azul*). Este tipo de funcionalidad de archivo de lanzamiento no se cubrió en la Asignación #1, pero [hay algunos recursos adicionales disponibles para ayudarte con esto](#advanced-launch-file-features).

<a name="arg_parsing"></a>

Al lanzar tu archivo de lanzamiento `task3.launch.py`, uno de tus nodes de ROS debe generar un Mensaje de Log para indicar el color especificado para la tarea de búsqueda. Este mensaje de log debe tener severidad `INFO` (es decir, usando una llamada al método `#!py get_logger().info()`), y debe generarse dentro de los 10 segundos de ejecutar tu archivo de lanzamiento. El mensaje debe estar formateado *exactamente* de la siguiente manera:

``` { .txt .no-copy }
TARGET BEACON: Searching for COLOUR.
```

...donde `COLOUR` debe reemplazarse con el color real que se pasó a tu archivo `task3.launch.py` (ya sea `yellow`, `red`, `green` o `blue`).

#### Guardar la Imagen

En la raíz de tu paquete debe haber un directorio llamado `snaps`, y la imagen debe guardarse en este directorio con el nombre de archivo: `target_beacon.jpg`, es decir:

``` { .txt .no-copy }
~/ros2_ws/src/ros2_lab_equipoXX/snaps/target_beacon.jpg
```

La imagen que se guarda aquí debe ser la *imagen sin procesar* de la cámara del robot, y no debe incluir ningún filtrado que puedas haber aplicado en post-procesamiento.

!!! warning "Ten en cuenta"
    
    [**Entendiendo los robots**: La Cámara y el Procesamiento de Imagen](../../../waffles/essentials.md#the-camera-and-image-processing). Hay algunas cosas clave que debes investigar aquí, como:
    
    * [ ] El nombre del topic de imagen de la cámara en los robots reales.
    * [ ] La resolución nativa de las imágenes de la cámara, y cómo esto podría afectar cualquier procesamiento de imagen que realices.

### Mapear el Entorno

También hay puntos disponibles en la Tarea 3 por usar SLAM para generar un mapa del entorno mientras tu robot explora, y guardar este mapa en el directorio de tu paquete (como una imagen).

#### Generar un Mapa

Uno de los primeros ejercicios que hiciste con los robots (¡en el laboratorio de la Semana 1!) fue [usar SLAM para crear un mapa del entorno](../../../waffles/basics.md#exSlam). También habrás intentado esto en simulación en la [Parte 3 de la Asignación #1](../../../course/part3.md#ex5). Nota que usaste el mismo archivo de lanzamiento en ambos casos, pero con una diferencia sutil:

=== "En el Mundo Real"

    ``` { .bash .no-copy }
    ros2 launch rigsa_tb3_tools slam.launch.py environment:=real
    ```

=== "En Simulación"

    ``` { .bash .no-copy }
    ros2 launch rigsa_tb3_tools slam.launch.py environment:=sim
    ```

... *¿cuál crees que podrías necesitar aplicar aquí?*

#### Guardar un Mapa

Piensa de nuevo en el [Ejercicio 5 de la Asignación #1 Parte 3](../../../course/part3.md#ex5) ahora, y en cómo pudiste guardar un mapa como imagen desde la línea de comandos usando una llamada `ros2 run`:

``` { .bash .no-copy }
ros2 run nav2_map_server map_saver_cli -f MAP_NAME
```

También es posible hacer esto *programáticamente* usando el framework de Servicios de ROS 2. Considera el [Ejercicio 6 de la Asignación #1 Parte 4](../../../course/part4.md#ex6) para ver cómo esto podría hacerse desde dentro de uno de tus nodes de ROS para la Tarea 3.

La raíz del directorio de tu paquete debe contener un directorio llamado `maps`, y el mapa que genera tu robot durante la exploración debe guardarse como una imagen `png` en este directorio con el nombre `arena_map.png`, es decir:

``` { .txt .no-copy }
~/ros2_ws/src/ros2_lab_equipoXX/maps/arena_map.png
```

## Ejecutar Tu Código {#launch}

El paquete de ROS de tu equipo debe contener un archivo de lanzamiento llamado `task3.launch.py`, de modo que (para la evaluación) podamos lanzar todos los nodes que hayas desarrollado para esta tarea mediante el siguiente comando:
  
``` { .bash .no-copy }
ros2 launch ros2_lab_equipoXX task3.launch.py target_beacon:=COLOUR
```
... donde `XX` será reemplazado con tu número de equipo y `COLOUR` será reemplazado por `yellow`, `red`, `green` o `blue`, por ejemplo:

=== "Yellow"

    ```bash
    ros2 launch ros2_lab_equipoXX task3.launch.py target_beacon:=yellow
    ```

=== "Red"

    ```bash
    ros2 launch ros2_lab_equipoXX task3.launch.py target_beacon:=red
    ```

=== "Green"

    ```bash
    ros2 launch ros2_lab_equipoXX task3.launch.py target_beacon:=green
    ```

=== "Blue"

    ```bash
    ros2 launch ros2_lab_equipoXX task3.launch.py target_beacon:=blue
    ```

!!! note
    ROS ya estará ejecutándose en el robot antes de que intentemos ejecutar tu archivo de lanzamiento, y [una *Sesión Zenoh* estará ejecutándose en la laptop, para permitir que los nodes que se ejecutan en la laptop se comuniquen con él](../../../waffles/launching-ros.md#step4).

### Características Avanzadas de Archivos de Lanzamiento

Como se discutió anteriormente, necesitarás poder hacer algunas cosas un poco más avanzadas con archivos de lanzamiento para esta tarea, como:

* Aceptar argumentos de línea de comandos.
* Pasar argumentos de línea de comandos a nodes de ROS.
* Lanzar otros archivos de lanzamiento y pasar argumentos de lanzamiento a estos también, para configurar su comportamiento.

Todo esto está cubierto en una sección adicional del Curso de ROS 2, mira aquí:

<center>[:material-file: Archivos de Lanzamiento (Avanzado)](../../../course/extras/launch-files.md){ .md-button target="_blank"}</center>

## Dependencias

Puedes hacer uso de bibliotecas de Python preexistentes o paquetes de ROS 2 en tu propio trabajo para la Asignación #2, pero **hay restricciones que debes conocer**. [Consulta aquí para más detalles sobre esto](../assessment.md#dependencies).

!!! info "Nav2"
    El uso de Nav2 *está* permitido para la Tarea 3, pero deberías **proceder con precaución** si optas por esto. [Consulta aquí para más detalles](./nav2.md).

## Marcación

Hay **40 puntos** disponibles para esta tarea en total, otorgados según los criterios descritos a continuación.

<center>

| Criterio | Puntos | Detalles |
| :--- | :---: | :--- |
| **A**: Exploración | 15/40 | Para esta tarea, el arena se dividirá en **dieciséis** zonas iguales. Se te otorgará 1 punto por cada zona que tu robot logre entrar, excluyendo aquella en la que empieza. El robot solo necesita entrar en cada zona una vez, pero **su cuerpo completo debe estar dentro del marcado de la zona** para recibir el punto asociado. |
| **B**: Una *'ejecución sin incidentes'* | 5/40 | Si tu robot completa la tarea (o transcurren los 180 segundos) sin hacer contacto con nada en el arena, se te otorgarán puntos completos aquí por una *ejecución sin incidentes*. Sin embargo, se te deducirá 1 punto por cada "incidente" único que ocurra durante la evaluación. Tu robot debe *al menos* salir de la zona en la que empieza para ser elegible para estos puntos y una vez que se hayan registrado cinco incidentes en total, la evaluación se detendrá. |
| **C**: Búsqueda de una Baliza | 15/40 | [Detalles adicionales abajo](#crit-c). |
| **D**: Mapeo del Entorno | 5/40 | [Detalles adicionales abajo](#crit-d). | 

</center>

### C: Búsqueda de una Baliza {#crit-c}

Hay **15 puntos** disponibles para el Criterio C.

<center>

| Criterio | Detalles | Puntos|
| :--- | :--- | :--- |
| **C1** | Al lanzar tu archivo de lanzamiento `task3.launch.py`, uno de tus nodes de ROS debe generar un Mensaje de Log para indicar el color objetivo **correcto** para la tarea de búsqueda. Este Mensaje de Log debe ocurrir dentro de los 10 segundos de ejecutar tu archivo de lanzamiento, estar [en el formato especificado aquí](#arg_parsing), y debe lograrse usando una llamada al método `#!py get_logger().info()`. | 2 |
| **C2** | Al final de la evaluación, un **único** archivo de imagen llamado `target_beacon.jpg` debe haberse obtenido de la cámara del robot (durante el transcurso de la evaluación). Este debe estar ubicado en una carpeta llamada `snaps` en la raíz del directorio de tu paquete: `~/ros2_ws/src/ros2_lab_equipoXX/snaps/target_beacon.jpg`. | 2 | 
| **C3** | Tu archivo de imagen `target_beacon.jpg` (en la ruta indicada arriba) contiene **cualquier parte** de la **baliza correcta**. | 3 |
| **C4** | Tu archivo de imagen `target_beacon.jpg` (en la ruta indicada arriba) ha capturado el **ancho completo** de la baliza correcta. | 3 |
| **C5** | Tu archivo de imagen `target_beacon.jpg` (en la ruta indicada arriba) ha capturado el **ancho completo** y **altura completa** de la baliza correcta, y la baliza está **completamente sin obstrucciones**. | 5 |

</center>

### D: Mapeo del Entorno {#crit-d}  

Hay **5 puntos** disponibles para el Criterio D.

<center>

| Criterio | Detalles | Puntos|
| :--- | :--- | :--- |
| **D1** | Un mapa de **cualquier parte** del arena robótico (por pequeña que sea) debe haberse generado *durante la evaluación*. Al final de la evaluación, deben existir dos archivos: un `png` y un `yaml`, ambos deben llamarse `arena_map`, y ambos deben estar ubicados en una carpeta `maps` en la raíz del directorio de tu paquete: `~/ros2_ws/src/ros2_lab_equipoXX/maps/arena_map.png` y `~/ros2_ws/src/ros2_lab_equipoXX/maps/arena_map.yaml`. | 2 |
| **D2** | Tu archivo `arena_map.png` (creado durante la evaluación y en la ruta indicada arriba) muestra todo el espacio libre/ocupado extendiéndose desde cualquiera de las paredes exteriores del arena hasta la pared exterior opuesta, sin interrupciones (es decir, sin regiones sin mapear), a través de cualquier parte del arena, con un ancho de al menos 0.5 metros. | 3 |   

</center>

## Recursos de Simulación

Al igual que con las Tareas 1 y 2, hay una simulación que puedes usar para desarrollar y probar el código de tu equipo.

!!! warning "Recuerda"
    
    * ¡El hecho de que funcione en simulación **NO** significa que funcionará igual de bien en el mundo real!
    * ¡Asegúrate de probar las cosas ^^a fondo^^ en los robots reales durante las sesiones de laboratorio!

Puedes lanzar la simulación desde el paquete `rigsa_task_sims` con el siguiente comando `ros2 launch`:

```bash
ros2 launch rigsa_task_sims explore.launch.py
```

<figure markdown>
  ![](../figures/explore.png){width=700px}
</figure>

Asegúrate de [revisar si hay actualizaciones al repositorio del curso](../../../course/extras/course-repo.md#updating) para garantizar que tengas la versión más actualizada de esto.

Una vez más, esto es solo un *ejemplo* de cómo podría verse el entorno del mundo real. Consulta las notas anteriores para [las diversas formas en que el entorno variará cuando esta tarea sea evaluada en el arena robótico real](#env-vars).

Además de esto, ten en cuenta que las balizas tendrán la misma forma, tamaño y color que las de la simulación, **pero** detectar colores es mucho más difícil en el mundo real que en la simulación, por lo que necesitarás hacer muchas pruebas en el mundo real para que esto funcione de manera robusta en el mundo real (tendrás acceso a todas las balizas durante las sesiones de laboratorio).
