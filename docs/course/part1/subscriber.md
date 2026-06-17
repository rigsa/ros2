---  
title: "Un Node Subscriber Simple"  
---

## El Código

Copia **todo** el código a continuación en tu archivo `subscriber.py` y (de nuevo) *¡asegúrate de leer las anotaciones para entender cómo funciona todo!*

```python title="subscriber.py"
--8<-- "code_templates/subscriber.py"
```

1. Al igual que con nuestro node publisher, necesitamos importar la biblioteca cliente `rclpy` y el tipo de mensaje `String` de la biblioteca `example_interfaces.msg` para escribir un Node ROS Python y usar los mensajes ROS relevantes:

2. Esta vez, creamos una Clase Python llamada `SimpleSubscriber()` en su lugar, pero que aún hereda la clase `Node` de `rclpy` como lo hicimos con el Publisher antes.

3. Una vez más, usando el método `#!python super()` llamamos al método `#!python __init__()` de la clase Node padre de la que deriva nuestra clase `SimpleSubscriber`, y proporcionamos un nombre para registrarlo en la red.

4. Ahora estamos usando el método `#!python create_subscription()` aquí, que le permitirá a este node *subscribirse* a los mensajes en un ROS Topic. Al llamar a esto proporcionamos 4 datos clave:

    1. `msg_type`: El **tipo** de mensaje que usa el topic (que podríamos obtener ejecutando el comando `ros2 topic info`).
        
        Sabemos (habiendo creado el publisher), que nuestro topic usa mensajes `String` (de `example_interfaces`).
    
    1. `topic`: El **nombre del topic** al que queremos escuchar (o subscribirnos).
        
        !!! warning "¡Completa el espacio en blanco!"
            ¡Reemplaza los `??` en el código anterior con el nombre del topic al que el node [`publisher.py`](./publisher.md) fue configurado para publicar!
    
    1. `callback`: Al construir un subscriber, necesitamos una *función callback*, que es una función que se ejecutará cada vez que se reciba un nuevo mensaje del topic.

        En esta etapa, definimos cómo se llama esta función callback (`self.msg_callback`), y definiremos la función en sí misma más adelante dentro de la Clase.
    
    1. `qos_profile`: Como antes, un **tamaño de cola** para limitar la cantidad de mensajes que se *ponen en cola* en un buffer.

5. Imprime un mensaje de Log en la terminal para indicar que el proceso de inicialización ha tenido lugar.

6. Aquí estamos definiendo qué sucederá cada vez que nuestro subscriber reciba un nuevo mensaje. Esta función callback debe tener solo un argumento (además de `self`), que contendrá los datos del mensaje que se han recibido:

    También estamos usando [una Anotación de Tipo Python](https://docs.python.org/3/library/typing.html){target="_blank"} aquí también, que informa al intérprete que el `topic_message` recibido por la función `msg_callback` será del tipo de datos `String`.
    
    (Todo esto realmente hace es permitir que la funcionalidad de autocompletado funcione dentro de nuestro editor de texto, de modo que cada vez que queramos extraer un atributo del objeto `topic_message` nos dirá qué atributos existen realmente dentro del objeto.)

7. En este ejemplo simple, todo lo que vamos a hacer al recibir un mensaje es imprimir un par de mensajes de log en la terminal, para incluir:

    1. El nombre de este node (usando el método `self.get_name()`)

    1. El mensaje que se ha recibido (`topic_message.data`)

8. El resto de esto es exactamente igual que antes con nuestro publisher.

## ¡No Olvides el Shebang! {#dfts}

Recuerda: **no olvides el shebang**, ¡es muy importante!

```python
#!/usr/bin/env python3
```
