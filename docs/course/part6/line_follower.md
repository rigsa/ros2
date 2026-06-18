---
title: "Parte 6: Configuración del Seguimiento de Línea"  
---

# Parte 6: Configuración del Seguimiento de Línea

Usa este código como punto de partida para la Parte A del ejercicio de Seguimiento de Línea.

```py title="line_follower.py"
--8<-- "code_templates/line_follower.py"
```

1. **Recorte de Imagen** 

    Aplica algo de recorte a la imagen sin procesar de la cámara (`cv_img`). 
    
    Recórtala a alrededor de 1/5 de su **altura** original, y a un **ancho** tal que la línea rosa sea apenas visible en el borde de la imagen. 

    Llama a tu nueva imagen recortada algo como `cropped_img`. Luego puedes usar el método `cv2.imshow()` para mostrarla en una ventana emergente adicional cuando se ejecute el node: 
    
    ```python
    cv2.imshow("cropped_image", cropped_img)
    ``` 

    <figure markdown>
      ![](line_following/partA_todo1.png)
    </figure>

2. **Detección de Color**

    Filtra la imagen recortada seleccionando valores HSV apropiados para que la línea rosa pueda aislarse del resto de la imagen.
    
    Es posible que necesites usar el node `rigsa_examples\image_colours.py` nuevamente para ayudarte a identificar el rango correcto de valores de Tono y Saturación.

    Usa `cv2.cvtColor()` para convertir tu `cropped_img` en una representación de color HSV:

    ```python
    hsv_img = cv2.cvtColor(cropped_img, cv2.COLOR_BGR2HSV)
    ```

    Usa `cv2.inRange()` para crear una máscara con el rango de valores HSV que has determinado:

    ```python
    line_mask = cv2.inRange(
        hsv_img, {lower_hsv_values}, {upper_hsv_values}
    )
    ```
    
    Y luego usa `cv2.bitwise_and()` para crear una nueva imagen con la máscara aplicada, de modo que la línea de color quede aislada:

    ```python
    line_isolated = cv2.bitwise_and(
        cropped_img, cropped_img, mask = line_mask
    )
    ``` 

    <figure markdown>
      ![](line_following/partA_todo2.jpg)
    </figure>

3. **Localización de la línea**

    Finalmente, encuentra la posición horizontal de la línea en el campo de visión del robot.
    
    Calcula los momentos de imagen del blob de color rosa que representa la línea (`line_mask`) usando el método `cv2.moments()`. Recuerda que es el componente $c_{y}$ el que nos interesa aquí:
    
    $$
    c_{y}=\dfrac{M_{10}}{M_{00}}
    $$

    En última instancia, esto nos proporcionará la señal de retroalimentación que podemos usar para un **controlador proporcional** que implementaremos en la siguiente parte del ejercicio.

    Una vez que hayas obtenido los momentos de imagen (y `cy`), usa `cv2.circle()` para marcar el centroide de la línea en la imagen filtrada (`line_isolated`) con un círculo. Para esto, también necesitarás calcular el componente $c_{z}$ del centroide:

    $$
    c_{z}=\dfrac{M_{01}}{M_{00}}
    $$

    Recuerda que una vez que hayas hecho todo esto, puedes mostrar la imagen filtrada de la línea aislada (con el círculo para indicar la ubicación del centroide) usando `cv2.imshow()` nuevamente:
    
    ```python
    cv2.imshow("filtered line", line_isolated)
    ```

    <figure markdown>
      ![](line_following/partA_todo3.jpg)
    </figure>
