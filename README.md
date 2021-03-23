
This is TikZ-Python, a python module that allows one to very simply and intuitively create complex figures in TikZ. 

## Why
This is for people who know basic Python and TikZ, but who have realized that while TikZ is amazing, it is *really* annoying to use. 

The goal of this is to automate most of the process of making TikZ figures so that it is no longer a tedious and inefficient task. This has led the philosophy of this code is to interpret tikz attributes as *class objects*. For example, we interpret a line as not only a drawing, but as an instance of a class `Line`. This allows us to easily draw and further subject a drawing to complex manipulations (e.g., rotations, shifting) which would require lots of copy-pasting, typing, backspacing, and debbuging in LaTeX alone. 

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

## Methods Provided
One can do more than just draw lines. The following table lists three things: Some objects one might want to draw in TikZ, an example of TikZ code on drawing such an object, and the code for how this module would write such commands.

Object        | Raw Tikz Code   | Tikz-Python Code |
 -------------| -------------   | ------------- |
Line         | `\draw[blue] (0,0) -- (1,1);`             | `tikz.line((0,0), (1,1), options = "blue")` 
Circle        | `\draw[fill = blue] (0,0) circle (2cm);` | `tikz.circle((0,0), 2, options = "fill = blue")`  |
Rectangle     | `\draw[blue] (0,0) rectangle (5, 6);`    | `tikz.rectangle((0,0), (5,6), options = "Blue")`  |
Ellipse       | `\draw (0,0) ellipse (2cm and 4cm)`      | `tikz.ellipse((0,0), 2, 4)`
Arc           | `\draw (1,1) arc (45:90:5cm)`            | `tikz.arc((1,1), 45, 90, 5)`
Node          | `\node[above] at (0,0) {I am a node!};`  | `tikz.node((0,0), "I am a node!", "above")`
Plot Coordinates   | `\draw plot[smooth cycle] coordinates {(4.9, 9) (3.7, 8.3) (2.3, 8.5) };` | `tikz.draw_plot_coords(draw_options = "Red", plot_options = "smooth cycle", points = [(4.9, 9), (3.7, 8.3), (2.3, 8.5)])`	

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
Python's flexibility can also allow us to easily create more complicated figures which would require way too much time and effort to do in TeX alone. The following example code generates the figure below.
```python
tikz = TikzPicture(new_file=True)

for i in range(30):
    point = (math.sin(2 * math.pi * i / 30), math.cos(2 * math.pi * i / 30))

    tikz.circle(point, 2, "Blue") 
    tikz.circle(point, 2.2, "Green")
    tikz.circle(point, 2.4, "Red")
    tikz.circle(point, 2.6, "Purple")

tikz.write()
```
<img src="https://github.com/ltrujello/Tikz-Python/blob/main/examples/example_imgs/circles.png" height = 250/>


### Example: Roots of Unity 
Suppose I want to talk about [roots of unity](https://en.wikipedia.org/wiki/Root_of_unity). The corresponding code would be
```python
tikz = TikzPicture()

n = 13
for i in range(n):
    theta = (2 * math.pi * i) / n
    x, y = scale * math.cos(theta), scale * math.sin(theta)
    root_label = f"$e^{{ (2 \cdot \pi \cdot {i})/ {n} }}$"

    # Draw line to nth root of unity
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
<img src="https://github.com/ltrujello/Tikz-Python/blob/main/examples/example_imgs/roots_of_unity.png" height = 300/>



### Barycentric subdivision
One can also create a function to perform the n-th barycentric subdivision of a triangle. The source [here](https://github.com/ltrujello/Tikz-Python/blob/main/examples/barycentric.py) generates the following pictures. 

<img src="https://github.com/ltrujello/Tikz-Python/blob/main/examples/example_imgs/barycentric.png" height = 250/>











