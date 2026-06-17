---
title: "Parte 6: Node de Detección de Objetos (Completo)"  
---

# Parte 6: Node de Detección de Objetos (Completo)

Aquí tienes un ejemplo completo del node `object_detection.py` que deberías haber desarrollado durante el [Ejercicio 2 de la Parte 6](../part6.md#ex2). También se incluye aquí una ilustración de cómo usar el método `cv2.circle()` para crear un marcador en una imagen que ilustre el centroide de la característica detectada, como se discute [aquí](../part6.md#image-moments).

```py title="object_detection_complete.py"
--8<-- "code_templates/object_detection_complete.py"
```

1. Todo aquí debería serte familiar de antes en este ejercicio, excepto esta sección...

2. Aquí obtenemos los momentos de nuestro blob de color proporcionando la representación booleana de él (es decir, el `img_mask`) a la función `cv2.moments()`.

3. Luego determinamos *dónde* se encuentra el punto central de este blob de color calculando las coordenadas `cy` y `cz` del mismo. Esto nos proporciona coordenadas de píxeles relativas a la esquina superior izquierda de la imagen.

4. Finalmente, esta función nos permite dibujar un círculo en nuestra imagen en la ubicación del centroide para que podamos visualizarlo. A esta función le pasamos:

    1. La imagen en la que queremos que se dibuje el círculo. En este caso: `filtered_img`.
    1. La *ubicación* donde queremos que se coloque el círculo, especificando las coordenadas de píxeles horizontales y verticales respectivamente: `(int(cy), int(cz))`.
    1. Qué tan *grande* queremos que sea el círculo: aquí especificamos un radio de 10 píxeles.
    1. El *color* del círculo, especificándolo usando un espacio de color Azul-Verde-Rojo: `(0, 0, 255)` (es decir: rojo puro en este caso)
    1. Finalmente, el grosor de la línea que se usará para dibujar el círculo, en píxeles.
