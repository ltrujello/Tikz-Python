from tikzpy import TikzPicture
from math import sin, cos, pi

tikz = TikzPicture()

tikz.line((-4, 0), (4, 0))
tikz.line((0, -4), (0, 4))
tikz.circle((0, 0), 0.2)
tikz.ellipse((0, 0), 2, 1, options="dashed")


def test_arc(start, end):
    arc = tikz.arc(
        (0, 0),
        start,
        end,
        x_radius=2,
        y_radius=1,
        options="fill=ProcessBlue!30",
        draw_from_start=False,
    )
    tikz.line((0, 0), (4 * cos(start * pi / 180), 4 * sin(start * pi / 180)))
    tikz.line((0, 0), (4 * cos(end * pi / 180), 4 * sin(end * pi / 180)))
    tikz.write()
    tikz.show(quiet=True)

    return arc
