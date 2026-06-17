---
title: Acceder o Instalar ROS 2
description: "Cómo acceder a ROS 2 en las computadoras del laboratorio, o instalarlo en tu propia máquina."
---

Para participar en [el Curso de ROS 2](../course/README.md) necesitarás acceso a un entorno de ROS. 

ROS puede ser un poco complicado de instalar, y está soportado principalmente solo en un puñado de sistemas operativos *"Tier 1"* ([listados aquí](https://docs.ros.org/en/jazzy/Installation.html){target="_blank"}), siendo la primera (y mejor) opción Ubuntu Linux. Para instalar o acceder a ROS 2 para este curso, recomendamos una de las siguientes opciones. Haz clic en el enlace correspondiente a continuación para acceder a más detalles:

## WSL-ROS2 (Windows)

*Exclusivo para participantes del laboratorio*

Hemos creado nuestro propio entorno personalizado de ROS 2 (Jazzy) y Ubuntu (24.04) para WSL específicamente para este curso, al que llamamos **"WSL-ROS2"**. El entorno contiene todas las herramientas y packages de ROS que necesitarás para los ejercicios y tareas del curso. 

**Esta es nuestra opción recomendada**, y hay dos formas de acceder a ella: 

1. [**Instálalo** en tu propia máquina Windows 10 u 11](./installing-wsl-ros2.md) a través del servicio de descarga de software del laboratorio.
1. [**Accede a él** en las computadoras del laboratorio](./using-wsl-ros/README.md).

## Mac y Linux

Para usuarios de Mac, la mejor opción para instalar ROS 2 en tu máquina es usar Docker, pero ten en cuenta que el rendimiento no es óptimo. 

La opción de Docker funciona *muy bien* en Linux.

* [Instalando ROS 2 con Docker](./docker-ros2.md).

## Ejecútalo en Tu Navegador (Sin Instalación)

¿No quieres instalar nada en absoluto — ni siquiera Docker en tu propia máquina? Si
alguien (un demostrador, o el laboratorio) tiene un sandbox en ejecución, puedes hacer
el curso completo en un navegador, con la simulación transmitida directamente a ti.

* [Ejecutar ROS 2 en Tu Navegador](./browser-ros2.md).