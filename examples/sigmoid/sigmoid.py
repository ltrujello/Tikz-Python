import numpy as np
from tikzpy import TikzPicture, R2_Space
import math

vert_scale = 4.5
horiz_scale = 1.5

def sigmoid(val):
    val = horiz_scale * val
    return 1/(1 + math.pow(math.e, -val))


if __name__ == "__main__":
    tikz = TikzPicture()
    xrange = (-3, 3)

    # Set up xy-plane
    xy_plane = R2_Space(x_interval=(-4, 4), y_interval=(0, vert_scale + .5))
    xy_plane.x_axis_options = "Gray!30, ->"
    xy_plane.y_axis_options = "Gray!30, ->"
    tikz.draw(xy_plane)

    # Collect (x,y) data
    x = horiz_scale * np.linspace(xrange[0], xrange[1], 200)
    y = [vert_scale*sigmoid(val) for val in x]

    line = tikz.line((-3.5, 4.5), (4.5, 4.5), options="dashed")
    tikz.node(line.start, options="left", text="$y=1$")
    # Plot it
    points = tikz.plot_coordinates(list(zip(x, y)), options="ProcessBlue")
    tikz.show()
