#!/bin/bash/python3
import numpy as np
from tikzpy import TikzPicture, PlotCoordinates

if __name__ == "__main__":
    tikz = TikzPicture(center=True)
    tikz.set_tdplotsetmaincoords(75, 120)

    HEIGHT = 3.75  # Height of the surace (from the floor)
    O = (1, 2, HEIGHT / 2)  # The origin

    # Draw the rectangle
    floor = tikz.plot_coordinates([(0, 0, 0), (5, 0, 0), (5, 5, 0), (0, 5, 0), (0, 0, 0)])
    floor.options = "shade, left color = NavyBlue!30, right color = NavyBlue, opacity = 0.3"

    # Initialize the top and bottom curves. Note the points are empty. We'll add to them.
    top_curve = PlotCoordinates([], options="line width = 0.07mm")
    bottom_curve = PlotCoordinates([], options="line width = 0.2mm")

    for t in np.linspace(0, 1, 100):
        # Compute points on the top and bottom curves. I guessed this formula in trying to mimic Hartshorne's image.
        top_pt = (1.5 + np.sin(10 * t), 3 * t + 0.5, HEIGHT)
        bottom_pt = (1.5 + np.sin(10 * t), 3 * t + 0.5, 0)

        # Lines from the origin to the current points on the curves
        line_1 = tikz.line(O, top_pt, "gray, opacity = 0.75, line width = 0.05mm")
        line_2 = tikz.line(O, bottom_pt, "gray, opacity = 0.75, line width = 0.05mm")

        # Collect points to later draw the top and bottom curves
        top_curve.points.append(top_pt)
        bottom_curve.points.append(bottom_pt)

    # We now draw the top and bottom curves
    tikz.draw(top_curve, bottom_curve)

    # Annotate the origin (O), rectangle (P^2), cone (C(Y)), variety (Y), and ambient space (A^3)
    tikz.circle(O, radius=0.03, action="fill")
    tikz.node(O, options="left", text="$O$")
    tikz.node((3, 3, 0), text="$Y$")
    tikz.node((1, 4.5, 0), text="$\mathbf{P}^2$")
    tikz.node((0, 2.5, 1), text="$C(Y)$")
    tikz.node((0, 4.2, 3.5), text="$\mathbf{A}^3$")

    tikz.show()
