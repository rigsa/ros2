---  
title: "El Repositorio del Curso ROS"
--- 

Se ha preparado un ROS Metapackage llamado `tuos_ros` para apoyar estos cursos. [Este package está disponible en GitHub aquí](https://github.com/tom-howard/tuos_ros/tree/jazzy){target="_blank"}. Este repositorio contiene los siguientes packages de ROS:

| Nombre del Package | Descripción |
| :---: | :--- |
| `tuos_examples` | Algunos scripts de ejemplo para apoyar ciertos ejercicios del Curso de ROS 2 |
| `tuos_interfaces` | Algunas interfaces personalizadas de ROS para apoyar ciertos ejercicios del Curso de ROS 2 |
| `tuos_simulations` | Algunas simulaciones de Gazebo Ignition para apoyar ciertos ejercicios del Curso de ROS 2 |
| `tuos_task_sims` | Recursos de simulación para apoyar tu trabajo de desarrollo en tareas del curso basadas en robot real |
| `tuos_tb3_tools` | Scripts y herramientas de visualización para los Waffles (real y en simulación) | 

## Instalación

[Al inicio de la Parte 1 del Curso de ROS 2](../part1.md#step-3-download-the-course-repo) explicamos cómo instalar el repositorio del curso `tuos_ros`, pero aquí están esas instrucciones nuevamente:

1. Navega al directorio `src` de tu ROS Workspace:

    ```bash
    cd ~/ros2_ws/src/
    ```

1. Clona el repositorio desde GitHub:

    ```bash
    git clone https://github.com/tom-howard/tuos_ros.git -b jazzy
    ```

1. Navega un directorio hacia atrás, hacia la *raíz* del workspace de ROS:

    ```bash
    cd ~/ros2_ws/
    ```

1. Ejecuta `colcon build` para compilar los packages:

    ```bash
    colcon build --packages-up-to tuos_ros
    ```

1. Luego vuelve a hacer source de tu `.bashrc`:

    ```bash
    source ~/.bashrc
    ```

### Verificar

Una vez que lo hayas instalado, puedes verificar que el proceso de compilación funcionó usando el siguiente comando:

```bash
colcon_cd tuos_ros
```

Lo cual debería llevarte a un directorio dentro del repositorio que también se llama `tuos_ros`, es decir:

```txt
~/ros2_ws/src/tuos_ros/tuos_ros
```

## Actualización

El repositorio del curso puede actualizarse de vez en cuando, por lo que vale la pena verificar regularmente que tienes la versión más actualizada. Puedes hacer esto descargando las últimas actualizaciones de GitHub usando `git pull`:

```bash
cd ~/ros2_ws/src/tuos_ros/ && git pull
```

Si ves el siguiente mensaje:

```txt
-bash: cd: tuos_ros/: No such file or directory
```

... entonces [regresa y asegúrate de haber instalado el repositorio primero](#instalación)!

Luego, ejecuta `colcon build` y vuelve a hacer source de tu entorno:

```bash
cd ~/ros2_ws && colcon build --packages-up-to tuos_ros && source ~/.bashrc
```