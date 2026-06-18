---
title: "Asignación #2: Proyecto de Robótica en Equipo"
description: Aplica tu conocimiento de ROS 2 a robots del laboratorio en el laboratorio.
--- 

## Descripción General

En la Asignación #2 pondrás en práctica todo lo que estás aprendiendo sobre ROS 2 en la Asignación #1, y explorarás las capacidades del framework con mayor profundidad.

Asistirás a una sesión de laboratorio de 2 horas por semana en el laboratorio de robótica durante el semestre completo de 12 semanas. Aquí trabajarás **en equipos** para desarrollar Nodes de ROS para nuestros robots de simulación *reales*, permitiéndoles completar con éxito varias tareas robóticas en un *entorno del mundo real*.

La Asignación #2 está dividida en dos partes: **Parte A** y **Parte B**. Completarás la Parte A en la primera mitad del semestre (Semanas 1-6) y luego pasarás a la Parte B en la segunda mitad del semestre (Semanas 7-12).

## Las Tareas

<center>

| Parte | Descripción | Puntos<br />(/100) | Entrega |
| :---: | :---  | :---: | :---: |
| **A** | **Tarea 1**: [Control de Velocidad](./part-a/task1.md)<br />**Tarea 2**: [Evasión de Obstáculos](./part-a/task2.md) | 20<br />20 | Viernes de la Semana 6 a las 6pm |
| **B** | **Tarea 3**: [Exploración y Búsqueda](./part-b/task3.md)<br />**[Viva de Equipo](./part-b/team-viva.md)** | 40<br />20 | Viernes de la Semana 12 a las 6pm |

</center>

Como se muestra arriba, hay **tres tareas de programación** y una **Viva de Equipo** que debes completar para la Asignación #2, con un total de **100 puntos** en general. Las fechas límite de entrega exactas se indicarán en la plataforma del curso.

Las tres tareas de programación requerirán que desarrolles nodes de ROS (y un paquete de ROS) para hacer que nuestros robots reales robot de simulación completen ciertos objetivos del mundo real en el arena del laboratorio de robótica. Las tres tareas serán evaluadas según qué tan bien el robot completa cada uno de los objetivos.

## Evaluación

Como equipo serás evaluado en un paquete de ROS que desarrollas para satisfacer las tareas anteriores.

Tu paquete de ROS será evaluado por el equipo docente en las semanas posteriores a las fechas límite de entrega (como se indicó arriba). Recibirás tus calificaciones, más videos de la evaluación dentro de las 3 semanas de la entrega.

### Tareas 1, 2 y 3

Cada entrega será evaluada desplegando tu paquete de ROS en una de las *laptops de robótica* que usarás extensamente durante las sesiones de laboratorio. Los nodes dentro de tu paquete se ejecutarán entonces en la laptop para controlar un robot real en el arena del laboratorio de robótica.

### Viva de Equipo

El objetivo principal de la *Viva de Equipo* es darte la oportunidad de mostrar la aplicación ROS que (*como equipo*) has construido para la Tarea 3: contarnos sobre tu enfoque, la lógica principal y por qué elegiste adoptarlo. También es una oportunidad para destacar aspectos novedosos o impresionantes de tu trabajo de los que estés particularmente orgulloso. [Para más detalles, consulta aquí](./part-b/team-viva.md).

### Entregas

Antes de comenzar cualquiera de las tareas, **como equipo** necesitarás crear un único paquete de ROS y alojarlo en GitHub (lo cual harás en [la Sesión de Laboratorio de la Semana 1](./getting-started.md)). Luego puedes agregar toda la funcionalidad necesaria para cada tarea a medida que avanzas. En cada una de las fechas límite de entrega (como se resume arriba y se detalla en la plataforma del curso) obtendremos el trabajo de tu equipo de tu repositorio de GitHub. [Consulta aquí para más detalles](./assessment.md).

!!! note
    Debes trabajar en cada tarea **como equipo**, y crear solo **un** paquete de ROS/repositorio de GitHub **por equipo** para esta asignación.

## Tu Paquete de ROS

### Lanzar Tu Código

Para lanzar la funcionalidad necesaria dentro de tu paquete para una tarea determinada necesitarás incluir *archivos de lanzamiento* con el nombre correcto: `task1.launch.py`, `task2.launch.py` y `task3.launch.py`. Esto te permitirá garantizar que toda la funcionalidad requerida se ejecute cuando se evalúe tu entrega, y también asegura que sepamos exactamente cómo lanzar esta funcionalidad para evaluarla. Los detalles completos de los requisitos para cada archivo de lanzamiento se proporcionan en la página de tarea correspondiente.

Para más información sobre cómo crear archivos `.launch.py`, consulta los siguientes recursos:

1. [Asignación #1 Parte 3](../../course/part3.md#ex1)
2. [Archivos de Lanzamiento (Avanzado)](../../course/extras/launch-files.md) 

### Prepararse para las Fechas Límite

[Puedes encontrar toda la información clave sobre la evaluación de las tareas de *programación* en esta página](./assessment.md). Es extremadamente importante que sigas todos los *Requisitos Clave* descritos aquí sobre la estructura, contenido y configuración de tu paquete de ROS, así que asegúrate de **leer esta página en su totalidad** a la mayor brevedad posible.
