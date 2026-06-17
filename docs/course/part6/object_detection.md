---  
title: "Parte 6: Node de Detección de Objetos"  
---

## El Código

Copia **todo** el código a continuación en tu archivo `object_detection.py`, ¡y **asegúrate de leer las anotaciones**!

```py title="object_detection.py"
--8<-- "code_templates/object_detection.py"
```

1. Nada nuevo aquí, continuamos...
   
2. Estamos importando la biblioteca OpenCV para Python (recuerda la API de Python [de la que hablamos antes](../part6.md#opencv)), que se llama `cv2`, y *también* esa interface puente entre ROS y OpenCV de la que hablamos antes: `cv_bridge`.

    De `cv_bridge` estamos importando las clases `CvBridge` y `CvBridgeError` de la biblioteca `cv_bridge` específicamente.

3. Necesitamos subscribirnos a un topic de imagen para obtener los datos que se publican en él. Ya deberías haber identificado el *tipo de interface* que se publica en el topic `/camera/image_raw`, así que importamos ese tipo de interface aquí (del package `sensor_msgs`) para poder construir un subscriber al topic más adelante.

4. También estamos importando la clase Python `Path` del [módulo `pathlib`](https://docs.python.org/3/library/pathlib.html){target="_blank"}. Una herramienta muy útil para realizar operaciones de archivos.

5. Inicializando nuestra Clase `#!py ObjectDetection()` (debería serte muy familiar a estas alturas):
    1. Dando un nombre a nuestro node.
    1. Creando un subscriber al topic `/camera/image_raw`, proporcionando el *tipo de interface* utilizado por el topic (`sensor_msgs/msg/Image`, como se importó anteriormente), y apuntándolo a una función callback (`camera_callback`, en este caso), para definir los procesos que deben realizarse cada vez que se obtiene un mensaje en este topic (en este caso, los mensajes serán nuestras imágenes de cámara)

6. Estamos creando una bandera para indicar si el node ha obtenido una imagen todavía o no. Para este ejercicio, solo queremos obtener una única imagen, así que estableceremos la bandera `waiting_for_image` en `False` una vez que se haya obtenido y procesado una imagen, para evitar capturar más. 

    Esta bandera se usará luego para cerrar el node cuando haya terminado su trabajo.

7. Aquí estamos definiendo una función callback para nuestro subscriber `self.camera_sub`...

8. Aquí creamos una instancia de la clase `CvBridge` que importamos anteriormente, y que usaremos más adelante para convertir datos de imagen ROS a un formato que OpenCV pueda entender.

9. Estamos usando la interface CvBridge para tomar nuestros datos de imagen ROS y convertirlos a un formato que OpenCV pueda entender. En este caso especificamos la conversión (o *"encoding"*) a un formato de imagen BGR (Azul-Verde-Rojo) de 8 bits: `"bgr8"`.
        
    Sin embargo, contenemos esto dentro de un bloque `#!py try`-`#!py except`, que es el [procedimiento recomendado al hacer esto](http://wiki.ros.org/cv_bridge/Tutorials/ConvertingBetweenROSImagesAndOpenCVImagesPython){target="_blank"}. Aquí *intentamos* convertir una imagen usando el encoding deseado, y si se genera un `CvBridgeError` entonces imprimimos un mensaje de **advertencia** en el terminal. Si esto sucede, esta ejecución particular de la función callback de la cámara se detendrá.

10. Luego verificamos la bandera `waiting_for_image` para ver si esta es la primera imagen recibida por el node. Si es así, entonces:

    1. Obtenemos la altura y el ancho de la imagen (en píxeles), así como el número de canales de color.
    1. Imprimimos un mensaje de registro con las dimensiones de la imagen.
    1. Pasamos los datos de la imagen a la función `show_image()` (definida a continuación). También pasamos un nombre descriptivo para la imagen a esta función (`img_name`).
    
11. Este método de clase nos presenta la imagen en una ventana emergente y también llama a otro método que guarda la imagen en un archivo para nosotros.    
    
12. Muestra la imagen real en una ventana emergente:

    1. Los datos de la imagen se pasan a la función a través del argumento `img`,
    1. Necesitamos darle un nombre a la ventana emergente, así que en este caso usamos el argumento `img_name` que se pasa a este método de clase.
    
13. El método de clase `show_image()` tiene un argumento `save_img`, que está establecido en `True` por defecto, de modo que esta condición `#!py if` se activa, y se llama a *otro* método de clase para guardar la imagen en un archivo.    

14. Proporcionamos un valor de `4000` aquí, lo que le dice a esta función que mantenga esta ventana abierta durante 4000 milisegundos (4 segundos) antes de cerrarla nuevamente.  
    
    Una vez que la ventana se haya cerrado, la ejecución de nuestro código puede continuar...    

15. Luego establecemos la bandera `waiting_for_image` en `False` para que estas etapas de procesamiento solo se realicen una vez (solo queremos capturar una única imagen). Esto activará el bucle `#!py while` principal para que se detenga (ver abajo), causando que la ejecución general del node se detenga también.

16. `cv2.destroyAllWindows()` garantiza que cualquier ventana emergente de imagen OpenCV que pueda seguir activa o en memoria sea destruida antes de que el método de clase salga (y el node se cierre).     

17. Este método de clase maneja el guardado de la imagen en un archivo usando herramientas de `cv2` y `pathlib`.
    
18. Aquí definimos una ubicación del sistema de archivos para guardar imágenes. 
    
    Queremos que exista en una carpeta llamada "`object_detection`" en el directorio de inicio, así que podemos usar `#!py Path.home().joinpath(...)` de Pathlib para definirla (una forma práctica de acceder al directorio de inicio del Usuario, sin necesidad de conocer el nombre del Usuario).
    
    Luego usamos el método `#!py Path.mkdir()` de Pathlib para crear este directorio si no existe todavía.    
    
19. Aquí se construye una ruta completa de archivo para la imagen (usando el método `Path.joinpath()`), basada en:
        
    1. El `base_image_path` que definimos anteriormente 
    1. Un nombre de imagen que se pasa a este método de clase a través del argumento `img_name`.

20. Esto guarda la imagen en un archivo `.jpg`. Proporcionamos la `full_image_path` que se creó anteriormente, y también los datos reales de la imagen (`self.cv_img`) para que la función sepa qué imagen queremos guardar.

21. Estamos imprimiendo un mensaje de registro en el terminal para informarnos de:

    1. Dónde se ha guardado la imagen
    1. Qué tan grande es la imagen (en términos de sus dimensiones en píxeles)
    1. Qué tan grande es el *archivo* de imagen (en bytes).

22. Estamos usando `spin_once()` dentro de un bucle `#!py while` aquí para poder vigilar el valor de la bandera `wait_for_image`, y dejar de hacer spin (es decir, salir del bucle `#!py while`) una vez que se vuelve `#!py False`.
    
## Dependencias

Modifica tu archivo `package.xml` para acomodar las diversas dependencias del node `object_detection.py`:

```xml title="package.xml"
<exec_depend>opencv2</exec_depend>
<exec_depend>cv_bridge</exec_depend>
<exec_depend>sensor_msgs</exec_depend>
```
