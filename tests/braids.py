import tikz_py
from sympy import *

tikz = tikz_py.TikzPicture()

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

# tikz.plot_coordinates(
#     [(1, 5), (2, 2 * 5 / 3), (2, 5 / 3), (1, 0)], plot_options="smooth, tension = 0.1"
# )

###########################################################################################
t = Symbol("t")


class Ball:
    def __init__(self, start, end):
        """We imagine that a ball must pass through points
            * start = (x_i, y_i)
            * end = (x_f, y_f)
        subject to the conditions specified :
            * x acceleration OR x initial velocity
            * y acceleration OR y initial velocity
        """
        # Acceleration
        self.x_acc = None
        self.y_acc = None
        # Initial velocity
        self.x_init_v = None
        self.y_init_v = None
        # Initial and find points
        self.x_i = start[0]
        self.y_i = start[1]
        self.x_f = end[0]
        self.y_f = end[1]

    """
    X-Dimension
    """

    def get_x_init_v(self):
        """* If self.x_init_v is not specified, then self.x_acc was, in which case
        we solve for the appropriate value of x_init_v.
        * If it was specified, then we return it.
        """
        if self.x_init_v == None:
            return self.x_f - self.x_i - 0.5 * self.x_acc
        else:
            return self.x_init_v

    def get_x_acc(self):
        """* If self.x_acc is not specified, then self.x_init_v was, in which case
        we solve for the appropriate value of x_acc.
        * If it was specified, then we return it.
        """
        if self.x_acc == None:
            return 2 * (self.x_f - self.x_i - self.x_init_v)
        else:
            return self.x_acc

    def x_vel(self):
        x_acc = self.get_x_acc()
        x_init_v = self.get_x_init_v()
        return Add(integrate(x_acc, t), x_init_v)

    def x_pos(self):
        x_vel = self.x_vel()
        return Add(integrate(x_vel, t), self.x_i)

    """
    Y-Dimension
    """

    def get_y_init_v(self):
        """* If self.y_init_v is not specified, then self.y_acc was, in which case
        we solve for the appropriate value of y_init_v.
        * If it was specified, then we return it.
        """
        if self.y_init_v == None:
            return self.y_f - self.y_i - 0.5 * self.y_acc  # ?
        else:
            return self.y_init_v

    def get_y_acc(self):
        """* If self.y_acc is not specified, then self.y_init_v was, in which case
        we solve for the appropriate value of y_acc.
        * If it was specified, then we return it.
        """
        if self.y_acc == None:
            return 2 * (self.y_f - self.y_i - self.y_init_v)
        else:
            return self.y_acc

    def y_vel(self):
        y_acc = self.get_y_acc()
        y_init_v = self.get_y_init_v()
        return Add(integrate(y_acc, t), y_init_v)

    def y_pos(self):
        y_vel = self.y_vel()
        return Add(integrate(y_vel, t), self.y_i)

    # Current velocity at time 0 < t < 1
    def vel_at_time(self, val):
        vx_t = self.x_vel()
        vx = float(vx_t.subs(t, val))

        vy_t = self.y_vel()
        vy = float(vy_t.subs(t, val))

        return vx, vy

    # Current position at time 0 < t < 1
    def pos_at_time(self, val):
        x_t = self.x_pos()
        x = float(x_t.subs(t, val))

        y_t = self.y_pos()
        y = float(y_t.subs(t, val))

        return x, y


# def draw_crossing(start, end):
start = (2, 5 / 3)  # (2, 2 * 5 / 3)  # (3, 5)
end = (3, 0)

strand = Ball(start, end)
strand.x_init_v = 3
strand.y_acc = 2
n_pts = 30
for i in range(1, n_pts):
    s = i / n_pts
    x, y = strand.pos_at_time(s)
    tikz.circle((x, y), radius=0.02, options="fil=Blue")

def draw_strand(points):
    for i, point in enumerate(points):
        start = points[0]
        end =  points[1]
        strand = Ball(start, end)
        x_i = start[0]
        y_i = start[1]
        x_f = points[1][0]
        y_f = points[1][1]

        if i == 0:
            strand.x_init_v = 0
            strand.y_acc = 2

        if x_i == 


tikz.write()
tikz.show()