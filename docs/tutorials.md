# Tutorials

This package is meant to have an extremely simple API that also resembles the creation of TikZ code very closely.
That is, we aim to minimize "surprises" such that users experienced with TikZ can easily use this package.
Towards that goal we offer step-by-step tutorials demonstrating this package.

## Logarithmic Branch Cut

Suppose we desire to create this diagram from mathematics, which illustrates the logarithmic branch cut.

<img src="../png/node_ex_1.png"/>


### Axes

The first thing we can do is create the x and y axes. To do this, we can create two 
`Line` objects for the x and y axes, and two `Node` objects to draw the labels for these axes.  

```python
from tikzpy import TikzPicture

tikz = TikzPicture()
axes_len = 4
# x,y axes
origin = (0, 0)
x_axis = tikz.line((-axes_len, 0), (axes_len, 0), options="Gray!40, ->")
y_axis = tikz.line((0, -axes_len), (0, axes_len), options="Gray!40, ->")
# axes labels
tikz.node(x_axis.end - (0.3, 0.3), text="$x$")
tikz.node(y_axis.end - (0.3, 0.3), text="$iy$")
tikz.show()
```

Note that this code is modular; the `Node` objects are dependent on the `Line.end` attributes, and the `Line` objects are dependent
on the `axes_len` value. This lets us experiment with various `axes_len` values, if we'd like.

This code generates the graphic below. 

<img src="../png/tutorial_imgs/log_cut_step_1.png"/>

### Cut branch

Next, let's add the "Cut" branch. We achieve this with one `Line` object and one `Node` object to put in the word "Cut".

```python
# Cut branch
cut_line = tikz.line((-axes_len, 0), origin, options="thick")
tikz.node(cut_line.midpoint(), text="Cut", options="above")
```

Again, this is modular. The cut `Line` is dependent on `axes_len` value. The `Node` object is positioned via 
`Line.midpoint()` method, which calculates the middle of the line. Thus, if we change the length of our line, we do not 
have to also change node's position. This saves us time. 

This so far generates 

<img src="../png/tutorial_imgs/log_cut_step_2.png"/>

### Line from origin

Next, let's add the line from the origin and annotate it. Again, we achieve this with a `Line` and a `Node` object. 

```python
# Line from origin
line = tikz.line(origin, (axes_len / 3, axes_len / 3), options="-o")
tikz.node(line.end + (0.7, 0), text="$z = re^{i\\theta}$", options="above")
```

In the code above, we draw 45-degree angled line from the origin to the point `(axes_len / 3, axes_len / 3)`. 
The denominator `3` is pretty arbitrary and subjective, and can be changed if the user likes. 
For our node, we use the `Line.end` attribute to specify the position and shift it to the right a bit by 0.7.
We then shift it up by specifying `options=above`, as one normally would in TikZ.

This then generates 

<img src="../png/tutorial_imgs/log_cut_step_3.png"/>

### Angle arc

Finally, we draw the dashed-angle. To achieve this we can use an `Arc` object and one `Node` object. 

```python
# Angle arc
from tikzpy import Point

arc_start = Point(1, 0)
tikz.arc(arc_start, 0, 45, radius=1, options="dashed")
tikz.node(arc_start + (0.3, 0.5), text="$\\theta$")
```

In the code above, we draw an arc starting at the point `arc_start` from angle 0 to 45. We define this point using 
the `Point` class instead of just a Python tuple. This is useful for when we create the node object, since we 
can specify the position of the node as `arc_start + (0.3, 0.5)`. 

All together, this generates the original image. The complete code is given below. 

```python
from tikzpy import TikzPicture, Point

tikz = TikzPicture(center=True)
axes_len = 4

# x,y axes
origin = (0, 0)
x_axis = tikz.line((-axes_len, 0), (axes_len, 0), options="Gray!40, ->")
y_axis = tikz.line((0, -axes_len), (0, axes_len), options="Gray!40, ->")
# axes labels
tikz.node(x_axis.end - (0.3, 0.3), text="$x$")
tikz.node(y_axis.end - (0.3, 0.3), text="$iy$")

# Cut branch
cut_line = tikz.line((-axes_len, 0), origin, options="thick")
tikz.node(cut_line.midpoint(), text="Cut", options="above")

# Line from origin
line = tikz.line(origin, (axes_len / 3, axes_len / 3), options="-o")
tikz.node(line.end + (0.7, 0), text="$z = re^{i\\theta}$", options="above")

# Angle arc
arc_start = Point(1, 0)
tikz.arc(arc_start, 0, 45, radius=1, options="dashed")
tikz.node(arc_start + (0.3, 0.5), text="$\\theta$")

tikz.show()
```


