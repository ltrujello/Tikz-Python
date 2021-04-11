#!/bin/bash/python3
from tikzpy import TikzPicture
from tikzpy.colors import rainbow_colors
import numpy as np

tikz = TikzPicture()
tikz.circle((0, 0), 3, options="thick, gray!10", action="filldraw")

x_r = 3
y_r = 1.5

for t in np.linspace(0, 2 * np.pi, 200):
    x_pos = 3 * np.cos(t)
    y_pos = 3 * np.sin(t)

    arc_one = tikz.arc(
        (x_pos, y_pos),
        0,
        180,
        x_radius=x_r,
        y_radius=y_r,
        options=f"color={rainbow_colors(int(t*180/np.pi))}",
    )
    arc_two = tikz.arc(
        (x_pos - 2 * x_r, y_pos),
        180,
        360,
        x_radius=x_r,
        y_radius=y_r,
        options=f"color={rainbow_colors(int(t*180/np.pi))}",
    )

tikz.write()
tikz.show()
