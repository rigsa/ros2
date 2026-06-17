---
title: "La Tarea de la Asignación"
description: "Detalles de la tarea de Exploración en el Mundo Real y los criterios de calificación"
---

## Exploración en el Mundo Real

Desarrolla los nodes de ROS para permitir que un TurtleBot3 Waffle explore de manera autónoma un **entorno del mundo real** que contiene varios obstáculos. ¡El robot debe explorar la mayor parte del entorno posible en 90 segundos sin chocar contra nada!

Esta tarea se evalúa en un entorno del mundo real, **^^NO^^ en simulación**.

!!! success "Entendiendo los Waffles"
    
    Por favor asegúrate de haber leído y entendido las siguientes secciones de la página [**"Entendiendo los Waffles"**](../../waffles/essentials.md), para asegurarte de estar completamente al tanto de cómo funcionan los robots reales:

    * [ ] Control de Movimiento y Velocidad
    * [ ] Lecturas de Desplazamiento Láser y el Sensor LiDAR

## Descripción General

La Parte 3 del Curso de Lab de Simulación te introduce a [el sensor LiDAR del Waffle](../../course/part3.md#lidar). Este sensor es muy útil, ya que nos dice la distancia a cualquier objeto presente en el entorno del robot. Debes usar esto como base de los algoritmos de exploración y evasión de obstáculos que desarrolles para esta tarea.

Sin embargo, ten en cuenta que el LiDAR puede generar puntos de datos *fuera de rango*, que necesitarán ser filtrados. Considera la Página *"Entendiendo los Waffles"* (vinculada arriba) así como el Ejercicio 4 de la Parte 3 ("[Construyendo una Función de Callback LaserScan](../../course/part3.md#ex4)") para formas de abordar esto. También es posible que quieras segmentar el arreglo `ranges` para poder enfocarte en algunas zonas clave alrededor del robot (por ejemplo, adelante, adelante-izquierda, adelante-derecha), y considerar los inputs/estados clave que podrías observar para diferentes escenarios en el arena y qué acciones tomar...

Algunos conceptos introducidos en las clases del curso también podrían adoptarse para esto. Por ejemplo, la *Máquina de Estado Finito* define explícitamente las acciones a tomar para ciertos inputs y el estado actual. También podrías considerar los *Campos de Potencial Artificial* que mapean directamente los movimientos del robot a su posición relativa con los obstáculos.

La solución para la última pregunta del Tutorial de la Unidad 1 (Robótica de Enjambre) también puede ser útil. Aquí, se discutió una máquina de estado finito de caminata aleatoria, que podría usarse como estrategia de evasión de obstáculos y exploración.

Estos también podrían integrarse con otras estrategias para un mejor rendimiento, por ejemplo, el *seguimiento de paredes* o la *búsqueda en espiral*.

¡Pero en última instancia, ¡depende de ti!

## Detalles

El entorno que tu robot necesitará explorar para esto será el Arena Robótico, que es un arena cuadrada de 4x4m. Para la tarea, el arena contendrá varios *"obstáculos"*, es decir: paredes cortas de madera y cilindros de colores. Tu robot necesitará poder detectar estos obstáculos y navegar alrededor de ellos para explorar completamente el espacio.

<figure markdown>
  ![](../../com/assignment2/figures/task2_arena_layout.png){width=600px}
  <figcaption>La configuración del Arena Robótico para esta tarea.</figcaption>
</figure>

Este es un *ejemplo* de cómo podría verse el entorno del mundo real. **TODOS** los objetos (es decir, los cuatro cilindros de colores y los cuatro conjuntos de paredes de madera interiores) podrían estar en *posiciones completamente diferentes*. ¡Las paredes de madera *pueden no estar tocando los bordes exteriores del arena*! Las únicas cosas que permanecerán iguales son el tamaño del arena, la ubicación de las paredes exteriores del arena y el diseño del suelo (es decir, la ubicación de las zonas de exploración).

1. El robot comenzará en el centro del arena, perpendicular a una de las cuatro paredes *exteriores* del arena.
1. Debe explorar el entorno durante **90 segundos** sin tocar **ninguna** de las paredes del arena ni los obstáculos dentro de él.

    **Nota**: *El temporizador de 90 segundos comenzará tan pronto como el robot empiece a moverse dentro del arena.*

1. Si el robot hace contacto con **cualquier cosa** antes de que haya transcurrido el tiempo, la evaluación se detendrá y el tiempo registrado para la calificación.

    Si el robot funciona durante *más de* 90 segundos, solo consideraremos lo que sucede hasta la marca de los 90 segundos. Cualquier cosa que ocurra después de este punto no afecta las calificaciones.

1. El suelo del arena se dividirá en 16 zonas iguales y el robot debe entrar en tantas de las **12 zonas exteriores** como sea posible durante el intento.

1. El robot debe estar en movimiento durante toda la duración de la tarea. ¡Simplemente girar sobre sí mismo durante todo el tiempo no cuenta!

    * Lo que queremos ver aquí es que el robot está haciendo constantemente un esfuerzo por explorar.
    * Sin embargo, está bien que el robot se detenga y gire sobre sí mismo durante unos segundos cuando sea necesario.
    * Si el robot explora durante un tiempo y luego se detiene y no se mueve durante el resto de los 90 segundos, los puntos de *Tiempo de Ejecución* se otorgarán hasta el punto en que el robot dejó de estar activo.
    * Los detalles adicionales sobre la elegibilidad para los puntos de *Tiempo de Ejecución* se proporcionan en [la Sección de Calificación a continuación](#marking).

### Característica Avanzada: Cartografía con SLAM

Se otorgan puntos adicionales si, mientras tu robot está completando esta tarea, también puedes ejecutar SLAM y generar un mapa del entorno en segundo plano.

Para lanzar SLAM en los robots reales debes usar:

``` bash
ros2 launch tuos_tb3_tools slam.launch.py environment:=real
```

En la [sección "Extras" del Curso de ROS 2](../../course/extras/launch-files.md#launching-launch-files-from-launch-files) discutimos cómo usar archivos de lanzamiento para lanzar *otros* archivos de lanzamiento. ¡Considera cómo podrías adoptar un enfoque similar para ejecutar SLAM desde tu propio archivo `explore.launch.py`!

Cuando se trate de guardar el mapa que ha sido generado por SLAM, lo hicimos desde la línea de comandos en el Ejercicio 5 de la Parte 3, usando el siguiente comando:

``` { .bash .no-copy }
ros2 run nav2_map_server map_saver_cli -f MAP_NAME
```

Sin embargo, también es posible hacer esto *programáticamente* usando el framework de Servicios de ROS 2. Por lo tanto, necesitarás trabajar a través de la [Parte 4 del Curso de Lab de Simulación](../../course/part4.md) si quieres saber cómo se puede hacer esto.

Para obtener los puntos por esta *característica avanzada* de la tarea, la raíz de tu directorio de paquete `ele_teamXX_2026` debe contener un directorio llamado `maps`, y el archivo de mapa que obtienes debe guardarse en este directorio con el nombre: `explore_map.png`.

### Ejecutar Tu Código {#launch}

El paquete de ROS que entregas debe contener un archivo de lanzamiento llamado `explore.launch.py`, de modo que la funcionalidad que desarrolles para esta tarea pueda lanzarse desde tu paquete mediante el comando:

``` { .bash .no-copy }
ros2 launch ele_teamXX_2026 explore.launch.py
```

Para más información sobre el proceso de entrega y preparar tu paquete para la entrega [consulta aquí](./submission.md).

!!! note "Notas"

    * ROS ya estará ejecutándose en el robot antes de que intentemos ejecutar tu archivo de lanzamiento.
    
    * [Una *Sesión Zenoh* estará ejecutándose en la laptop, para permitir que los nodes que se ejecutan en la laptop se comuniquen con él](../../waffles/launching-ros.md#step4).

    * La ubicación, orientación y cantidad de obstáculos en el arena no se revelarán de antemano, por lo que el paquete de ROS que desarrolles necesitará ser capaz de acomodar un entorno desconocido.

### Dependencias

Puedes hacer uso de cualquier biblioteca de Python preexistente o paquete de ROS 2 para esta tarea **siempre que estén preinstalados en el entorno WSL-ROS2**. El entorno WSL-ROS2 es equivalente a la configuración de software en el hardware robótico real, por lo que cualquier paquete que exista en uno también existirá en el otro.

!!! danger "Nota"
    ¡No podrás solicitar que se instalen *bibliotecas/paquetes adicionales*!

## Calificación {#marking}

La entrega de cada equipo será evaluada **tres veces** para esta tarea. El robot siempre comenzará en el centro del arena, pero su orientación será diferente para cada ejecución individual. La orientación del robot siempre será perpendicular a las paredes exteriores del arena y la disposición del arena será la misma cada vez también.

Hay **25 puntos** disponibles para esta tarea (por ejecución), como se describe en la tabla a continuación.

<center>

| Criterio | Puntos | Detalles |
| :--- | :---: | :--- |
| **A**: Exploración | 12/25 | Se te otorgará 1 punto por cada una de las 12 zonas exteriores del arena que el robot logre entrar (es decir, excluyendo las cuatro zonas en el centro). El robot solo necesita entrar en cada una de las 12 zonas una vez por ejecución, pero **su cuerpo completo debe estar dentro del marcado de la zona** para recibir el punto. |
| **B**: Tiempo de Ejecución | 8/25 | Se te otorgarán puntos por la cantidad de tiempo que tu robot pase explorando el entorno antes de que transcurran los 90 segundos, **O** el robot haga contacto con cualquier cosa en su entorno ([según la tabla a continuación](#run-time)). **El robot debe salir de la zona roja central** (un área de 1x1m) para ser elegible para cualquiera de estos puntos. Si el robot no explora más allá de **la zona naranja central**, se aplicará un factor de multiplicación de $0.5\times$ a los puntos de tiempo de ejecución. |
| **C**: Cartografía con SLAM | 5/25 | [Detalles adicionales abajo](#map-marks). |

</center>

La calificación general final otorgada a cada equipo se basará en los puntos obtenidos para cada una de las tres ejecuciones, pero con una ponderación aplicada a cada una:

* **60% de ponderación**: aplicada a la ejecución que obtuvo la calificación **más alta**
* **10% de ponderación**: aplicada a la ejecución que obtuvo la calificación **más baja**
* **30% de ponderación**: aplicada a la puntuación de la ejecución restante

Por ejemplo, si tu equipo obtiene puntuaciones de $\frac{23}{25}$, $\frac{8}{25}$ y $\frac{12}{25}$ de las ejecuciones 1, 2 y 3 respectivamente, entonces la calificación general final será:

$$
(23\times0.6)+(12\times0.3)+(8\times0.1)=\frac{18.2}{25} (73\%)
$$

### Criterio B: Tiempo de Ejecución {#run-time}

**Puntos:** 8/25

Los puntos se otorgarán de la siguiente manera:

<center>

| Tiempo (Segundos) | Puntos |
| :---: | :---: |
| 0-9 | 0 |
| 10-19 | 1 |
| 20-29 | 2 |
| 30-39 | 3 |
| 40-49 | 4 |
| 50-59 | 5 |
| 60-89 | 6 |
| ¡Los 90 completos! | 8 |

</center>

### Criterio C: Cartografía con SLAM {#map-marks}  

**Puntos:** 5/25

<center>

| Criterio | Detalles | Puntos|
| :--- | :--- | :--- |
| **C1** | Al final de la evaluación, un mapa del arena robótico (o cualquier parte de él) debe haberse generado. Deben existir dos archivos: un `.png` y un `.yaml`, ambos deben llamarse `explore_map`, y ambos deben estar ubicados en una carpeta `maps` en la raíz del directorio de paquete de tu equipo, es decir, `ele_teamXX_2026/maps/explore_map.png` y `ele_teamXX_2026/maps/explore_map.yaml`. | 2 |
| **C2** | El mapa `ele_teamXX_2026/maps/explore_map.png` que se crea *durante la evaluación* muestra **alguna parte** del arena robótico real. | 3 |   

</center>
