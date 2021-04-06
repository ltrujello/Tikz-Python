from tikzpy.drawing_objects.drawing_object import _DrawingObject
from tikzpy.utils.transformations import shift_coords, scale_coords, rotate_coords


class Ellipse(_DrawingObject):
    """
    A class to create lines in the tikz environment

    Attributes :
        center (tuple) : Pair of floats representing the center of the ellipse
        horiz_axis (float): The length (in cm) of the horizontal axis of the ellipse
        vert_axis (float): The length (in cm) of the vertical axis of the ellipse
    """

    def __init__(self, center, horiz_axis, vert_axis, options="", action="draw"):
        self.center = center
        self.horiz_axis = horiz_axis
        self.vert_axis = vert_axis
        self.options = options
        super().__init__(action, self.options, self._command)

    @property
    def _command(self):
        return f"{self.center} ellipse ({self.horiz_axis}cm and {self.vert_axis}cm);"

    def shift(self, xshift, yshift):
        self.center = shift_coords([self.center], xshift, yshift)[0]

    def scale(self, scale):
        scaled_center = scale_coords([self.center], scale)[0]
        scaled_h = round(self.horiz_axis * scale, 7)
        scaled_v = round(self.vert_axis * scale, 7)

        self.center = scaled_center
        self.horiz_axis = scaled_h
        self.vert_axis = scaled_v

    def rotate(self, angle, about_pt, radians=False):
        self.center = rotate_coords([self.center], angle, about_pt, radians)[0]
