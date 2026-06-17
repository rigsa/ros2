---
title: "Un Ejemplo Resuelto de move_circle.py" 
---

Un node `move_circle.py` funcional (del [Ejercicio 5 de la Parte 2](../part2.md#ex5)) con un procedimiento de apagado adecuado. Úsalo como punto de partida para tu node `param_circle.py` en el Ejercicio de Parameters de la Parte 3.

## El Código

```python title="move_circle.py"
--8<-- "https://raw.githubusercontent.com/tom-howard/com2009_exercises/refs/heads/jazzy/part2_navigation/scripts/move_circle.py"
```

## Agregando Dependencias del Package

Asegúrate de definir las dependencias de este node dentro del archivo `package.xml` de tu package.

Encuentra esta línea:

```xml title="package.xml"
...
<exec_depend>geometry_msgs</exec_depend>
...
```
