#!/bin/bash/python3
from math import exp
from tikzpy import TikzPicture
from tikzpy.colors import rainbow_colors

tikz = TikzPicture()
# points = [(14.4, 3.2), (16.0, 3.6), (16.8, 4.8), (16.0, 6.8), (16.4, 8.8), (13.6, 8.8), (12.4, 7.6), (12.8, 5.6), (12.4, 3.6)]
# points = [(6.6,11.4), (5.3,8.8), (3.6,9.9), (2.8,7.9), (3.7,6.1), (4.5,4), (6.2,4.2), (6.7,5.5), (8.5,4.3), (9.5,6.7), (8.8,8.5), (9.4,11.1), (7.7,11)]
points = [
    (5.6, 11.1),
    (5.2, 9.6),
    (3.2, 10.6),
    (4.3, 7.3),
    (3, 4.1),
    (5.6, 5.2),
    (7.2, 3.9),
    (8.4, 5.6),
    (10.2, 4.5),
    (8.7, 6.9),
    (10, 8.6),
    (8.1, 8.8),
    (9.3, 11.8),
    (7.2, 11.1),
    (6.2, 12.5),
]

for theta in range(0, 540, 5):
    # Plot the points
    plot = tikz.plot_coordinates(
        options=f"fill = {rainbow_colors(theta)}",
        plot_options="smooth, tension=.5, closed hobby",
        points=points,
    )
    # Rotate them
    plot.rotate(theta, about_pt=(0, 0))
    # Scale them
    plot.scale(exp(-1.5 * theta / 180))

tikz.write()
tikz.show()
