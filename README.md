# Tikz-Python
An object-oriented Python approach towards providing a giant wrapper for Tikz code, with the goal of streamlining the process of creating complex figures for TeX documents.

To install it, run 
```
pip install tikz-python
```

## Documentation

We have documentation now! Please visit the [documentation](https://ltrujello.github.io/Tikz-Python) site.

## Examples
Want to see some nice examples of what this package can do? See [here](https://ltrujello.github.io/Tikz-Python/examples/).

## How to Use: Basics
An example of this package in action is below. 
```python
from tikzpy import TikzPicture  # Import the class TikzPicture

tikz = TikzPicture()
tikz.circle((0, 0), 3, options="thin, fill=orange!15")

arc_one = tikz.arc((3, 0), 0, 180, x_radius=3, y_radius=1.5, options="dashed")
arc_two = tikz.arc((-3, 0), 180, 360, x_radius=3, y_radius=1.5)

tikz.show()  # Displays a pdf of the drawing to the user
```
which produces
<img src="https://github.com/ltrujello/Tikz-Python/blob/main/docs/png/basic.png?raw=true"/> 

We explain line-by-line the above code.

* `from tikzpy import TikzPicture` imports the `TikzPicture` class from the `tikzpy` package. 

* The second line of code is analogous to the TeX code `\begin{tikzpicture}` and `\end{tikzpicture}`. The variable `tikz` is now a tikz environment, specifically an instance of the class `TikzPicture`, and we can now append drawings to it.

* The third, fourth, and fifth lines draw a filled circle and two elliptic arcs, which give the illusion of a sphere.

* In the last line, the call `show()` immediately displays the PDF of the drawing to the user.

