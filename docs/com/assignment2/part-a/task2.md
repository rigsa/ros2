---  
title: "Tarea 2: Evasión de Obstáculos" 
---  

Desarrolla los nodes de ROS para permitir que un TurtleBot3 Waffle real explore de manera autónoma un entorno que contiene varios obstáculos. ¡El robot debe explorar la mayor parte del entorno posible en 90 segundos sin chocar contra nada!

!!! success "Puntos de Control del Curso"
    
    Aspira a haber completado **hasta e incluyendo la [Parte 3 de la Asignación #1](../../../course/part3.md)** para apoyar tu trabajo en esta tarea.

    **Ver También** - [Entendiendo los Waffles](../../../waffles/essentials.md):
    
    * [ ] Control de Movimiento y Velocidad
    * [ ] Lecturas de Desplazamiento Láser y el Sensor LiDAR 

## Resumen

La Asignación #1 Parte 3 introduce [el sensor LiDAR del Waffle](../../../course/part3.md#lidar). Este sensor es muy útil, ya que nos dice la distancia a cualquier objeto presente en el entorno del robot. En la [Asignación #1 Parte 5](../../../course/part5.md#explore) veremos cómo estos datos, en combinación con el *framework de Acciones de ROS*, pueden usarse como base para una estrategia de exploración básica que incorpora evasión de obstáculos. Ampliando esto en el [Ejercicio 6 de la Parte 5](../../../course/part5.md#ex6), discutimos cómo esto podría desarrollarse más creando un *cliente* de acción que pudiera hacer llamadas sucesivas al servidor de acción para mantener el robot moviéndose aleatoriamente, e indefinidamente, por un arena mientras evita obstáculos.

Este es un enfoque que podrías usar para esta tarea, pero también hay otras formas (y potencialmente más simples) de lograrlo.

Otro aspecto de esta tarea es la *exploración*: tu robot recibirá más puntos por navegar por más partes del entorno. Considera las estrategias de búsqueda como el *"Movimiento Browniano"* y los *"Paseos de Lévy"*. ¿Podría implementarse algo a lo largo de estas líneas en el Waffle?

## Detalles

El Arena Robótico es un arena cuadrada de 4x4m. Para la tarea, el arena contendrá varios *"obstáculos"*, es decir: paredes cortas de madera y cilindros de colores. Tu robot necesitará poder detectar estos obstáculos y navegar alrededor de ellos para explorar completamente el espacio.

Los puntos de exploración se otorgarán cuando el robot entre en cada una de las 12 zonas exteriores del arena (cada una de 1x1m cuadrado), como se muestra a continuación.

<a name="cr5-layout"></a>
<figure markdown>
  ![](../figures/task2_arena_layout.png){width=600px}
  <figcaption>La configuración del Arena Robótico para la Tarea 2.</figcaption>
</figure>

<a name="env-vars"></a>

!!! danger "Importante"
    Este es un *ejemplo* de cómo podría verse el entorno:
    
    * **TODOS** los objetos (es decir, los cuatro cilindros de colores y los cuatro conjuntos de paredes) podrían estar en *posiciones completamente diferentes*.
    * ¡Las paredes de madera *pueden no estar tocando los bordes exteriores del arena*!
    * Los cilindros de colores *podrían* estar dentro de zonas de exploración.
    * Las únicas cosas que permanecerán iguales son el tamaño del arena, la presencia de las paredes exteriores del arena y el diseño del suelo (es decir, la ubicación de todas las zonas).

1. El robot comenzará en el centro del arena, perpendicular a una de las cuatro paredes exteriores.
1. Debe explorar el entorno durante 90 segundos sin tocar **ninguna** de las paredes del arena ni los obstáculos dentro de él.

    **Nota**: *El temporizador de 90 segundos comenzará tan pronto como el robot empiece a moverse dentro del arena.*

1. Si el robot hace contacto con **cualquier cosa** antes de que haya transcurrido el tiempo, el intento termina, y este tiempo se registrará para determinar una marca de *"Tiempo de Ejecución"* ([ver abajo](#run-time)).
1. Como se muestra arriba, el suelo del arena estará marcado con 12 zonas iguales (1x1m) y el robot debe entrar en tantas de estas 12 **zonas de exploración** como sea posible durante el intento.
1. El robot debe estar en movimiento durante toda la duración de la tarea. ¡Simplemente girar sobre sí mismo durante todo el tiempo no cuenta!

    * Lo que queremos ver aquí es que el robot está haciendo constantemente un esfuerzo por explorar.
    * Sin embargo, está bien que el robot se detenga y gire sobre sí mismo durante unos segundos cuando sea necesario.
    * Si el robot explora durante un tiempo y luego se detiene y no se mueve durante el resto de los 90 segundos, los puntos de *Tiempo de Ejecución* se otorgarán hasta el punto en que el robot dejó de estar activo.
    * Los detalles adicionales sobre la elegibilidad para los puntos de *Tiempo de Ejecución* se proporcionan en [la Sección de Marcación a continuación](#marking).

## Ejecutar Tu Código {#launch}

Al evaluar tu código para esta tarea, el equipo docente usará el siguiente comando para ejecutar toda la funcionalidad necesaria desde dentro del paquete de ROS 2 de tu equipo:

```bash
ros2 launch ros2_lab_equipoXX task2.launch.py
```

... donde `XX` será reemplazado con *tu número de equipo*.

Por lo tanto, el paquete de ROS 2 que tu equipo entregue debe contener un archivo de lanzamiento llamado `task2.launch.py`, para ejecutar toda la funcionalidad necesaria dentro de tu paquete para esta tarea.

!!! note
    ROS ya estará ejecutándose en el robot antes de que intentemos ejecutar tu archivo de lanzamiento, y [una *Sesión Zenoh* estará ejecutándose en la laptop, para permitir que los nodes que se ejecutan en la laptop se comuniquen con él](../../../waffles/launching-ros.md#step4).

## Dependencias

Puedes hacer uso de bibliotecas de Python preexistentes o paquetes de ROS 2 en tu propio trabajo para la Asignación #2, pero **hay restricciones que debes conocer**. [Consulta aquí para más detalles sobre esto](../assessment.md#dependencies).

!!! failure "Nav2"
    Además de lo anterior, **el uso de [Nav2](https://docs.nav2.org/){target="_blank"} ^^no está permitido^^ para esta tarea**.

## Marcación

Hay **20 puntos** disponibles para la Tarea 2 en total, otorgados de la siguiente manera:

<center>

| Criterio | Puntos | Detalles |
| :--- | :---: | :--- |
| **A**: Tiempo de Ejecución | 8/20 | Se te otorgarán puntos por la cantidad de tiempo que tu robot pase explorando el entorno antes de que transcurran los 90 segundos, **O** hasta que el robot haga contacto con algo en su entorno por primera vez ([según la tabla a continuación](#run-time)). **El robot debe salir de la zona central** (un cuadro de 1x1m, indicado en rojo [en la figura anterior](#cr5-layout)) para ser elegible para cualquiera de estos puntos. Si el robot no explora más allá de **la zona de "exploración parcial"** (indicada en naranja en la figura) se aplicará un factor de multiplicación de $0.5\times$ a los puntos de tiempo de ejecución. |
| **B**: Exploración | 12/20 | Se te otorgará 1 punto por cada una de las 12 zonas de exploración que el robot logre entrar. El robot solo necesita entrar en cada una de las 12 zonas una vez, pero su cuerpo completo debe estar dentro del marcado de la zona para obtener el punto. |

</center>

### Criterio A: Tiempo de Ejecución {#run-time}

**Puntos:** 8/20

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

## Recursos de Simulación

Dentro del paquete `tuos_task_sims` hay un arena de ejemplo que puede usarse para desarrollar y probar los nodes de evasión de obstáculos de tu equipo para esta tarea[^update-course-repo]. [Como se indicó arriba](#env-vars), sin embargo, esto es solo un *ejemplo* de cómo podría verse el entorno del mundo real.

[^update-course-repo]: Asegúrate de [revisar si hay actualizaciones al Repositorio del Curso](../../../course/extras/course-repo.md#updating) para garantizar que tengas la versión más actualizada de estas simulaciones.

La simulación puede lanzarse usando el siguiente comando `ros2 launch`:

```bash
ros2 launch tuos_task_sims obstacle_avoidance.launch.py
```

<figure markdown>
  ![](../figures/task2.png)
  <figcaption>Un entorno de simulación para representar la configuración del arena robótico para la Tarea 2.</figcaption>
</figure>

!!! danger "Recuerda"
    
    **Configuración del Arena**:
    
    * [Como se indicó arriba](#env-vars), esto es un *ejemplo* de cómo podría verse el entorno.
    * **TODOS** los objetos (es decir, los cuatro cilindros de colores y los cuatro conjuntos de paredes) podrían estar en *posiciones completamente diferentes*.
    * ¡Las paredes de madera *pueden no estar tocando los bordes exteriores del arena*!
    * Los cilindros de colores *podrían* estar dentro de zonas de exploración.
    * Las únicas cosas que permanecerán iguales son el tamaño del arena, la presencia de las paredes exteriores del arena y el diseño del suelo (es decir, la ubicación de todas las zonas).
    
    **Mundo Real vs. Simulación**:

    * **¡El hecho de que funcione en simulación ^^NO^^ significa que funcionará en el mundo real!**
    * ¡Asegúrate de probar las cosas ^^a fondo^^ en los robots reales durante las sesiones de laboratorio!
