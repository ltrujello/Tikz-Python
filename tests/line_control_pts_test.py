import sys
from sympy import *

sys.path.append("/Users/luketrujillo/Desktop/github/tikz-python")
from tikz_methods import *

tikz = TikzPicture()

BRAID_HEIGHT = 5
SEP = 2

# Top and bottom bars
tikz.line((0, BRAID_HEIGHT), (12, BRAID_HEIGHT), options="thick")
tikz.line((0, 0), (12, 0), options="thick")

# Draw circles on the top and bottom bars
for i in range(1, 6 * SEP, SEP):
    tikz.circle((i, 0), radius=0.05, options="fill=black")
    tikz.circle((i, BRAID_HEIGHT), radius=0.05, options="fill=black")

tikz.circle((2, 2 * 5 / 3), radius=0.05, options="fill=red")
tikz.circle((2, 5 / 3), radius=0.05, options="fill=red")

##################################################################
# force = FORCE
# alpha = 2 * 5 / 3

t = Symbol("t")


class Ball:
    def __init__(self, start, end):
        # Initial velocity
        self.x_init_v = 0
        self.y_init_v = 0
        # Initial position
        self.x_i = start[0]
        self.y_i = start[1]
        # Final position
        self.x_f = end[0]
        self.y_f = end[1]

    @property
    def y_acc(self):
        return 2 * (self.y_f - self.y_i - self.y_init_v)

    @property
    def x_vel(self):
        return self.x_f - self.x_i

    @property
    def y_vel(self):
        return Add(integrate(self.y_acc, t), self.y_init_v)

    @property  # When t = 1, we need x_pos = end[0], y_pos = end[1]
    def x_pos(self):
        return Add(integrate(self.x_vel, t), self.x_i)

    @property
    def y_pos(self):
        return Add(integrate(self.y_vel, t), self.y_i)

    def pos_at_time(self, val):
        return float(self.x_pos.subs(t, val)), float(self.y_pos.subs(t, val))


def draw_crossing(start, end, y_init_v):
    strand = Ball(start, end)
    strand.y_init_v = y_init_v  # This changes a lot...
    n_pts = 30
    for i in range(1, n_pts):
        t = i / n_pts
        x, y = strand.pos_at_time(t)
        tikz.circle((x, y), radius=0.02, options="Blue")

    return strand


draw_crossing((3, 5), (2, 2 * 5 / 3), -3)
draw_crossing((1, 5), (2, 2 * 5 / 3), -3)
draw_crossing((2, 2 * 5 / 3), (4, 5 / 3), 0)
draw_crossing((4, 5 / 3), (5, 0), -2)

# strand_before((2, 2 * 5 / 3), (2, 1 * 5 / 3))

tikz.write()
tikz.show()