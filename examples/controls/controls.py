#!/bin/bash/python3
from tikzpy import TikzPicture
from tikzpy.colors import rainbow_colors

""" Draws a series of rainbow lines in a manner such that their control points are shifted.
"""

tikz = TikzPicture()
for i in range(0, 15):
    line = tikz.line((i, 0), (0, 5))
    line.options = f"color={rainbow_colors(i)}"
    line.control_pts = [(i - 2, -1), (i + 2, -2)]

tikz.write()
tikz.show()
