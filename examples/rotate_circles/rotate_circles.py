#!/bin/bash/python3
from math import pi, sin, cos
from tikzpy import TikzPicture
from tikzpy.colors import rainbow_colors

if __name__ == "__main__":
    tikz = TikzPicture(center=True)

    n = 30
    for i in range(n):
        point = (sin(2 * pi * i / n), cos(2 * pi * i / n))

        for j in range(0, 8):
            tikz.circle(point, 2 + j * 0.2, options="color=" + rainbow_colors(i + j)).shift_(
                0, -2
            )

    tikz.show()
