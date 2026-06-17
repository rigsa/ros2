# Laboratorio de Robótica con ROS 2

## Con el TurtleBot3 Waffle, Go2 EDU y ROS 2 Jazzy

Material de enseñanza para el laboratorio de ROS 2, adaptado para Panamá.

Accede al sitio aquí: https://rigsa.github.io/ros2/

> Este material está basado en el curso original de [Tom Howard](https://github.com/tom-howard) (Universidad de Sheffield), disponible en [https://github.com/tom-howard/tuos_ros](https://github.com/tom-howard/tuos_ros), y está licenciado bajo [CC BY-SA 4.0](http://creativecommons.org/licenses/by-sa/4.0/).

## Contribuir

### Configurar el entorno Python

El sitio se construye con [Material for MkDocs](https://squidfunk.github.io/mkdocs-material/).

Primero, crea un entorno virtual de Python (3.9 o superior):

```
python3 -m venv venv
```

**[Activa el entorno](https://realpython.com/what-is-pip/#using-pip-in-a-python-virtual-environment)** e instala las dependencias desde [`requirements.txt`](./requirements.txt):

```
pip install -r requirements.txt
```

### Edición

El contenido del sitio se encuentra en el directorio `docs/`. Referencias útiles:

* Guía general de Markdown: [Markdown Cheatsheet](https://www.markdownguide.org/cheat-sheet/)
* Documentación de Material for MkDocs: https://squidfunk.github.io/mkdocs-material/reference/

Para previsualizar el sitio mientras editas (¡asegúrate de tener el entorno activo!):

```
mkdocs serve
```

Luego abre http://localhost:8000/ros2/ en el navegador.
