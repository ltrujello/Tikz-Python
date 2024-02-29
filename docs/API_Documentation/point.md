# Point

::: tikzpy.drawing_objects.point.Point

# Examples
The `Point` class can be instantiated from a tuple or at least two `Number`s. One can also represent a point in 3D with this class.

```python
>>> from tikzpy import Point
>>> my_point = Point(-1, 2)
>>> my_point.x
-1
>>> my_point.y
2
```
You can also perform arithmetic with `Point` objects, either with other `Point` objects or with Python tuples. For example, the following are all valid.
```python
>>> my_point + (1, 1)  # Add it to another tuple
Point(0, 3)
>>> my_point + Point(2, 2)  # Add it with another point object
Point(1, 4)
>>> 2 * my_point  # Can also do my_point * 2 
Point(-2, 4)
>>> my_point / 3 
Point(-0.33333333, 0.666666666)
```

This allows you to write things like
```python
>>> circle = tikz.circle((0,0), radius=3)
>>> circle.center += (1, 1)  # This is valid
>>> circle.center /= 3  # Also valid
```
and this feature becomes quite useful in drawings that are highly complex.
