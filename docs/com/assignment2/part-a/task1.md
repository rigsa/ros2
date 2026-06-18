---  
title: "Tarea 1: Control de Velocidad"
---  

Desarrolla una aplicación de ROS funcional para hacer que un *robot real del laboratorio* siga un perfil de movimiento prescrito, mientras imprime información clave en la terminal.

!!! success "Puntos de Control del Curso"
    
    Las siguientes partes del [Curso de ROS 2](../../assignment1.md) apoyarán tu trabajo en esta tarea:

    * [ ] **Parte 1**: en su totalidad.
    * [ ] **Parte 2**: hasta (e incluyendo) el [Ejercicio 5](../../../course/part2.md#ex5).
    * [ ] **Parte 3**: [Ejercicio 1](../../../course/part3.md#ex1).
    
    **Ver También** - [Entendiendo los robots](../../../waffles/essentials.md):
    
    * [ ] Control de Movimiento y Velocidad

## Resumen

El objetivo principal de esta tarea es crear un node de ROS (o múltiples nodes) que hagan que tu robot siga un patrón de **figura ocho** en el suelo del arena robótico. La trayectoria de figura ocho debe generarse siguiendo dos bucles, ambos de 1 metro de diámetro, como se muestra a continuación. <a name="fig-eight"></a>

<figure markdown>
  ![](../figures/task1_motion_path.png){width=400px}
  <figcaption>La trayectoria de figura ocho para la Tarea 1.</figcaption>
</figure>

El Arena Robótico estará configurado de la siguiente manera para esta tarea:

<figure markdown>
  ![](../figures/task1_arena_layout.jpg){width=500px}
  <figcaption>La configuración del Arena Robótico para la Tarea 1.</figcaption>
</figure>

Mientras haces esto, también necesitarás presentar datos de odometría del robot en la terminal a intervalos regulares ([ver abajo para los detalles específicos](#details)). Tu node debe generar estos datos como Mensajes de Log de ROS 2 con severidad `INFO`, es decir, usando llamadas `#!py get_logger().info()` dentro de uno de tus nodes. Los mensajes de log se usan en muchos de los ejercicios y el código de ejemplo a lo largo de la Asignación #1, por lo que debes consultarlos para orientación si lo necesitas.

Además, para esta tarea, los mensajes de log deben estar *formateados* de una manera particular, por lo que quizás quieras consultar la documentación sobre [Formato de Cadenas de Python](https://docs.python.org/3/tutorial/inputoutput.html){target="_blank"}, y leer los detalles a continuación cuidadosamente para saber qué se espera.

## Detalles

1. "**Bucle 1**": El robot debe comenzar moviéndose en sentido **antihorario**, siguiendo una trayectoria de movimiento circular de 1 m de diámetro alrededor de la baliza roja [como se muestra arriba](#fig-eight).
1. "**Bucle 2**": Una vez que el robot haya regresado al punto de partida, debe girar en sentido **horario** para seguir una segunda trayectoria circular, también de 1 m de diámetro, esta vez alrededor de la baliza azul.
1. Después del Bucle 2, el robot debe detenerse en la línea de inicio/fin (:material-plus-minus:10 cm, como indica el marcado en el suelo).
1. La velocidad del robot debe definirse para asegurar que toda la secuencia tome **60 segundos** en completarse (:material-plus-minus:5 segundos).

    **Nota**: *El temporizador comenzará tan pronto como el robot empiece a moverse*.

1. La pose en tiempo real del robot debe imprimirse en la terminal durante todo el proceso, donde los mensajes deben tener el siguiente formato (**exactamente**): <a name="msg-format"></a>
	
    ``` { .txt .no-copy }
    x={x} [m], y={y} [m], yaw={yaw} [degrees].
	```

	Donde `{x}`, `{y}` y `{yaw}` deben reemplazarse con los datos de odometría en tiempo real correctos de la siguiente manera:
	
	1. `{x}`: la posición lineal del robot en el eje X, citada en metros a **dos decimales**.
    1. `{y}`: la posición lineal del robot en el eje Y, citada en metros a **dos decimales**.
	1. `{yaw}`: la orientación del robot alrededor del eje Z, citada en grados a **un decimal**.
	
	Los datos deben citarse relativos a su posición de inicio al comienzo de la tarea, por ejemplo, al inicio de la tarea (antes de que el robot se haya movido) los mensajes de la terminal deben decir:

    ``` { .txt .no-copy }
    x=0.00 [m], y=0.00 [m], yaw=0.0 [degrees].
    ```
	
	Estos mensajes deben imprimirse en la terminal **a una tasa de 1Hz**. No importa si los mensajes continúan imprimiéndose en la terminal después de que el robot se haya detenido (es decir, después de que la figura ocho se haya completado).

    !!! warning "Importante"
        Debes usar llamadas al método `#!py get_logger().info()` dentro de tu node para imprimir estos mensajes en la terminal.

### Una nota sobre la Odometría

Cuando el robot se coloca en el arena al inicio de la tarea **su odometría puede no ser necesariamente cero**, por lo que necesitarás compensar esto. Por lo tanto, deberás obtener la pose del robot del topic `/odom` antes de que tu robot empiece a moverse, y luego usarla como referencia cero para convertir todas las lecturas de odometría posteriores que obtengas a lo largo de la tarea.

La odometría y el seguimiento de la *pose* del robot se discuten en detalle en la [Asignación #1 Parte 2](../../../course/part2.md).

## Ejecutar Tu Código {#launch}

Al evaluar tu código para esta tarea, el equipo docente usará el siguiente comando para ejecutar toda la funcionalidad necesaria desde dentro de tu paquete:
	 
``` { .bash .no-copy }
ros2 launch ros2_lab_equipoXX task1.launch.py
```

... donde `XX` será reemplazado con *tu número de equipo*.

Por lo tanto, tus Nodes de ROS 2 para la Tarea 1 **DEBEN** ser ejecutables a través de un archivo de lanzamiento, y este archivo de lanzamiento **DEBE** llamarse `task1.launch.py`.

!!! note
    ROS ya estará ejecutándose en el robot antes de que intentemos ejecutar tu archivo de lanzamiento, y [una *Sesión Zenoh* estará ejecutándose en la laptop, para permitir que tus nodes (ejecutándose en la laptop) se comuniquen con él](../../../waffles/launching-ros.md#step4). No necesitas incluir nada de esto en la descripción de lanzamiento de tu `task1.launch.py`.

## Marcación

Esta tarea será evaluada por el equipo docente como parte de la Parte A (es decir, junto con la [Tarea 2](./task2.md)).

Hay **20 puntos** disponibles para esta tarea en total, resumidos de la siguiente manera:

<center>

| Criterio | Puntos | Detalles |
| :--- | :---: | :--- |
| **A**: La Trayectoria de Movimiento | 10/20 | Qué tan de cerca el robot real sigue *una verdadera trayectoria de figura ocho* en el arena robótico, basado en [la tabla de criterios a continuación](#criterion-a-the-motion-path). |
| **B**: Mensajes de Terminal | 10/20 | El formato correcto de tus mensajes de odometría, y la validez de los datos que se presentan en la terminal mientras el robot realiza la tarea, basado en [la tabla de criterios a continuación](#criterion-b-terminal-messages). |

</center>

### Criterio A: La Trayectoria de Movimiento

**Puntos:** 10/20

<center>

| Criterio | Detalles | Puntos|
| :--- | :--- | :--- |
| **A1**: Dirección de desplazamiento | El robot debe moverse en sentido antihorario para el primer bucle ("Bucle 1") y luego en sentido horario para el segundo ("Bucle 2"). | 2 |
| **A2**: Bucle 1 | El bucle debe ser de 1 m de diámetro, centrado alrededor de la baliza roja. | 2 |
| **A3**: Bucle 2 | El bucle debe ser de 1 m de diámetro, centrado alrededor de la baliza azul. | 2 |
| **A4**: Parada | Una vez que el robot complete su figura ocho, debe detenerse con ambas ruedas **dentro de los 10 cm** de la línea de inicio (como indica el marcado en el suelo). | 2 |
| **A5**: Temporización | El robot debe completar la figura ocho completa y detenerse en 55-65 segundos. | 2 |

</center>

### Criterio B: Mensajes de Terminal

**Puntos:** 10/20

<center>

| Criterio | Detalles | Puntos|
| :--- | :--- | :--- |
| **B1**: Tasa | Los mensajes deben imprimirse en la terminal **a una tasa de 1 Hz**. | 2 |
| **B2**: Formato | Los mensajes impresos en la terminal deben estar formateados **exactamente** [como se detalla arriba](#msg-format), y deben presentarse como Mensajes de Log de ROS 2 con severidad `INFO` (es decir, usando llamadas al método `#!py get_logger().info()`). | 2 |
| **B3**: Datos | Cada valor del mensaje (`x`, `y` y `yaw`) debe ser plausible, es decir: representar la pose real del robot en todos los puntos a lo largo de la figura ocho, basándose en que todas las lecturas se establezcan en cero en la línea de inicio/fin ([como se ilustra arriba](#fig-eight)). Además, cada valor debe citarse en las unidades correctas (metros / grados, según corresponda). | 6 |

</center>

## Recursos de Simulación

Podría resultarte útil desarrollar la funcionalidad principal para esta tarea en simulación antes de ejecutar las cosas en el robot real.

!!! warning "Mundo Real vs. Simulación"

    **¡No hay sustituto para las pruebas en el mundo real!**

    Aunque podrías desarrollar una aplicación de ROS que funcione perfectamente en simulación, esto no significa que funcione igual de bien en el mundo real.

    En última instancia, esta tarea (y de hecho todas las demás tareas de programación de la Asignación #2) será evaluada en robots reales, así que aprovecha al máximo las sesiones de laboratorio y **prueba las cosas en los robots reales ^^a fondo^^**.

[Como se muestra arriba](#fig-eight), para la evaluación habrá balizas cilíndricas colocadas en el centro de cada uno de los bucles de la figura ocho alrededor de las cuales el robot deberá moverse mientras completa la tarea. Por lo tanto, también hemos creado un entorno de simulación que es representativo del entorno del mundo real. Este está disponible en el paquete `rigsa_task_sims`, que es parte del Repositorio del Curso `rigsa_ros`. Las instrucciones para descargarlo e instalarlo dentro de tu propia instalación local de ROS están [disponibles aquí](../../../course/extras/course-repo.md).

Si ya lo has instalado (quizás como parte de la Asignación #1), vale la pena asegurarse de tener la versión más actualizada ([como se discute aquí](../../../course/extras/course-repo.md#updating)).

Una vez que hayas hecho todo esto, deberías poder lanzar la simulación usando `ros2 launch` de la siguiente manera:

```bash
ros2 launch rigsa_task_sims fig_of_eight.launch.py
```

<figure markdown>
  ![](../figures/task1.png)
  <figcaption>Un entorno de simulación para representar la configuración del arena robótico para la Tarea 1.</figcaption>
</figure>

!!! note
    Los marcadores de bucle son *ilustrativos*, no habrá ninguno en el suelo del arena robótico real durante la evaluación.
