---
title: "Usar Nav2 para la Tarea 3"
---

[Nav2](https://docs.nav2.org/){target="_blank"} es una pila de navegación autónoma integrada en ROS 2. Puede parecer la elección lógica para la Tarea 3, pero hay algunas consideraciones importantes que debes tener en cuenta antes de optar por este enfoque.

## Algunas Advertencias

### "Esto funcionó genial en simulación, pero..."

Muchas preguntas que recibimos en el laboratorio comienzan con esta frase.

Nav2 es un ejemplo clásico de esto: puedes pasar mucho tiempo elaborando cuidadosamente una solución que funciona genial en simulación, solo para descubrir que nada funciona igual en el hardware real en el laboratorio. **Necesitarás hacer muchas pruebas en el mundo real** para optimizar y ajustar la pila de navegación para que funcione efectivamente en el arena robótico real.

Si quieres usar Nav2, asegúrate de tener esto en cuenta: solo tienes acceso limitado al hardware real, así que planifica en consecuencia y asegúrate de poder hacer suficientes pruebas para estar seguro de que tu solución funcionará como se espera el día de la evaluación.

En última instancia, **no podemos darte acceso adicional a los robots fuera de los laboratorios/sesiones de consulta** (y recuerda que las reservas para las sesiones de consulta son limitadas y están disponibles por orden de llegada).

### No Somos Expertos en Nav2

El equipo docente no tiene experiencia extensiva en el uso de Nav2 (¡no tenemos el tiempo!), por lo que si tienes problemas es poco probable que podamos ayudarte mucho en los laboratorios.

### Garantizar un Rendimiento Óptimo de WiFi en el Laboratorio

Dependemos en gran medida de un buen WiFi en el laboratorio para que nuestros robots funcionen efectivamente. Hemos trabajado muy duro para asegurarnos de que nuestros robots y nuestra red WiFi en el laboratorio sean suficientes para el *uso general* de todos los equipos en los laboratorios.

En el pasado, hemos observado que Nav2 genera una demanda excesiva en la red y provoca problemas de rendimiento para todos. En última instancia, no consideramos Nav2 como una herramienta de *"uso general"*, y por lo tanto no priorizaremos este tipo de uso en el laboratorio. Esto significa que, si observamos problemas durante las sesiones de laboratorio que surgen debido al uso intensivo de Nav2, limitaremos el número de equipos que pueden usarlo simultáneamente.

## En Resumen

Cualquier equipo que desee usar Nav2 para la Tarea 3 ***lo hace bajo su propio riesgo***.
