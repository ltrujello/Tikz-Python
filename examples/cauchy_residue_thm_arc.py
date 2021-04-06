from tikzpy import TikzPicture, arrows_along_path_style

tikz = TikzPicture()
tikz.add_styles(*arrows_along_path_style)
tikz.options = "thick"

# x and Y axes
x_axis = tikz.line((-4, 0), (4, 0), options="->")
y_axis = tikz.line((0, -1), (0, 4), options="->")
tikz.node(x_axis.end, options="below", text="$\\mathbb{R}$")
tikz.node(y_axis.end, options="left", text="$i$")

# Red Semicircle
arc = tikz.arc(
    (0, 0),
    0,
    180,
    radius=2,
    options="arrows_along_path=red, red",
    draw_from_start=False,
)
# Draws the blue path [-R, R]
bottom_path = tikz.line((-2, 0), (2, 0), options="blue, arrows_along_path=blue")
tikz.node((bottom_path.start[0], bottom_path.start[1] - 0.5), text="$R$")
tikz.node((bottom_path.end[0], bottom_path.end[1] - 0.5), text="$-R$")

# % Draws the points z_1, z_2 of interest
circle_1 = tikz.circle((0.7, 0.7), 0.05, action="fill")
circle_2 = tikz.circle((-0.7, 0.7), 0.05, action="fill")
tikz.node(circle_1.center, options="right", text="$z_1$")
tikz.node(circle_2.center, options="left", text="$z_2$")

tikz.write()
tikz.show()