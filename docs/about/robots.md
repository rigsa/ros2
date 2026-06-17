---
title: "Los Robots del Laboratorio"
description: Conoce más sobre los robots TurtleBot3 Waffle con los que trabajarás en el laboratorio.
---

## El TurtleBot3 Waffle {#robots}

### ¿TurtleBot qué?

Para enseñar ROS utilizamos el robot [TurtleBot3 Waffle](https://emanual.robotis.com/docs/en/platform/turtlebot3/overview/){target="_blank"}, fabricado por Robotis. Este es el robot de 3ª generación de la [familia TurtleBot](http://wiki.ros.org/Robots/TurtleBot){target="_blank"} (que ha sido la plataforma de referencia de hardware para ROS desde 2010). La familia de robots TurtleBot existe para proporcionar hardware accesible y de costo relativamente bajo junto con software de código abierto, con el objetivo de facilitar el aprendizaje de robótica y ROS.

### Nuestros Robots

En el laboratorio contamos con robots TurtleBot3 Waffle para las prácticas (también conocidos como *"los Waffles"*):

<figure markdown>
  ![](../images/waffle/cabinet.jpg){width=500px} 
</figure>

Nuestros robots son una versión mejorada del *TurtleBot3 WafflePi* que se puede adquirir en Robotis. Se han realizado algunos ajustes, como se muestra a continuación:

<figure markdown>
  ![](../images/waffle/features.png){width=800px}
</figure>

Los Waffles cuentan con los siguientes componentes de hardware principales:

* Una placa microcontroladora OpenCR para alimentar y controlar los motores de las ruedas, distribuir energía a otros elementos de hardware y proporcionar una interfaz para sensores adicionales.
* Una [computadora de placa única (SBC) UP Squared](https://up-board.org/upsquared/specifications/){target="_blank"} con procesador Intel y 32 GB de almacenamiento eMMC integrado. Esta placa actúa como el "cerebro" del robot.
* Motores de rueda izquierda y derecha independientes (DYNAMIXEL XM430) para mover el robot en una configuración de *tracción diferencial*.

Esta configuración de tracción permite que los robots se muevan con las siguientes **velocidades máximas**: <a name="max_vels"></a>

<center>

| Componente de velocidad | Límite superior | Unidades |
| :--- | :---: | :--- |
| *Lineal* | 0.26 | m/s |
| *Angular* | 1.82 | rad/s |

</center>

Además, los robots están equipados con los siguientes sensores:

* Un sensor de detección y medición de distancia por luz (*LiDAR*), que gira continuamente mientras el robot está en operación. Utiliza luz en forma de pulsos láser para medir la distancia a los objetos circundantes, proporcionando una visión de 360&deg; del entorno.
* Una [cámara Intel RealSense D435](https://www.intelrealsense.com/depth-camera-d435/){target="_blank"} con sensores de imagen izquierdo y derecho, que permite la detección de profundidad además de la captura estándar de imágenes.
* Una Unidad de Medición Inercial (IMU) de 9 ejes integrada en la placa microcontroladora OpenCR, que utiliza un acelerómetro, giroscopio y magnetómetro para medir la fuerza específica, aceleración y orientación del robot.
* Encoders en cada uno de los motores de rueda DYNAMIXEL, que permiten medir la velocidad y el conteo de rotaciones de cada rueda.

#### Dimensiones

Algunas dimensiones útiles de los Waffles se muestran a continuación:

<figure markdown>
  ![](../images/waffle/dims_and_turning_circle.svg){width=600px}
  <figcaption>Adaptado del <a href="https://emanual.robotis.com/docs/en/platform/turtlebot3/features/#data-of-turtlebot3-waffle-pi" target="_blank">Manual electrónico TurtleBot3 de ROBOTIS</a>.</figcaption>
</figure>

#### Software

Nuestros robots actualmente ejecutan [ROS 2 Jazzy Jalisco](https://docs.ros.org/en/jazzy/index.html){target="_blank"} (o simplemente *"Jazzy"*). Los materiales del curso están basados en esta versión de ROS. La forma más sencilla de instalar Jazzy es a través de paquetes Deb para Ubuntu Noble Numbat (24.04), que es la configuración que utilizan todos nuestros robots.

Para la parte del curso basada en simulación, hemos preparado un entorno de simulación utilizando [Windows Subsystem for Linux (WSL)](https://docs.microsoft.com/en-us/windows/wsl/){target="_blank"}, que puede ejecutarse en las computadoras del laboratorio con Windows 11, así como en otras máquinas. Este entorno de simulación se denomina *"WSL-ROS2"*. [Consulta aquí para más detalles](../software/README.md). También existe una [opción basada en navegador](../software/browser-ros2.md) que no requiere instalación local.

!!! tip "¿Trabajando hacia un robot diferente?"
    Todo lo que se practica aquí se enseña utilizando interfaces estándar de ROS 2, no
    código específico de TurtleBot3. Si tu objetivo final es una plataforma diferente —
    por ejemplo, un Unitree Go2 EDU o B2 — consulta
    [Portando a Unitree Go2/B2](../course/extras/porting-to-unitree.md)
    para ver cómo los temas y patrones que aprendes aquí son aplicables.

## Laptops del Laboratorio

En el laboratorio contamos con laptops dedicadas para trabajo con los robots reales, que ejecutan el mismo sistema operativo y versión de ROS mencionados anteriormente. [Consulta aquí para más detalles](../waffles/intro.md#laptops).
