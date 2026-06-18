---
title: Ejecutar ROS 2 en Tu Navegador (Sin Instalación)
description: "Realiza los laboratorios del curso completamente en un navegador, sin necesidad de instalación local de ROS 2/Gazebo/WSL."
---

**Aplicable a**: Cualquier computadora con un navegador web moderno (Windows, Mac, Linux,
Chromebooks) y Docker instalado en la máquina que aloja el sandbox.

## Qué es esto

Un sandbox autocontenido que ejecuta una sesión completa del curso - un editor de código y una
simulación Gazebo/RViz del TurtleBot3 Waffle - dentro de un único contenedor Docker,
transmitido directamente a tu navegador. No hay nada que instalar más allá del propio Docker
(sin WSL, sin ROS 2 ni Gazebo instalados manualmente), y los archivos de inicio de cada parte
del curso están precargados para ti.

Actualmente es una herramienta **solo local**: alguien (tú, un demostrador del laboratorio, o el
área de TI) lo ejecuta en una máquina con Docker, y tú te conectas desde cualquier
navegador en la misma red. Aún no está alojado centralmente.

## Cómo ponerlo en marcha

El sandbox vive en un repositorio separado, [`tom-howard/ros2-sandbox`](https://github.com/tom-howard/ros2-sandbox){target="_blank"}
(las instrucciones de compilación y ejecución están en el `README.md` de ese repositorio). En términos generales:

1. Compila la imagen del sandbox una vez (`docker build` - esto incorpora ROS 2 Jazzy, Gazebo,
   y [el repositorio del curso](../course/extras/course-repo.md)).
2. Inicia la pequeña aplicación orquestadora local y ábrela en tu navegador.
3. Elige una parte del curso y asígnate un nombre de sesión - tu código se conserva entre
   visitas siempre que reutilices el mismo nombre.

Llegarás a una página de sesión con dos paneles: un editor de código completo (con los archivos
de inicio de esa parte ya abiertos) a la izquierda, y un escritorio transmitido que muestra
Gazebo/RViz a la derecha - exactamente las mismas ventanas que verías en una instalación local
de WSL-ROS2 o Docker, solo que ejecutándose de forma remota y mostradas en tu navegador.

## Ejecutar los laboratorios

Una vez que estés en una sesión, trabaja exactamente como el resto de este curso describe: abre un
terminal (el editor tiene uno integrado), ejecuta `colcon build` en tu package, haz `source` de tu
workspace, y usa `ros2 run`/`ros2 launch` para lanzar tus nodes. El mundo de simulación para la
parte que elegiste ya está en ejecución y visible en el panel derecho - nada sobre los
comandos de ROS 2 en sí mismos cambia.

## Limitaciones de esta opción (por ahora)

- Sin inicio de sesión/cuentas todavía - las sesiones se identifican por un nombre que escribes, así que no
  reutilices el nombre de sesión de otra persona.
- Solo el TurtleBot3 Waffle simulado está soportado - si estás trabajando hacia un
  robot diferente (por ejemplo, un Unitree Go2/B2), consulta
  [Portando a un Unitree Go2/B2](../course/extras/porting-to-unitree.md) para ver cómo
  los conceptos y topics de ROS 2 que practicas aquí se transfieren.
- Necesita una máquina razonablemente capaz para alojar el contenedor (está ejecutando un escritorio
  completo + Gazebo por sesión) - esto funciona mejor en una PC del laboratorio o en tu propia máquina
  que en algo de muy baja potencia.