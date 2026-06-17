---
title: "Crear tu Paquete de ROS 2 del Equipo"
description: "El primer paso es crear un paquete de ROS para que viva tu código" 
---

# Crear tu Paquete de ROS 2 del Equipo

Debes usar los mismos procedimientos que usaste en los Labs de Simulación para crear un paquete de ROS 2 para esta asignación (descrito nuevamente a continuación). Debes crear **un paquete por equipo**, así que nomina a **un** miembro de tu equipo para hacer esta parte.

Debes hacer esto desde dentro de tu propia instalación local de ROS (es decir, en tu propia computadora), o una instancia de terminal WSL-ROS2.

1. Dirígete a la carpeta `src` de tu espacio de trabajo de ROS 2 en tu terminal:

    ```bash
    cd ~/ros2_ws/src/
    ```

1. Clona la *Plantilla de Paquete de ROS 2* de GitHub:

    ```bash
    git clone https://github.com/tom-howard/ros2_pkg_template.git
    ```
    
1. Ejecuta el script `init_pkg.sh` de la siguiente manera (**presta atención a la información adicional a continuación sobre el nombre de tu paquete**):

    ``` { .bash .no-copy }
    ./ros2_pkg_template/init_pkg.sh ele_teamXX_2026
    ```

    Tu paquete **debe** tener el nombre: `ele_teamXX_2026`

    ... donde `XX` debe reemplazarse con *tu* número de equipo (consulta la plataforma del curso si no estás seguro de cuál es el número de tu equipo).

    **Si tu número de equipo es menor que 10**: pon un cero antes de él, para que el número de equipo siempre tenga **2 dígitos de longitud**, por ejemplo:
    
    * `ele_team03_2026` para el **Equipo 3**
    * `ele_team08_2026` para el **Equipo 8**
    * `ele_team15_2026` para el **Equipo 15**

    !!! warning "Importante"
        El nombre de tu repositorio debe coincidir exactamente con el formato anterior:
            
        * Todos los caracteres deben estar en **minúsculas**

1. A continuación, navega a la **raíz** de tu nuevo paquete:

    ``` { .bash .no-copy }
    cd ./ele_teamXX_2026/
    ```

    ...y crea un nuevo directorio allí llamado `launch`:

    ```bash
    mkdir launch
    ```

1. Dentro de aquí, crea un archivo vacío llamado `explore.launch.py`:

    ```bash
    touch ./launch/explore.launch.py
    ```

    ... deja esto vacío por ahora. Necesitarás llenarlo apropiadamente más adelante (más detalles en [el Brief de la Tarea](./task.md)).

1. Abre el archivo `CMakeLists.txt` de tu paquete y agrega el siguiente texto **justo encima** de la línea `ament_package()` al final del archivo:

    ```txt title="ele_teamXX_2026/CMakeLists.txt"
    install(DIRECTORY
      launch
      DESTINATION share/${PROJECT_NAME}
    )
    ```

1. Ahora puedes construir esto usando Colcon siguiendo **el mismo proceso de tres pasos** que has seguido a lo largo del Curso de Lab de Simulación:

    1. **Paso 1**, navega a la **raíz** del espacio de trabajo de ROS 2:

        ```bash
        cd ~/ros2_ws/
        ```

    1. **Paso 2**, construye tu paquete con Colcon:

        ``` { .bash .no-copy }
        colcon build --packages-select ele_teamXX_2026 --symlink-install
        ```

    1. **Paso 3**, recarga el `.bashrc`:

        ```bash
        source ~/.bashrc
        ```
    
    !!! tip "No olvides"
        Necesitarás seguir el proceso **de tres pasos** de `colcon build` siempre que hagas cosas como:

        1. Agregar un nuevo node a tu paquete (¡no olvides modificar también el archivo `CMakeLists.txt`!)
        1. Agregar **o modificar** un archivo de lanzamiento
        1. Agregar **o modificar** una interface personalizada (como en [la Parte 1](../../course/part1.md#ex7))
        1. Copiar tu paquete en una computadora diferente

## Ver También

* [Transferir tu Paquete de ROS a las Laptops de Robótica](./first-lab.md#transferring-your-ros-package-to-the-robotics-laptops)
* [Exportar tu Paquete de ROS para Entrega](./submission.md#exporting-your-ros-package-for-submission)
