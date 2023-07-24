#!/bin/bash/python3
from tikzpy import TikzPicture
from tikzpy.styles import arrows_along_path_style

""" Illustrates a use case of Cauchy's Residue Theorem. In this case 
    we have two singularities that occur within the semicircle.
"""

if __name__ == "__main__":
    tikz = TikzPicture()

    points = [
        (-3, -0.5),
        (-1, -1.5),
        (2, -1.5),
        (4, -1.5),
        (5, 0),
        (3, 2.4),
        (-1, 2.6),
        (-3, 2),
    ]

    tikz.add_styles(*arrows_along_path_style)
    tikz.options = "thick"

    # Draws the main boundary
    plot = tikz.plot_coordinates(
        options="arrows_along_path=red",
        plot_options="smooth, tension=.5, closed hobby",
        points=points,
        action="draw",
    )

    # Draws the inner circles
    singularity_1 = tikz.circle((3, -0.3), 0.7, "arrows_along_path=blue")
    singularity_2 = tikz.circle((1.3, 1.3), 0.7, "arrows_along_path=blue")
    singularity_3 = tikz.circle((-0.4, -0.2), 0.7, "arrows_along_path=blue")
    singularity_4 = tikz.circle((-2, 1.1), 0.7, "arrows_along_path=blue")

    # Draws the paths that connect the circles
    tikz.line((3.7, -0.5), (4.6, -1), options="bend left, <-")
    tikz.line((1.4, 0.6), (2.3, -0.3), options="bend right, <-")
    tikz.line((-0.25, 0.5), (0.6, 1.4), options="bend left, <-")
    tikz.line((-1.29, 1.1), (-0.6, 0.46), options="bend left, <-")
    tikz.line((-2.5, 1.6), (-2.8, 2.15), options="bend left, ->")

    # Draws and labels the points a_1, a_2, a_3, and a_4.
    for ind, singularity in enumerate(
        [singularity_1, singularity_2, singularity_3, singularity_4]
    ):
        tikz.circle(singularity.center, 0.05, action="fill")
        tikz.node(singularity.center, options="right", text=f"$a_{ind+1}$")

    tikz.write()
    tikz.show()
