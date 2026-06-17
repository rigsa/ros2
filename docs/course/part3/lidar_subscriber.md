---  
title: Construyendo un Node Subscriber Básico para LaserScan
---

## El Código

Copia **todo** el código a continuación en tu archivo `lidar_subscriber.py` y luego **revisa las anotaciones** para entender cómo funciona todo.

```python title="lidar_subscriber.py"
--8<-- "code_templates/lidar_subscriber.py"
```

1. Nada de esto debería ser nuevo para ti en este punto. [Recuerda de la Parte 2](../part2.md#ex5) que estamos usando `SignalHandlerOptions` para manejar solicitudes de apagado (activadas con ++ctrl+c++).
2. Aquí estamos construyendo un subscriber para el topic `/scan`, y sabemos que este topic usa el tipo de interfaz `sensor_msgs/msg/LaserScan`, así que lo importamos aquí.
3. `numpy` es una librería Python que nos permite trabajar con datos numéricos, muy útil para arreglos grandes como `ranges`.
4. Construimos un subscriber de la misma manera que lo hemos hecho en las Partes 1 y 2, pero esta vez apuntando al topic `/scan`.
5. Desde el frente del robot, obtenemos un arco de 20&deg; de datos de escaneo a cada lado del eje x (consulta la figura a continuación).

6. Luego combinamos los arreglos de datos `left_20_deg` y `right_20_deg`, y los convertimos de una lista Python a un arreglo `numpy` (consulta la figura a continuación).

7. Esto ilustra una de las grandes características de los arreglos `numpy`: podemos filtrarlos.

    Recuerda que `front` ahora es un arreglo `numpy` que contiene 40 puntos de datos.
    
    Recuerda *también* que típicamente habrá varios valores `inf` dispersos en el arreglo LaserScan, resultado de lecturas del sensor que están fuera del rango de medición del sensor (es decir, *mayores que* `range_max` o *menores que* `range_min`). Necesitamos eliminar estos, así que le pedimos a `numpy` que filtre nuestro arreglo de la siguiente manera:

    1. De todos los valores en el arreglo `front`, determina cuáles **no son iguales** a `inf`: 
        
        `#!py front != float("inf")`

    1. Usa este *filtro* para eliminar los valores `inf` del arreglo `front`:
        
        `#!py front[front != float("inf")]`
    
    1. Devuelve esto como un *nuevo* arreglo `numpy` llamado `valid_data`:

        `#!py valid_data = front[front != float("inf")]`

8. En ciertas situaciones (por ejemplo, en entornos muy vacíos) *todos* los valores podrían ser iguales a `inf` (imagina la simulación "empty world"). Aquí verificamos el tamaño del arreglo `valid_data` para asegurarnos de no haber eliminado *todos* los valores con el filtrado anterior.

9. Si el arreglo no está vacío, usa el método `mean()` para determinar el *promedio* de todas las lecturas dentro del conjunto de datos.
10. Si el arreglo *está* vacío, devuelve *"not a number"* (es decir, "nan") en su lugar. 
11. Imprime este valor en el terminal, pero limita los mensajes para que solo se muestre uno por segundo.

    !!! question
        Si *no* limitáramos esto, ¿a qué tasa se imprimirían los mensajes?

El procesamiento de datos se ilustra en la figura a continuación:

<figure markdown>
  ![](./scandata.png){width=600px}
</figure>

## Dependencias del Package

Este node tiene dependencias en dos librerías Python externas (además de `rclpy`): 

```py
from sensor_msgs.msg import LaserScan
import numpy as np
```

Por lo tanto, debes incluirlas en el archivo `package.xml` (bajo la línea `#!xml <exec_depend>rclpy</exec_depend>`):

```xml title="package.xml"
<exec_depend>sensor_msgs</exec_depend>
<exec_depend>python3-numpy</exec_depend>
```
