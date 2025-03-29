from tikzpy import TikzPicture, R2_Space


if __name__ == "__main__":
    tikz = TikzPicture()
    axes_len = 4
    vert_scale = 4.5

    # Set up xy-plane
    xy_plane = R2_Space(x_interval=(-axes_len, axes_len), y_interval=(0, vert_scale + .5))
    xy_plane.x_axis_options = "Gray!30, ->"
    xy_plane.y_axis_options = "Gray!30, ->"
    tikz.draw(xy_plane)

    line = tikz.line((-3.5, 4.5), (4.5, 4.5), options="dashed")
    tikz.node(line.start, options="left", text="$y=1$")
    # Plot it
    origin = (0, 0)
    tikz.line((-axes_len, 0), origin, options="ProcessBlue, <-")
    tikz.line(origin, (4.5, 4.5), options="ProcessBlue, ->")

    tikz.show()
