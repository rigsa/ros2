---
title: "Recursos de Simulación"
description: "Detalles del entorno de simulación que puedes usar para probar tus algoritmos"
---

Dentro del paquete `rigsa_task_sims` hay un arena de ejemplo que puede usarse para desarrollar y probar el trabajo de tu equipo para esta tarea.

!!! info 
    Asegúrate de [revisar si hay actualizaciones al Repositorio del Curso](../../course/extras/course-repo.md#updating) para garantizar que tengas la versión más actualizada de esto.

La simulación puede lanzarse usando el siguiente comando `ros2 launch`:

```bash
ros2 launch rigsa_task_sims obstacle_avoidance.launch.py
```

<figure markdown>
  ![](../../com/assignment2/figures/task2.png){width=700px}
  <figcaption>Un arena de desarrollo para la Tarea de Exploración en el Mundo Real.</figcaption>
</figure>

!!! warning
    ¡La ubicación y orientación de los obstáculos **serán diferentes** a las de esta simulación!

Por defecto, el robot aparecerá en el arena en la orientación mostrada en la figura anterior; sin embargo, puedes probar *diferentes* orientaciones de inicio para el robot suministrando un argumento de línea de comandos adicional al archivo `obstacle_avoidance.launch.py`:

``` { .bash .no-copy }
ros2 launch rigsa_task_sims obstacle_avoidance.launch.py yaw:=X
```

Donde el valor de `X` puede ser cualquier ángulo de orientación, en radianes. Recuerda que para la evaluación de esta tarea, el robot **siempre** estará orientado *perpendicular* a una de las cuatro paredes exteriores del arena al inicio de la tarea; por lo tanto, solo cuatro valores de `yaw` son realmente relevantes para ti:

<center>

| `yaw:=` | Orientación |
| :---: | :--- |
| `0.0` | El robot está mirando hacia la baliza **Azul** al aparecer (por defecto) |
| `1.571` | El robot está mirando hacia la baliza **Verde** al aparecer |
| `-1.571` | El robot está mirando hacia la baliza **Roja** al aparecer |
| `3.142` | El robot está mirando hacia la baliza **Amarilla** al aparecer |

</center>

## Simulación vs. el Mundo Real

Esta simulación se proporciona como una forma de desarrollar tus algoritmos en simulación, y para permitirte hacer algo de trabajo en esta asignación fuera de las sesiones de laboratorio. Sin embargo, **¡el hecho de que funcione en simulación ^^NO^^ significa que funcionará en el mundo real**!

Asegúrate de probar las cosas a fondo durante las sesiones de laboratorio con robots reales en las Semanas 8-11.
