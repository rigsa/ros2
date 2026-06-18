---
title: Información y Requisitos Clave de Evaluación
---

!!! warning
    ¡No cumplir con todos los requisitos listados en esta página podría resultar en **penalizaciones** aplicadas a tu calificación, o en **cero puntos** otorgados para un punto de entrega y/o tarea de la asignación!

Tu paquete de ROS debe estar alojado en GitHub, configurado como repositorio privado, y debes haber agregado a los colaboradores del equipo docente.

Además de esto, [debes haber registrado tu paquete con el equipo docente](./getting-started.md#pkg-reg), para que sepamos dónde encontrarlo en las fechas límite de entrega.

Todo lo anterior fue cubierto en [la sección de Primeros Pasos](./getting-started.md), que debías haber completado en el Lab de la Semana 1.

Habiendo completado todo esto *exitosamente*, podremos obtener tu paquete en cada una de las fechas de entrega para que el trabajo de Asignación #2 de tu equipo pueda ser evaluado. ¡Si *no* has completado todo esto, podrías recibir cero puntos!

!!! note "Confirmación :wave:"
    En algún momento dentro de las primeras semanas del curso se enviará un archivo `hello.md` a tu repositorio para confirmar que ha sido registrado correctamente.

## Puntos de Entrega

[Como se discute aquí](./README.md#the-tasks), hay **dos puntos de entrega** para la Asignación #2 y **cuatro tareas** que completar en total:

<center>

| Parte | Tareas | Puntos<br />(/100) | Entrega |
| :---: | :---  | :---: | :---: |
| **A** | **Tareas 1 y 2** | 40 | Viernes de la Semana 6 a las 6pm |
| **B** | **Tarea 3 y Viva de Equipo** | 60 | Viernes de la Semana 12 a las 6pm |

</center>

Consulta las páginas de cada tarea para ver los detalles completos.

## Dependencias

Puedes hacer uso de cualquier biblioteca de Python preexistente o paquete de ROS 2 en tu propio trabajo para la Asignación #2 **siempre que estén preinstalados en el hardware robótico real** (es decir, las laptops Linux en el laboratorio). El entorno WSL-ROS2 es equivalente a la configuración de software en el hardware robótico real, por lo que cualquier paquete que exista en uno también existirá en el otro.

!!! danger "Nota"
    No podrás solicitar que se instalen *bibliotecas/paquetes adicionales*.

## Requisitos Clave

Además de registrar tu paquete correctamente (como se indicó arriba), **debes** asegurarte también de que los siguientes *Requisitos Clave* se cumplan para cada uno de los puntos de entrega (**A** y **B**):

* [ ] El nombre de tu paquete de ROS debe ser:

    ``` { .txt .no-copy }
    ros2_lab_equipoXX
    ```

    ... donde `XX` debe reemplazarse con tu número de equipo.

* [ ] Debe ser posible construir tu paquete ejecutando el siguiente comando desde la raíz del Espacio de Trabajo de ROS 2 local, y esto debe construirse sin errores:
    
    ``` { .bash .no-copy }
    colcon build --packages-select ros2_lab_equipoXX
    ```

* [ ] Debes asegurarte de que exista un archivo de lanzamiento para cada una de las tareas de *programación* (Tareas 1, 2 y 3) y que estos sean *ejecutables* (después de haber ejecutado el comando `colcon build` anterior) para que podamos lanzar tu trabajo usando `ros2 launch` de la siguiente manera[^launch-files]:
    
    [^launch-files]: Asegúrate de haber [definido un directorio `install` apropiado en el `CMakeLists.txt` de tu paquete](../../course/part3.md#ex1) 

    ``` { .bash .no-copy }
    ros2 launch ros2_lab_equipoXX tareaY.launch.py
    ```

    ... donde `XX` será reemplazado por tu número de equipo, y `Y` será reemplazado por el número de tarea apropiado.

    !!! warning "Importante"
        Debes asegurarte de que **tus archivos de lanzamiento tengan el nombre correcto** (como se detalla en cada una de las páginas de tareas). No usaremos ningún otro método para lanzar tus nodes de ROS durante la evaluación de cada tarea de programación.
    
* [ ] Los archivos de lanzamiento deben estar correctamente definidos en un directorio dedicado `launch` en la raíz del directorio de tu paquete (para orientación, [consulta la Asignación #1 Parte 3](../../course/part3.md#ex1)).

* [ ] Cualquier node dentro de tu paquete que sea ejecutado por los archivos de lanzamiento anteriores **debe** haber sido definido correctamente como ejecutable del paquete (es decir, en tu `CMakeLists.txt`) y también **debe** haber recibido el permiso de ejecución apropiado (es decir, con `chmod`).  

    !!! warning "Importante"
        Depende **de ti** asegurarte de que tu código se lance según lo previsto para una tarea dada. Si no es así, se te otorgarán cero puntos, así que **asegúrate de probarlo todo antes de la entrega**.
    
    <a name="build-files"></a>

* [ ] Tu paquete no debe contener **archivos de construcción** (`build/`, `install/`, `log/`) que se generarían como resultado de ejecutar incorrectamente `colcon build` desde dentro de tu paquete.

    !!! tip "Recuerda"
        **Siempre** ejecuta `colcon build` desde la **raíz** del espacio de trabajo de ROS (por ejemplo, `~/ros2_ws/`), para asegurarte de que todos los archivos de construcción se generen en la ubicación correcta en el sistema de archivos (`~/ros2_ws/build/`, `~/ros2_ws/install/`, `~/ros2_ws/log/`).

* [ ] En cada una de las fechas límite, obtendremos tu trabajo de la rama `main` de tu repositorio de paquetes. ¡Solo evaluaremos el trabajo en tu rama `main`!

* [ ] El archivo `package.xml` de tu paquete debe contener una etiqueta `#!xml <maintainer>` para cada miembro de tu equipo. Agrégalos según sea necesario, por ejemplo:

    ```xml
    <maintainer email="correo@institucion.edu">Nombre del Miembro 1</maintainer>
    <maintainer email="correo@institucion.edu">Nombre del Miembro 2</maintainer>
    ...
    ```
    (proporcionando el nombre completo y dirección de correo de cada miembro del equipo.)

Para la evaluación de cada Tarea de la Asignación #2, tu paquete será construido y desplegado en una de las Laptops de Robótica con las que habrás trabajado extensamente durante las sesiones de laboratorio. Usaremos la cuenta de usuario `student` estándar, y tu paquete será descargado al directorio `~/ros2_ws/src/`.

## Otra Información Importante 

* El [Repositorio del Curso `rigsa_ros`](../../course/extras/course-repo.md) estará instalado y actualizado en la Laptop de Robótica que usemos para evaluar tu trabajo.

* La Laptop de Robótica que usemos para la evaluación será seleccionada al azar.

* Esta laptop habrá sido vinculada con un robot antes de que intentemos ejecutar tu entrega.

* El robot también será seleccionado al azar.

* Ya habremos [lanzado el *bringup* en el robot](../../waffles/launching-ros.md#step3), por lo que ROS estará funcionando y el robot estará listo para operar en el arena.

* [Una Sesión Zenoh ya estará funcionando en la laptop](../../waffles/launching-ros.md#step4) para conectarse al *Router* Zenoh del Robot, y **las comunicaciones habrán sido probadas** antes de que intentemos lanzar tu trabajo para cada tarea.
