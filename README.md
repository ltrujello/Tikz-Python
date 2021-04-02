# Tikz-Python
An object-oriented Python approach towards providing a giant wrapper for Tikz code, with the goal of streamlining the process of creating complex figures for TeX documents.


## How to Use: Basics
Am example of this package in action is below. 
```python
from tikzpy import TikzPicture  # Import the class TikzPicture

tikz = TikzPicture(tikz_file = "my_tikz_code.tex") # Line 1
tikz.line((0,0), (1,1), options = "thick, blue") # Line 2
tikz.write() # Line 3
```
We explain line-by-line what this means.

* `from tikzpy import TikzPicture` imports the `TikzPicture` class from the `tikzpy` package. For this to work, simply put the repository `tikzpy` with your other python packages.

* **Line 1** is analagous to the TeX code `\begin{tikzpicture}` and `\end{tikzpicture}`. The variable `tikz` is now a tikz environment, specifically an instance of the class `TikzPicture`, and we can now append drawings to it. And `tikz_file` is the file (or more generally, any file path) where our tikz code will be stored.

* **Line 2** draws a blue line in the tikz environment `tikz`. 
In TeX, this code would be `\draw[thick, blue] (0,0) -- (1,1);`.

* **Line 3** writes all of our code into the file `my_tikz_code.tex`.

### Example: Line and two nodes
Suppose I want to create a line and two labels at the ends:
```python
import tikzpy

tikz = tikzpy.TikzPicture()
line = tikz.line((0,0), (1,1), options = "thick, blue, o-o")
start_node = tikz.node(line.start, options = "below", text = "Start!")
end_node = tikz.node(line.end, options = "above", text = "End!")
```
Saving the line as a variable `line` allows us to pass in `line.start` and `line.end` into the node positions, so we don't have to type out the exact coordinates. 
This is because lines, nodes, etc. are class instances with useful attributes: 
```python
>>> line.start
(0,0)
>>> line.end
(1,1)
>>> start_node.text
"Start!"
```
Running our previous python code, we obtain
<img src="https://github.com/ltrujello/Tikz-Python/blob/main/examples/example_imgs/line_and_two_nodes.png" height = 200/> 


### Example: Circles
Pythons `for` loop is a lot less messier and much more powerful than the `\foreach` loop provided in Tikz via TeX. (For example, Tikz with TeX alone guesses your step size, and hence it cannot effectively [loop over two different sequences at the same time](https://tex.stackexchange.com/questions/171426/increments-in-foreach-loop-with-two-variables-tikz)).

In this example, we see that looping is pretty clean. 
```python
import tikzpy

tikz = tikzpy.TikzPicture(center=True)
for i in range(30):
    # i/30-th point on the unit circle
    point = (math.sin(2 * math.pi * i / 30), math.cos(2 * math.pi * i / 30))

    # Create four circles of different radii with center located at point
    tikz.circle(point, 2, "ProcessBlue")
    tikz.circle(point, 2.2, "ForestGreen")
    tikz.circle(point, 2.4, "red") 
    tikz.circle(point, 2.6, "Purple")

tikz.write()
```
<img src="https://github.com/ltrujello/Tikz-Python/blob/main/examples/example_imgs/circles.png" height = 350/>


### Example: Roots of Unity 
Suppose I want to draw the [roots of unity](https://en.wikipedia.org/wiki/Root_of_unity). Normally, I would have to spend 30 minutes reading some manual about how TeX handles basic math. With Python, I know I can `import math` and make intuitive computations to quickly build a function that displays the nth roots of unity.
```python
import math
import tikzpy

tikz = tikzpy.TikzPicture()
n = 13 # Let's see the 13 roots of unity

for i in range(n):
    # Find the angle/location of the nth root on the unit circle
    theta = (2 * math.pi * i) / n
    x = scale * math.cos(theta) 
    y = scale * math.sin(theta)
    
    # A label for our node
    root_label = f"$e^{{ (2 \cdot \pi \cdot {i})/ {n} }}$"

    # Draw a line from the origin to our point 
    tikz.line((0, 0), (x, y), options="-o")

    if 0 <= theta <= math.pi:
        node_option = "above"
    else:
        node_option = "below"

    # Label the nth root of unity
    tikz.node((x, y), options=node_option, text=root_label)

tikz.write()
```
Which generates: 
<img src="https://github.com/ltrujello/Tikz-Python/blob/main/examples/example_imgs/roots_of_unity.png" height = 350/>

### Example: General Ven Diagrams 
Python has access to many libraries that help one efficiently build very complex functions. Such libraries are simply not possible to implement in TeX (well, not impossible, but it'd be ridiculous). 
Tikz-Python offers [this function](https://github.com/ltrujello/Tikz-Python/blob/main/tests/intersections_scope_clip.py), which uses `itertools.combinations`, to take in an arbitrary number of 2D Tikz figures and colors each and every single intersection. For example, here is what all of the intersections of nine circles in a 3 x 3 grid looks like.

<img src="https://github.com/ltrujello/Tikz-Python/blob/main/examples/example_imgs/intersection_circles.png" height = 350/>

Here's what the intersections of three random blobs looks like:

<img src="https://github.com/ltrujello/Tikz-Python/blob/main/examples/example_imgs/intersection_blobs.png" height = 350/>

As one might guess, this is useful for creating topological figures, as manually writing all of the `\scope` and `\clip` commands to create such images is pretty tedious.

### Example: Barycentric subdivision
Another example of using simple python libraries is the following. [The source here](https://github.com/ltrujello/Tikz-Python/blob/main/examples/barycentric.py) allows us to generate the the n-th barycentric subdivision of a triangle. 

<img src="https://github.com/ltrujello/Tikz-Python/blob/main/examples/example_imgs/barycentric.png" height = 350/>

### Example 
In [the source here](https://github.com/ltrujello/Tikz-Python/blob/main/tests/integrate_and_plot.py), we use `numpy` and `sympy` to very simply perform symbolic integration. The result is a function which plots and labels the integrals of a polynoimal. For example, the output of `x**2` (the polymoial x^2) generates the image below. 

<img src="https://github.com/ltrujello/Tikz-Python/blob/main/examples/example_imgs/integration_ex.png"/>



# Class: `TikzPicture`
Initialize an object of this class as below
```python
import tikzpy

tikz = tikzpy.TikzPicture(tikz_file, center, options)
```
or more simply as 
```python
from tikzpy import TikzPicture

tikz = TikzPicture(tikz_file, center, options)
```


Parameter    | Description | Default|
-------------|-------------|-------------|
`tikz_file` (str) | The desired file path for Tikz code output. Can be a relative or full path. | `tikz_code/tikz_code.tex`|
`center` (bool) | True if you would like your tikzpicture to be centered, false otherwise. | `False`|
`options` (str) | A string containing valid Tikz options. | `""`|


## Methods  
### `TikzPicture.write()`
Writes the currently recorded Tikz code into the .tex file located at `my_tikz_file`. If `my_tikz_file` is not specified, the directory `tikz/tikz_file.tex` is created automatically and the code is stored there.

**Question:** If I call `tikz.write()` twice on accident, won't that accidentally add duplicate code? No! (You can, however, if you want). This is the key feature of `write()`. In fact, you can continue editing even after you call `write` so that you may periodically view your Tikz picture while you build it.

For example, suppose I want to draw a blue circle.
```python
>>> tikz = tikzpy.TikzPicture()
>>> circle_1 = tikz.circle((0,0), 2, options = "fill=Blue, opacity=0.5") # Draws a blue circle 
>>> tikz.write() # Write it 
```
<img src="https://github.com/ltrujello/Tikz-Python/blob/main/examples/example_imgs/tikz_write_ex_1.png"/>

I called `.write()` which writes the code for a blue circle. In the same instance, I can add `circle_2`, a red circle, to the picture. I can also update the center of `circle_1`.
```python
>>> circle_2 = tikz.circle((1,1), 2, options = "fill=red, opacity=0.5") # I want another circle...
>>> circle_1.center = (2,2) # I want to change my other circle's center...
>>> tikz.write() # Write it 
>>> tikz # The resulting tikzcode. We get what we'd expect  
... \begin{tikzpicture}[]% TikzPython id = (1) 
	\draw[fill=Blue] (2, 2) circle (2cm);
	\draw[fill=Red] (1, 1) circle (2cm);
\end{tikzpicture}
```
<img src="https://github.com/ltrujello/Tikz-Python/blob/main/examples/example_imgs/tikz_write_ex_2.png"/>

This feature, in combination with `.remove()` and `.show()` (see below), allows you to gradually build and view a TikzPicture quite painlessly.

### `TikzPicture.remove(draw_obj)`
Removes a drawing object, such as a line, from a TikzPicture. Here, we draw an arc and a line. Then, we remove the line.

```python
>>> tikz = tikzpy.TikzPicture()
>>> line = tikz.line((0,0), (1,1), options = "Blue") # Draws a line 
>>> arc = tikz.arc((0,0), 45, 90, 3) # Draws an arc
>>> tikz 
... \begin{tikzpicture}[]% TikzPython id = (1)
    \draw[Blue] (0, 0) -- (1,1); # The line
    \draw (0, 0) arc (45:90:3cm);
\end{tikzpicture}
>>> tikz.remove(line) # The line is removed
>>> tikz 
... \begin{tikzpicture}[]% TikzPython id = (1) 
	\draw (0, 0) arc (45:90:3cm);
\end{tikzpicture}
```

### `TikzPicture.draw(draw_obj)`
Draws a drawing object, such as a line, onto the TikzPicture. Sometimes, we want to construct a drawing object before we want to draw it onto the tikzpicture. 
```python
>>> line = tikzpy.Line((0,0) (1,0), to_options = "to[bend right = 30]")
>>> end_c = tikzpy.Circle(line.start, radius = 0.2)
>>> start_c = tikzpy.Circle(line.end, radius = 0.2)
>>> tikz.draw(line, end_c, start_c) # The line is now drawn
```
Here we use `tikzpy.Line` and `tikzpy.Circle` to construct a line and circle. These objects have no relation to our image until we draw them with `tikz.draw`.


### `TikzPicture.show()`
Compiles the tikz code and pulls up a PDF of the current drawing to the user in your browser (may default to your PDF viewer). Of course, execute `TikzPicture.write()` prior in order to view your latest changes. 

### `TikzPicture.add_statement(str)`
Manually add a valid string of Tikz code to the environment. This is for the off-chance that the user would rather manually type something into their tikzpicture.


# Colors
Coloring Tikz pictures in TeX tends to be annoying. A goal of this has been to make it as easy as possible to color Tikz pictures.

- One is free to use whatever colors they like, but `\usepackage[dvipnames]{xcolor}` is loaded in the TeX document which compiles the Tikz code. Additionally, 68 xcolor dvipnames are stored within a global variable `xcolors`. (Hence, they can be looped over). 

- There is also a global function `rgb(r, g, b)` which can be called to color a Tikz object by RGB values. For example, 
```python
>>> tikz = tikzpy.TikzPicture()
>>> line =  tikz.line((1,2), (4,3), options = "color=" + rgb(253, 0, 0))
>>> rectangle = tikz.rectangle( (0,0), (5,5)), options = "fill=" + rgb(120, 0, 120))
```

- A wrapper function `rainbow_colors` uses the above function to provide rainbow colors. The function takes in any integer, and grabs a rainbow color, computing a modulo operation if necessary  (hence, any integer is valid). 
```python
>>> tikz = tikzpy.TikzPicture()
>>> for i in range(0, 20):
        circle = tikz.circle((i/20, 3 - i**2/20), 3)
        circle.options = "opacity = 0.7, fill = " + rainbow_colors(i)
```


# Class: `Line`
There are two ways to initalize a line object. We've already seen this way:
```python
import tikzpy

tikz = tikzpy.TikzPicture()
line = tikz.line(start, end, options, to_options, control_pts, action) # A line is created and drawn
```
This is a "quick draw": we simultaneously create a line instance *and* draw it. 
But we can also initailize a line in its own right:
```python
from tikzpy import Line

line = Line(start, end, options, to_options, control_pts, action) # We create a line
```
We can add this line in later to see it whenever we like via `tikz.draw(line)`. 

Note: A natural question is: Why the two ways? This is because sometimes we want to obtain information from a drawing object to perform some calculations *before* we decide to actually draw it. One familiar with Tikz will realize that this is analagous to the `\path` command in Tikz, which is often very useful. 

Parameter    | Description | Default|
-------------|-------------|-------------|
`start` (tuple) | Pair of floats representing the start of the line | 
`end` (tuple) | Pair of floats representing the end of the line |
`options` (str) | String containing valid Tikz drawing options, e.g. "Blue" | `""`
`to_options` (str) | String containing Tikz specifications for connecting the start to the end (e.g. `"to [bend right = 45]"`) | "--"
`control_pts` (list) | List of control points for the line | `[]`
`action` (str) | An action to perform with plot (e.g., `\draw`, `\fill`, `\filldraw`, `\path`) | `"\draw"`

## Examples
We've already seen an example of this class. Here's another.
```python
import tikzpy

tikz = tikzpy.TikzPicture()
tikz.line((0, 0), (4, 0), options="->", control_pts=[(1, 1), (3, -1)])
```
produces the line 

<img src="https://github.com/ltrujello/Tikz-Python/blob/main/examples/example_imgs/line_ex_1.png"/> 

## Methods 
### `Line.shift(xshift, yshift)`
Shifts the current line by amount `xshift` in the x-direction and `yshift` in the y-direction. For example, we can shift in a for loop as below
```python
import tikzpy

tikz = tikzpy.TikzPicture(center=True)

line_template = tikzpy.Line((0, 0), (4, 0), control_pts=[(1, 1), (3, -1)])
for i in range(0, 10):
    line = line_template.copy() # Make a copy 
    line.shift(0, (5 - i) / 4) # Shift the copy
    line.options = f"color={rainbow_colors(i)}, o->" #Specify options
    tikz.draw(line)
```
which produces the set of lines 

<img src="https://github.com/ltrujello/Tikz-Python/blob/main/examples/example_imgs/line_ex_2.png" height = 250/>

### `Line.scale(scale)`
Scales a line by an amount `scale`, usually a python float. 

### `Line.rotate(angle, about_pt = None, radians = True)`
Rotates a line counterclockwise by angle `angle` relative to the point `about_pt`. One can specify their angle units via the boolean `radians`. If `about_pt` is not specified, the default is to rotate the line about its midpoint.

Here's an example of both `.scale` and `rotate` being used.



# Class: `PlotCoordinates`
Initialize an object of the class as below:
```python
import tikzpy

tikz = tikzpy.TikzPicture()
plot = tikz.plot_coordinates(points, options, plot_options, action)
```
which simultaneously creates and draws a `PlotCoordinates` object. Or more simply, we can create an instance as:
```python
from tikzpy import PlotCoordinates

plot = PlotCoordinates(points, options, plot_options, action)
```
which we can add to our picture later via `tikz.draw(plot)`.

Parameter    | Description | Default|
-------------|-------------|-------------|
`points` (list) | A list of tuples (x, y) representing coordinates that one wishes to create a plot for. |
`options` (str) | A string of valid Tikz drawing options. | `""`
`plot_options` (str) | A string of valid Tikz plotting options | `""`
`action` (str) | An action to perform with the line (e.g., `\draw`, `\fill`, `\filldraw`, `\path`) | `"\draw"`

This class is analagous to the Tikz command `\draw plot coordinates{...};`.

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

<img src="https://github.com/ltrujello/Tikz-Python/blob/main/examples/example_imgs/plotcoordinates_ex_1.png" height = 250/>

Alternatively we can set `action = "fill"` (analogous to `\fill` in Tikz) as in the code below
```python
import tikzpy

tikz = tikzpy.TikzPicture()
points = [(2, 2), (4, 0), (1, -3), (-2, -1), (-1, 3)]
plot = tikz.plot_coordinates(points, options="Blue", action="fill")
plot.plot_options = "smooth cycle, tension = 0.5"
```
to produce the image

<img src="https://github.com/ltrujello/Tikz-Python/blob/main/examples/example_imgs/plotcoordinates_ex_2.png" height = 250/>

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
<img src="https://github.com/ltrujello/Tikz-Python/blob/main/examples/example_imgs/plotcoordinates_ex_3.png" height = 250/>

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

<img src="https://github.com/ltrujello/Tikz-Python/blob/main/examples/example_imgs/PlotCoords_rotate_Example.png" height = 300/>


# Class: `Circle`
Initialize an object of the class as below:
```python
import tikzpy

tikz = tikzpy.TikzPicture()
circle = tikz.circle(center, radius, options, action)
```
which creates a `Circle` object and draws it. Alternatively, we can initalize more simply as 
```python
from tikzpy import Circle

circle = Circle(center, radius, options, action)
```
and later draw this via `tikz.draw(circle)`.

Parameter    | Description | Default|
-------------|-------------|-------------|
`center` (tuple) | A tuple (x, y) of floats representing the coordinates of the center of the circle. |
`radius` (float) | Length (in cm) of the radius. (By the way, all lengths are taken in cm). | 
`options` (str) | String containing valid Tikz drawing options (e.g, "Blue") | `""`
`action` (str) | An action to perform with the circle (e.g., `\draw`, `\fill`, `\filldraw`, `\path`) | `"\draw"`


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

<img src="https://github.com/ltrujello/Tikz-Python/blob/main/examples/example_imgs/circle_ex_1.png"/>

We can also use circles to create the [Hawaiian Earing](https://en.wikipedia.org/wiki/Hawaiian_earring).

```python
import tikzpy

tikz = tikzpy.TikzPicture()

radius = 5
for i in range(1, 60):
    n = radius / i
    tikz.circle((n, 0), n)
```
<img src="https://github.com/ltrujello/Tikz-Python/blob/main/examples/example_imgs/circle_ex_2.png" height = 250/>


## Methods
`Circle` has access to methods `.shift()`, `.scale()`, `.rotate()`, which behave as one would expect and takes in parameters as described before.


# Class: `Node`
Initialize an object of the class as below:
```python
import tikzpy

tikz = tikzpy.TikzPicture()
node = tikz.node(position, options, text)
```
which creates a `Node` object and draws it. We can also intiailize a 
node object directly with
```python
from tikzpy import Node

node = Node(position, options, text)
```
We can then add the node later via `tikz.draw(node)`.

Parameter    | Description | Default|
-------------|-------------|-------------|
`position` (tuple) | A tuple (x, y) of floats representing the position of the node |
`options` (str) | String containing valid Tikz node options (e.g., "Above") | `""`
`text` (str) | A string containing content, such as text or LaTeX code, to be displayed with the node | `""`

## Examples
Here we use some nodes to label a figure explaining the logarithm branch cut
```python
import tikzpy

tikz = tikzpy.TikzPicture()
# x,y axes
tikz.line((-4, 0), (4, 0), options="Gray!40, ->")
tikz.line((0, -4), (0, 4), options="Gray!40, ->")
# Cut
tikz.line((-4, 0), (0, 0), options="thick")
# Line out
tikz.line((0, 0), (1.414, 1.414), options="-o")
tikz.arc((1, 0), 0, 45, radius=1, options="dashed")

# Labels
tikz.node((3.6, -0.2), text="$x$")
tikz.node((-0.24, 3.53), text="$iy$")
tikz.node((1.3, 0.4), text="$\\theta$")
tikz.node((2.1, 1.7), text="$z = re^{i\\theta}$")
tikz.node((-2, 0.3), text="Cut")
```
which produces
<img src="https://github.com/ltrujello/Tikz-Python/blob/main/examples/example_imgs/node_ex_1.png" height = 250/>

Here's another example of usings nodes to illustrate the concept of a multivariable function.
```python
import tikzpy

row_1 = tikzpy.TikzPicture()

# Lines and rectangles
row_1.line((0, 0), (2, 0), options="->")
row_1.rectangle((2, -0.5), (4, 0.5))
row_1.line((4, 0), (6, 0), options="->")
# Labels
row_1.node((-1.2, 0), text="$(x_1, \dots, x_n)$")
row_1.node((1, 0.3), text="input")
row_1.node((3, 0), text="$f$")
row_1.node((5, 0.3), text="output")
row_1.node((7.3, 0), text="$f(x_1, \dots, x_n)$")
```

<img src="https://github.com/ltrujello/Tikz-Python/blob/main/examples/example_imgs/node_ex_2.png"/>

## Methods

`Node` has access to methods `.shift()`, `.scale()`, `.rotate()`, which behave as one would expect and takes in parameters as described before.

# Class: `Rectangle`
Initialize an object of the class as below:
```python
import tikzpy

tikz = tikzpy.TikzPicture()
rectangle = tikz.rectangle(left_corner, right_corner, options, action)
```
which creates a `Rectangle` object and draws it. We can also write
```python
from tikzpy import Rectangle

rectangle = Rectangle(left_corner, right_corner, options, action)
```
to create an instance, and later draw via `tikz.draw(Rectangle)`.

Parameter    | Description | Default|
-------------|-------------|-------------|
`left_corner`  (tuple)| A tuple (x, y) of floats representing the position of the node. | 
`right_corner` (str) | String containing valid Tikz node options (e.g., "above") | `""`
`options` (str) | A string containing valid Tikz draw optins, (e.g, "fill = Blue"). | `""` 
`action` (str) | An action to perform with the rectangle (e.g., `\draw`, `\fill`, `\filldraw`, `\path`) | `"\draw"`

## Example
Rectangles are often used as a background to many figures; in this case, 
we create a fancy colored background.

```python
import tikzpy

tikz = tikzpy.TikzPicture()

tikz.rectangle((-3.5, -2.5), (4.5, 2.5), options="rounded corners, Yellow!30",action="filldraw")
# Params
r = 2
n_nodes = 7
nodes = []
# Draw the nodes
for i in range(1, n_nodes + 1):
    angle = 2 * math.pi * i / n_nodes 
    x = r * math.cos(angle)
    y = r * math.sin(angle)
    node = tikz.node((x, y), text=f"$A_{{{i}}}$")
    nodes.append(node)

# Draw the lines between the nodes
for i in range(len(nodes)):
    start = nodes[i].position
    end = nodes[(i + 1) % len(nodes)].position
    tikz.line(start, end, options="->, shorten >= 10pt, shorten <=10pt")
```

<img src="https://github.com/ltrujello/Tikz-Python/blob/main/examples/example_imgs/rectangle_ex_1.png" height = 250/>


## Methods
`Rectangle` has access to methods `.shift()`, `.scale()`, `.rotate()`, which behave as one would expect and takes in parameters as described before.

# Class: `Ellipse`
Initialize an object of the class as below:
```python
import tikzpy

tikz = tikzpy.TikzPicture()
ellipse = tikz.ellipse(center, horiz_axis, vert_axis, options, action)
```
which creates an `Ellipse` object and draws it. We can also write
```python
from tikzpy import Ellipse

ellipse = Ellipse(center, horiz_axis, vert_axis, options, action)
```
and draw this later to the Tikz picture via `tikz.draw(ellipse)`.

Parameter    | Description | Default|
-------------|-------------|-------------|
`center` (tuple) | Pair of floats representing the center of the ellipse |
`horiz_axis` (float)| The length (in cm) of the horizontal axis of the ellipse | 
`vert_axis` (float)| The length (in cm) of the vertical axis of the ellipse |
`action` (str) | An action to perform with the ellipse (e.g., `\draw`, `\fill`, `\filldraw`, `\path`) | `"\draw"`


## Example
Here we draw and ellipse and define the major and minors axes.
```python
import tikzpy

tikz = tikzpy.TikzPicture()

# x,y axes
tikz.line((-5, 0), (5, 0), options="Gray!40, ->")
tikz.line((0, -5), (0, 5), options="Gray!40, ->")
# Ellipse
ellipse = tikz.ellipse(
    (0, 0), 4, 3, options="fill=ProcessBlue!70, opacity=0.4", action="filldraw"
)
# Labels
h_line = tikz.line((0, 0), (ellipse.horiz_axis, 0), options="thick, dashed, ->")
v_line = tikz.line((0, 0), (0, ellipse.vert_axis), options="thick, dashed, ->")
tikz.node(h_line.midpoint, options="below", text="Major")
tikz.node(v_line.midpoint, options="left", text="Minor")
```

<img src="https://github.com/ltrujello/Tikz-Python/blob/main/examples/example_imgs/ellipse_ex_1.png" height = 250/>


## Methods
`Ellipse` has access to methods `.shift()`, `.scale()`, `.rotate()`, which behave as one would expect and takes in parameters as described before.


# Class: `Arc`
Initialize an object of the class as below:

```python
import tikzpy

tikz = tikzpy.TikzPicture()
arc = tikz.arc(center, start_angle, end_angle, radius, options, radians, action)
```
which creates an `Arc` object and draws it. Again, we can 
also initalize an instance with
```python
from tikzpy import Arc

arc = Arc(center, start_angle, end_angle, radius, options, radians, action)
```
which we can draw later via `tikz.draw(arc)`.

Parameter    | Description | Default|
-------------|-------------|-------------|
`center` (tuple) | Pair of points representing the relative center of the arc |
`start_angle` (float) | The angle (in degrees) of the start of the arc |
`end_angle` (float) | The angle (in degrees) of the end of the arc |
`radius` (float) | The radius (in cm) of the arc |
`options` (str) | A string of containing valid Tikz arc options | `""`
`radians` (bool) | `True` if angles are in radians, `False` otherwise | `False`
`action` (str) | An action to perform with the arc (e.g., `\draw`, `\fill`, `\filldraw`, `\path`) | `"\draw"`

## Example
Here we draw and fill a sequence of arcs
```python
import tikzpy

tikz = tikzpy.TikzPicture()

for i in range(1, 10):
    t = 4 / i
    arc = tikz.arc((0, 0), 0, 180, radius=t, options=f"fill={rainbow_colors(i)}")
```
which generates the image

<img src="https://github.com/ltrujello/Tikz-Python/blob/main/examples/example_imgs/arc_ex_1.png"/>

## Methods 
`Arc` has access to methods `.shift()`, `.scale()`, `.rotate()`, which behave as one would expect and takes in parameters as described before.

# `Class: Scope`
Initialize a Tikz scope environment as follows:
```python
import tikzpy

tikz = tikzpy.TikzPicture()
scope = Scope(options)
```
Or more directly as 
```python
from tikzpy import Scope

scope = Scope(options)
```
As one may guess, `options` is any string of valid Tikz scoping options (i.e., options which become applied to the elements within the scoping evnironment). 

### `Scope.append(draw_obj)`
Appends any drawing object `draw_obj` to the scope environment. If one updates an attribute of a drawing object even after it has been appended, the updates are reflected in scope. 

### `Scope.remove(draw_obj)`
Removes a drawing object `draw_obj` which has been appended to the scoping environment.

### `Scope.clip(draw_obj, draw)`
Clips the drawing object `draw_obj` from the scope environment by creating an instance of the class `Clip`. Here, `draw` is a boolean regarding whether or not you want to actually draw what you are clipping. It is set to `False` by default. 

The class `Scope` also as access to methods `.shift()`, `.scale()`, `.rotate()`. In this case, such operations are applied to every single member of the scoping environment, made possible by the fact that every drawing object itself has access to these methods. These work as one would expect, which is unlike Tikz, since sometimes applying transformations to scoping environments in Tikz does not behave intuitively. 

# `Class: Clip`
A class to clip a single drawing object `draw_obj`.
One can initialize an instance of this class via an instance of `Scope`:
```python
import tikzpy

tikz = TikzPicture()
scope = tikz.scope()
clip = scope.clip(draw_obj, draw)
```
or more directly as 
```python
from tikzpy import Clip

clip = Clip(draw_obj, draw).
```
As before, `draw` is a boolean set to `False` by default. It specifies whether or not to show the drawing object which is being clipped.

The class `Clip` has access to methods `.shift()`, `.scale()`, `.rotate()`, 
although this is more for consistency (e.g., in case a `Scope` environment changes) and less for direct use of the user. 
