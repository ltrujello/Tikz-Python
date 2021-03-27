# Tikz-Python
This an object-oriented approach via Python towards providing a giant wrapper for Tikz code, with the goal of streamling the process of creating complex figures for TeX documents.

## Why
This is for people who know basic Python and TikZ, but who have realized that while TikZ is amazing, it is *really* annoying to use. 
 

## How to Use: Basics
A typical example of this module in action is below. 
```python
import tikz_python

tikz = TikzPicture(tikz_file = "my_tikz_code.tex")
tikz.line((0,0), (1,1), options = "thick, blue")
tikz.write()
```
We explain line-by-line what this means.

* When we begin a TikZ drawing in LaTeX, we write `\begin{tikzpicture}` and `\end{tikzpicture}`. This is analagous to the code `tikz = TikzPicture(tikz_file = "my_tikz_code.tex")`. The variable `tikz` is now a tikz environment that we can append drawings to. `TikzPicture` is a class to create such tikz environments. And `tikz_file` is the file (or more generally, any file path) where our tikz code will be stored.

* The line `tikz.line((0,0), (1,1), options = "thick, blue")` draws a blue line in the tikz environment `tikz`. 
In TeX, this code would be `\draw[thick, blue] (0,0) -- (1,1);`.

* Finally, `tikz.write()` writes all of our code into the file `my_tikz_code.tex`.

## What Else?
One can do more than just draw lines. The following table lists three things: Some objects one might want to draw in TikZ, an example of TikZ code on drawing such an object, and the code for how this module would write such commands.

Object        | Raw Tikz Code   | Tikz-Python Code |
 -------------| -------------   | ------------- |
Line          | `\draw[blue] (0,0) -- (1,1);`             | `tikz.line((0,0), (1,1), options = "blue")` 
Circle        | `\draw[fill = blue] (0,0) circle (2cm);` | `tikz.circle((0,0), 2, options = "fill = blue")`  |
Rectangle     | `\draw[blue] (0,0) rectangle (5, 6);`    | `tikz.rectangle((0,0), (5,6), options = "Blue")`  |
Ellipse       | `\draw (0,0) ellipse (2cm and 4cm)`      | `tikz.ellipse((0,0), 2, 4)`
Arc           | `\draw (1,1) arc (45:90:5cm)`            | `tikz.arc((1,1), 45, 90, 5)`
Node          | `\node[above] at (0,0) {I am a node!};`  | `tikz.node((0,0), "I am a node!", "above")`
Plot Coordinates   | `\draw plot[smooth cycle] coordinates {(4.9, 9) (3.7, 8.3) (2.3, 8.5) };` | `tikz.plot_coords(options = "Red", plot_options = "smooth cycle", points = [(4.9, 9), (3.7, 8.3), (2.3, 8.5)])`|	
Scope| `\begin{scope} ... \end{scope}` | `tikz.scope()`|
Clip | `\clip[draw] (0,0) circle (5cm)`| `tikz.scope.clip(circle((0,0), 2), draw = True)`

Again: The difference with TikZ, and with other Python-Tikz mashups, is that the above python calls are class instances that we can subject to further manipulations.


### Example: Line and two nodes
Suppose I want to create a line and two labels at the ends:
```python
tikz = TikzPicture()
line = tikz.line((0,0), (1,1), options = "thick, blue, o-o")
start_node = tikz.node(line.start, options = "below", content = "Start!")
end_node = tikz.node(line.end, options = "above", content = "End!")
```
Saving the line as a variable `line` allows us to pass in `line.start` and `line.end` into the node positions, so we don't have to type out the exact coordinates. 
This is because lines, nodes, etc. are class instances with useful attributes: 
```python
>>> line.start
(0,0)
>>> line.end
(1,1)
>>> start_node.contents
"Start!"
```
Running our previous python code, we obtain
<img src="https://github.com/ltrujello/Tikz-Python/blob/main/examples/example_imgs/line_and_two_nodes.png" height = 200/> 


### Example: Circles
Pythons `for` loop is a lot less messier and much more powerful than the `\foreach` loop provided in Tikz via TeX. (For example, Tikz with TeX alone guesses your step size, and hence it cannot effectively [loop over two different sequences at the same time](https://tex.stackexchange.com/questions/171426/increments-in-foreach-loop-with-two-variables-tikz)).

In this example, we see that looping is pretty clean. 
```python
tikz = TikzPicture()

for i in range(30):
    # i/30-th point on the unit circle
    point = (math.sin(2 * math.pi * i / 30), math.cos(2 * math.pi * i / 30))
    
    # Create four circles of different radii with center located at point
    tikz.circle(point, 2, "Blue") 
    tikz.circle(point, 2.2, "Green")
    tikz.circle(point, 2.4, "Red")
    tikz.circle(point, 2.6, "Purple")

tikz.write()
```
<img src="https://github.com/ltrujello/Tikz-Python/blob/main/examples/example_imgs/circles.png" height = 250/>


### Example: Roots of Unity 
Suppose I want to talk about [roots of unity](https://en.wikipedia.org/wiki/Root_of_unity). Normally, I would have to spend 30 minutes reading some manual about how TeX handles basic math. With Python, I know I can `import math` and make intuitive computations to quickly build a function that displays the nth roots of unity.
```python
import math

tikz = TikzPicture()
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
    tikz.node((x, y), options=node_option, content=root_label)

tikz.write()
```
Which generates: 
<img src="https://github.com/ltrujello/Tikz-Python/blob/main/examples/example_imgs/roots_of_unity.png" height = 350/>



### Example: Barycentric subdivision
One can also create a function to perform the n-th barycentric subdivision of a triangle. The source [here](https://github.com/ltrujello/Tikz-Python/blob/main/examples/barycentric.py) generates the following pictures. 

<img src="https://github.com/ltrujello/Tikz-Python/blob/main/examples/example_imgs/barycentric.png" height = 250/>

### Example: Arbitrary Intersections 
Python has access to many libraries that help one efficiently build very complex functions. Such libraries are simply not possible to implement in TeX (well, not impossible, but it'd be ridiculous). 
[This code](), which uses `itertools.combinations`, takes in an arbitrary number of 2D Tikz figures and colors each and every single intersection. For example, here is what all of the intersections of nine circles in a 3 x 3 grid looks like.

<img src="https://github.com/ltrujello/Tikz-Python/blob/main/examples/example_imgs/intersection_circles.png" height = 250/>

Here's what the intersections of three random blobs looks like:

<img src="https://github.com/ltrujello/Tikz-Python/blob/main/examples/example_imgs/intersection_blobs.png" height = 250/>

As one might guess, this is useful for creating topological figures, as manually writing all of the `\scope` and `\clip` commands to create such images is pretty tedious.

# Class: `TikzPicture`
Initialize an object of the class as below:
```python
tikz = TikzPicture(tikz_file, center, options)
```
We describe the methods for this class as below. 

Parameter    | Description | Default|
-------------|-------------|-------------|
`tikz_file` (str) | The desired file path for Tikz code output. Can be a relative or full path. | `tikz_code/tikz_code.tex`|
`center` (bool) | True if you would like your tikzpicture to be centered, false otherwise. | `False`|
`options` (str) | A string containing valid Tikz options. | `""`|

If `tikz_file` is not specified, the directory `tikz/tikz_file.tex` is created automatically. Thus, it is actually less work for the user to leave this variable unspecified and let the program organize the file for you.

### `TikzPicture.write()`
This method does three things.
1. Writes the current Tikz code into the .tex file located at `my_tikz_file`.

2. Links the Tikz code to a TeX file `tex_file.tex` placed in a folder `./tex` in the same directory as `my_tikz_file`. The TeX file is then compiled.

3. Moves the compiled PDF into the same directory as `my_tikz_file` for viewing. All the silly `.aux` and `.log` files are left behind in the `/tex` folder.

The program uses `latexmk`, which comes on most installations, to compile the TeX document.

And now the key feature: You can continue editing your tikzpicture even after you've executed `.write()`. And you won't add duplicate code (i.e., code you've already written) by executing `.write()` twice. For example, I can create a circle
```python
>>> tikz = TikzPicture()
>>> circle = tikz.circle((0,0), 2, options = "Blue") # Draws a blue circle 
>>> tikz.write()
>>> tikz 
... \begin{tikzpicture}[]% TikzPython id = (1) 
	\draw[Blue] (0, 0) circle (2cm);
\end{tikzpicture}
```
and even though I called `tikz.write()`, I can still add code, and make changes to my previous drawings as well.
```python
>>> another_circle = tikz.circle((1,1), 2, options = "Red") # I want another circle...
>>> circle.center = (2,2) # I want to change my other circle's center...
>>> tikz.write() 
>>> tikz # We get what we'd expect  
... \begin{tikzpicture}[]% TikzPython id = (1) 
	\draw[Blue] (2, 2) circle (2cm);
	\draw[Red] (1, 1) circle (2cm);
\end{tikzpicture}
```
This feature, in combination with `.remove()` and `.show()` (see below), allows you to gradually build and view a tikzpicture quite painlessly.

### `TikzPicture.add_statement(str)`
Manually add a valid line of Tikz code to the environment. This is for the off-chance that the user would rather manually type something into their tikzpicture.


### `TikzPicture.remove(draw_obj)`
Removes a drawing object, such as a line, from a TikzPicture. 

Example:
```python
>>> tikz = TikzPicture()
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
Draws a drawing object, such as a line, onto the TikzPicture. This is useful because sometimes we define drawing objects outside of any reference to a TikzPicture, but we want to add it later.
Below, we create a line and two circles, and then add them later.
```python
>>> line = Line((0,0) (1,0), to_options = "to[bend right = 30]")
>>> end_c = Circle(line.start, radius = 0.2)
>>> start_c = Circle(line.end, radius = 0.2)
>>> tikz.draw(line, end_c, start_c) # The line is now drawn
```


### `TikzPicture.show()`
Pulls up a PDF of the current drawing to the user in your browser (may default to your PDF viewer). Of course, execute `TikzPicture.write()` prior in order to view your latest changes. 

# Colors
Coloring Tikz pictures in TeX tends to be annoying. A goal of this has been to make it as easy as possible to color Tikz pictures.

- One is free to use whatever colors they like, but `\usepackage[dvipnames]{xcolor}` is loaded in the TeX document which compiles the Tikz code. Additionally, 68 xcolor dvipnames are stored within a global variable `xcolors`. (Hence, they can be looped over). 

- There is also a global function `rgb(r, g, b)` which can be called to color a Tikz object by RGB values. For example, 
```python
>>> tikz = TikzPicture()
>>> line =  tikz.line((1,2), (4,3), options = "color=" + rgb(253, 0, 0))
>>> rectangle = tikz.rectangle( (0,0), (5,5)), options = "fill=" + rgb(120, 0, 120))
```

- A wrapper function `rainbow_colors` uses the above function to provide rainbow colors. The function takes in any integer, and grabs a rainbow color, computing a modulo operation if necessary  (hence, any integer is valid). 
```python
>>> tikz = TikzPicture()
>>> for i in range(0, 20):
        circle = tikz.circle((i/20, 3 - i**2/20), 3)
        circle.options = "opacity = 0.7, fill = " + rainbow_colors(i)
```


# Class: `Line`
There are two ways to initalize a line object. We've already seen this way:
```python
tikz = TikzPicture()
line = tikz.line(start, end, options, to_options, control_pts, action) # A line is created and drawn
```
This is a "quick draw": we simultaneously create a line instance *and* draw it. 
But we can also initailize a line in its own right:
```python
line = Line(start, end, options, to_options, control_pts, action) # We create a line
```
We can add this line in later to see it whenever we like via `tikz.draw(line)`. 

Note: A natural question is: Why the two ways? This is because sometimes we want to obtain information from a drawing object to perform some calculations *before* we decide to actually draw it. One familiar with Tikz will realize that this is analagous to the `\path` command in Tikz, which is often very useful. 

We explain the parameters for our class `Line`. 

Parameter    | Description | Default|
-------------|-------------|-------------|
`start` (tuple) | Pair of floats representing the start of the line | 
`end` (tuple) | Pair of floats representing the end of the line |
`options` (str) | String containing valid Tikz drawing options, e.g. "Blue" | `""`
`to_options` (str) | String containing Tikz specifications for connecting the start to the end (e.g. `"to [bend right = 45]"`) | "--"
`control_pts` (list) | List of control points for the line | `[]`
`action` (str) | An action to perform with plot (e.g., `\draw`, `\fill`, `\filldraw`, `\path`) | `"\draw"`

We can also call some useful methods on instances of this class.

### `Line.shift(xshift, yshift)`
Shifts the current line by amount `xshift` in the x-direction and `yshift` in the y-direction.
```python
>>> line = tikz.line((0,0), (1,1), options = "Blue", control_pts = [(0.5, 0.5), (0.75, -2)])
>>> line 
... \draw[Blue] (0, 0) .. controls (0.5, 0.5) and (0.75, -2)  .. (1, 1);
>>> line.shift(2, 2) # Shift!
>>> line
... \draw[Blue] (2, 2) .. controls (2.5, 2.5) and (2.75, 0)  .. (3, 3);
```

### `Line.scale(scale)`
Scales a line by an amount `scale`, usually a python float. 

### `Line.rotate(angle, about_pt = None, radians = True)`
Rotates a line counterclockwise by angle `angle` relative to the point `about_pt`. One can specify their angle units via the boolean `radians`. If `about_pt` is not specified, the default is to rotate the line about its midpoint.


# Class: `PlotCoordinates`
Initialize an object of the class as below:
```python
tikz = TikzPicture()
plot = tikz.plot_coords(points, options, plot_options, action)
```
which simultaneously creates and draws a `PlotCoordinates` object. Or more simply, we can create an instance as:
```python
plot = PlotCoordinates(points, options, plot_options, action)
```
which we can add to our picture later via `tikz.draw(plot)`.
We explain the parameters.

Parameter    | Description | Default|
-------------|-------------|-------------|
`points` (list) | A list of tuples (x, y) representing coordinates that one wishes to create a plot for. |
`options` (str) | A string of valid Tikz drawing options. | `""`
`plot_options` (str) | A string of valid Tikz plotting options | `""`
`action` (str) | An action to perform with the line (e.g., `\draw`, `\fill`, `\filldraw`, `\path`) | `"\draw"`

This method is analagous to the Tikz command `\draw plot coordinates{...};`. For example, the code
```python
>>> tikz = TikzPicture()
>>> points = [(2,2), (4,0), (1,-3), (-2, -1), (-1, 3)]
>>> plot = tikz.plot_coords(points, options = "Blue", plot_options = "smooth cycle, tension = 0.5")
```
corresponds to the Tikz command `\draw[Blue] plot[smooth cycle, tension = 0.5] coordinates{(2,2), (4,0), (1,-3) (-2, -1), (-1, 3)};`.

`PlotCoordinates` has methods `.shift()`, `.scale`, and `.rotate`, similar to the class `Line`, and the parameters behave similarly. These methods are more interestingly used on `PlotCoordinates` than on `Line`. For example, the code
```python
tikz = TikzPicture()
tikz = TikzPicture()
points = [(14.4, 3.2), (16.0, 3.6), (16.8, 4.8), (16.0, 6.8), (16.4, 8.8), (13.6, 8.8), (12.4, 7.6), (12.8, 5.6), (12.4, 3.6)]

for i in range(0, 20):
    options = f"fill = {rainbow_colors(i)}, opacity = 0.7"
    # Requires \usetikzlibrary{hobby} here
    plot_options = "smooth, tension=.5, closed hobby"
    plot = tikz.plot_coords(points, options, plot_options)
    plot.scale((20 - i) / 20) # Shrink it 
    plot.rotate(15 * i) # Rotate it
```
generates the image

<img src="https://github.com/ltrujello/Tikz-Python/blob/main/examples/example_imgs/PlotCoords_rotate_Example.png" height = 300/>


# Class: `Circle`
Initialize an object of the class as below:
```python
tikz = TikzPicture()
circle = tikz.circle(center, radius, options, action)
```
which creates a `Circle` object and draws it. Alternatively, we can initalize more simply as 
```python
circle = Circle(center, radius, options, action)
```
and later draw this via `tikz.draw(circle)`.

We explain the parameters. 

Parameter    | Description | Default|
-------------|-------------|-------------|
`center` (tuple) | A tuple (x, y) of floats representing the coordinates of the center of the circle. |
`radius` (float) | Length (in cm) of the radius. (By the way, all lengths are taken in cm). | 
`options` (str) | String containing valid Tikz drawing options (e.g, "Blue") | `""`
`action` (str) | An action to perform with the circle (e.g., `\draw`, `\fill`, `\filldraw`, `\path`) | `"\draw"`

`Circle` has access to methods `.shift()`, `.scale()`, `.rotate()`, which behave as one would expect and take in parameters as described before.


# Class: `Node`
Initialize an object of the class as below:
```python
tikz = TikzPicture()
node = tikz.node(position, options, content)
```
which creates a `Node` object and draws it. We can also intiailize a 
node object directly with
```python
node = Node(position, options, content)
```
We can then add the node later via `tikz.draw(node)`.

Parameter    | Description | Default|
-------------|-------------|-------------|
`position` (tuple) | A tuple (x, y) of floats representing the position of the node |
`options` (str) | String containing valid Tikz node options (e.g., "Above") | `""`
`content` (str) | A string containing content, such as text or LaTeX code, to be displayed with the node | `""`

`Node` has access to methods `.shift()`, `.scale()`, `.rotate()`, which behave as one would expect and take in parameters as described before.

# Class: `Rectangle`
Initialize an object of the class as below:
```python
tikz = TikzPicture()
rectangle = tikz.rectangle(left_corner, right_corner, options, action)
```
which creates a `Rectangle` object and draws it. We can also write
```python
rectangle = Rectangle(left_corner, right_corner, options, action)
```
to create an instance, and later draw via `tikz.draw(Rectangle)`.

Parameter    | Description | Default|
-------------|-------------|-------------|
`left_corner`  (tuple)| A tuple (x, y) of floats representing the position of the node. | 
`right_corner` (str) | String containing valid Tikz node options (e.g., "above") | `""`
`options` (str) | A string containing valid Tikz draw optins, (e.g, "fill = Blue"). | `""` 
`action` (str) | An action to perform with the rectangle (e.g., `\draw`, `\fill`, `\filldraw`, `\path`) | `"\draw"`


`Rectangle` has access to methods `.shift()`, `.scale()`, `.rotate()`, which behave as one would expect and take in parameters as described before.

# Class: `Ellipse`
Initialize an object of the class as below:
```python
tikz = TikzPicture()
ellipse = tikz.ellipse(center, horiz_axis, vert_axis, action)
```
which creates an `Ellipse` object and draws it. We can also write
```python
ellipse = Ellipse(center, horiz_axis, vert_aixs, action)
```
and draw this later to the Tikz picture via `tikz.draw(ellipse)`.

Parameter    | Description | Default|
-------------|-------------|-------------|
`center` (tuple) | Pair of floats representing the center of the ellipse |
`horiz_axis` (float)| The length (in cm) of the horizontal axis of the ellipse | 
`vert_axis` (float)| The length (in cm) of the vertical axis of the ellipse |
`action` (str) | An action to perform with the ellipse (e.g., `\draw`, `\fill`, `\filldraw`, `\path`) | `"\draw"`


`Ellipse` has access to methods `.shift()`, `.scale()`, `.rotate()`, which behave as one would expect and take in parameters as described before.


# Class: `Arc`
Initialize an object of the class as below:

```python
tikz = TikzPicture()
arc = tikz.arc(start, end, options, control_pts, action)
```
which creates an `Arc` object and draws it. Again, we can 
also initalize an instance with
```python
arc = Arc(start, end, options, control_pts, action)
```
which we can draw later via `tikz.draw(arc)`.

Parameter    | Description | Default|
-------------|-------------|-------------|
`center` (tuple) | Pair of points representing the relative center of the arc |
`start_angle` (float) | The angle (in degrees) of the start of the arc |
`end_angle` (float) | The angle (in degrees) of the end of the arc |
`radius` (float) | The radius (in cm) of the arc |
`action` (str) | An action to perform with the arc (e.g., `\draw`, `\fill`, `\filldraw`, `\path`) | `"\draw"`


`Arc` has access to methods `.shift()`, `.scale()`, `.rotate()`, which behave as one would expect and take in parameters as described before.

# `Class: Scope`
Initialize a Tikz scope environment as follows:
```python
tikz = TikzPicture()
scope = Scope(options)
```
Or more directly as 
```python
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
tikz = TikzPicture()
scope = tikz.scope()
clip = scope.clip(draw_obj, draw)
```
or more directly as 
```python
clip = Clip(draw_obj, draw).
```
As before, `draw` is a boolean set to `False` by default.

The class `Clip` has access to methods `.shift()`, `.scale()`, `.rotate()`, 
although this is more for consistency (e.g., in case a `Scope` environment changes) and less for direct use of the user. 
