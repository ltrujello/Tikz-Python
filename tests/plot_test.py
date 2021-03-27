import sys

sys.path.append("/Users/luketrujillo/Desktop/github/tikz-python")
from tikz_methods import *

tikz = TikzPicture(center=True)
points = [
    (14.4, 3.2),
    (16.0, 3.6),
    (16.8, 4.8),
    (16.0, 6.8),
    (16.4, 8.8),
    (13.6, 8.8),
    (12.4, 7.6),
    (12.8, 5.6),
    (12.4, 3.6),
]

for i in range(0, 5):
    options = f"fill = {rainbow_colors(i)}, opacity = 0.7"
    plot_options = "smooth, tension=.5, closed hobby"

    # Make a plot, but don't draw it yet
    plot = PlotCoordinates(points, options, plot_options)
    center_before = plot.center
    plot.shift(i % 2, 1.5 * i)
    center_after = plot.center

    tikz.draw(plot)  # Now draw it
    tikz.line(center_before, center_after, options="->", to_options="bend left = 30")

    points = shift_coords(points, i % 2, 1.5 * i)  # Shift the points for the next loop
