#!/bin/bash/python3
from math import pi, cos, sin, tan, atan
import numpy as np
from tikzpy import TikzPicture

""" Plots the blowup at a point.
"""

tikz = TikzPicture(center=True)
tikz.set_tdplotsetmaincoords(65, 25)
tikz.options = "tdplot_main_coords"

# The blowup
def blowup(r, t):
    theta = 2 * atan(t * 2 / pi)
    return r * cos(theta), r * sin(theta), 6 * atan(tan(theta) / 6)


# Parameters for surface
vmin = -pi / 2 + 0.1
vmax = pi / 2 - 0.1
umin = -5
umax = 5

# Draws the gray vertical line
for j in np.linspace(umin, umax, 40):
    points = []
    for i in np.linspace(vmin, vmax, 50):
        points.append(blowup(j, i))
    tikz.plot_coordinates(points, options="gray!10, thin", plot_options="smooth")

# Draws the main blue vertical lines for visual aid
for j in np.linspace(umin, umax, 10):
    points = []
    for i in np.linspace(vmin, vmax, 50):
        points.append(blowup(j, i))
    tikz.plot_coordinates(points, options="ProcessBlue!70", plot_options="smooth")

# Draws the horizontal lines
for i in np.linspace(vmin, vmax, 50):
    new_points = []
    for j in np.linspace(umin, umax, 10):
        new_points.append(blowup(j, i))
    tikz.plot_coordinates(new_points, options="ProcessBlue!70", plot_options="smooth")

tikz.write()
tikz.show()
