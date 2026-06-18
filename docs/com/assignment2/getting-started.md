---  
title: "Semana 1: Primeros Pasos"
---  

Antes de comenzar con la Asignación #2 (como se detalla en las páginas que siguen), debes trabajar en las siguientes tareas en tus equipos durante el primer laboratorio de la Semana 1.

* [ ] Configurar el Paquete de ROS de tu Equipo
* [ ] Conocer los Robots

Las instrucciones a continuación te guiarán a través de estos primeros pasos clave.

## Configurar el Paquete de ROS de tu Equipo

Como se discute en [la Descripción General de la Asignación #2](./README.md), todo lo que tu equipo entregue para esta asignación de laboratorio debe estar contenido dentro de un único paquete de ROS. Dentro de este desarrollarás todos los nodes necesarios para hacer que un robot de simulación complete cada una de las tareas de la asignación, así como alguna documentación para describir tu enfoque. El equipo docente evaluará cada tarea a través de *archivos de lanzamiento* que también debes proporcionar dentro de tu paquete.

Sin embargo, el primer paso es crear el Paquete de ROS de tu equipo.

El paquete de tu equipo deberá estar alojado en GitHub, por lo que cada miembro del equipo necesitará una cuenta de GitHub. Dirígete a [GitHub](https://github.com){target="_blank"} y crea una cuenta si aún no tienes una[^github-pro].

[^github-pro]: Puedes solicitar el [GitHub Student Developer Pack](https://education.github.com/pack){target="_blank"}, que te da acceso a una variedad de herramientas de desarrollo incluyendo *GitHub Pro*. GitHub Pro te permite tener colaboradores ilimitados en tus repositorios, lo que podría ayudarte a colaborar en tu paquete de ROS con tu equipo.

!!! tip "Trabajar con Git y GitHub"

    Trabajarás con Git y GitHub bastante extensamente durante la Asignación #2. Con suerte, muchos de vosotros ya estaréis bastante familiarizados con estas herramientas, pero si no, os recomendamos encarecidamente que reviseis [este curso sobre Git y GitHub](https://srse-git-github-zero2hero.netlify.app/){target="_blank"}.

### Crear el Repositorio del Paquete de tu Equipo (en GitHub)

Nomina a **solo un miembro de tu equipo** para hacer esta parte.

1. Asegúrate de haber iniciado sesión en tu cuenta de GitHub, luego ve al [repositorio `ros2_pkg_template`](https://github.com/tom-howard/ros2_pkg_template){target="_blank"}.
1. Haz clic en el botón verde `Use this template` y luego selecciona `Create a new repository` del menú desplegable.

    <figure markdown>
      ![](./getting-started/ros2_pkg_template.png){width=700px}
    </figure>

    Luego deberías ver una pantalla de **Create a new repository**.

1. El nombre de tu repositorio **debe** ser el siguiente:

    ``` { .txt .no-copy }
    ros2_lab_equipoXX
    ```

    ... donde `XX` debe reemplazarse con *tu* número de equipo de la Asignación #2. Introduce esto en el cuadro `Repository name`.

    **Si tu número de equipo es menor que 10**: pon un cero antes del número, de modo que el número de equipo siempre tenga **2 dígitos de longitud**, por ejemplo:
    
    * `ros2_lab_equipo03` para el **Equipo 3**
    * `ros2_lab_equipo08` para el **Equipo 8**
    * `ros2_lab_equipo15` para el **Equipo 15**

    !!! warning "Importante"
        El nombre de tu repositorio debe coincidir exactamente con el formato anterior:
            
        * Todos los caracteres deben estar en **minúsculas**

1. En `Configuration`, selecciona `Private` para **hacer el repositorio privado**:

    <figure markdown>
      ![](./getting-started/gh-repo-config.png){width=600px}
    </figure>

    Luego haz clic en el botón verde `Create repository`.

1. Serás dirigido a la página principal de tu repositorio. Desde aquí, haz clic en `Settings`, luego en `Access` haz clic en `Collaborators`:

    <figure markdown>
      ![](./getting-started/repo_collaborators.png){width=700px}
    </figure>

    (Es posible que se te solicite 2FA.)

1. En el área `Manage access`, haz clic en el botón verde `Add people` y agrega a los miembros del equipo docente según te indiquen.

1. Finalmente, haz clic en el botón `Add people` y agrega al resto de los miembros de tu equipo como colaboradores de este repositorio también.

### Registrar la URL de tu Paquete de ROS con el Equipo Docente {#pkg-reg}

Habiendo creado tu paquete, deberás informarnos tu nombre de usuario de GitHub y la URL de tu repositorio de GitHub de equipo, para que podamos acceder a él y descargar tu trabajo cuando se acerquen las fechas de entrega.

Hay un formulario que **debes completar** (como equipo) para registrar tu paquete de ROS con nosotros para la Asignación #2. El formulario está disponible a través del enlace que te compartirá el equipo docente (también disponible en la plataforma del curso).

El miembro del equipo que creó el repositorio (en el paso anterior) debe completar este formulario **ahora**.

!!! warning
    ¡No hacer esto (y hacerlo correctamente) podría resultar en que recibas **0 puntos** para las tareas de la asignación!

En algún momento dentro de las primeras semanas del curso se enviará un archivo `hello.md` a tu repositorio para confirmar que ha sido registrado correctamente.

### Inicializar el Paquete de ROS de tu Equipo (Localmente)

Nomina también a **solo un miembro de tu equipo** para hacer esta parte.

Debes hacerlo desde dentro de tu propia instalación de ROS (o WSL-ROS2), en lugar de en la laptop de robótica que usarás para trabajar con los robots reales en el laboratorio.

1. En GitHub, regresa a la página principal de tu repositorio haciendo clic en la pestaña `<> Code` en la parte superior izquierda.

1. Haz clic en el botón verde `Code` y luego, del menú desplegable, haz clic en el botón :octicons-copy-16: para copiar la URL **HTTPS** remota de tu repositorio.

    <figure markdown>
      ![](./getting-started/code-copy-url.png){width=600px}
    </figure>

1. Desde tu instalación local de ROS, abre una instancia de terminal y navega al directorio `src` del Espacio de Trabajo de ROS:

    ```bash
    cd ~/ros2_ws/src
    ```

1. Clona tu repositorio aquí usando la URL HTTPS remota:

    ```bash
    git clone REMOTE_HTTPS_URL
    ```

    Luego se te pedirá que ingreses tu nombre de usuario de GitHub, seguido de una contraseña. **¡Esta contraseña no es la contraseña de tu cuenta de GitHub!**

    !!! warning
        **¡La contraseña de tu cuenta de GitHub no funcionará aquí!** Necesitarás [generar un token de acceso personal](https://docs.github.com/en/authentication/keeping-your-account-and-data-secure/creating-a-personal-access-token#creating-a-personal-access-token-classic){target="_blank"} y usarlo en su lugar.

1. Navega al directorio del paquete usando el comando `cd`:

    ```bash
    cd ros2_lab_equipoXX
    ```
    
    (...reemplazando `XX` con tu número de equipo de la Asignación #2.)

1. Luego, ejecuta un script de inicialización para configurar tu paquete de ROS apropiadamente:

    ```bash
    ./init_pkg.sh
    ``` 

### Configurar Git {#git}

A continuación, deberás asegurarte de que Git esté correctamente configurado en tu instalación local de ROS antes de hacer cualquier otra cosa.

1. Desde la misma instancia de terminal que antes, ejecuta los siguientes comandos para actualizar tus datos personales en el archivo de configuración global de Git en tu máquina:

    ``` { .bash .no-copy }
    git config user.name "tu_nombre"
    ```
    ...¡reemplazando `tu_nombre` con tu nombre real! Por ejemplo: `#!bash git config --global user.name "Juan García"`
    
    ``` { .bash .no-copy }
    git config user.email "tu_dirección_de_correo"
    ```
    ...¡reemplazando `tu_dirección_de_correo` con tu dirección de correo real!

2. Si estás trabajando en WSL-ROS2 en una máquina del laboratorio, no olvides ejecutar `wsl_ros backup` para guardar estos cambios en tu archivo de respaldo externo de WSL-ROS2, para que siempre se restauren cuando ejecutes `wsl_ros restore` en una nueva instancia de WSL-ROS2 en otra máquina.

    !!! note
        **¡Todos los miembros del equipo deberán hacer esta parte antes de interactuar con Git!**

        Independientemente de qué miembro del equipo esté configurando el paquete de ROS de tu equipo para comenzar, todos **necesitaréis** interactuar con Git para esta asignación, y por lo tanto deberíais *cada uno* configurar vuestras propias configuraciones de Git individuales (a través de los pasos anteriores) antes de trabajar individualmente en el paquete de ROS de tu equipo.

### Publicar tu Paquete de ROS Local en GitHub {#git-push}

Nuevamente, **solo un miembro de tu equipo** necesita hacer esta parte.

Habiendo inicializado el paquete de ROS de tu equipo, ¡ya está listo para que comiences a llenarlo con código para las Tareas de la Asignación #2! Sin embargo, el primer paso es publicar los cambios realizados en el paso de inicialización (anterior) de vuelta en GitHub, para que todos en tu equipo estén trabajando desde el punto de partida correcto.

1. Desde la misma terminal que antes, usa el comando `git status` para ver todos los cambios realizados en el repositorio durante el proceso de inicialización:

    ```bash
    git status
    ```

1. Usa `git add` para *preparar* todos estos cambios para un commit inicial:

    ```bash
    git add .
    ```

    !!! warning
        ¡No olvides el `.` al final!

1. Luego realiza el commit:

    ```bash
    git commit -m "Package initialisations complete."
    ```

1. Finalmente, *publica* los cambios locales de vuelta al repositorio "remoto" en GitHub:

    ```bash
    git push origin main
    ```

    Luego se te pedirá que ingreses tu nombre de usuario y contraseña de GitHub nuevamente.
    
    !!! warning "Recuerda" 
        **No** es la contraseña de tu cuenta de GitHub... Usa el token de acceso personal que creaste anteriormente.

1. Todos los miembros del equipo deberían entonces poder clonar el repositorio remoto en sus propios Espacios de Trabajo de ROS (`#!bash cd ~/ros2_ws/src/ && git clone REMOTE_HTTPS_URL`), hacer contribuciones y publicarlas de vuelta al repositorio remoto según sea necesario (usando sus propias credenciales de cuenta de GitHub y tokens de acceso personal).

Necesitarás copiar tu paquete de ROS a las Laptops de los Robots cuando trabajes en las tareas basadas en robots reales, lo cual cubriremos con más detalle más adelante.

## Conocer los Robots Reales

La Asignación #2 involucra trabajo extenso con nuestros robots reales, y por lo tanto tendrás acceso a los robots durante cada sesión de laboratorio para que puedas trabajar en estas tareas como desees. Todos los detalles sobre cómo funcionan los robots, cómo ponerlos en marcha y comenzar a programarlos se pueden encontrar en la sección "Waffles" de este sitio del curso. Procede ahora de la siguiente manera (**en tus equipos**):

1. A cada equipo se le ha asignado un robot específico. Cuando estés listo, habla con un miembro del equipo docente quien te proporcionará el robot que se te ha asignado.
1. Trabaja en cada página de [la sección "Waffles" de este sitio](../../waffles/README.md) (**en orden**):
   
    * [ ] Lee sobre [el hardware](../../waffles/intro.md).
    * [ ] Aprende cómo [lanzar ROS y poner los robots en marcha](../../waffles/launching-ros.md).
    * [ ] Trabaja en los [Conceptos Básicos de Waffle (y ROS)](../../waffles/basics.md), que te ayudarán a comenzar y entender cómo funcionan ROS y los robots.
    * [ ] También hay información esencial adicional de la que debes ser consciente cuando trabajas con los robots reales. Trabaja en [los ejercicios adicionales aquí](../../waffles/essentials.md) ahora.
    * [ ] Finalmente, revisa los [Procedimientos de Apagado](../../waffles/shutdown.md). Sigue estos pasos para apagar el robot y apagar la laptop de robótica al final de cada sesión de laboratorio.
