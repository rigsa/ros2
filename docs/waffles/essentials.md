---  
title: Consideraciones Esenciales 
---

En ocasiones, los robots reales se comportan de maneras inesperadas. Ciertas cosas funcionan de forma diferente en el hardware real que en una simulación. En esta página destacamos una serie de *aspectos clave que debes investigar ^^lo antes posible^^*, para evitar sorpresas desagradables en el laboratorio.

## Movimiento y Control de Velocidad

1. **¿Qué ocurre si no le indicas explícitamente a un robot que se detenga?**

    Esto no es diferente en el mundo real que en una simulación, pero considera lo que tuvimos que hacer **[en este Ejercicio](./basics.md#exSimpleVelCtrl)** para detener el robot, y por qué es importante [construir nodos con procedimientos de apagado adecuados](../course/part2.md#ex5).

1. **¿Cuáles son los límites de velocidad máxima del robot, y qué ocurre si se exceden?**

    Los sistemas físicos tienen sus límites, ¡y ningún motor puede girar a una velocidad ilimitada! [Nuestros robots tienen límites de velocidad máxima](../about/robots.md#max_vels), y es importante que los conozcas. Intenta enviar un comando de velocidad a un robot que esté fuera del rango de velocidad máxima... ¿qué hace el robot?

1. **¿Qué ocurre si aplicas una velocidad angular y lineal elevada a un robot de forma instantánea, desde una posición de reposo?**

    Es perfectamente factible que nuestros robots alcancen sus velocidades máximas; sin embargo, ¡no necesariamente responden bien cuando se les pide pasar de estar detenidos a máxima velocidad de forma instantánea! Considera probar esto en un robot real para observar qué sucede. Con el robot detenido, **[usa la línea de comandos](../course/part2.md#ex3)** para publicar un comando de velocidad al robot que contenga tanto una componente lineal *alta* como una angular *alta*. ¿Qué *esperarías* observar?[^hint-circle] ... Lo que *realmente* observes podría ser diferente. ¿Cómo podrías lograr el movimiento deseado (suponiendo que las velocidades estén dentro de los límites máximos)?

    [^hint-circle]: El robot *debería* girar en círculo, pero si las velocidades están cerca de los límites máximos, ¿realmente ocurre esto?

## Lecturas de Desplazamiento Láser y el Sensor LiDAR

1. **¿Cuáles son las distancias mínima y máxima que puede detectar el sensor LiDAR del robot?**

    Puedes usar **[el mismo proceso que en simulación](../course/part3.md#range_max_min)** para determinar esto.

    Si nuestra arena de robots mide 4x4 metros, *¿es probable que el robot encuentre lecturas fuera de este rango?*

1. **¿Qué informa el sensor cuando se superan estos límites, y en qué se diferencia de una simulación?**

    El LiDAR nos proporciona una medida precisa de la distancia a los obstáculos en el entorno del robot, siempre que esos obstáculos estén dentro del rango de medición del sensor (como se describió anteriormente). Si los obstáculos están más allá del rango de medición del sensor, el sensor devuelve en su lugar un valor *fuera de rango*. En nuestro código es importante que **[detectemos estos valores *fuera de rango* y los descartemos](../course/part3/lidar_subscriber.md)**, ya que si no los manejamos correctamente esto puede afectar la capacidad del robot para detectar y evitar obstáculos eficazmente. En simulación, el valor fuera de rango es `inf`, pero ¿es lo mismo en los robots reales?[^hint-lidar]

    [^hint-lidar]: En los robots reales, el valor fuera de rango **NO** es `inf`, ¡así que necesitas averiguar cuál es!

1. **Los datos de un sensor LiDAR real serán "ruidosos". ¿Cuáles son las implicaciones de esto para las aplicaciones del mundo real?**

    Puede que notes, si **[observas los datos del sensor LiDAR de un robot en RViz](./basics.md#exViz)**, que los puntos verdes se mueven bastante, incluso cuando el robot no se está moviendo, o cuando nada en el entorno está cambiando realmente. Esto se llama *"ruido de medición"*, y es común en todos los sensores. Es importante entonces considerar el procesamiento que realizas sobre estos datos: supón que quieres determinar la distancia al objeto más cercano en el entorno de tu robot; quizás podrías considerar aplicar una función `min()` para determinarlo. Sin embargo, esto sería muy sensible al ruido de medición: los valores mínimos podrían no representar siempre mediciones de distancia genuinas. ¿Existen formas alternativas de manejar estos datos?

## La Cámara y el Procesamiento de Imágenes

1. **¿En qué topic se publican los datos de imagen en los robots reales? ¿Es el mismo que en una simulación?**

    Con el robot real a disposición, usa herramientas de línea de comandos de ROS como `ros2 topic list` y `ros2 topic info` para interrogar la Red ROS e identificar el nombre del topic de imagen de la cámara usado en los robots reales. *¿Es igual o diferente?*

1. **¿Cuál es la resolución de las imágenes obtenidas de la cámara de un robot real?**

    Habiendo confirmado el nombre del topic de imagen de la cámara (como se indicó anteriormente), usa **[los métodos descritos aquí](../course/part6.md#camera-topics-and-data)** para identificar la resolución de las imágenes que se están publicando. Es importante conocer esto, especialmente cuando se trata de aplicar recortes a las imágenes sin procesar: si no sabes qué tan grandes (o pequeñas) son las imágenes de partida, podrías terminar cortando más (o menos) de lo que pretendías.

1. **¿Producen las mismas técnicas de procesamiento de imágenes los mismos resultados en simulación y en el mundo real?**

    En general, la detección de imágenes se vuelve un poco más desafiante en el mundo real, donde el mismo objeto podría aparecer (para la cámara de un robot) con tonos de color ligeramente diferentes bajo diferentes condiciones de luz, desde diferentes ángulos, con diferentes niveles de sombra, etc. En simulación, puede que **[construyas un nodo `colour_search.py` extremadamente efectivo](../course/part6.md#ex3)** para detectar cada uno de los cuatro pilares de colores en un mundo simulado, pero esto podría no funcionar tan bien en el mundo real sin algunos ajustes. Por eso es realmente importante **siempre** probar tu código en el mundo real; ¡que funcione en simulación **no** significa que funcionará en los robots reales!

## Resumen

A lo largo de este curso realizarás bastante trabajo de desarrollo en simulación, donde es más fácil probar las cosas y menos grave si algo sale mal. En general, podrás desarrollar mucho más rápido de esta manera, y puedes hacerlo también fuera de tus sesiones semanales de laboratorio. Mientras lo haces, sin embargo, ten en cuenta todas las diferencias que hemos identificado anteriormente, para que haya menos sorpresas desagradables cuando llegues a desplegar tus aplicaciones ROS en el mundo real.
