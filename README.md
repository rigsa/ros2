# Laboratorio de Robótica con ROS 2

## Con el TurtleBot3 Waffle, Go2 EDU y ROS 2 Jazzy

Material de enseñanza para el laboratorio de ROS 2, adaptado para Panamá.

Accede al sitio aquí: https://rigsa.github.io/ros2/

> Este material está basado en el curso original de [Tom Howard](https://github.com/tom-howard) (Universidad de Sheffield), disponible en [https://github.com/tom-howard/tuos_ros](https://github.com/tom-howard/tuos_ros), y está licenciado bajo [CC BY-SA 4.0](http://creativecommons.org/licenses/by-sa/4.0/).

## Desarrollo local

El sitio se construye con [Material for MkDocs](https://squidfunk.github.io/mkdocs-material/). Requiere Python 3.9 o superior.

```bash
# 1. Crear y activar entorno virtual
python3 -m venv venv
source venv/bin/activate        # Windows: venv\Scripts\activate

# 2. Instalar dependencias
pip install -r requirements.txt

# 3. Previsualizar en vivo
mkdocs serve
```

Abre http://localhost:8000/ros2/ en el navegador. El sitio se recarga automáticamente al guardar cambios en `docs/`.

## Despliegue en GitHub Pages

El sitio se publica automáticamente vía GitHub Actions al hacer push a `main` (ver [`.github/workflows/gh-pages.yml`](.github/workflows/gh-pages.yml)).

Para publicar manualmente desde tu máquina (requiere el entorno virtual activo y permisos de escritura al repo):

```bash
mkdocs gh-deploy --force
```

Esto construye el sitio y lo empuja a la rama `gh-pages`. El sitio queda disponible en https://rigsa.github.io/ros2/ en ~1 minuto.

## Estructura del contenido

El contenido del sitio se encuentra en `docs/`. Referencias útiles:

- Guía de Markdown: [Markdown Cheatsheet](https://www.markdownguide.org/cheat-sheet/)
- Referencia de Material for MkDocs: https://squidfunk.github.io/mkdocs-material/reference/
