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
    draw_options = f"fill = {rainbow_colors(i)}, opacity = 0.7"
    plot_options = "smooth, tension=.5, closed hobby"
    plot = tikz.plot_coords(points, draw_options, plot_options)

    shifted_points = shift_coords(points, 0, i * 1.2)
    for i in range(len(points)):
        # tikz.circle(plot.points[i], 0.1, options="fill = Red")
        tikz.line(plot.points[i], shifted_points[i])

    # plot.shift(0, i)
