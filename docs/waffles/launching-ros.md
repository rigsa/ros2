---  
title: Lanzando ROS (y Emparejando la Laptop)
---  

El primer paso es lanzar ROS en el Waffle.

!!! info "Importante"
    ¡Esto garantiza que toda la funcionalidad básica de ROS se ejecute en el robot; sin esto, el robot no podrá hacer *nada*!

## Paso 1: Identificar tu Waffle

Los robots se nombran de la siguiente manera:

    robot-X

... donde `X` es el *'Número de Robot'* (un número entre 1 y 50). ¡Asegúrate de saber con cuál robot estás trabajando revisando la etiqueta impresa en la parte superior!

## Paso 2: Emparejar tu Waffle con una Laptop

[Como se explicó anteriormente](./intro.md#laptops), se te proporcionará una de nuestras Laptops del Laboratorio para trabajar en el laboratorio, y el robot debe emparejarse con esta para que ambos funcionen juntos.

1. Abre una instancia de terminal en la laptop, ya sea usando el atajo de teclado ++ctrl+alt+t++ o haciendo clic en el ícono de la aplicación Terminal en la barra de favoritos del lado izquierdo del escritorio:
    
    <figure markdown>
      ![](../images/laptops/terminal_icon.svg){width=60px}
    </figure>

1. Usaremos nuestra CLI `waffle` específicamente diseñada para manejar el proceso de emparejamiento. Ejecútala en la terminal ingresando el siguiente comando para *emparejar* la laptop y el robot:

    ```bash
    waffle X pair
    ```
    Reemplazando `X` con el número del robot con el que estás trabajando.
    
1. Es posible que veas un mensaje como este al inicio del proceso de emparejamiento:

    <figure markdown>
      ![](../images/laptops/ssh_auth.svg){width=600px}
    </figure>

    Si es así, simplemente escribe `yes` y presiona ++enter++ para confirmar que deseas continuar.

1. Ingresa la contraseña del robot cuando se te solicite (¡te la indicaremos en el laboratorio!)

    !!! note
        No verás ningún cambio en la pantalla cuando estés ingresando la contraseña. ¡Esto es normal, sigue escribiendo!
    
1. El proceso de emparejamiento tardará un minuto, pero una vez finalizado deberías ver un mensaje que dice `pairing complete`, mostrado en azul en la terminal.

1. Luego, en la misma terminal, ingresa el siguiente comando: <a name="tmux"></a>

    ```bash
    waffle X term
    ```
    (nuevamente, reemplazando `X` con el número de *tu* robot).
    
    Debería aparecer un banner verde en la parte inferior de la ventana de la terminal:
    
    <figure markdown>
      ![](../images/laptops/tmux.svg){width=500px}
    </figure>

    Esta es una instancia de terminal que se ejecuta **en el robot**, y cualquier comando que ingreses aquí se ejecutará *en el robot* (¡no en la laptop!)

## Paso 3: Lanzando ROS {#step3}

Lanza ROS en el robot ingresando el siguiente comando:

```bash
ros2 launch rigsa_tb3_tools ros.launch.py
```

Si todo está bien, el robot reproducirá un agradable sonido *"do-re-mi"* y debería aparecer un mensaje como este (entre todo el otro texto):

``` { .txt .no-copy }
[tb3_status.py-#] ######################################
[tb3_status.py-#] ### robot-X is up and running! ###
[tb3_status.py-#] ######################################
```

Ya no deberías necesitar interactuar con esta instancia de terminal, pero la pantalla te proporcionará información en tiempo real sobre el estado del robot. Por tanto, mantén esta terminal abierta en segundo plano y verifica el indicador de `Battery` de vez en cuando:

``` { .txt .no-copy } 
Battery: 12.40V [100%]
```

!!! info "Batería Baja :material-battery-low:"

    **¡La batería del robot no durará una sesión de laboratorio completa de 2 horas!**

    Cuando el indicador de capacidad llegue alrededor del 15%, comenzará a emitir pitidos, y cuando llegue a ~10% dejará de funcionar por completo. Avísale a un miembro del equipo docente cuando la batería esté baja y la reemplazaremos para ti. (¡Es más fácil hacerlo cuando llega al 15%, en lugar de esperar a que baje del 10%!)


## Paso 4: Conectarse al *Router Zenoh* {#step4}

Usamos una implementación de Middleware de ROS 2 (RMW) llamada [Zenoh](https://github.com/ros2/rmw_zenoh) para habilitar la comunicación robot-laptop a través de la red inalámbrica. El Waffle actúa como el *Router* Zenoh, y esto se habilitó como parte de las operaciones de *bringup* que lanzaste en el [Paso 3 anterior](#step3). Ahora necesitamos lanzar una *Sesión* en la laptop para conectarse a este router.

!!! warning "¡Esto es Esencial!"
    ¡**Siempre** necesitas tener una sesión Zenoh ejecutándose en la laptop para poder comunicarte con tu robot!

Abre **una nueva instancia de terminal** en la laptop (ya sea usando el atajo ++ctrl+alt+t++ o haciendo clic en el ícono de la aplicación Terminal) e ingresa el siguiente comando:

```bash
ros2 run rmw_zenoh_cpp rmw_zenohd
```

Ahora deberías tener dos terminales activas:

1. La terminal del *robot* donde ejecutaste la operación `ros2 launch rigsa_tb3_tools ros.launch.py` (también conocida como *"el bringup"*) en el [Paso 3](#step3)[^term_recover]
1. La terminal de la *laptop* donde acabas de ejecutar el nodo `rmw_zenohd`

[^term_recover]: Si llegaste a cerrar la terminal del *robot*, puedes volver a ella ingresando `waffle X term` desde una nueva instancia de terminal en la laptop.

Deja ambas terminales en funcionamiento, pero **mantenlas ejecutándose en segundo plano en todo momento** mientras trabajas con tu robot.

## Apagado (al final de una Sesión de Laboratorio)

Cuando hayas terminado de trabajar con un robot, es muy importante **apagarlo correctamente** antes de apagar el interruptor de encendido. Consulta los [procedimientos de apagado seguro](./shutdown.md) para más información.
