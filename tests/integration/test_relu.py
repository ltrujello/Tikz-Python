import numpy as np
from tikzpy import TikzPicture, Point, R2_Space
import math

code = r"""\begin{tikzpicture}
    \begin{scope}
	\draw[Gray!30, ->] (-4, 0) to (4, 0);
	\draw[Gray!30, ->] (0, 0) to (0, 5.0);
	\node[below] at (4, 0) { $x$ };
	\node[left] at (0, 5.0) { $y$ };
\end{scope}

    \draw[dashed] (-3.5, 4.5) to (4.5, 4.5);
    \node[left] at (-3.5, 4.5) { $y=1$ };
    \draw[ProcessBlue, <-] (-4, 0) to (0, 0);
    \draw[ProcessBlue, ->] (0, 0) to (4.5, 4.5);
\end{tikzpicture}
"""


def test_relu_example():
    tikz = TikzPicture()
    xrange = (-3, 3)
    vert_scale = 4.5
    horiz_scale = 1.5

    # Set up xy-plane
    xy_plane = R2_Space(x_interval=(-4, 4), y_interval=(0, vert_scale + 0.5))
    xy_plane.x_axis_options = "Gray!30, ->"
    xy_plane.y_axis_options = "Gray!30, ->"
    tikz.draw(xy_plane)

    line = tikz.line((-3.5, 4.5), (4.5, 4.5), options="dashed")
    tikz.node(line.start, options="left", text="$y=1$")
    # Plot it
    tikz.line((-4, 0), (0, 0), options="ProcessBlue, <-")
    tikz.line((0, 0), (4.5, 4.5), options="ProcessBlue, ->")
    assert str(tikz) == code
