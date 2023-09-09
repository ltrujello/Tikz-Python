# `PlotCoordinates`

The `PlotCoordinates` class is used to represent the plot_coordinates functionality in TikZ. It is analagous to the TikZ command 
```
\draw plot[<options>] coordinates{ <points> };
```
The signature of the class is given below.
```python
from tikzpy import PlotCoordinates

plot = PlotCoordinates(points, options, plot_options, action)
```

| Parameter            | Description                                                                            | Default   |
| -------------------- | -------------------------------------------------------------------------------------- | --------- |
| `points` (list)      | A list of tuples (x, y) representing coordinates that one wishes to create a plot for. |
| `options` (str)      | A string of valid Tikz drawing options.                                                | `""`      |
| `plot_options` (str) | A string of valid Tikz plotting options                                                | `""`      |
| `action` (str)       | An action to perform with the line (e.g., `\draw`, `\fill`, `\filldraw`, `\path`)      | `"\draw"` |


## Examples
Introducing examples of `PlotCoordinates` gives us an opportunity to illustrate the optional parameter `action`. By default, `action` is `"draw"` (analogous to `\draw` in Tikz) so the code below
```python
import tikzpy

tikz = tikzpy.TikzPicture()
points = [(2, 2), (4, 0), (1, -3), (-2, -1), (-1, 3)]
plot = tikz.plot_coordinates(points) # action="draw" by default
plot.plot_options = "smooth cycle, tension = 0.5"
```
produces the image 

<img src="../png/plotcoordinates_ex_1.png"/>

Alternatively we can set `action = "fill"` (analogous to `\fill` in Tikz) as in the code below
```python
import tikzpy

tikz = tikzpy.TikzPicture()
points = [(2, 2), (4, 0), (1, -3), (-2, -1), (-1, 3)]
plot = tikz.plot_coordinates(points, options="Blue", action="fill")
plot.plot_options = "smooth cycle, tension = 0.5"
```
to produce the image

<img src="../png/plotcoordinates_ex_2.png"/>

If we want both, we can set `action = "filldraw"` (analogous to `\filldraw` in Tikz)
```python
import tikzpy

tikz = tikzpy.TikzPicture()
points = [(2, 2), (4, 0), (1, -3), (-2, -1), (-1, 3)]
plot = tikz.plot_coordinates(points, options="Blue", action="filldraw")
plot.options = "fill=ProcessBlue!50"
plot.plot_options = "smooth cycle, tension = 0.5"
```
which produces. 
<img src="../png/plotcoordinates_ex_3.png"/>

Finally, we can set `action = "path"` (analogous to `\path` in Tikz), but as one would expect this doesn't draw anything. 


## Methods

`PlotCoordinates` has methods `.shift()`, `.scale`, and `.rotate`, similar to the class `Line`, and the parameters behave similarly. These methods are more interestingly used on `PlotCoordinates` than on `Line`. For example, the code
```python
import tikzpy

tikz = tikzpy.TikzPicture()
points = [(14.4, 3.2), (16.0, 3.6), (16.8, 4.8), (16.0, 6.8), (16.4, 8.8), (13.6, 8.8), (12.4, 7.6), (12.8, 5.6), (12.4, 3.6)]

for i in range(0, 20):
    options = f"fill = {rainbow_colors(i)}, opacity = 0.7"
    # Requires \usetikzlibrary{hobby} here
    plot_options = "smooth, tension=.5, closed hobby"
    plot = tikz.plot_coordinates(points, options, plot_options)
    plot.scale((20 - i) / 20) # Shrink it 
    plot.rotate(15 * i) # Rotate it
```
generates the image

<img src="../png/PlotCoords_rotate_Example.png"/>

