---  
title: "Plantilla de Declaración de GenIA"  
--- 

<!-- For info: https://ai-declaration.md/en/0.1.2/ -->

Todos los equipos **DEBEN** incluir un archivo `AI-Declaration.md` en la raíz del directorio de su paquete:

``` { .txt .no-copy }
ros2_lab_equipoXX/AI-Declaration.md
```

Este archivo debe estar escrito con *Texto con Formato Markdown* y debe seguir la plantilla que se muestra aquí:

```html title="AI-Declaration.md"
# Declaración de GenIA del Equipo XX <!-- (6)! -->

Declaración del uso de IA Generativa para la Asignación #2 Parte B (Tarea 3). 

## Reconocimiento

Reconocemos el uso de <!-- (1)! --> para los siguientes propósitos:
<!-- (2)! -->
* [ ] para investigación de fondo en la elaboración de esta evaluación. 
* [ ] para generar materiales que fueron incluidos en el envío final de código de forma modificada.

## Descripción
<!-- (3)! -->

## Evidencia
<!-- (4)! -->

## Declaración
<!-- (5)! -->
* [ ] Confirmamos que ningún contenido creado por IA generativa ha sido presentado como nuestro propio trabajo. 

```

1. Inserta el nombre del/los sistema(s) de IA aquí.

2. Para marcar una casilla usando Markdown, pon una `x` dentro de los corchetes:
    
    ``` { .md .no-copy }
    * [ ] para investigación de fondo...
    * [x] para generar materiales... 
    ```

3. Proporciona un resumen de cómo usaste la IA generativa en esta asignación. Puede que desees incluir la siguiente información:

    * ¿Qué indicaciones (prompts) usaste?
    * ¿Qué resultados generaste?
    * ¿Cómo usaste/adaptaste/desarrollaste los resultados?

4. Proporciona evidencia de los resultados que se generaron, por ejemplo:

    ```  { .md .no-copy }
    Sistema de IA Generativa:
    Indicación (Prompt):
    Resultado:
    ```

    o [proporcionando capturas de pantalla](https://docs.github.com/en/get-started/writing-on-github/getting-started-with-writing-and-formatting-on-github/basic-writing-and-formatting-syntax#images){target="_blank"}.

5. **Importante**: Marca la casilla para confirmar esto:

    ``` { .md .no-copy }
    * [x] Confirmamos que ... 
    ```

6. Reemplaza `XX` con tu número de equipo.

[Para sintaxis básica de formato Markdown, consulta aquí](https://docs.github.com/en/get-started/writing-on-github/getting-started-with-writing-and-formatting-on-github/basic-writing-and-formatting-syntax){target="_blank"}.

Si tu equipo no usó GenIA de ninguna manera para la Asignación #2 Parte B, entonces el siguiente `AI-Declaration.md` será suficiente:

```html title="AI-Declaration.md"
# Declaración de GenIA del Equipo XX <!-- (1)! -->

Declaración del uso de IA Generativa para la Asignación #2 Parte B (Tarea 3). 

## Declaración
<!-- (2)! -->
* [ ] No usamos IA de ninguna manera para esta asignación. 

```

1. Reemplaza `XX` con tu número de equipo.
2. Asegúrate de marcar la casilla para confirmar esto:

    ``` { .md .no-copy }
    * [x] No usamos IA ... 
    ```
