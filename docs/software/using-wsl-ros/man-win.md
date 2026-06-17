---
title: Primeros Pasos con WSL-ROS2 en las Computadoras del Laboratorio
---

## Requisitos Previos

* [Acceder a WSL-ROS2 en una Computadora del Laboratorio](./README.md)

## Lanzar WSL-ROS2

1. Haz clic en el botón del Menú Inicio de Windows: ![](../figures/win-logo.svg)
    
1. Luego, comienza a escribir `wsl-ros` y haz clic en el acceso directo de la aplicación que debería aparecer en la lista:

    <figure markdown>
      ![](../figures/win-menu.svg){width=600px}
    </figure>

    Si hay múltiples opciones, ¡asegúrate de seleccionar **WSL-ROS2**! 

    Luego se te presentará la siguiente pantalla:

    <figure markdown>
      ![](../figures/wsl-ros2-first-install.png){width=600px}
    </figure>

    WSL-ROS2 se está instalando ahora, lo que puede tardar un par de minutos en completarse. Una vez hecho, el *Windows Terminal* debería lanzarse automáticamente:

    <figure markdown>
      ![](../figures/win-term-welcome-v2526-03.png){width=600px}
    </figure>

¡Esta es una **Instancia de Terminal WSL-ROS2**!

<!-- ## Configurar Visual Studio Code {#configure-vscode}

*Visual Studio Code* (o *"VS Code"*, para abreviar) debería estar instalado en todas las computadoras del laboratorio que tienen WSL-ROS2 preinstalado. Este es un excelente *Entorno de Desarrollo Integrado (IDE)* que usaremos extensamente a lo largo del curso. Sin embargo, primero deberás asegurarte de que esté configurado correctamente, así que sigue las instrucciones a continuación en preparación para más adelante:

<center>[Configurar Visual Studio Code](./vscode.md){ .md-button }</center>

!!! tip
    Solo necesitarás hacer esto una vez: las configuraciones deberían guardarse en tu perfil de usuario, ¡y deberían transferirse a cualquier otra computadora del laboratorio en la que inicies sesión! -->

## Hacer Copia de Seguridad (y Restaurar) tus Datos

Si estás trabajando con WSL-ROS en una computadora del laboratorio, el entorno WSL-ROS solo se conservará por un tiempo limitado en la máquina en la que lo instalaste. Por lo tanto, ¡cualquier trabajo que hagas dentro de WSL-ROS **no se conservará** entre sesiones o en diferentes máquinas automáticamente! Por eso es *muy importante* que ejecutes un script de copia de seguridad antes de cerrar WSL-ROS. Hacerlo es muy fácil, simplemente ejecuta el siguiente comando desde cualquier Instancia de Terminal WSL-ROS:

```bash
wsl_ros backup
```

Esto creará un archivo de tu *Directorio de Inicio* ([más detalles aquí](./linux-term.md)) y lo guardará en tu unidad `U:`. Cada vez que lances un *entorno WSL-ROS2 nuevo* en otro día, o en una máquina diferente, simplemente ejecuta el siguiente comando para restaurar tu trabajo en él:

```bash
wsl_ros restore
```

Para hacer las cosas un poco más fáciles, al lanzar WSL-ROS el sistema verificará si ya existe un archivo de copia de seguridad de una sesión anterior. Si existe, entonces se te preguntará si deseas restaurarlo de inmediato:

``` { .txt .no-copy }
It looks like you already have a backup from a previous session:
  U:\wsl-ros\ros2-backup-XXX.tar.gz
Do you want to restore this now? [y/n]
```

Ingresa ++y+enter++ para restaurar tus datos desde este archivo de copia de seguridad, o ++n+enter++ para dejar el archivo de copia de seguridad tal como está y trabajar desde cero (no se restaurará ninguno de tu trabajo anterior). 

## Volver a Lanzar el Entorno

Como se discutió anteriormente, el entorno WSL-ROS2 no se conserva en las computadoras del laboratorio indefinidamente. Sin embargo, si vuelves a iniciar sesión en la misma máquina dentro de unas pocas horas, es posible que todavía esté allí, y se te presentará el siguiente mensaje cuando lo lances:

<figure markdown>
  ![](../figures/resume.png){width=700px}
</figure>

Ingresa ++y+enter++ para continuar donde dejaste las cosas anteriormente, o ++n+enter++ para comenzar desde una instalación nueva.

!!! warning
    ¡Si seleccionas ++n++ entonces cualquier trabajo que hayas creado en el entorno existente será eliminado! ¡Siempre asegúrate de hacer una copia de seguridad de tu trabajo usando [el procedimiento descrito anteriormente](#hacer-copia-de-seguridad-y-restaurar-tus-datos)!