---
title: La Plantilla del Explore Server de la Parte 5
---

## El Código

```py title="explore_server.py"
--8<-- "code_templates/explore_server.py"
```

1. Algunas variables para almacenar datos de los subscribers `/odom` (`posx` y `posy`) y `/scan` (`lidar_reading`), y compartir estos datos en toda la clase.
2. Un flag de apagado (ya lo has visto antes).
3. Algunos flags para determinar cuándo hemos recibido datos de los subscribers `/odom` y `/scan`, para asegurarnos de que el callback de ejecución principal del action server no comience hasta que tengamos datos válidos con los que trabajar (ver uso a continuación).
4. Aquí estamos creando un objeto que podemos usar en el callback de ejecución principal de nuestro action server para controlar la velocidad de ejecución dentro de un loop `#!py while` (ver uso a continuación).
5. Consulta el [Subscriber de Odometría de la Parte 2](../part2/odom_subscriber.md#modifying-the-message-callback) para obtener ayuda con esto (si la necesitas).
6. Consulta el [Subscriber de LiDAR de la Parte 3](../part3/lidar_subscriber.md) para obtener ayuda con esto (si la necesitas).
7. Llamar esto aquí bloqueará cualquier ejecución de código adicional hasta que haya transcurrido suficiente tiempo.
    
    Este tiempo está dictado por el parámetro `frequency` que definimos cuando lo configuramos anteriormente:

    ```py
    self.loop_rate = self.create_rate(
        frequency=5, 
        clock=self.get_clock()
    )
    ```

## Dependencias

Aquí se introducen algunas dependencias adicionales, debido a los diversos módulos Python adicionales que importa el Explore Server. Asegúrate de agregar estas a tu archivo `package.xml`:

```xml title="package.xml"
<exec_depend>sensor_msgs</exec_depend>
<exec_depend>geometry_msgs</exec_depend>
<exec_depend>nav_msgs</exec_depend>
<exec_depend>python3-numpy</exec_depend>
```
