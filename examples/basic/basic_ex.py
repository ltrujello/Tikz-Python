#!/bin/bash/python3
from tikzpy import TikzPicture  # Import the class TikzPicture

""" Draws a circle and two ellipses to create the illusion of sphere.
"""

tikz = TikzPicture()
tikz.circle((0, 0), 3, options="thin, fill=orange!15")

arc_one = tikz.arc((3, 0), 0, 180, x_radius=3, y_radius=1.5, options=f"dashed")
arc_two = tikz.arc((-3, 0), 180, 360, x_radius=3, y_radius=1.5)

tikz.write()  # Writes the Tikz code into a file
tikz.show(quiet=True)  # Displays a pdf of the drawing to the user
