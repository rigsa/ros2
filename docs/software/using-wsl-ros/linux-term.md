---
title: Una Breve Introducción al Terminal de Linux
---

Trabajarás extensamente con el Terminal de Linux a lo largo de este curso. Una instancia de terminal WSL-ROS2 *inactiva* se verá así:

<figure markdown>
  ![](../figures/wsl-ros-term-antd.svg){width=700px}
</figure>

Aquí, la presencia del símbolo `$` indica que el terminal está listo para aceptar un comando. El texto antes del símbolo `$` tiene dos partes separadas por el símbolo `:`:

* El texto a la **izquierda** del `:` nos indica el nombre del usuario de Linux ("student" en este caso) seguido de la versión de WSL-ROS2 con la que estás trabajando.

    !!! note
        La versión actual de WSL-ROS2 es `2526`.

* El texto a la **derecha** del `:` nos indica dónde en el Sistema de Archivos de Linux estamos ubicados actualmente (`~` significa *"El Directorio de Inicio"*, que es un alias para la ruta: `/home/student/`).

Si no ves el símbolo `$` en absoluto, entonces significa que hay un proceso en ejecución actualmente. Para detener cualquier proceso en ejecución presiona ++ctrl+c++ simultáneamente en tu teclado.