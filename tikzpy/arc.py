from tikzpy.drawing_object import _DrawingObject


class Arc(_DrawingObject):
    """
    A class to create lines in the tikz environment

    Attributes :
        center (tuple) : Pair of points representing the relative center of the arc
        start_angle (float) : The angle of the start of the arc
        end_angle (float) : The angle of the end of the arc
        radius (float) : The radius (in cm) of the arc
        radians (bool) : Set true if inputting radians. Default behavior is for degrees.
    """

    def __init__(
        self,
        center,
        start_angle,
        end_angle,
        radius,
        options="",
        radians=False,
        action="draw",
    ):
        self.center = center
        self.start_angle = start_angle
        self.end_angle = end_angle
        self.radius = radius
        self.options = options

        if radians:
            self.start_angle = round(self.start_angle, 180 / math.pi, 7)
            self.end_angle = round(self.end_angle, 180 / math.pi, 7)

        super().__init__(action, self.options, self._command)

    @property
    def _command(self):
        return (
            f"{self.center} arc ({self.start_angle}:{self.end_angle}:{self.radius}cm);"
        )

    def shift(self, xshift, yshift):
        self.center = shift_coords([self.center], xshift, yshift)[0]

    def scale(self, scale):
        scaled_center = scale_coords([self.center], scale)
        scaled_radius = round(self.radius * scale, 7)

        self.center = scaled_center[0]
        self.radius = scaled_radius

    def rotate(self, angle, about_pt, radians=False):
        self.center = rotate_coords([self.center], angle, about_pt, radians)[0]
