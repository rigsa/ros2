---  
title: Un Action Client Mínimo
---

## El Código

Revisa el código (incluyendo las anotaciones) y luego toma una copia de él.

```py title="camera_sweep_action_client.py"
--8<-- "code_templates/camera_sweep_action_client.py"
```

1. Como ya sabes, para desarrollar nodes de ROS usando Python necesitamos importar la librería cliente `rclpy` y la clase `Node` en la que basar nuestro node. Además, aquí también importamos una clase `ActionClient`.

2. Sabemos que el Action Server `/camera_sweep` usa la interface `action` `CameraSweep` del paquete `rigsa_interfaces`, así que la importamos aquí también (la cual usamos para hacer una llamada al servidor).

3. Práctica estándar al inicializar nodes de ROS: *debemos darles un nombre*.

4. Aquí instanciamos un objeto de la clase `ActionClient`. Al hacer esto definimos el `node` al que se agrega el action client (en nuestro caso `self`, es decir, nuestra clase `CameraSweepActionClient`). Luego también definimos el tipo de interface utilizado por el servidor (`CameraSweep`) y el nombre del action que queremos llamar (`action_name="camera_sweep"`).

5. Aquí estamos declarando dos parámetros de ROS: `goal_images` y `goal_angle`.

    Los usaremos para establecer goals para el action server en tiempo de ejecución.

    Por defecto, estos valores están configurados en `0`, ¡así que si no establecemos explícitamente valores para estos dos parámetros, permanecerán en `0`!

    !!! question
        ¿Cómo establecemos valores para los parámetros en tiempo de ejecución (es decir, cuando ejecutamos este node usando `ros2 run`)?

        [Recuerda cómo lo hicimos en la Parte 4](../part4.md#ex5).

6. Aquí definimos un método de clase para construir y enviar un goal al servidor.

7. Como sabemos de antes, un `CameraSweep.Goal()` contiene dos parámetros a los que podemos asignar valores: `sweep_angle` y `image_count`.

    Como se indicó arriba, los valores asignados a estos provienen de dos parámetros de ROS: `goal_angle` y `goal_images`.

    !!! warning "Recuerda"
        Por defecto, ambos parámetros tendrán un valor de `0` a menos que les asignemos explícitamente un valor (ver arriba).

        ¿Cómo asignamos valores a estos parámetros en tiempo de ejecución? [Recuerda cómo lo hicimos en la Parte 4](../part4.md#ex5).

8. El goal se envía al servidor usando el método `send_goal_async()`, que devuelve un *future*: es decir, algo que sucederá en el futuro y en lo que podemos esperar. Este future se devuelve una vez que los parámetros del goal han sido aceptados por el servidor, *no* cuando el action server ha completado realmente su tarea.

9. En nuestro método `main` inicializamos `rclpy` y nuestra clase `CameraSweepActionClient` (nada nuevo aquí), pero luego llamamos al método `send_goal()` de nuestra clase (como se discutió arriba), que devuelve un *future*. Entonces podemos usar el método `rclpy.spin_until_future_complete()` para activar nuestro node *solo* hasta que este objeto future haya terminado.

## Dependencias del Paquete

El action client tiene *dos dependencias clave*, por lo que necesitamos modificar el archivo `package.xml` (debajo de la línea `#!xml <exec_depend>rclpy</exec_depend>`) para incluirlas:

```xml title="package.xml"
<exec_depend>action_msgs</exec_depend>
<exec_depend>rigsa_interfaces</exec_depend>
``` 
