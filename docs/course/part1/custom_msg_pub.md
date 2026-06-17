---  
title: "El Publisher del Mensaje `Example`"
---

# El Publisher del Mensaje `Example`

## El Código

Copia **todo** el código a continuación en tu archivo `custom_msg_publisher.py` y **revisa las anotaciones** para ver qué es diferente respecto al publisher básico del Ejercicio 5.

```py title="custom_msg_publisher.py"
--8<-- "code_templates/custom_msg_publisher.py"
```

1. Ahora estamos importando el mensaje `Example` de nuestro propio package `part1_pubsub`.

2. Ahora también estamos declarando que `"my_topic"` usará la estructura de datos del mensaje `Example` para enviar mensajes.

3. Ahora necesitamos manejar los mensajes del topic de manera diferente, para dar cuenta de la estructura más compleja.

    Ahora llenamos nuestros mensajes con dos campos: `info` (un `string`) y `time` (un `int`). Identifica qué ha cambiado aquí...
