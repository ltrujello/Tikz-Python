#!/bin/bash/python3
import numpy as np
from tikzpy import TikzPicture

tikz = TikzPicture(center=True)

for i in np.linspace(0, 1, 30):
    point = (np.sin(2 * np.pi * i), np.cos(2 * np.pi * i))

    # Create four circles of different radii with center located at point
    tikz.circle(point, 2, "ProcessBlue")
    tikz.circle(point, 2.2, "ForestGreen")
    tikz.circle(point, 2.4, "red")  # xcolor Red is very ugly
    tikz.circle(point, 2.6, "Purple")

tikz.write()
tikz.show()