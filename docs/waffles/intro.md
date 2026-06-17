---
title: Introducción
---

# Introducción

## Manejo de los Robots

!!! warning "Salud y Seguridad"
    Todos deben completar un cuestionario de salud y seguridad relacionado con el trabajo con los robots reales. Este cuestionario (y la fecha límite para completarlo) está disponible en el sistema de gestión del curso.

    ¡Asegúrate de que **al menos un miembro de tu equipo** lo haya completado antes de continuar!

<figure markdown>
  ![](../images/waffle/handling.png){width=600px}
</figure>

Como puedes ver en la figura anterior, los robots tienen muchos sensores y componentes electrónicos expuestos, por lo que **debes tener mucho cuidado** al manejarlos para evitar que se dañen. Al manipular un robot, sostenlo siempre por las *Capas Waffle* negras o por los *Pilares de Soporte* verticales (como se resalta en la figura anterior).

!!! important 
    ¡No levantes ni cargues el robot por la cámara ni por el sensor LiDAR! ¡Son dispositivos delicados que pueden dañarse fácilmente!

Gran parte de la electrónica del robot se encuentra alojada en la capa waffle del medio. Trata de no tocar ninguna de las tarjetas de circuito y ten cuidado de no jalar ningún cable ni intentar retirar o recolocar ninguna de las conexiones. Si tienes alguna inquietud sobre la electrónica o el cableado, si algo se ha soltado, o si tu robot no parece estar funcionando correctamente, pide a un miembro del equipo docente que lo revise.

Los robots se te proporcionarán con una batería ya instalada y lista para usar. **¡No intentes desconectar ni retirar la batería tú mismo!** El robot emitirá un pitido cuando la batería esté baja; si esto ocurre, pide a un miembro del equipo que te proporcione una de repuesto (hay muchas disponibles).

## Las Laptops del Laboratorio {#laptops}

Se te proporcionará una de nuestras *Laptops del Laboratorio* preconfiguradas cuando trabajes con los Waffles reales. Esta tendrá todo el software necesario instalado y listo para usar.

Ya hay una cuenta de usuario `student` configurada, y deberás usarla cuando trabajes en el laboratorio. Necesitarás una contraseña para iniciar sesión, que te proporcionaremos durante las sesiones de laboratorio.

## Red

Los robots y las laptops deben poder conectarse entre sí a través de una conexión de red. Los robots se conectan a una red inalámbrica dedicada en el laboratorio llamada `LAB-WIFI`. Para que las laptops puedan "ver" a los robots, deben estar conectadas a la red usando cualquiera de las siguientes opciones:

1. El SSID WiFi `eduroam`
1. El SSID WiFi `LAB-WIFI` (**¡sin acceso a internet!**)
1. Una conexión directa por cable (ethernet) entre el robot y la laptop

Las credenciales WiFi para `LAB-WIFI` y `eduroam` ya están configuradas en las laptops, lo que te permite conectarte a cualquiera de las dos redes de inmediato. Si tienes algún problema, habla con un miembro del equipo docente.

## VS Code

*Visual Studio Code* está instalado en las laptops para que lo uses cuando trabajes en tus aplicaciones ROS 2 con robots reales. Puedes lanzar VS Code desde cualquier terminal simplemente escribiendo `code`. También puedes iniciarlo haciendo clic en el ícono en la barra de favoritos del lado izquierdo de la pantalla:

<figure markdown>
  ![](../images/vscode/icon.png)
</figure>
