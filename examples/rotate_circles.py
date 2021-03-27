import sys

sys.path.append("/Users/luketrujillo/Desktop/github/tikz-python")
from tikz_methods import *

tikz = TikzPicture(center=True)

n = 30
for i in range(n):
    point = (math.sin(2 * math.pi * i / n), math.cos(2 * math.pi * i / n))

    tikz.circle(point, 2, options="color=" + rainbow_colors(i)).shift(0, -2)
    tikz.circle(point, 2.2, options="color=" + rainbow_colors(i + 1)).shift(0, -2)
    tikz.circle(point, 2.4, options="color=" + rainbow_colors(i + 2)).shift(0, -2)
    tikz.circle(point, 2.6, options="color=" + rainbow_colors(i + 3)).shift(0, -2)
    tikz.circle(point, 2.8, options="color=" + rainbow_colors(i + 4)).shift(0, -2)
    tikz.circle(point, 3.0, options="color=" + rainbow_colors(i + 5)).shift(0, -2)
    tikz.circle(point, 3.2, options="color=" + rainbow_colors(i + 6)).shift(0, -2)
    tikz.circle(point, 3.4, options="color=" + rainbow_colors(i + 7)).shift(0, -2)

    tikz.line((-4, -6), (-4, -2), options="color= " + rainbow_colors(i)).rotate(
        (2 * math.pi * i / n), about_pt=(0, 0), radians=True
    )

tikz.write()