---
title: "Semana 12: Detalles de Entrega (y Requisitos Clave)"
description: "Cómo entregar tu paquete de ROS para la Asignación de Lab con Robot Real"
---

## Fecha Límite

La fecha límite para la entrega de tu paquete de ROS para esta tarea es **23:59 del viernes de la Semana 12**.

Debes entregar el paquete de ROS de tu equipo a través de la plataforma del curso, siguiendo los pasos descritos a continuación. Debes hacer **una entrega por equipo**, así que nomina a un miembro del equipo para hacer esto.

Tu paquete de ROS entregado será evaluado por el equipo docente fuera de línea durante el Período de Exámenes. Antes del final del período de exámenes recibirás tus puntos, más videos de la evaluación.

## Requisitos Clave

!!! warning
    ¡No cumplir con todos los requisitos listados en esta página podría resultar en **penalizaciones** aplicadas a tu calificación, o en que se te otorguen **cero puntos** para la tarea de la asignación!

Antes de entregar tu trabajo, **debes** asegurarte de que los siguientes *Requisitos Clave* se cumplan en cuanto a tu paquete de ROS:

* [ ] El nombre de tu paquete de ROS debe ser:

    ``` { .txt .no-copy }
    ele_teamXX_2026
    ```

    ... donde `XX` debe reemplazarse con tu número de equipo.

    <a name="build-files"></a>

* [ ] Tu paquete no debe contener **archivos de construcción** (`build/`, `install/`, `log/`) que se generarían como resultado de ejecutar `colcon build` desde dentro de tu paquete.

    !!! warning "Recuerda"
        **Siempre** ejecuta `colcon build` desde la **raíz** del espacio de trabajo de ROS (por ejemplo, `~/ros2_ws/`), para asegurarte de que todos los archivos de construcción se generen en la ubicación correcta en el sistema de archivos (`~/ros2_ws/build/`, `~/ros2_ws/install/`, `~/ros2_ws/log/`).

Para la evaluación de la tarea, tu paquete será construido y desplegado en una de las Laptops de Robótica con las que habrás estado trabajando durante las sesiones de laboratorio. Usaremos la cuenta de usuario `student` estándar, y tu paquete será descargado al directorio `~/ros2_ws/src/`.

* [ ] Debe ser posible construir tu paquete ejecutando el siguiente comando desde la raíz del Espacio de Trabajo de ROS 2 local, y esto debe construirse sin errores:
    
    ``` { .bash .no-copy }
    colcon build --packages-select ele_teamXX_2026
    ```

* [ ] Debes asegurarte de que exista un archivo de lanzamiento para la tarea y que este sea ejecutable (después de haber ejecutado el comando `colcon build` anterior) para que podamos lanzar tu trabajo de la siguiente manera[^launch-files]:
    
    [^launch-files]: Asegúrate de haber [definido un directorio `install` apropiado en el `CMakeLists.txt` de tu paquete](../../course/part3.md#ex1)

    ``` { .bash .no-copy }
    ros2 launch ele_teamXX_2026 explore.launch.py
    ```

    ... donde `XX` será reemplazado por tu número de equipo.

* [ ] Cualquier node dentro de tu paquete que sea ejecutado por los archivos de lanzamiento anteriores **debe** haber sido definido correctamente como ejecutable del paquete (es decir, en tu `CMakeLists.txt`) y también **debe** haber recibido el permiso de ejecución apropiado (es decir, con `chmod`).  

    !!! warning 
        ¡Depende de **ti** asegurarte de que tu código se lance según lo previsto para una tarea dada. Si no es así, se te otorgarán cero puntos, así que **asegúrate de probarlo todo antes de la entrega**!

## Otra Información Importante 

* El [Repositorio del Curso `rigsa_ros`](../../course/extras/course-repo.md) estará instalado y actualizado en la Laptop de Robótica que usemos para evaluar tu trabajo.

* La Laptop de Robótica que usemos para la evaluación será seleccionada al azar.

* Esta laptop habrá sido vinculada con un robot antes de que intentemos ejecutar tu entrega.

* El robot también será seleccionado al azar.

* Ya habremos [lanzado el *bringup* en el robot](../../waffles/launching-ros.md#step3), por lo que ROS estará funcionando y el robot estará listo para operar en el arena.

* [Una Sesión Zenoh ya estará funcionando en la laptop](../../waffles/launching-ros.md#step4) para conectarse al *Router* Zenoh del Robot, y **las comunicaciones habrán sido probadas** antes de que intentemos lanzar tu trabajo para cada tarea.

## Exportar tu Paquete de ROS para Entrega {#exporting-your-ros-package-for-submission}

Cuando llegue el momento de la entrega, es importante que sigas los pasos a continuación cuidadosamente para crear un archivo de tu paquete de ROS correctamente.

1. Desde tu instalación local de ROS (es decir, WSL-ROS2), ejecuta el comando `tar` para comprimir el paquete de tu equipo en un archivo `.tar`:

    ``` { .bash .no-copy }
    tar -cvf ~/ele_teamXX_2026.tar -C ~/ros2_ws/src/ ele_teamXX_2026
    ```
    
    ... ¡reemplazando `XX` con tu propio número de equipo, por supuesto!

    Esto creará un archivo `.tar` de tu paquete en tu directorio de inicio.

1. **Si estás haciendo esto desde dentro de WSL-ROS2 (es decir, en Windows)**, accede a esto usando el Explorador de Archivos de Windows. En la misma terminal que antes, introduce el siguiente comando para primero navegar al directorio de inicio, y luego lanzar el Explorador de Windows en esta ubicación:

    ```bash
    cd ~ && explorer.exe .
    ```

1. Debería abrirse una ventana del Explorador, y allí deberías poder ver el archivo `ele_teamXX_2026.tar` que acabas de crear. Cópialo y pégalo en algún lugar conveniente en tu máquina.

6. Entrega este archivo `.tar` a través de la plataforma del curso siguiendo las instrucciones que se te indiquen.
