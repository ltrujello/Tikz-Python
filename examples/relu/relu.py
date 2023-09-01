import numpy as np
from tikzpy import TikzPicture, Point, R2_Space
import math


if __name__ == "__main__":
    tikz = TikzPicture()
    xrange = (-3, 3)
    vert_scale = 4.5
    horiz_scale = 1.5

    # Set up xy-plane
    xy_plane = R2_Space(x_interval=(-4, 4), y_interval=(0, vert_scale + .5))
    xy_plane.x_axis_options = "Gray!30, ->"
    xy_plane.y_axis_options = "Gray!30, ->"
    tikz.draw(xy_plane)

    line = tikz.line((-3.5, 4.5), (4.5, 4.5), options="dashed")
    tikz.node(line.start, options="left", text="$y=1$")
    # Plot it
    tikz.line((-4, 0), (0, 0), options="ProcessBlue, <-")
    tikz.line((0, 0), (4.5, 4.5), options="ProcessBlue, ->")

    tikz.show()
