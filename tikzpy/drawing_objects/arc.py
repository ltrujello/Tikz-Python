from math import sin, cos, tan, atan, atan2, pi, sqrt
from math import radians as degs_2_rads
from math import degrees as rads_2_degs
from tikzpy.utils.transformations import shift_coords, scale_coords, rotate_coords
from tikzpy.drawing_objects.drawing_object import _DrawingObject


class Arc(_DrawingObject):
    """
    A class to create arcs in the tikz environment.

    Attributes :
        center (tuple) : Pair of points representing the relative center of the arc
        start_angle (float) : The angle of the start of the arc
        end_angle (float) : The angle of the end of the arc
        radius (float) : The radius (in cm) of the arc
        radians (bool) : Set true if inputting radians. Default behavior is for degrees.
        draw_from_start (bool) : Set true if you are drawing the arc by specifying the point from
                                 where it should start drawing. False will draw the arc from the center specified.
    """

    def __init__(
        self,
        position,
        start_angle,
        end_angle,
        radius=None,
        x_radius=None,
        y_radius=None,
        options="",
        radians=False,
        draw_from_start=True,
        action="draw",
    ):
        self.position = position
        self.start_angle = start_angle
        self.end_angle = end_angle
        self.radius = radius
        self.x_radius = x_radius
        self.y_radius = y_radius
        self.options = options
        self.radians = radians
        self.draw_from_start = draw_from_start

        super().__init__(action, self.options, self._command)

    @property
    def _start_angle(self):
        return Angle(self.start_angle, self.radians)

    @property
    def _end_angle(self):
        return Angle(self.end_angle, self.radians)

    @property
    def arc_type(self):
        if self.radius != None:
            if self.x_radius != None or self.y_radius != None:
                raise ValueError(
                    "Cannot set radius AND x_radius, y_radius at the same time."
                )
            else:
                self.radius_statement = f"radius = {self.radius}cm"
                return "circle"

        else:
            if self.x_radius == None or self.y_radius == None:
                raise ValueError(
                    f"x_radius was set to {self.x_radius}, y_radius was set to {self.y_radius}, but neither should be None."
                )
            if self.x_radius <= 0 or self.y_radius <= 0:
                raise ValueError(
                    f"x_radius is {self.x_radius}, y_radius is {self.y_radius}, but neither can be <= 0."
                )
            else:
                self.radius_statement = (
                    f"x radius = {self.x_radius}cm, y radius = {self.y_radius}cm"
                )
                return "ellipse"

    @property
    def _position(self):
        """We return the point at which we should begin drawing the arc. This takes a
        bit of work since we allow the user to possibly specify the center of the
        arc of which they would like to see drawn.
        """
        if self.draw_from_start:
            start_pos = self.position
        elif self.arc_type == "circle":
            start_pos = self.start_pos_circle()
        elif self.arc_type == "ellipse":
            start_pos = self.start_pos_ellipse()
        else:
            raise ValueError(
                f"The type of arc you want to see, which is {self.arc_type}, is not 'circle' or 'ellipse'."
            )
        return start_pos

    @_position.setter
    def _position(self, new_pos):
        return self.position

    @property
    def _command(self):
        if self.arc_type == "circle":
            start_angle, end_angle = self._start_angle.degs(), self._end_angle.degs()
        else:  # This is for the case the ellipse.
            # We need to calculate the parameter t at which (x_r*cos(self.start_angle), y_r*sin(self.start_angle)) hits
            t_start = self.atan2_for_ellipse(self._start_angle)
            t_end = self.atan2_for_ellipse(self._end_angle)

            start_angle, end_angle = rads_2_degs(t_start), rads_2_degs(t_end)
        return f"{self._position} arc [start angle = {start_angle}, end angle = {end_angle}, {self.radius_statement}]"

    def start_pos_circle(self):
        """Calculates the point at which the CIRCLE arc should begin
        drawing, given that the user specified what the center, radius,
        start, and end angles of the desired circular arc.
        """
        assert self.arc_type == "circle"
        # Obtain the angles in radians
        start_angle = self._start_angle.rads()
        # Calculate the point at which the arc should begin drawing
        start_pt_x = self.position[0] + self.radius * cos(start_angle)
        start_pt_y = self.position[1] + self.radius * sin(start_angle)

        return (start_pt_x, start_pt_y)

    def start_pos_ellipse(self):
        """Calculates the point at which the ELLIPSE arc should begin
        drawing, given that the user specified what the center, x_radius, y_radius,
        start, and end angles of the desired elliptic arc.
        """
        assert self.arc_type == "ellipse"
        # Obtain the angles in radians
        start_angle = self._start_angle.rads()
        # We calculate r_at_theta, the distance between the origin and the point on the ellipse which occurs at angle self.start_angle.
        r_at_theta = (self.x_radius * self.y_radius) / sqrt(
            (self.y_radius * cos(start_angle)) ** 2
            + (self.x_radius * sin(start_angle)) ** 2
        )
        # We then use r_at_theta to calculate the desired point on the ellipse
        start_pt_x = self.position[0] + r_at_theta * cos(start_angle)
        start_pt_y = self.position[1] + r_at_theta * sin(start_angle)

        return (start_pt_x, start_pt_y)

    def shift(self, xshift, yshift):
        self.center = shift_coords([self.center], xshift, yshift)[0]

    def scale(self, scale):
        scaled_center = scale_coords([self.center], scale)
        scaled_radius = self.radius * scale

        self.center = scaled_center[0]
        self.radius = scaled_radius

    def rotate(self, angle, about_pt=None, radians=False):
        if about_pt == None:
            self._position
        self.center = rotate_coords([self.center], angle, about_pt, radians)[0]

    def atan2_for_ellipse(self, angle):
        """We need to perform a tangent inverse operation which returns values between
        0 and 2pi. Built in functions only do -pi/2 -- pi/2 (atan) or -pi -- pi (atan2).
        Further, we need to maintain arithmetic precision. We use the .quadrant attribute to
        help with this.
        """
        theta = angle.rads()
        t = atan2(
            self.x_radius * tan(theta), self.y_radius
        )  # The value of t such that (b*cos(t), a*sin(t)) makes angle theta to the axis.
        if angle.quadrant == 0:
            t += 0
        elif angle.quadrant == 1 or angle.quadrant == 2:
            t += pi
        else:
            t += 2 * pi
        return t


class Angle:
    def __init__(self, angle, radians):
        self.angle = angle
        self.radians = radians
        self.quadrant = self.quadrant(angle)

    def degs(self):
        if self.radians:
            angle = rads_2_degs(self.angle)
        else:
            angle = self.angle
        return angle

    def rads(self):
        if not self.radians:
            angle = degs_2_rads(self.angle)
        else:
            angle = self.start_angle

        return angle

    def quadrant(self, angle):
        if self.radians:
            if 0 <= angle <= pi / 2:
                return 0
            elif pi / 2 < angle <= pi:
                return 1
            elif pi < angle <= 3 * pi / 2:
                return 2
            else:
                return 3
        else:
            if 0 <= angle <= 90:
                return 0
            elif 90 < angle <= 180:
                return 1
            elif 180 < angle <= 270:
                return 2
            else:
                return 3
