---  
title: "VS Code y WSL"  
---

## Lanzar VS Code desde el Terminal {#the-top}

1. Puedes lanzar VS Code directamente desde una instancia de terminal WSL-ROS2. Simplemente escribe `code .` en el prompt del terminal y luego presiona ++enter++:

    ```bash
    code .
    ```

1. Entonces puede aparecer un mensaje de advertencia:

    <figure markdown>
      ![](../figures/code-allow-host.png){width=500px}
    </figure>

    Marca la casilla para "Permanently allow ..." y luego haz clic en el botón `Allow`.

1. VS Code debería entonces lanzarse, y se te presentará otro diálogo de confianza:

    <figure markdown>
      ![](../figures/code-trust-home.png){width=500px}
    </figure>

    Haz clic en el botón azul `Yes, I trust the authors`.

## Instalar la Extensión WSL {#wsl-ext}

1. La primera vez que lances VS Code (como se indicó arriba) debería aparecerte una ventana emergente en la parte inferior derecha de la pantalla, preguntando si deseas "instalar la extensión 'WSL' recomendada de Microsoft..."

    <figure markdown>
      ![](../figures/code-install-wsl-ext-prompt.png){width=500px}
    </figure>

    Haz clic en el botón azul "Install".

    ??? bug "¿No ves la ventana emergente?" 
        
        También puedes instalar la extensión 'WSL' manualmente.
        
        Haz clic en el ícono "Extensions" en la barra de herramientas de la izquierda (o presiona ++ctrl+shift+x++), escribe "wsl" en el cuadro de búsqueda y haz clic en el botón de instalar en la extensión correcta, como se muestra a continuación:

        <figure markdown>
          ![](../figures/wsl-ext-manual-install-annt.png){width=600px}
        </figure>

1. Una vez instalada, cierra VS Code, regresa a la instancia de terminal WSL-ROS2 y vuélvelo a lanzar usando el comando `code .`.
    
    Esta vez, se te presentará *otro* diálogo emergente de confianza. Una vez más, marca la casilla para "Trust the authors" y luego haz clic en el botón azul `Yes, I trust the authors`. 

1. Ahora puedes navegar por el sistema de archivos WSL-ROS2 en la ventana del explorador en el lado izquierdo de la pantalla de VS Code. ¡Necesitarás usar esto para localizar los packages y scripts que crees a lo largo de este curso!

    <figure markdown>
      ![](../figures/code-wsl-explorer-annt.svg){width=600px}
    </figure>

## ¡Siempre asegúrate de que la extensión "WSL" esté habilitada!! {#verify}

Verifica que tu ícono azul de "Remote Window" en la parte inferior izquierda de la pantalla de VS Code siempre se vea así:

<figure markdown>
  ![](../figures/code-wsl-ext-on.svg){width=400px}
</figure>

¡Si no es así, regresa al [inicio de esta página](#the-top) e inténtalo de nuevo!