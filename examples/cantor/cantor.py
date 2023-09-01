import numpy as np
from tikzpy import TikzPicture, R2_Space


def cantor(n):
    """A wrapper to perform cantor subdivision on [0, 1]."""
    return [0] + subdivide(0, 1, n) + [1]


def subdivide(x_1, x_2, n):
    """Performs the n-th cantor subdivision of the interval (x_1, x_2), a subset [0, 1]"""
    if n == 0:
        return []

    new_x_1 = 2 * (x_1 / 3) + x_2 / 3
    new_x_2 = x_1 / 3 + 2 * (x_2 / 3)
    return (
        subdivide(x_1, new_x_1, n - 1)
        + [new_x_1, new_x_2]
        + subdivide(new_x_2, x_2, n - 1)
    )


if __name__ == "__main__":
    tikz = TikzPicture()
    s = 4  # Scale

    # Set up xy-plane
    xy_plane = R2_Space(x_interval=(0, s), y_interval=(0, s))
    xy_plane.x_axis_options = "Gray!30, ->"
    xy_plane.y_axis_options = "Gray!30, ->"
    tikz.draw(xy_plane)

    # Collect (x,y) cantor data
    x = np.array(cantor(10))
    y = np.cumsum(np.ones(len(x)) / (len(x) - 2)) - 1 / (len(x) - 2)
    y[-1] = 1

    # Plot it
    points = tikz.plot_coordinates(list(zip(x, y)), options="ProcessBlue")
    points.scale(4)
    tikz.show()
