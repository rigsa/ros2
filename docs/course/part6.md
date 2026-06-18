---
title: "Parte 6: Cámaras, Visión Artificial y OpenCV"  
description: Aprende a trabajar con imágenes de la cámara de un robot. Aprende técnicas para detectar características en estas imágenes y utiliza esto para informar la toma de decisiones del robot.
---

## Introducción

:material-pen: **Ejercicios**: 4  
:material-timer: **Tiempo Estimado de Finalización**: 2 horas  
:material-gauge-full: **Nivel de Dificultad**: Avanzado 

### Objetivos

En esta parte del curso utilizaremos la cámara del robot y veremos cómo trabajar con imágenes en ROS. Aquí aprenderemos a construir nodes ROS que capturen y procesen imágenes. Exploraremos algunas formas en que estos datos pueden utilizarse para informar la toma de decisiones en aplicaciones robóticas.  

### Resultados de Aprendizaje Esperados

Al finalizar esta sesión serás capaz de:

1. Usar una variedad de herramientas ROS para interrogar topics de imágenes de cámara en una Red ROS y ver las imágenes que se transmiten a ellos.
1. Usar la biblioteca de visión artificial *OpenCV* con ROS, para obtener imágenes de la cámara y procesarlas en tiempo real.  
1. Aplicar procesos de filtrado para aislar objetos de interés dentro de una imagen.
1. Desarrollar nodes de detección de objetos y aprovechar la información generada por estos procesos para controlar la posición de un robot.
1. Usar datos de la cámara como señal de retroalimentación para implementar un comportamiento de seguimiento de línea usando control proporcional.

### Enlaces Rápidos

#### Ejercicios

* [Ejercicio 1: Usar el node `rqt_image_view` mientras se cambia el punto de vista del robot](#ex1)
* [Ejercicio 2: Detección de Objetos](#ex2)
* [Ejercicio 3: Usar Momentos de Imagen para el Control del Robot](#ex3)
* [Ejercicio 4: Seguimiento de línea](#ex4)

#### Recursos Adicionales

* [El Código Inicial de Detección de Objetos (para el Ejercicio 2)](./part6/object_detection.md){target="_blank"}
* [Un Ejemplo Completo del Node `object_detection.py`](./part6/object_detection_complete.md){target="_blank"}
* [La Plantilla `line_follower` (para el Ejercicio 4)](./part6/line_follower.md){target="_blank"}

## Primeros Pasos

**Paso 1: Iniciar tu Entorno ROS**

Inicia tu entorno ROS ahora para tener acceso a una instancia de terminal de Linux (también conocida como **TERMINAL 1**).

**Paso 2: Restaurar tu trabajo (SOLO usuarios de WSL-ROS2 en computadoras del laboratorio)**

Recuerda que cualquier trabajo que realices dentro del Entorno WSL-ROS2 no se conservará entre sesiones ni en diferentes computadoras del laboratorio, por lo que debes hacer copias de seguridad de tu trabajo en tu unidad `U:\` regularmente. Cuando se te solicite (al primer inicio de WSL-ROS2 en **TERMINAL 1**), ingresa `Y` para restaurarlo[^1].

[^1]: Recuerda: también puedes usar el comando `wsl_ros restore` en cualquier momento.

**Paso 3: Iniciar VS Code** 

*Usuarios de WSL* [recuerda verificar esto](../software/using-wsl-ros/vscode.md#verify).

**Paso 4: Asegurarse de que el Repositorio del Curso Esté Actualizado**

Verifica que el Repositorio del Curso esté actualizado antes de comenzar estos ejercicios. [Consulta aquí cómo actualizar](./extras/course-repo.md#updating). 

**Paso 5: Iniciar la Simulación del Robot**

En esta sesión comenzaremos trabajando con el mismo entorno de *mundo misterioso* de la Parte 5. En **TERMINAL 1**, usa el siguiente comando para cargarlo:

```bash
ros2 launch rigsa_simulations coloured_pillars.launch.py
```
...y luego espera a que se abra la ventana de Gazebo:

<figure markdown>
  ![](../images/gz/coloured_pillars.png){width=600px}
</figure>

## Trabajando con Cámaras e Imágenes en ROS

### Topics de Cámara y Datos

Hay varias herramientas que podemos usar para ver las imágenes en vivo que captura la cámara de un robot en ROS. Como con todos los datos del robot, estos flujos se publican en *topics*, por lo que primero necesitamos identificar esos topics.

En una nueva instancia de terminal (**TERMINAL 2**), ejecuta `ros2 topic list` para ver la lista completa de topics actualmente activos en nuestro sistema. Convenientemente, ¡todos los topics relacionados con la *camera* de nuestro robot tienen el prefijo `/camera`! Filtra la salida de `ros2 topic list` usando `grep` (un comando de Linux), para mostrar solo los topics con este prefijo:

```bash
ros2 topic list | grep /camera
```

Esto debería proporcionar la siguiente lista filtrada:

``` { .txt .no-copy }
/camera/camera_info
/camera/image_raw
/camera/image_raw/compressed
/camera/image_raw/compressedDepth
/camera/image_raw/theora
/camera/image_raw/zstd
```

El elemento principal que nos interesa aquí son los *datos de imagen sin procesar*, y el topic clave que por lo tanto usaremos es:

``` { .txt .no-copy }
/camera/image_raw
```

Ejecuta `ros2 topic info` sobre este para identificar la interface utilizada por este topic.

Luego, ejecuta `ros2 interface show` sobre la *interface* para conocer el formato de datos. Deberías obtener una salida que se vea así (simplificada ligeramente aquí):

``` { .txt .no-copy }
# This message contains an uncompressed image
# (0, 0) is at top-left corner of image

std_msgs/Header header # Header timestamp should be acquisition time of image
        builtin_interfaces/Time stamp
                int32 sec
                uint32 nanosec
        string frame_id

uint32 height                # image height, that is, number of rows
uint32 width                 # image width, that is, number of columns

string encoding       # Encoding of pixels -- channel meaning, ordering, size
                      # taken from the list of strings in include/sensor_msgs/image_encodings.hpp

uint8 is_bigendian    # is this data bigendian?
uint32 step           # Full row length in bytes
uint8[] data          # actual matrix data, size is (step * rows)
```

<a name="cam_img_questions"></a>

!!! question "Preguntas"
    1. ¿Qué *tipo* de interface usa este topic, y de qué *package* se deriva?
    1. Usando `ros2 topic echo` y la información sobre el mensaje del topic (como se muestra arriba), determina el *tamaño* de las imágenes que capturará la cámara de nuestro robot (es decir, sus *dimensiones*, en píxeles). Será bastante importante conocer esto cuando comencemos a manipular estas imágenes de cámara más adelante. 
    1. Finalmente, considerando la lista anterior nuevamente, ¿qué parte del mensaje crees que contiene los *datos reales de la imagen*?

### Visualizando Flujos de Cámara {#viz}

Podemos *ver* las imágenes que se transmiten al topic de cámara anterior (en tiempo real) de varias maneras diferentes, y exploraremos algunas de ellas ahora.

Una forma es usar *RViz*, que puede iniciarse con el siguiente comando `ros2 launch` en **TERMINAL 2**:

```bash
ros2 launch rigsa_tb3_tools rviz.launch.py environment:=sim
```

Una vez que RViz se inicie, deberías ver un panel de cámara en la esquina inferior izquierda con un flujo en vivo de las imágenes obtenidas de la cámara del robot.

<figure markdown>
  ![Vista de RViz con el robot de simulación y datos de cámara](../images/rviz/waffle_antd.svg){width=800px}
</figure>

Cierra RViz ingresando ++ctrl+c++ en **TERMINAL 2**.  

#### :material-pen: Ejercicio 1: Usar RQT mientras se cambia el punto de vista del robot {#ex1}

Otra herramienta que podemos usar para ver flujos de datos de cámara es *RQT*.

1. Ingresa el siguiente comando en **TERMINAL 2** para iniciarlo:

    ```bash
    rqt
    ```
    <figure markdown>
      ![](../images/rqt/main.png){width=600}
    </figure>

1. En el menú superior selecciona `Plugins` > `Vizualisation` > `Image View`.

    <figure markdown>
      ![](../images/rqt/image_view_antd.svg){width=500px}
    </figure>

    Esto nos permite ver fácilmente imágenes que se están publicando en cualquier topic de cámara en la red ROS. Otra característica útil es la capacidad de guardar estas imágenes (como archivos `.jpg`) en el sistema de archivos: consulta el botón "Save image" resaltado en la figura anterior. Esto podría ser útil más adelante...

1. Haz clic en el cuadro desplegable en la parte superior izquierda de la ventana para seleccionar un topic de imagen para mostrar. Selecciona `/camera/image_raw` (si no está ya seleccionado).

1. Mantén esta ventana abierta ahora e inicia una nueva instancia de terminal (**TERMINAL 3**).

1. Inicia el node `teleop_keyboard`. Rota el robot en el lugar, manteniendo un ojo en la ventana RQT Image View mientras lo haces. Detén el robot una vez que uno de los pilares de colores en la arena esté aproximadamente en el centro del campo de visión del robot, luego cierra el node `teleop_keyboard` y RQT Image View ingresando ++ctrl+c++ en **TERMINAL 3** y **TERMINAL 2** respectivamente.

## OpenCV y ROS {#opencv}

[OpenCV](https://opencv.org/){target="_blank"} es una biblioteca de visión artificial madura y poderosa diseñada para realizar análisis de imágenes en tiempo real, y por lo tanto es extremadamente útil para aplicaciones robóticas. La biblioteca es multiplataforma y tiene una API de Python (`cv2`), que usaremos para realizar algunas tareas de visión artificial por nuestra cuenta durante esta sesión de laboratorio. Si bien podemos trabajar con OpenCV usando Python de inmediato (a través de la API), la biblioteca no puede interpretar directamente el formato de imagen nativo utilizado por ROS, por lo que hay una *interface* que necesitamos usar. La interface se llama [CvBridge](http://wiki.ros.org/cv_bridge){target="_blank"}, que es un *package ROS* que maneja la conversión entre los formatos de imagen ROS y OpenCV. Por lo tanto, necesitaremos usar estas dos bibliotecas (OpenCV y CvBridge) de la mano cuando desarrollemos nodes ROS para realizar tareas relacionadas con visión artificial.

### Detección de Objetos

Una tarea común que a menudo queremos que realice un robot es la *detección de objetos*, e ilustraremos cómo se puede lograr esto usando herramientas de OpenCV para *filtrado de color*, para detectar el pilar de color que tu robot debería estar mirando ahora.  

#### :material-pen: Ejercicio 2: Detección de Objetos {#ex2}

En este ejercicio aprenderás a usar OpenCV para capturar imágenes, filtrarlas y realizar otros análisis para confirmar la presencia y ubicación de características que nos podrían interesar.

##### Paso 1: Primeros Pasos

1. Primero crea un nuevo package llamado `part6_vision` usando [el enfoque habitual](./part1.md#ex4). 

1. Navega hasta el directorio `scripts` de este nuevo package (usando `cd`), crea un nuevo archivo llamado `object_detection.py` (usando `touch`), hazlo ejecutable (`chmod`) y decláralo como ejecutable en el `CMakeLists.txt` del package (lo has hecho muchas veces, pero revisa las partes anteriores del curso si necesitas recordar cómo hacerlo).

1. Abre el archivo Python `object_detection.py` en VS Code y echa un vistazo al siguiente código:

    <center>[:material-file-code-outline: El código `object_detection.py`](./part6/object_detection.md){ .md-button target="_blank" }</center>

    ¡Lee las anotaciones para que entiendas cómo funciona el node y qué debería suceder cuando lo ejecutes!

1. Copia el código en el archivo `object_detection.py` vacío y guárdalo.

1. Compila el package con `colcon`:

    1. En **TERMINAL 2**, asegúrate de estar en la raíz del Workspace:
        
        ```bash
        cd ~/ros2_ws/
        ```

    1. Ejecuta `colcon build`:

        ```bash
        colcon build --packages-select part6_vision --symlink-install 
        ```

    1. Y finalmente re-carga el `.bashrc`:

        ```bash
        source ~/.bashrc
        ```

1. Ejecuta el node usando `ros2 run ...` 
    
    Debería aparecer una imagen de la cámara del robot y luego desaparecer después de unos segundos.
    
1. Como deberías saber por leer la explicación, el node acaba de guardar esta imagen en una ubicación de tu sistema de archivos. Navega a esta ubicación y ve la imagen usando `eog`.

    Lo que puede que hayas notado en la salida del terminal cuando ejecutaste el node `object_detection.py` es que la cámara del robot captura imágenes con un tamaño nativo de 1080x1920 píxeles. ¡Eso son más de *2 millones de píxeles* en total en una sola imagen (2,073,600 píxeles por imagen, para ser exactos), y cada píxel tiene un valor azul, verde y rojo asociado: ¡por lo que hay una gran cantidad de datos en un solo archivo de imagen! 

    !!! question
        El tamaño del archivo de imagen (en bytes) en realidad se imprimió en el terminal cuando ejecutaste el node `object_detection.py`. ¿Notaste qué tan grande era exactamente?

Procesar una imagen de este tamaño es por lo tanto un trabajo arduo para un robot: cualquier análisis que hagamos será lento y cualquier imagen sin procesar que capturemos ocupará una cantidad considerable de espacio de almacenamiento. El siguiente paso entonces es reducir esto recortando la imagen a un tamaño más manejable.

##### Paso 2: Recorte 

Vamos a modificar el node `object_detection.py` ahora para:

* Capturar una nueva imagen en su tamaño nativo
* Recortarla para enfocarse en un área de interés particular
* Guardar ambas imágenes (la recortada debería ser mucho más pequeña que la original)  

<a name="step2"></a>

1. En tu node `object_detection.py` localiza la línea:

    ``` { .python .no-copy}
    self.show_image(img=cv_img, img_name="step1_original")
    ```

1. **Debajo de esto**, agrega las siguientes líneas adicionales de código:

    ```python
    crop_width = width - 400
    crop_height = 400
    crop_y0 = int((width / 2) - (crop_width / 2))
    crop_z0 = int((height / 2) - (crop_height / 2))
    cropped_img = cv_img[crop_z0:crop_z0+crop_height, crop_y0:crop_y0+crop_width]

    self.show_image(img=cropped_img, img_name="step2_cropping")
    ```

1. Ejecuta el node nuevamente.  

    ¡Ahora se te presentarán *dos* ventanas de imagen, pero **ten paciencia**! ¡Tendrás que esperar unos segundos para que cada ventana se abra!

    Navega de regreso al directorio donde se han guardado las imágenes y usa `eog` nuevamente para verlas y examinarlas más de cerca.
    

El código que acabamos de agregar aquí ha creado un nuevo objeto de imagen llamado `cropped_img` a partir de un subconjunto del original (`cv_img`). Esto se logró especificando una `crop_height` y `crop_width` deseadas en relación con las dimensiones originales de la imagen (en píxeles). Además, también hemos especificado *dónde* en la imagen original (en términos de coordenadas de píxeles) queremos que comience este subconjunto, usando `crop_y0` y `crop_z0`. Este proceso se ilustra en la figura siguiente:

<figure markdown>
  ![](part6/ex2/od1_cropping.svg){width=600px}
</figure>

<a name="img_cropping" ></a>La imagen original (`cv_img`) se recorta usando un proceso llamado *"slicing"*:

``` { .python .no-copy }
cropped_img = cv_img[
    crop_z0:crop_z0+crop_height,
    crop_y0:crop_y0+crop_width
]
```
Esto puede parecer bastante confuso, pero con suerte la figura a continuación ilustra lo que está sucediendo aquí:

<figure markdown>
  ![](part6/ex2/img_slicing.svg){width=500px}
</figure>

##### Paso 3: Enmascaramiento

Como se discutió anteriormente, una imagen es esencialmente una serie de píxeles cada uno con un valor azul, verde y rojo asociado para representar los colores reales de la imagen. De la imagen original que acabamos de obtener y recortar, *ahora* queremos deshacernos de cualquier color que no esté asociado con el pilar que queremos que el robot detecte. Por lo tanto, necesitamos aplicar un *filtro* a los píxeles, que usaremos en última instancia para descartar cualquier dato de píxel que no esté relacionado con el pilar de color, mientras retenemos los datos que sí lo están.  

Este proceso se llama *enmascaramiento* y, para lograrlo, necesitamos establecer algunos umbrales de color. Esto puede ser difícil de hacer en un espacio de color estándar Azul-Verde-Rojo (BGR) o Rojo-Verde-Azul (RGB), y puedes ver un buen ejemplo de esto en [este artículo de RealPython.com](https://realpython.com/python-opencv-color-spaces/){target="_blank"}. Aplicaremos algunos pasos discutidos en este artículo para convertir nuestra imagen recortada a un espacio de color [Tono-Saturación-Valor (HSV)](https://en.wikipedia.org/wiki/HSL_and_HSV){target="_blank"} en su lugar, lo que facilita un poco el proceso de enmascaramiento de color.

1. Primero, analiza los valores de *Tono* y *Saturación* de la imagen recortada. Para hacer esto, navega al directorio `~/object_detection`, donde se están guardando todas las imágenes sin procesar:

    ```bash
    cd ~/object_detection
    ```
    
    Luego, ejecuta el siguiente node ROS (del package `rigsa_examples`), proporcionando el nombre de la imagen recortada como argumento adicional:<a name="img_cols_node"></a>
    
    ```bash
    ros2 run rigsa_examples image_colours.py step2_cropping.jpg
    ```
    
1. El node debería producir un diagrama de dispersión, ilustrando los valores de Tono y Saturación de cada uno de los píxeles en la imagen. Cada punto de datos en el gráfico representa un solo píxel de la imagen y cada uno está coloreado para coincidir con su valor RGB:

    <figure markdown>
      ![](part6/ex2/od2_hs_scatter.png){width=600px}
    </figure>

1. Deberías ver en la imagen que todos los píxeles relacionados con el pilar de color que queremos detectar están agrupados juntos. Podemos usar esta información para especificar un rango de valores de Tono y Saturación que se pueden usar para enmascarar nuestra imagen: filtrando cualquier color que esté fuera de este rango y permitiéndonos aislar el pilar en sí. Los píxeles también tienen un *Valor* (o *"Brillo"*), que no se muestra en este gráfico. Como regla general, un rango de valores de brillo entre 100 y 255 generalmente funciona bastante bien.

    <figure markdown>
      ![](part6/ex2/od3_hs_thresholds.svg){width=600px}
    </figure>

    En este caso entonces, seleccionamos los umbrales HSV superior e inferior de la siguiente manera:

    ```python
    lower_threshold = (115, 225, 100)
    upper_threshold = (130, 255, 255)
    ```

    Usa el gráfico que has generado tú mismo para determinar tus *propios* umbrales superior e inferior. <a name="bw_and"></a>

    OpenCV contiene una función integrada para detectar qué píxeles de una imagen caen dentro de un rango HSV especificado: `cv2.inRange()`. Esto produce una matriz, del mismo tamaño y forma que el número de píxeles en la imagen, pero que contiene solo valores `True` (`1`) o `False` (`0`), que ilustran qué píxeles *sí* tienen un valor dentro del rango especificado y cuáles no. Esto se conoce como una *Máscara Booleana* (esencialmente, una serie de unos o ceros). Luego podemos aplicar esta máscara a la imagen, usando una operación [Bitwise AND](https://en.wikipedia.org/wiki/Bitwise_operation#AND){target="_blank"}, para deshacernos de cualquier píxel de imagen cuyo valor de máscara sea `False` y mantener cualquiera marcado como `True` (o *dentro del rango*).

1. Para hacer esto, primero localiza la siguiente línea en tu node `object_detection.py`:

    ``` { .python .no-copy }
    self.show_image(img=cropped_img, img_name="step2_cropping")
    ```

1. Debajo de esto, agrega lo siguiente:

    ```python
    hsv_img = cv2.cvtColor(cropped_img, cv2.COLOR_BGR2HSV)
    lower_threshold = (115, 225, 100)
    upper_threshold = (130, 255, 255)
    img_mask = cv2.inRange(hsv_img, lower_threshold, upper_threshold)

    self.show_image(img=img_mask, img_name="step3_image_mask")
    ```

1. Ahora, ejecuta el node nuevamente. Ahora también debería generarse una *tercera* imagen. 
    
    Como se muestra en la figura a continuación, la tercera imagen debería ser simplemente una representación en blanco y negro de la imagen recortada, donde las regiones blancas deberían indicar las áreas de la imagen donde los valores de píxeles caen dentro del rango HSV especificado anteriormente. 
    
    Observa (en el texto impreso en el terminal) que la imagen recortada y la máscara de imagen tienen las mismas dimensiones, pero el archivo de máscara de imagen tiene un tamaño de archivo significativamente menor. Si bien la máscara contiene el mismo *número* de píxeles, estos píxeles solo tienen un valor de `1` o `0`, mientras que, en la imagen recortada del mismo tamaño en píxeles, cada píxel tiene un valor Rojo, Verde y Azul: cada uno con un rango entre `0` y `255`, lo que representa significativamente más datos.

    <figure markdown>
      ![](part6/ex2/od4_masking.svg){width=600px}
    </figure>

##### Paso 4: Filtrado {#bitwise_and}

Finalmente, podemos aplicar esta máscara a la imagen recortada, generando una versión final de ella donde solo los píxeles marcados como `True` en la máscara retienen sus valores RGB, y el resto simplemente se elimina. [Como se discutió anteriormente](#bw_and), usamos una operación *Bitwise AND* para hacer esto y, una vez más, OpenCV tiene una función integrada para esto: `cv2.bitwise_and()`.

1. Localiza la siguiente línea en tu node `object_detection.py`:

    ``` { .python .no-copy }
    self.show_image(img=img_mask, img_name="step3_image_mask")
    ```

1. Y, debajo de esto, agrega lo siguiente:

    ```python
    filtered_img = cv2.bitwise_and(cropped_img, cropped_img, mask = img_mask)

    self.show_image(img=filtered_img, img_name="step4_filtered_image")
    ```

1. Ejecuta este node nuevamente, y ahora también debería generarse una cuarta imagen, esta vez mostrando la imagen recortada tomada de la cámara del robot, pero que solo contiene datos relacionados con el pilar de color, con todos los demás datos de imagen de fondo eliminados (y renderizados en negro):

    <figure markdown>
      ![](part6/ex2/od5_filtering.svg){width=600px}
    </figure>

### Momentos de Imagen

Ahora has aislado exitosamente un objeto de interés dentro del campo de visión de tu robot, pero quizás queremos hacer que nuestro robot se mueva hacia él, o, por el contrario, hacer que nuestro robot navegue alrededor de él y evite chocar con él. Por lo tanto, también necesitamos saber la *posición* del objeto en relación con el punto de vista del robot, y podemos hacer esto usando **momentos de imagen**.

El trabajo que acabamos de hacer arriba nos llevó a obtener lo que se conoce como un *blob de color*. OpenCV también tiene herramientas integradas que nos permiten calcular el *centroide* de un blob de color como este, lo que nos permite determinar exactamente dónde dentro de una imagen se encuentra el objeto de interés (en términos de píxeles). Esto se hace usando el principio de *momentos de imagen*: esencialmente parámetros estadísticos relacionados con una imagen, que nos indican cómo se distribuye una colección de píxeles (es decir, el blob de color que acabamos de aislar) dentro de ella. [Puedes leer más sobre los Momentos de Imagen aquí](https://theailearner.com/tag/image-moments-opencv-python/){target="_blank"}. Usando este proceso, las coordenadas centrales de un blob de color se pueden obtener considerando algunos momentos clave de la *máscara de imagen* que obtuvimos anteriormente del umbralado:

* $M_{00}$: la suma de todos los píxeles no nulos en la máscara de imagen (es decir, el tamaño del blob de color, en píxeles)
* $M_{10}$: la suma de todos los píxeles no nulos en el eje horizontal (y), ponderada por el número de *fila*
* $M_{01}$: la suma de todos los píxeles no nulos en el eje vertical (z), ponderada por el número de *columna*

!!! info "Recuerda"
    Nos referimos al eje *horizontal* como el *eje y* y al eje *vertical* como el *eje z* aquí, para coincidir con la terminología que hemos usado anteriormente para definir [los ejes principales de nuestro robot](./part2.md#principal-axes).

En realidad no necesitamos preocuparnos demasiado por la derivación de estos momentos. OpenCV tiene una función integrada `moments()` que podemos usar para obtener esta información de una máscara de imagen (como la que generamos anteriormente):

```python
m = cv2.moments(img_mask)
```

Entonces, usando esto podemos obtener las coordenadas `y` y `z` del centroide del blob de manera bastante sencilla:

```python
cy = m['m10']/(m['m00']+1e-5)
cz = m['m01']/(m['m00']+1e-5) 
```

!!! question
    Estamos sumando un número muy pequeño al momento $M_{00}$ aquí para asegurarnos de que el divisor en las ecuaciones anteriores nunca sea cero y así garantizar que nunca nos sorprenda ningún error de "división por cero". ¿Por qué podría ser esto necesario?

<figure markdown>
  ![](part6/ex2/od6_centroid.svg){width=600px}
</figure>

Una vez más, hay una herramienta integrada de OpenCV que podemos usar para agregar un círculo en una imagen para ilustrar la ubicación del centroide dentro del campo de visión del robot: `cv2.circle()`. Así es como produjimos el círculo rojo que puedes ver en la figura anterior. Puedes ver cómo se implementa esto aquí:

<center>[:material-file-code-outline: Un ejemplo completo del node `object_detection.py`](./part6/object_detection_complete.md){ .md-button target="_blank" }</center> 

En nuestro caso, en realidad no podemos cambiar la posición de nuestro robot en el eje z, por lo que el componente de centroide `cz` aquí puede no ser tan importante para nosotros con fines de navegación. Sin embargo, es posible que queramos usar la coordenada de centroide `cy` para entender dónde se encuentra una característica *horizontalmente* en el campo de visión de nuestro robot, y usar esta información para girar hacia ella (o alejarse de ella, dependiendo de lo que estemos tratando de lograr). Podemos entonces usar esto como base para un **control de bucle cerrado** real.

#### :material-pen: Ejercicio 3: Usar Momentos de Imagen para el Control del Robot {#ex3}

Dentro del package `rigsa_examples` hay un node que ha sido desarrollado para ilustrar cómo todas las herramientas de OpenCV que has explorado hasta ahora podrían usarse para buscar en un entorno y detener un robot cuando está mirando directamente a un objeto de interés. Todas las herramientas utilizadas en este node deberían resultarte familiares a estas alturas, y en este ejercicio vas a hacer una copia de este node y modificarlo para mejorar su funcionalidad.

Asegúrate de que el mundo "Coloured Pillars" siga activo y continúa con los siguientes pasos ahora en **TERMINAL 2**.

1. El node se llama `colour_search.py`, y se encuentra en la carpeta `scripts` del package `rigsa_examples`. Cópialo en la carpeta `scripts` de tu propio package `part6_vision` asegurándote primero de estar ubicado en la carpeta de destino deseada:

    ```bash
    cd ~/ros2_ws/src/part6_vision/scripts
    ```
    
1. Luego, copia el node `colour_search.py` usando `cp` de la siguiente manera:

    ```bash
    cp ~/ros2_ws/src/rigsa_ros/rigsa_examples/scripts/colour_search.py ./
    ```

1. Abre el archivo `colour_search.py` en VS Code para ver el contenido. Examínalo y ve si puedes entender cómo funciona. La estructura general debería ser bastante familiar para ti a estas alturas: tenemos una estructura de clase Python, un Subscriber con una función callback, un temporizador con un callback que contiene todo el código de control del robot, y muchas de las herramientas de OpenCV que has explorado hasta ahora en esta parte del curso. Esencialmente este node funciona de la siguiente manera:
    1. El robot gira en el lugar mientras obtiene imágenes de su cámara (suscribiéndose al topic `/camera/image_raw`).
    1. Se obtienen imágenes de la cámara, se recortan, y luego se aplica un umbral a las imágenes recortadas para detectar el pilar azul en el entorno simulado.
    1. Si el robot no puede ver un pilar azul, gira en el lugar **rápidamente**.
    1. Una vez detectado, el centroide del blob azul que representa el pilar se calcula para obtener su *ubicación* actual en el campo de visión del robot.
    1. Tan pronto como el pilar azul entra en el campo de visión, el robot comienza a girar más **lentamente**.
    1. El robot **se detiene** girando tan pronto como determina que el pilar está situado directamente frente a él (determinado usando el componente `cy` del centroide del blob azul).
    1. El robot luego **espera** un tiempo y luego comienza a girar nuevamente.
    1. Todo el proceso se repite hasta que encuentra el pilar azul nuevamente.

1. Agrega el node `colour_search.py` a la lista de ejecutables Python en tu archivo `part6_vision/CMakeLists.txt`.

1. Agrega la siguiente dependencia adicional a tu `part6_vision/package.xml`:

    ```xml
    <exec_depend>geometry_msgs</exec_depend>
    ```

1. Recompila tu package con `colcon`.

1. Ejecuta el node tal como está para verlo en acción. Observa los mensajes de registro mientras se imprimen en el terminal durante la ejecución.

1. **Tu tarea** es entonces modificar el node para que se detenga frente a *cada pilar de color* en la arena (hay cuatro en total, cada uno de un color diferente, como sabes). Para esto, es posible que necesites usar algunos de los métodos que has explorado en los ejercicios anteriores.
    1. Primero es posible que quieras usar algunos de los métodos que usamos para obtener y analizar algunas imágenes de la cámara del robot:
        1. Usa el node `teleop_keyboard` para mover manualmente el robot, haciéndolo mirar a cada pilar de color en la arena individualmente.
        1. Ejecuta el node `object_detection.py` que desarrollaste en el ejercicio anterior para capturar una imagen, recortarla, guardarla en el sistema de archivos y luego introducir esta imagen recortada en el node `image_colours.py` del package `rigsa_examples` ([como lo hiciste anteriormente](#img_cols_node))
        1. A partir del gráfico generado por el node `image_colours.py`, determina algunos umbrales HSV apropiados para aplicar a cada pilar de color en la arena.
    1. Una vez que tengas los umbrales correctos, puedes agregarlos a tu node `colour_search.py` para que tenga la capacidad de detectar *cada* pilar de la misma manera que actualmente detecta el azul.

### Control PID y Seguimiento de Línea {#pid}

¡El seguimiento de línea es una habilidad útil para un robot! Podemos lograrlo en el robot de simulación usando su sistema de cámara y las técnicas de procesamiento de imágenes que se han cubierto hasta ahora en esta sesión.

Un algoritmo bien establecido para el control de bucle cerrado se conoce como **Control PID**, y esto puede usarse para lograr dicho comportamiento de seguimiento de línea.

En el corazón de esto está el principio del control de *Retroalimentación Negativa*, que considera una **Entrada de Referencia**, una **Señal de Retroalimentación** y el **Error** entre estas.

<a name="neg_fdbck_ctrl"></a>

<figure markdown>
  ![](part6/pid/negative_feedback_control.png){width=500}
  <figcaption>
    Control de Retroalimentación Negativa<br />
    Adaptado de <a href="https://commons.wikimedia.org/wiki/File:PID_en.svg">Arturo Urquizo</a>, <a href="https://creativecommons.org/licenses/by-sa/3.0">CC BY-SA 3.0</a>, via Wikimedia Commons</a>
  </figcaption>
</figure>

La **Entrada de Referencia** representa un estado deseado que nos gustaría que nuestro sistema mantuviera. Si queremos que el robot siga exitosamente una línea de color en el suelo, necesitará mantener el blob de color que representa esa línea de color en el centro de su punto de vista en todo momento. El *estado deseado* sería por lo tanto mantener el centroide `cy` del blob de color en el centro de su visión.

Una **Señal de Retroalimentación** nos informa de cuál es el estado actual real del sistema. En nuestro caso, esta señal de retroalimentación sería la ubicación en tiempo real de la línea de color en las imágenes de cámara en vivo, es decir, su centroide `cy` (obtenido usando métodos de procesamiento como los cubiertos en el Ejercicio 3 anterior). 

La diferencia entre estas dos cosas es el **Error**, y el algoritmo de control PID nos proporciona un medio para controlar este error y minimizarlo, de modo que el estado *actual* de nuestro robot coincida con el estado *deseado*. Es decir: la línea de color siempre está en el centro de su campo de visión.

<a name="pid_terms"></a>

<figure markdown>
  ![](part6/pid/terms.png){width=700px}
</figure>

<a name="pid_eqn"></a>

El algoritmo PID es el siguiente:

$$
u(t)=K_{P} e(t) + K_{I}\int e(t)dt + K_{D}\dfrac{d}{dt}e(t)
$$

Donde $u(t)$ es la **Salida Controlada**, $e(t)$ es el **Error** (como se ilustra en la figura anterior) y $K_{P}$, $K_{I}$ y $K_{D}$ son las **Ganancias** Proporcional, Integral y Diferencial respectivamente. Estas tres ganancias son constantes que deben establecerse para cualquier sistema dado mediante un proceso llamado *sintonización*. Exploraremos este proceso de sintonización en el ejercicio práctico que sigue.

#### :material-pen: Ejercicio 4: Seguimiento de Línea {#ex4}

##### Parte A: Configuración {#ex4a}

1. Asegúrate de que todos los procesos ROS del ejercicio anterior estén cerrados ahora, incluido el node `colour_search.py` y la simulación de Gazebo en **TERMINAL 1**.

1. En **TERMINAL 1** inicia una nueva simulación del package `rigsa_simulations`:

    ```bash
    ros2 launch rigsa_simulations line_following.launch.py tuning:=true
    ```
    
    Tu robot debería ser lanzado en una pista larga y estrecha con una línea rosa pintada en el centro del suelo:

    <figure markdown>
      ![](part6/line_following/setup.png){width=800px}
    </figure>

1. En **TERMINAL 2** deberías seguir ubicado en tu directorio `part6_vision/scripts`, pero si no es así, ve allí ahora:

    ```bash
    cd ~/ros2_ws/src/part6_vision/scripts
    ```

1. Realiza los pasos necesarios para crear un nuevo archivo Python vacío llamado `line_follower.py` y prepáralo para su ejecución como node dentro de tu package.

1. Una vez hecho eso, abre el archivo vacío en VS Code y echa un vistazo a la siguiente plantilla de código:
    
    <center>[:material-file-code-outline: La plantilla de código `line_follower.md`](./part6/line_follower.md){ .md-button target="_blank" }</center>

    La plantilla contiene tres "TODOs" que debes completar, todos los cuales se explican en detalle en las anotaciones del código, así que léelas cuidadosamente. En última instancia, todo esto lo hiciste en el [Ejercicio 2](#ex2), así que regresa aquí si necesitas un recordatorio de cómo funciona algo. 

    Tu objetivo aquí es hacer que el código genere una imagen recortada, con la línea de color aislada y ubicada dentro de ella, así:

    <figure markdown>
      ![](part6/line_following/setup_complete.jpg)
    </figure> 

##### Parte B: Implementación y Sintonización de un Controlador Proporcional {#ex4b}

Refiriéndonos de vuelta a [la ecuación del algoritmo PID discutida anteriormente](#pid_eqn), los componentes Proporcional, Integral y Diferencial tienen diferentes efectos en un sistema en términos de su capacidad para mantener el estado deseado (la entrada de referencia). Los términos de ganancia asociados con cada uno de estos componentes ($K_{P}$, $K_{I}$ y $K_{D}$) deben ser *sintonizados* apropiadamente para cualquier sistema dado para lograr la estabilidad del control.

Un Controlador PID puede tomar tres formas diferentes:

1. **Control "P"**: Solo se usa una ganancia *Proporcional* ($K_{P}$), todas las demás ganancias se establecen en cero.
1. **Control "PI"**: Se aplican ganancias *Proporcional* e *Integral* ($K_{P}$ y $K_{I}$), la ganancia Diferencial se establece en cero. 
1. **Control "PID"**: El controlador hace uso de los tres términos de ganancia ($K_{P}$, $K_{I}$ y $K_{D}$)

Para permitir que el robot siga una línea, en realidad solo necesitamos un **Controlador "P"**, por lo que nuestra ecuación de control se vuelve bastante simple, reduciéndose a:

$$
u(t)=K_{P} e(t)
$$

La siguiente tarea entonces es adaptar nuestro node `line_follower.py` para implementar este algoritmo de control y encontrar una ganancia proporcional apropiada para nuestro sistema.

1. Regresa a tu archivo `line_follower.py`. Debajo de la línea que dice:

    ```python
    cv2.waitKey(1)
    ```

    Pega el siguiente código adicional:

    ```python
    kp = self.get_parameter('kp').get_parameter_value().double_value
    reference_input = ?
    feedback_signal = cy
    error = feedback_signal - reference_input 

    ang_vel = kp * error
    self.get_logger().info(
        f"\nkp = {kp:.4f},"
        f"\nError = {error:.1f} pixels,"
        f"\nControl Signal = {ang_vel:.2f} rad/s."
    )
    ```

    <a name="blank-1"></a>

    !!! warning "¡Completa el Espacio en Blanco!"
        ¿Cuál es la **Entrada de Referencia** al sistema de control (`reference_input`)? Consulta [esta figura de antes](#pid_terms). 

    Aquí hemos implementado nuestro Controlador "P". La **Señal de Control** que se está calculando aquí es la velocidad angular que se aplicará a nuestro robot (¡el código no hará que el robot se mueva todavía, pero llegaremos a esa parte pronto!). La **Salida Controlada** será por lo tanto la posición angular (es decir, el **yaw**) del robot.  

1. Ejecuta el código tal como está y considera lo siguiente:

    1. ¿Qué ganancia proporcional ($K_{P}$) estamos aplicando?
    1. ¿Cuál es [la velocidad angular máxima que se puede aplicar a nuestro robot](../about/robots.md#max_vels)? ¿Es la velocidad angular que se ha calculado realmente apropiada?
    1. ¿La velocidad angular calculada es positiva o negativa? ¿Esto hará que el robot gire en la dirección correcta y se mueva hacia la línea?  

1. Abordemos primero la tercera pregunta (**c**)...

    Una velocidad angular **positiva** debería hacer que el robot gire en sentido **antihorario** (es decir, hacia la izquierda), y una velocidad angular **negativa** debería hacer que el robot gire en sentido **horario** (hacia la derecha).
    
    Para empezar, la línea debería estar a la izquierda del robot, lo que significa que se requiere una velocidad angular **positiva** para hacer que el robot gire hacia ella. 
    
    Si el valor de la **Señal de Control** que está calculando nuestro controlador proporcional (como se imprime en el terminal) es negativo, entonces esto no es correcto. 
    
    El signo de nuestra ganancia proporcional ($K_{P}$) debe cambiarse para corregir esto. $K_{P}$ se define en nuestro código como un *Parámetro* llamado `kp`, y si no definimos explícitamente un valor para esto (lo cual hasta ahora no hemos hecho) entonces se usará un valor predeterminado. Definimos este valor predeterminado en el `#!py __init__()` de nuestro Node, cuando declaramos el parámetro por primera vez:

    ```python
    self.declare_parameter("kp", 0.01)
    ```

    Con tu node todavía en ejecución, cambia el valor ahora con una llamada `ros2 param` desde **TERMINAL 3**:

    ```txt
    ros2 param set /line_follower kp -0.01
    ```
    ... el valor de la **Señal de Control** (es decir, `ang_vel`) debería ser ahora mayor que cero, lo que (cuando los comandos de velocidad se publiquen realmente) hará que el robot gire *hacia la izquierda*, es decir, *hacia* la línea, tratando así de *minimizar* el error de posición.

1. Detén el node con ++ctrl+c++. Cambia el código para que la línea `declare_parameter()` ahora establezca el parámetro `kp` como negativo por defecto:

    ```py
    self.declare_parameter("kp", -0.01)
    ```

1. A continuación, abordemos la segunda de las preguntas anteriores (**b**)...

    La velocidad angular máxima que se puede aplicar a nuestro robot es &plusmn;1.82 rad/s. Si nuestro controlador proporcional está calculando un valor para la **Señal de Control** que es mayor que 1.82, o menor que -1.82, entonces esto necesita limitarse. **Entre** las siguientes dos líneas de código:

    ``` { .python .no-copy }
    ang_vel = kp * error
    self.get_logger().info(...
    ```

    Inserta lo siguiente:
    ```python
    if ang_vel < -1.82:
        ang_vel = -1.82
    elif ang_vel > 1.82:
        ang_vel = 1.82
    ```

1. Finalmente, necesitamos pensar en la ganancia proporcional que se está aplicando. Aquí es donde necesitamos *sintonizar* nuestro sistema encontrando un valor de ganancia proporcional ($K_{P}$) que controle nuestro sistema apropiadamente.

    Regresa a tu archivo `line_follower.py`. **Debajo** de las líneas que dicen:

    ``` { .python .no-copy }
    self.get_logger().info(
        f"\nkp = {kp:.4f},"
        f"\nError = {error:.1f} pixels,"
        f"\nControl Signal = {ang_vel:.2f} rad/s."
    )
    ```

    Pega lo siguiente:

    ```python
    self.vel_cmd.twist.linear.x = 0.1
    self.vel_cmd.twist.angular.z = ang_vel
    self.vel_pub.publish(self.vel_cmd)
    ```

    Una vez en ejecución, el código *debería* hacer que el robot se mueva con una velocidad lineal constante de 0.1 m/s en todo momento, mientras que su velocidad angular estará determinada por nuestro controlador proporcional, basado en el error del controlador y el parámetro de ganancia proporcional `kp`.

    La figura a continuación ilustra los efectos que diferentes valores de ganancia proporcional pueden tener en un sistema.

    <figure markdown>
      ![](part6/pid/kp.png){width=600}
      <figcaption>
        Cortesía de Prof. Roger Moore<br />
        Tomado de Clase 6: Control PID
      </figcaption>
    </figure>

    Ejecuta el código y observa lo que sucede. Deberías encontrar que el robot se comporta de manera bastante errática, lo que indica que `kp` (actualmente en 0.01) probablemente sea demasiado grande.

1. Intenta reducir `kp` por un factor de 100. Desde **TERMINAL 3**: 
    
    ```txt
    ros2 param set /line_follower kp -0.0001
    ```
    
    Con una ganancia `kp` modificada, deberías encontrar que el robot ahora se acerca gradualmente a la línea, pero puede tardar un tiempo en hacerlo.

    !!! tip

        La línea que el robot está intentando seguir es bastante larga, pero si llega al final de ella, o si se desvía y termina bastante lejos de la línea, siempre puedes:
        
        1. Detener tu node `line_following.py` con ++ctrl+c++.
        1. Iniciar el node `teleop_keyboard`:

            ```txt
            ros2 run turtlebot3_teleop teleop_keyboard
            ```
        1. Conducir el robot de regreso a la línea manualmente.
        1. Detener el node `teleop_keyboard` con ++ctrl+c++ y luego iniciar tu node `line_following.py` nuevamente. 
        
1. A continuación, aumenta `kp` por un factor de 10: 
    
    Una vez más (si es necesario), usa el node `teleop_keyboard` para llevar el robot de regreso a la línea de inicio. Luego, vuelve a iniciar el node `line_follower.py`.
    
    Actualiza la ganancia proporcional una vez más con una llamada `ros2 param`: 
    
    ```txt
    ros2 param set /line_follower kp -0.001
    ```
    
    Con esta nueva ganancia `kp`, el robot debería llegar a la línea mucho más rápido y seguir la línea bien una vez que llegue a ella.

1. ¿Se podría modificar más `kp` para mejorar el control? Experimenta un poco más y observa lo que sucede. Pondremos esto a prueba en una pista más desafiante en la siguiente parte de este ejercicio.

##### Parte C: Seguimiento de Línea Avanzado {#ex4c}

1. Cierra el entorno de *"sintonización"* de Seguimiento de Línea si todavía está en ejecución.

1. Luego, en **TERMINAL 1** inicia uno nuevo:

    ```bash
    ros2 launch rigsa_simulations line_following.launch.py
    ```
    
    Tu robot debería ser lanzado a un entorno con una línea más interesante que seguir:

    <figure markdown>
      ![](part6/line_following/advanced.png){width=800px}
    </figure>

1. En **TERMINAL 2**, ejecuta tu node `line_follower.py` y observa su desempeño. ¿Necesita ajustarse más la ganancia proporcional para optimizar el rendimiento?

1. A continuación, piensa en condiciones donde la línea inicialmente no puede verse...

    Como sabes, la velocidad angular se determina considerando el componente `cy` de un blob de color que representa la línea. ¿Qué sucede en situaciones donde el blob de color no está ahí? ¿Qué influencia tendría esto en las Señales de Control que calcula el controlador proporcional? Para considerar esto más a fondo, intenta lanzar el robot en la misma arena pero con una pose de inicio diferente, y piensa cómo podrías abordar esta situación:

    ```txt
    ros2 launch rigsa_simulations line_following.launch.py \
        x_pose:=-3 y_pose:=-3 yaw:=-1.57
    ```

1. Finalmente, ¿qué sucede cuando el robot llega a la línea de llegada? ¿Cómo podrías agregar funcionalidad adicional para asegurarte de que el robot se detenga cuando llegue a este punto? ¿Qué características de la arena podrías usar para activar esto?

## Conclusión

En esta sesión has aprendido a usar datos de la cámara de un robot para extraer más información sobre su entorno. La cámara permite que nuestro robot "vea" y la información que obtenemos de este dispositivo puede permitirnos desarrollar comportamientos robóticos más avanzados como buscar objetos, seguir cosas o, por el contrario, alejarse o evitarlos. Has aprendido a realizar algunas tareas básicas con OpenCV, pero esta es una biblioteca enorme y muy capaz de herramientas de visión artificial, y te animamos a explorar esto más por tu cuenta para mejorar algunos de los principios básicos que te hemos mostrado hoy.

### Usuarios de WSL-ROS2 en computadoras del laboratorio: ¡Guarda tu trabajo! {#backup}

Recuerda guardar el trabajo que has realizado en WSL-ROS2 durante esta sesión para poder restaurarlo en una máquina diferente en una fecha posterior. Ejecuta el siguiente script en cualquier instancia de Terminal WSL-ROS2 inactiva ahora:

```bash
wsl_ros backup
```

Luego podrás restaurarlo a un entorno WSL-ROS2 nuevo cuando lo necesites de nuevo (`wsl_ros restore`).
