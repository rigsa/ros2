---
title: "A move_circle.py Worked Example" 
---

A working `move_circle.py` node (from [Part 2 Exercise 5](../part2.md#ex5)) complete with a proper shutdown procedure. Use this as a starting point for your `param_circle.py` node for the Part 3 Parameters Exercise.

## The Code

```python title="param_circle.py"
--8<-- "https://raw.githubusercontent.com/tom-howard/com2009_exercises/refs/heads/jazzy/part2_navigation/scripts/move_circle.py"
```

## Adding Package Dependencies

The `param_circle.py` node will live inside your `part3_beyond_basics` package, and so make sure you define the necessary dependencies within the `package.xml` file.

Find this line:

```xml title="part3_beyond_basics/package.xml"
...
<exec_depend>geometry_msgs</exec_depend>
...
```
