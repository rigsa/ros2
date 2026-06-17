---  
title: "Un Node Publisher Simple"
---

## El Código

Copia **todo** el código a continuación en tu archivo `publisher.py` y **revisa las anotaciones** para entender cómo funciona todo.

<a name="shebang"></a>

!!! tip "¡No olvides el Shebang!"
    La primera línea del código parece un comentario, pero en realidad es una parte muy crucial del script:

    ```python
    #!/usr/bin/env python3
    ```

    Esto se llama el *Shebang*, y le indica al sistema operativo qué intérprete usar para ejecutar el código. En nuestro caso, le indica al sistema operativo dónde encontrar el *intérprete de Python* correcto que debe usarse para ejecutar el código.


```python title="publisher.py"
--8<-- "code_templates/publisher.py"
```

1. `rclpy` es la *Biblioteca Cliente de ROS para Python*.
    
    Esta es una importación vital que nos permite crear nodes de ROS e inicializarlos en la red ROS.
    
    También importamos la clase `Node` de la biblioteca `rclpy.node`. Esta es una Clase Python ya preparada que contiene toda la funcionalidad necesaria que un Node ROS Python podría necesitar, por lo que la usaremos como base para nuestro propio node (que crearemos en breve).

2. También necesitamos importar el tipo de mensaje `String` de la biblioteca `example_interfaces.msg` para publicar nuestros mensajes.

3. Creamos una *clase Python* llamada `#!python SimplePublisher()`, que usaremos para encapsular toda la funcionalidad de nuestro node.
    
    La gran mayoría de la funcionalidad de este node se hereda de la Clase `#!python Node()` de `rclpy.node`, que importamos arriba.

4. Usando el método `#!python super()` llamamos al método `#!python __init__()` de la clase Node padre de la que deriva nuestra clase `SimplePublisher`.
    
    Proporcionamos un *nombre* aquí, que es el nombre que se usará para registrar nuestro node en la red ROS (podemos llamar al node como queramos, pero es una buena idea llamarlo con algo significativo).

5. Luego usamos el método `#!python create_publisher()` (heredado de la clase `Node`) para proporcionar a nuestro node la capacidad de publicar mensajes en un ROS Topic. Al llamar a esto proporcionamos 3 datos clave:

    1. `msg_type`: El **tipo** de mensaje que queremos publicar.
        
        En nuestro caso, un mensaje `String` del módulo `example_interfaces.msg`.
    
    1. `topic`: El **nombre del topic** al que queremos publicar estos mensajes.
        
        Este podría ser un topic existente (en cuyo caso, necesitaríamos asegurarnos de usar el tipo de mensaje correcto), o un nuevo topic (en cuyo caso, el nombre puede ser cualquier cosa que queramos).
        
        En nuestro caso, queremos crear un nuevo topic en la red ROS llamado `"my_topic"`.
    
    1. `qos_profile`: Un **tamaño de cola**, que es una configuración de *"Calidad de Servicio"* (QoS) que limita la cantidad de mensajes que se *ponen en cola* en un buffer.
    
        En nuestro caso, lo estamos configurando en `10`, lo que generalmente es apropiado para la mayoría de las aplicaciones en las que trabajaremos.

6. Aquí, estamos llamando al método `#!python create_timer()`, que usaremos para controlar la frecuencia a la que se publican mensajes en nuestro topic. Aquí definimos 2 cosas:

    1. `timer_period_sec`: La frecuencia a la que queremos que se ejecute el timer. Esto debe proporcionarse como un *período*, en segundos. En la línea anterior, hemos especificado una *frecuencia* de publicación (en Hz):
    
        <center>`#!python publish_rate = 1 # Hz`</center>
        
        Entonces el *período* de tiempo asociado (en segundos) es:

        <center>$T = \frac{1}{f}$</center>

    1. `callback`: Esta es una función que se ejecutará cada vez que el timer transcurra a la frecuencia deseada (1 Hz). Estamos especificando una función llamada `timer_callback`, que definiremos más adelante en el código...

7. Finalmente, usamos el método `#!python get_logger().info()` para enviar un mensaje de *Log* a la terminal para informarnos que la inicialización de nuestro node está completa.

8. Aquí definimos la función callback del timer. Todo lo que esté aquí se ejecutará a la frecuencia que especificamos cuando creamos la instancia `#!python create_timer()` antes. En nuestro caso:

    1. Usamos el método `#!python get_clock()` para obtener el *Tiempo ROS* actual.
    1. Instanciamos un mensaje `String()` (definido como `topic_msg`).
    1. Llenamos este mensaje con *datos*. En nuestro caso, una declaración que incluye el Tiempo ROS obtenido anteriormente.
    1. Llamamos al método `#!python publish()` de nuestro objeto `my_publisher`, para publicar realmente este mensaje en el topic `"my_topic"`.
    1. También enviamos los datos del mensaje a la terminal como un mensaje de log, para que podamos ver qué es cuando nuestro Node está realmente ejecutándose.

9. Con la funcionalidad de nuestra clase `SimplePublisher` ahora establecida, definimos una función `#!python main()` para el Node. Esto será bastante común en la mayoría de los Nodes Python que creemos, con los siguientes 5 procesos clave:

    1. Inicializar la biblioteca `rclpy`.
    1. Crear una instancia de nuestro node `#!python SimplePublisher()`.
    1. Hacer "spin" al node para mantenerlo vivo de modo que cualquier callback pueda ejecutarse según sea necesario (en nuestro caso aquí, solo el `#!python timer_callback()`).
    1. Destruir el node una vez que se solicite la terminación (activada al ingresar ++ctrl+c++ en la terminal).
    1. Apagar la biblioteca `rclpy`.

10. Finalmente, llamamos a la función `#!python main()` para poner todo en marcha. Hacemos esto dentro de una instrucción `#!python if`, para asegurarnos de que nuestro node sea el *ejecutable principal* (es decir, ha sido ejecutado directamente (a través de `ros2 run`), y no ha sido llamado por otro script).

## Definición de Dependencias del Package

Aquí estamos importando un par de bibliotecas Python en nuestro node, lo que significa que nuestro package tiene dos *dependencias*: `rclpy` y `example_interfaces`:

```py
import rclpy 
from rclpy.node import Node

from example_interfaces.msg import String
```

Es una buena práctica añadir estas dependencias a tu archivo `package.xml`. Localiza este archivo (`ros2_ws/src/part1_pubsub/package.xml`), ábrelo y encuentra la siguiente línea:

```xml
<exec_depend>rclpy</exec_depend>
```

`rclpy` ya está definido como una *dependencia de ejecución* (lo que significa que nuestro package necesita esta biblioteca para ejecutar nuestro código), pero también necesitamos añadir `example_interfaces`, así que añade la siguiente línea adicional debajo:

```xml
<exec_depend>example_interfaces</exec_depend>
```

Listo. Guarda el archivo y ciérralo.
