#!/bin/bash/python3
from math import pi, sin, cos
from tikzpy import TikzPicture


def roots_of_unity(n, scale=5):
    """Creates a diagram for the n-th roots of unity.
    n (int) : The number of roots of unity we display
    scale (float) : A parameter which controls the size of the image. This should be >5 for larger roots of unity.
    """
    tikz = TikzPicture(center=True)

    for i in range(n):
        theta = (2 * pi * i) / n

        # Draw line to nth root of unity
        line_to_root = tikz.line(
            (0, 0), (scale * cos(theta), scale * sin(theta)), options="-o"
        )

        if 0 <= theta <= pi:
            node_option = "above"
        else:
            node_option = "below"

        # Label the nth root of unity
        tikz.node(
            line_to_root.end,
            options=node_option,
            text=f"$e^{{ (2 \cdot \pi \cdot {i})/ {n} }}$",
        )

    tikz.write()
    tikz.show()
