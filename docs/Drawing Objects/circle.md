# `Circle`

The `Circle` class helps create circles in Tikz. It is analagous to the Tikz code 
```
\draw <center> circle <radius>
```
The signature of the class is below.
```python
from tikzpy import Circle

circle = Circle(center, radius, options, action)
```


| Parameter        | Description                                                                         | Default   |
| ---------------- | ----------------------------------------------------------------------------------- | --------- |
| `center` (tuple) | A tuple (x, y) of floats representing the coordinates of the center of the circle.  |
| `radius` (float) | Length (in cm) of the radius. (By the way, all lengths are taken in cm).            |
| `options` (str)  | String containing valid Tikz drawing options (e.g, "Blue")                          | `""`      |
| `action` (str)   | An action to perform with the circle (e.g., `\draw`, `\fill`, `\filldraw`, `\path`) | `"\draw"` |


## Examples
Here we create several circles, making use of the `action` parameter. 
```python
import tikzpy

tikz = tikzpy.TikzPicture()
tikz.circle((0, 0), 1.25) #action="draw" by default
tikz.line((0, 0), (0, 1.25), options="dashed")
tikz.circle((3, 0), 1, options="thick, fill=red!60", action="filldraw")
tikz.circle((6, 0), 1.25, options="Green!50", action="fill")
```

<img src="/Tikz-Python/png/circle_ex_1.png"/>

We can also use circles to create the [Hawaiian Earing](https://en.wikipedia.org/wiki/Hawaiian_earring).

```python
import tikzpy

tikz = tikzpy.TikzPicture()

radius = 5
for i in range(1, 60):
    n = radius / i
    tikz.circle((n, 0), n)
```
<img src="/Tikz-Python/png/circle_ex_2.png"/>


## Methods
`Circle` has access to methods `.shift()`, `.scale()`, `.rotate()`, which behave as one would expect and takes in parameters as described before.

