---  
title: Procedimientos de Apagado 
---

## Robots

Los Waffles son alimentados por [una Computadora de Placa Única (SBC)](../about/robots.md#our-waffles), que ejecuta un sistema operativo completo. Como con cualquier sistema operativo, es importante **apagarlo correctamente**, en lugar de simplemente desconectar la alimentación, para evitar pérdida de datos u otros problemas.

Por lo tanto, una vez que hayas terminado de trabajar con un robot durante una sesión de laboratorio, sigue los pasos a continuación para apagarlo.

1. Abre una **nueva** instancia de terminal en la laptop (++ctrl+alt+t++), e ingresa lo siguiente:

    ``` { .bash .no-copy }
    waffle X off
    ```
    ... reemplazando `X` con el número del robot con el que has estado trabajando.
    
1. Se te pedirá confirmar que deseas apagar el robot:

    ``` { .bash .no-copy }
    [INPUT] Are you sure you want to shutdown robot-X? [y/n] >> 
    ```

    Ingresa ++y++ y presiona ++enter++ y la SBC del robot se apagará.

1. Una vez que la luz azul en la esquina de la SBC se apague, es seguro deslizar el botón de encendido hacia la **izquierda** para apagar el dispositivo completamente.

    <figure markdown>
      ![](../images/waffle/sbc.png){width=600px}
    </figure>

## Laptops

Una vez que hayas apagado el robot, **¡recuerda apagar también la laptop!** Haz esto haciendo clic en el ícono de la batería en la parte superior derecha del escritorio y seleccionando la opción "Power Off / Log Out" en el menú desplegable.

<figure markdown>
  ![](../images/laptops/ubuntu_poweroff.svg){width=300px}
</figure>

<center>

  **¡Entrega tu robot y laptop a un miembro del equipo docente, quien los guardará por ti!**

</center>
