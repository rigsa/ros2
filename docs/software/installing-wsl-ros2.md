---
title: Instalando WSL-ROS2 en Windows 
---

**Aplicable a**: Computadoras personales (no administradas) con Windows 10 u 11

## El Entorno de Simulación WSL-ROS2

Para apoyar este curso hemos creado un entorno personalizado de ROS 2 que se ejecuta en Windows 10 u 11 usando el [Windows Subsystem for Linux (WSL)](https://docs.microsoft.com/en-us/windows/wsl/){target="_blank"}. Lo llamamos "**WSL-ROS2**" y está disponible a través del equipo del laboratorio.

!!! note
    Cuando recibas el enlace de descarga de WSL-ROS2, recibirás también instrucciones de instalación. Recomendamos que sigas las instrucciones proporcionadas en *esta página*, ya que esta página se mantendrá más actualizada a lo largo del semestre.

## Requisitos Previos

1. Tu computadora debe estar ejecutando Windows 10 **Build 19044 o superior**, o Windows 11.
2. [Actualiza los controladores de GPU de tu máquina](https://learn.microsoft.com/en-us/windows/wsl/tutorials/gui-apps#install-support-for-linux-gui-apps){target="_blank"}.
3. Instala o actualiza WSL:
    1. Si aún no tienes WSL instalado en tu máquina, sigue [estas instrucciones para instalarlo](https://learn.microsoft.com/en-us/windows/wsl/tutorials/gui-apps#fresh-install---no-prior-wsl-installation){target="_blank"}.
    2. Si *ya tienes* WSL instalado en tu máquina, sigue [estas instrucciones para actualizarlo](https://learn.microsoft.com/en-us/windows/wsl/tutorials/gui-apps#existing-wsl-install){target="_blank"}.
4. [Instala el Windows Terminal](https://learn.microsoft.com/en-us/windows/terminal/install){target="_blank"}.
5. [Instala Visual Studio Code](https://code.visualstudio.com/){target="_blank"} y [la extensión WSL para VS Code](https://marketplace.visualstudio.com/items?itemName=ms-vscode-remote.remote-wsl){target="_blank"}.
1. Instala el [VcXsrv Windows X Server](https://sourceforge.net/projects/vcxsrv/){target="_blank"}.

## Instalación

1. Solicita el enlace de descarga al coordinador del laboratorio.

1. El enlace te permitirá descargar **WSL-ROS2** en tu máquina como un archivo `.zip` (~2 GB).
    
1. En tu computadora, crea una nueva carpeta en la raíz de tu unidad `C:\` llamada `WSL-ROS2`.

1. Guarda el archivo `.zip` en esta nueva carpeta (`C:\WSL-ROS2\`)

1. **Inicia PowerShell**, luego ejecuta los siguientes comandos en orden:

    1. Identifica el archivo zip:

        ```powershell
        $zipFile = Get-ChildItem "C:\WSL-ROS2\WSL-ROS2_*_SDS.zip" | 
            Sort-Object Name -Descending | 
            Select-Object -First 1
        ```

    2. Extráelo:

        ```powershell
        Expand-Archive -Path $zipFile.FullName `
            -DestinationPath "C:\WSL-ROS2\" -Force
        ```
    
    3. Identifica el archivo `.tar` extraído:

        ```powershell
        $tarFile = Get-ChildItem "C:\WSL-ROS2\wsl-ros2-v*.tar" | 
            Sort-Object Name -Descending | 
            Select-Object -First 1
        ```
    
    4. Impórtalo como una distribución WSL:

        ```powershell
        wsl --import WSL-ROS2 "$env:localappdata\WSL-ROS2" `
            $tarFile.FullName --version 2
        ```

1. Esto puede tardar un par de minutos. Una vez completado, puedes verificar que fue exitoso con el siguiente comando:

    ```powershell
    wsl -l -v
    ```

    Donde `WSL-ROS2` debería estar listado.

1. A continuación (**opcional**), abre la aplicación Windows Terminal, luego:
    
    1. Ve a Configuración (++ctrl+comma++)
    1. En `Perfiles` en el menú de la izquierda, encuentra `WSL-ROS2` (o desplázate más abajo y haz clic en el botón `Agregar un nuevo perfil` para crearlo).
    1. Configura los ajustes para el perfil `WSL-ROS2` como se muestra a continuación:

        <figure markdown>
          ![](./figures/win_term_profile_settings.png){width=600px}
        </figure>

    1. Luego, en `Inicio` (de regreso en el menú de la izquierda), bajo `Perfil predeterminado`, selecciona **WSL-ROS2** de la lista desplegable.

        Esto asegurará que cada vez que abras la aplicación Windows Terminal *o* presiones el botón Nueva Pestaña (:material-plus:) se lance por defecto una Instancia de Terminal WSL-ROS2.


## Configuración Inicial

Dentro de una instancia de terminal WSL-ROS2, necesitarás ejecutar algunos comandos iniciales para configurar las cosas.

1. Primero, ejecuta el siguiente comando para intentar usar el soporte nativo de Interfaz Gráfica de Usuario (GUI) (que debería funcionar si seguiste todos [los requisitos previos anteriores](#requisitos-previos)):

    ```bash
    echo "export XSERVER=false" > $HOME/.diamond/xserver.sh
    ```

1. Luego, vuelve a hacer source de tu archivo `.bashrc` para que este cambio surta efecto:

    ```bash
    source ~/.bashrc
    ```

1. Ejecuta el siguiente comando de ROS para ver si puedes lanzar la GUI de Gazebo:

    ```bash
    ros2 launch turtlebot3_gazebo empty_world.launch.py
    ```

    Esto debería presentarte algo como esto:

    <figure markdown>
      ![](../images/gz/tb3_empty_world_top.png){width=600px}
    </figure>

    Si esto no funciona, entonces podrías intentar usar un X Server de terceros (VcXsrv) en su lugar...

## Usar un X Server de Terceros

Si no puedes ejecutar aplicaciones GUI de forma nativa (habiendo completado los pasos en la sección anterior), entonces podrías intentar usar un X Server de terceros (*"VcXsrv"*) en su lugar. En [los requisitos previos](#requisitos-previos), ya deberías haber instalado VcXsrv.

!!! note 
    Solo haz esto si **no pudiste** lanzar la simulación del robot en la sección anterior.

1. [Habiendo instalado VcXsrv en la Sección de Requisitos Previos](#requisitos-previos)...
1. Descarga este [archivo de configuración para VcXsrv](https://drive.google.com/file/d/1CMJZ6xVXJ2cKZ0NmdYaxUw9RfPsIGLX9/view?usp=sharing){target="_blank"} y guárdalo en tu escritorio como `wsl_ros_config.xlaunch`.

    <figure markdown>
      ![](./figures/wsl-ros-config.png)
    </figure>

1. Haz doble clic en esto para lanzar VcXsrv con la configuración apropiada. Debería aparecer un ícono en tu bandeja de notificaciones (abajo a la derecha) para indicar que el X Server está en ejecución:
    
    <figure markdown>
      ![](./figures/xlaunch_icon.png){width=25px}
    </figure>

1. Lanza el entorno WSL-ROS2 iniciando la aplicación Windows Terminal:

    <figure markdown>
      ![](./figures/launch-win-term.png){width=700px}
    </figure>

1. En una Instancia de Terminal WSL-ROS2, ejecuta lo siguiente:

    ```bash
    echo "export XSERVER=true" > $HOME/.tuos/xserver.sh
    ```

1. Vuelve a hacer source de tu archivo `.bashrc` para que este cambio surta efecto:

    ```bash
    source ~/.bashrc
    ```

1. Intenta ejecutar la simulación Gazebo de mundo vacío de nuevo:

    ```bash
    ros2 launch turtlebot3_gazebo empty_world.launch.py
    ```

    !!! warning "Importante"
        Debes asegurarte de tener el X Server en ejecución (haciendo clic en el acceso directo `wsl_ros_config.xlaunch`) **cada vez** que trabajes con WSL-ROS2. 

## Reiniciar el Motor WSL

Si tienes problemas con WSL, a veces un reinicio ayuda.  

Primero, cierra cualquier ventana de terminal WSL-ROS2 que tengas abierta (y cualquier conexión a WSL-ROS2 en VS Code). Luego, inicia PowerShell y *apaga* el motor WSL:

```powershell
wsl --shutdown
```

Reinicia el motor WSL lanzando una nueva instancia de terminal WSL-ROS2.

## Ver También

* [Configurar VS Code para WSL](./using-wsl-ros/vscode.md)
* [Una Breve Introducción al Terminal de Linux](./using-wsl-ros/linux-term.md)