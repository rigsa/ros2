---  
title: Trabajar con tu Paquete de ROS (en el Laboratorio)
---  

Habiendo seguido [las instrucciones en la página de Primeros Pasos](./getting-started.md) (en la Semana 1), el paquete de ROS de tu equipo estará alojado en GitHub, lo que hace mucho más fácil colaborar y transferir tu trabajo al hardware real durante las sesiones de laboratorio[^rse].

[^rse]: **Recuerda**: Si aún no estás familiarizado con cómo usar herramientas como Git y GitHub, te recomendamos encarecidamente que consultes [este curso sobre Git y GitHub](https://srse-git-github-zero2hero.netlify.app/){target="_blank"}.

Necesitarás transferir tu paquete de ROS a una laptop de robot siempre que quieras trabajar en un robot real durante los laboratorios.

## Primeros Pasos en Cada Sesión de Laboratorio {#getting-started}

Tu equipo debería tener la misma laptop para cada sesión de laboratorio. Habiendo completado todos los pasos para configurar las Claves SSH (como se describe en las secciones a continuación), deberías poder regresar a la laptop, re-clonar tu paquete y continuar trabajando con relativa facilidad al inicio de cada sesión de laboratorio.

1. **Verificar si ya tienes una Clave SSH**: Guardarás una clave SSH privada (privada para ti y el resto de tu equipo) en la laptop que se te ha designado para cada sesión de laboratorio. El primer paso es verificar si esta existe en tu laptop:

    ``` { .txt .no-copy }
    ls -al ~/.ssh | grep ros2_lab_equipoXX
    ```

    Reemplaza `XX` con tu número de equipo.

    Si se presenta la clave ssh de tu equipo, entonces puedes continuar con el Paso 2. Si no, ve a la sección **[Configurar Claves SSH](#setting-up-ssh-keys)** a continuación.

1. **Si existe la Clave SSH de tu equipo**: inicia el agente ssh de la laptop y activa tu clave:

    ```bash
    eval "$(ssh-agent -s)"
    ```
    
    ``` { .bash .no-copy }
    ssh-add ~/.ssh/ros2_lab_equipoXX
    ```

    Reemplazando `XX` con tu número de equipo.

1. Luego, [clona tu paquete en la laptop](#ssh-clone).

    Se te pedirá tu frase de contraseña secreta, ¡con suerte la recuerdas!

    !!! warning
        Te recomendamos encarecidamente que [elimines el paquete de tu equipo de la laptop](#deleting-your-ros-package-after-a-lab-session) al final de cada sesión de laboratorio.

## Configurar Claves SSH {#setting-up-ssh-keys}

Usando *claves SSH*, puedes clonar el paquete de ROS de tu equipo en las laptops de robots, hacer commits y publicarlos de vuelta a GitHub durante los laboratorios, sin necesidad de proporcionar tu nombre de usuario de GitHub y un token de acceso personal cada vez. ¡Esto hace la vida mucho más fácil! Los siguientes pasos describen el proceso que debes seguir para lograrlo[^github-docs].

[^github-docs]: Adaptado de [GitHub Docs](https://docs.github.com/en/authentication/connecting-to-github-with-ssh){target="_blank"}

### Paso 1: Generar una clave SSH (en la Laptop) {#ssh-keygen}

1. Desde una instancia de terminal en la laptop navega a la carpeta `~/.ssh`:

    ```bash
    cd ~/.ssh
    ```

1. Crea una nueva clave SSH en la laptop, usando tu dirección de correo de GitHub:

    ``` { .txt .no-copy }
    ssh-keygen -t ed25519 -C "tu.correo@institucion.edu"
    ```

    Reemplazando `tu.correo@institucion.edu` con **tu dirección de correo de GitHub**.

    <a name="ssh-key-name"></a>

1. Luego se te pedirá que `Ingreses un archivo en el que guardar la clave`. Esto debe ser único, así que introduce el nombre de tu paquete de ROS, por ejemplo: `ros2_lab_equipoXX` (donde `XX` es reemplazado con tu número de equipo).

1. Luego se te pedirá que `ingreses una frase de contraseña`. Esta es la forma de hacer segura tu clave SSH, para que ningún otro equipo que use la misma laptop pueda acceder y hacer cambios en el paquete/repositorio de GitHub de tu equipo. Se te pedirá que la ingreses siempre que intentes hacer commit/publicar nuevos cambios en tu paquete de ROS en GitHub. Decide una frase de contraseña y compártela **SOLO** con tus compañeros de equipo.

1. A continuación, inicia el agente ssh de la laptop:

    ```bash
    eval "$(ssh-agent -s)"
    ```

1. Agrega tu clave privada SSH al agente ssh de la laptop. Necesitarás ingresar el nombre del archivo de clave SSH que creaste en el paso anterior (por ejemplo: `ros2_lab_equipoXX`)

    ``` { .txt .no-copy }
    ssh-add ~/.ssh/ros2_lab_equipoXX
    ```

    ¡Reemplazando `XX` con tu número de equipo por supuesto!

1. Luego necesitarás agregar la clave SSH a tu cuenta en GitHub...

### Paso 2: Agregar una clave SSH a tu cuenta de GitHub

*Estas instrucciones están replicadas de [esta página de GitHub Docs](https://docs.github.com/en/authentication/connecting-to-github-with-ssh/adding-a-new-ssh-key-to-your-github-account?platform=linux){target="_blank"}*.

1. En la laptop, copia la clave pública SSH que creaste en los pasos anteriores a tu portapapeles.
    
    Haz esto desde una terminal en la laptop, usando `cat`:

    ``` { .txt .no-copy }
    cat ~/.ssh/ros2_lab_equipoXX.pub
    ```

    Reemplazando `XX` con tu número de equipo una vez más.

    El contenido del archivo se mostrará entonces en la terminal... cópialo desde aquí.

    !!! tip "Consejos"
        1. Para copiar texto desde dentro de una ventana de terminal usa ++ctrl+shift+c++
        2. También podrías abrir el archivo en VS Code y copiarlo desde allí:

            ``` { .txt .no-copy }
            code ~/.ssh/ros2_lab_equipoXX.pub
            ```

2. Ve a tu cuenta de GitHub en un navegador web. En la esquina superior derecha de cualquier página, haz clic en tu foto de perfil, luego haz clic en **Settings**.

3. En la sección "Access" de la barra lateral, haz clic en **SSH and GPG keys**.

4. Haz clic en **New SSH key**.

5. Introduce un nombre descriptivo para la clave en el campo "Title", por ejemplo `ros2_lab_laptop1`.

6. Selecciona `Authentication Key` como el "Key Type."

7. Pega el texto de tu archivo de Clave Pública SSH en el campo "Key".

8. Finalmente, haz clic en el botón "Add SSH Key".

## Clonar tu paquete de ROS en la Laptop {#ssh-clone}

Con tus claves SSH configuradas, podrás clonar tu paquete de ROS en la laptop.

Hay un Espacio de Trabajo de ROS 2 en cada una de las laptops de robots y (al igual que en tu propio entorno local de ROS) ¡tu paquete **debe** residir dentro de este espacio de trabajo!

1. Desde una terminal en la laptop, navega al directorio `src` del Espacio de Trabajo de ROS 2:

    ```bash
    cd ~/ros2_ws/src/
    ```

1. Ve a tu paquete de ROS en GitHub. Haz clic en el botón Code y luego selecciona la opción SSH para revelar la dirección SSH de tu repositorio. Cópiala.

1. Regresa a la instancia de terminal en la laptop para luego clonar tu paquete en el directorio `ros2_ws/src/` usando `git`:

    ```bash
    git clone REMOTE_SSH_ADDRESS
    ```

    Donde `REMOTE_SSH_ADDRESS` es la dirección SSH que acabas de copiar de GitHub.

1. Ejecuta Colcon para construir tu paquete, que es un **proceso de tres pasos**:
	
    1. Navega a la **raíz** del Espacio de Trabajo de ROS:

        ```bash
        cd ~/ros2_ws
        ```
    
    1. Ejecuta el comando `colcon build`, apuntando solo a tu paquete:
    
        ``` { .txt .no-copy }
        colcon build --packages-select ros2_lab_equipoXX --symlink-install
        ```
        (Nuevamente, reemplazando `XX` con *tu* número de equipo.)
        
    1. Luego, recarga el entorno:
	
        ```bash
        source ~/.bashrc
        ```

1. Navega a tu paquete:

    ``` { .txt .no-copy }
    cd ~/ros2_ws/src/ros2_lab_equipoXX/
    ```

    ... y luego ejecuta los siguientes comandos para establecer tu identidad (lo que te permitirá hacer commits en el repositorio de tu paquete):

    ``` { .txt .no-copy }
    git config user.name "tu nombre"
    ```
    ``` { .txt .no-copy }
    git config user.email "tu dirección de correo"
    ```

¡Luego deberías poder hacer commit y publicar cualquier actualización que hagas en tu paquete de ROS mientras trabajas en la laptop, de vuelta a tu repositorio remoto usando la frase de contraseña secreta que definiste anteriormente!

## Eliminar tu paquete de ROS después de una sesión de laboratorio

Recuerda que las Laptops de Robótica usan una cuenta a la que todos en la clase tienen acceso. Por lo tanto, es posible que quieras eliminar tu paquete de la laptop al final de cada sesión de laboratorio. Es muy fácil volver a clonarlo en la laptop siguiendo [los pasos anteriores](#getting-started) al inicio de cada sesión de laboratorio. Eliminar tu paquete (siguiendo las instrucciones a continuación) **no** eliminará tu clave SSH de la laptop, por lo que no necesitarás hacer todo eso de nuevo, y tu clave SSH seguirá estando protegida con la frase de contraseña secreta que configuraste cuando generaste la clave SSH para comenzar (¡suponiendo que estés trabajando en la misma laptop, por supuesto!)

!!! warning
    ¡Asegúrate de haber publicado todos los cambios en GitHub antes de eliminar tu paquete!

Elimina tu paquete simplemente ejecutando el siguiente comando desde cualquier terminal en la laptop:

```bash
rm -rf ~/ros2_ws/src/ros2_lab_equipoXX
```

... ¡reemplazando `XX` con el número de tu propio equipo!
