import tikzpy
from sympy import poly
from sympy.abc import x

tikz = tikzpy.TikzPicture()

BRAID_HEIGHT = 5
SEP = 2

# Top and bottom bars
top_bar = tikz.line((0, BRAID_HEIGHT), (12, BRAID_HEIGHT), options="thick")
bottom_bar = tikz.line((0, 0), (12, 0), options="thick")

# Draw circles on the top and bottom bars
for i in range(1, 6 * SEP, SEP):
    tikz.circle((i, 0), radius=0.05, options="fill=black")
    tikz.circle((i, BRAID_HEIGHT), radius=0.05, options="fill=black")

tikz.circle((2, 2 * 5 / 3), radius=0.05, options="fill=red")
tikz.circle((2, 5 / 3), radius=0.05, options="fill=red")

#########################################################


def hermite(start, end, tangent_start, tangent_end):
    x_i = start[0]
    y_i = start[1]
    x_f = end[0]
    y_f = end[1]

    x_t = poly(
        (2 * x ** 3 - 3 * x ** 2 + 1) * x_i
        + (x ** 3 - 2 * x ** 2 + x) * tangent_start[0]
        + (-2 * x ** 3 + 3 * x ** 2) * x_f
        + (x ** 3 - x ** 2) * tangent_end[0]
    )
    y_t = poly(
        (2 * x ** 3 - 3 * x ** 2 + 1) * y_i
        + (x ** 3 - 2 * x ** 2 + x) * tangent_start[1]
        + (-2 * x ** 3 + 3 * x ** 2) * y_f
        + (x ** 3 - x ** 2) * tangent_end[1]
    )

    return x_t, y_t


for points in [(3, 5), (2, 2 * 5 / 3), (2, 5 / 3)]:


x_t, y_t = hermite(start, end, (0, -1), (-1, 0))

n_pts = 30
for i in range(1, n_pts):
    s = i / n_pts
    x = x_t.subs("x", s)
    y = y_t.subs("x", s)
    tikz.circle((x, y), radius=0.02, options="fil=Blue")



x_t, y_t = hermite(start, end, (-1, 0), (1, 0))
n_pts = 30
for i in range(1, n_pts):
    s = i / n_pts
    x = x_t.subs("x", s)
    y = y_t.subs("x", s)
    tikz.circle((x, y), radius=0.02, options="fil=Blue")

# x_t, y_t = hermite(start, end, (-1, 0), (1, 0))

# n_pts = 30
# for i in range(1, n_pts):
#     s = i / n_pts
#     x = x_t.subs("x", s)
#     y = y_t.subs("x", s)
#     tikz.circle((x, y), radius=0.02, options="fil=Blue")

tikz.write()
tikz.show()