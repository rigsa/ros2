---  
title: Crear un Python Service Client
---

Copia **todo** el código a continuación en tu archivo `number_game_client.py` y luego **revisa las anotaciones** para entender cómo funciona todo.

```python title="number_game_client.py"
--8<-- "code_templates/number_game_client.py"
```

1. Crear un *Client* de Service se hace usando el método de clase `create_client()`, proporcionando el nombre del service que queremos llamar (`srv_name`), y especificando el tipo de interface utilizado por él (`srv_type`). 

    `srv_type` y `srv_name` **deben** coincidir con la definición en el server, para poder comunicarse y enviar requests a él. 

2. Aquí estamos declarando algunos parámetros (recuerda la [Parte 3](../part3.md#ex2)). Sin embargo, esta vez los usaremos de manera diferente: *para crear una interfaz de línea de comandos (CLI) para nuestro nodo*. Esencialmente, estableceremos estos parámetros dinámicamente cuando lo llamemos con `ros2 run` (para poder cambiar los valores cada vez que iniciemos el client).

    Estamos definiendo dos parámetros para el nodo, para que coincidan con los atributos de la request de service:

    1.`"guess"`: Un entero, con un valor predeterminado de `0`. 
    2. `"cheat"`: Un booleano, con un valor predeterminado de `False`.

    (Verás cómo funciona todo esto en breve, cuando realmente ejecutemos el nodo.)

3. Usamos un bucle `while` aquí para detener la ejecución del código en este punto y esperar a que el service esté disponible (si no lo está ya). 

    ¡No podemos enviar una request a un service que no esté realmente en ejecución!

4. En este método de clase construimos la request de service y la enviamos.
    
    (Este método es llamado en la función `main()` a continuación.)

5. Lee el valor del parámetro `guess`, que estableceremos desde la línea de comandos cuando llamemos al nodo (con `ros2 run`).

    ¡Esto se ha dividido en tres líneas, de lo contrario se vuelve demasiado largo y se sale de la pantalla!

6. Lee el valor del parámetro `cheat`, que *también* estableceremos desde la línea de comandos (lo veremos en breve).

    ¡*También* dividido en tres líneas por ninguna razón más que la legibilidad!

7. Aquí estamos imprimiendo los valores de los parámetros en la terminal como un mensaje de log, para confirmar exactamente qué request se enviará al server.

8. Aquí realmente construimos la request, usando una instancia de la clase de interface `part4_services/srv/MyNumberGame`, como se importó arriba.

9. `#!py call_async(request)` luego realmente envía esta request al server.

10. Luego llamamos al método de clase `send_request()` de nuestro client, que a su vez (como sabes de arriba) iniciará la construcción de la request y la enviará al server. 

    La salida de esta función es la salida de la llamada `call_async(request)`, que asignamos a una variable llamada `future`.

11. Usamos el método `rclpy.spin_until_future_complete()` aquí, que (como su nombre lo indica) permitirá que nuestro nodo (`client`) haga spin *solo* hasta que nuestra request de service (`future`) haya sido completada. 

12. Una vez que hemos llegado a este punto, el service ha completado y devuelto su **Response**. 
    
    Obtenemos la response de nuestro objeto `future` para poder leer sus valores...

13. Para terminar, construimos un mensaje de log final que contiene los valores devueltos por el Server (es decir, la **Response**). 
    
    Sabemos cómo se llaman estos atributos porque los definimos en el archivo `MyNumberGame.srv`, que podemos revisar en cualquier momento usando `ros2 interface show`:

    ``` { .txt .no-copy }
    $ ros2 interface show part4_services/srv/MyNumberGame
    
    int32 guess
    bool cheat
    ---
    int32 num_guesses
    string hint
    bool correct
    ```
