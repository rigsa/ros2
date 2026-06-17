---
title: "Semana 8: Tu Primer Lab con Robot Real"
description: "Algunos ejercicios para ayudarte a conocer los robots reales y cómo funcionan"
---

## Conocer los Robots Reales

Esta tarea de asignación involucra trabajo extenso con nuestros robots reales, y por lo tanto tendrás acceso a los robots durante cada sesión de laboratorio a partir de la Semana 8. Todos los detalles sobre cómo funcionan los robots, cómo ponerlos en marcha y comenzar a programarlos se pueden encontrar en la sección "Waffles" de este sitio del curso (a la que llegaremos en un momento).

A cada equipo se le ha asignado una *"laptop de robótica"* específica (hay una lista en la plataforma del curso). El equipo docente te proporcionará un robot y la laptop de tu equipo al comienzo de la sesión de laboratorio.

!!! warning "Importante"
    * El robot y la laptop solo son accesibles durante las sesiones de laboratorio. Debes devolver todo el hardware al final del laboratorio.
    * Las sesiones de laboratorio empiezan en punto, y tienen **1 hora y 50 minutos** de duración. Debes asegurarte de que todo el hardware esté apagado y devuelto al personal docente **con prontitud** al final de la sesión de laboratorio (**a los 10 minutos para terminar la hora**). Sigue los procedimientos de apagado adecuados para apagar el hardware al final de cada sesión de laboratorio.

### Lista de Tareas para la Semana 8

Una vez que te hayan proporcionado tu robot y laptop, trabaja en cada página de [la sección "Waffles" de este sitio](../../waffles/README.md) (**en orden**) para familiarizarte con cómo funcionan:
   
* [ ] Lee sobre [el hardware](../../waffles/intro.md).
* [ ] Aprende cómo [lanzar ROS y poner los robots en marcha](../../waffles/launching-ros.md).
* [ ] Trabaja en los [Conceptos Básicos de Waffle (y ROS)](../../waffles/basics.md), que te ayudarán a comenzar y entender cómo funcionan ROS y los robots.
* [ ] Finalmente, revisa los [Procedimientos de Apagado](../../waffles/shutdown.md). Sigue estos pasos para apagar el robot y apagar la laptop de robótica al final de cada sesión de laboratorio.

## Transferir tu Paquete de ROS a las Laptops de Robótica

En la semana 6 habrás comenzado a desarrollar los algoritmos necesarios para esta tarea, y con suerte habrás empezado a probar las cosas en un mundo simulado. ¡El siguiente paso es hacer que las cosas funcionen en el robot real!

Habiendo familiarizado con cómo funcionan los robots (trabajando en los ejercicios anteriores), la siguiente tarea es instalar tu paquete en la laptop de robótica para probar tus algoritmos en el mundo real, y comenzar a depurar y optimizar.

Hay algunos métodos que podrías usar para copiar tu paquete de ROS en la laptop del robot; el más sencillo es usar una memoria USB, o subir tu código a Google Drive y luego descargarlo en la laptop[^git].

[^git]: Otra alternativa es usar Git y GitHub, pero esto requiere conocimiento de estas herramientas de software particulares. Si quieres seguir este enfoque, necesitarías convertir tu paquete de ROS en un repositorio git, publicarlo en GitHub y luego [consultar estas instrucciones para clonar tu paquete en las laptops de robótica](../../com/assignment2/ros-pkg-tips.md){target="_blank"}.

Hay un Espacio de Trabajo de ROS 2 en cada una de las laptops de robots (al igual que en el entorno WSL-ROS2), y tu paquete debe residir dentro del directorio `ros2_ws/src` (¡al igual que TODOS los paquetes que creaste a lo largo de los labs de simulación!)

La mejor manera de transferir tu paquete entre sistemas es como archivo `.tar`. Los siguientes pasos ilustran cómo hacerlo:

1. Desde tu instalación local de ROS (es decir, WSL-ROS2), ejecuta el comando `tar` para comprimir el paquete de tu equipo en un archivo `.tar`:

    ``` { .bash .no-copy }
    tar -cvf ~/ele_teamXX_2026.tar -C ~/ros2_ws/src/ ele_teamXX_2026
    ```
    
    ... ¡reemplazando `XX` con tu propio número de equipo, por supuesto!

    Esto creará un archivo `.tar` de tu paquete en tu directorio de inicio.

2. Si estás usando WSL-ROS2 (o cualquier otra instalación de ROS basada en WSL), puedes acceder a esto usando el Explorador de Archivos de Windows. En la terminal, introduce el siguiente comando:

    ```bash
    cd ~ && explorer.exe .
    ```

    Luego puedes copiar el archivo `ele_teamXX_2026.tar` a una ubicación portátil, que luego puedes transferir a la laptop del robot.

3. Copia el archivo `ele_teamXX_2026.tar` en la laptop de robótica, idealmente a la carpeta `Downloads`.

4. Abre una instancia de terminal en la laptop, ya sea usando el atajo de teclado ++ctrl+alt+t++, o haciendo clic en el ícono de la aplicación Terminal en la barra de favoritos del escritorio:
    
    <figure markdown>
      ![](../../images/laptops/terminal_icon.svg){width=60px}
    </figure>

5. Usa `cd` para navegar a la carpeta a la que copiaste tu archivo `ele_teamXX_2026.tar`, por ejemplo:

    ```bash
    cd ~/Downloads/
    ```

6. Luego, usa el comando `tar` nuevamente para extraer tu paquete de ROS en el Espacio de Trabajo de ROS2:

    ``` { .bash .no-copy }
    tar -xvf ele_teamXX_2026.tar -C ~/ros2_ws/src/
    ```

7. Sigue el proceso habitual de **tres pasos** de `colcon build`:
    
    1. Navega al Espacio de Trabajo de ROS2:

    ```bash
    cd ~/ros2_ws/ 
    ```

    1. Construye tu paquete:

    ``` { .bash .no-copy }
    colcon build --packages-select ele_teamXX_2026 --symlink-install 
    ```

    1. Y finalmente, no olvides recargar el entorno:

    ```bash
    source ~/.bashrc
    ```
