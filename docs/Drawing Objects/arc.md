# `Arc`

The arc class helps create arcs in Tikz. It is analagous to the TikZ code 
``` 
\draw <center> arc (<start_angle>:<end_angle>:<radius>);
```
The signature of this class is below.
```python
from tikzpy import Arc

arc = Arc(center, start_angle, end_angle, radius, options, radians, action)
```

| Parameter                | Description                                                                                                                                      | Default   |
| ------------------------ | ------------------------------------------------------------------------------------------------------------------------------------------------ | --------- |
| `position` (tuple)       | Pair of points representing either the center of the arc or the point at which it should begin drawing (see `draw_from_start`                    |
| `start_angle` (float)    | The angle (relative to the horizontal) of the start of the arc                                                                                   |
| `end_angle` (float)      | The angle (relative to the horizontal) of the end of the arc                                                                                     |
| `radius` (float)         | The radius (in cm) of the arc. If specified, `x_radius` and `y_radius` cannot be specified.                                                      |
| `x_radius` (float)       | The x radius (in cm) of the arc. In this case, `y_radius` must also be specified.                                                                |
| `y_radius` (float)       | The y radius (in cm) of the arc. In this case, the `x_radius` must also be specified.                                                            |
| `options` (str)          | A string of containing valid Tikz arc options                                                                                                    | `""`      |
| `radians` (bool)         | `True` if angles are in radians, `False` otherwise                                                                                               | `False`   |
| `draw_from_start` (bool) | `True` if `position` represents the point at which the arc should begin drawing. `False` if `position` represents the center of the desired arc. | `True`    |
| `action` (str)           | An action to perform with the arc (e.g., `\draw`, `\fill`, `\filldraw`, `\path`)                                                                 | `"\draw"` |


## Example
Here we draw and fill a sequence of arcs. We also demonstrate `draw_from_start` set to `True` and `False`. In the code below, it is by default set to `True`.
```python
from tikzpy import TikzPicture
from tikzpy.utils import rainbow_colors

tikz = TikzPicture()

for i in range(1, 10):
    t = 4 / i
    arc = tikz.arc((0, 0), 0, 180, radius=t, options=f"fill={rainbow_colors(i)}")

```
This generates the image

<img src="../png/arc_ex_1.png"/>

If instead we would like these arcs sharing the same center, we can use the same code, but pass in `draw_from_start=False` to achieve 

<img src="../png/arc_ex_2.png"/>

Without this option, if we were forced to specify the point at which each arc should begin drawing, we would have to calculate the x-shift for every arc and apply such a shift to keep the centers aligned. That sounds inefficient and like a waste of time to achieve something so simple, right?


## Methods 
`Arc` has access to methods `.shift()`, `.scale()`, `.rotate()`, which behave as one would expect and takes in parameters as described before.

## A few comments...
This class not only provides a wrapper to draw arcs, but it also fixes a few things that Tikz's `\draw arc` command simply gets wrong and confuses users with.

1. With Tikz in TeX, to draw a circular arc one must specify `start_angle` and `end_angle`. These make sense: they are the start and end angles of the arc relative to the horizontal. To draw an elliptic arc, one must again specify `start_angle` and `end_angle`, but these actually do not represent the starting and end angles of the elliptic arc. They are the parameters `t` which parameterize the ellipse `(a*cos(t), b*sin(t))`. This makes drawing elliptic arcs inconvenient.

2. With Tikz in TeX, the position of the arc is specified by where the arc should start drawing. However, it is sometimes easier to specify the *center* of the arc.

With Tikz-Python, `start_angle` and `end_angle` will always coincide with the starting and end angles, so the user will not get weird unexpected behavior. Additionally, the user can specify the arc position via its center by setting `draw_from_start=False`, but they can also fall back on the default behavior.

