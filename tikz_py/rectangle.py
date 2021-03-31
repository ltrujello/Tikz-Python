from tikz_py.drawing_object import _DrawingObject


class Rectangle(_DrawingObject):
    """
    A class to create lines in the tikz environment

    Attributes :
        left_corner (tuple) : Pair of floats representing the position of the bottom left corner
        right_corner (tuple) : Pair of floats representing the position of the upper right corner
        options (str) : String containing the drawing options, e.g, ("Blue")
    """

    def __init__(self, left_corner, right_corner, options="", action="draw"):
        self.left_corner = left_corner
        self.right_corner = right_corner
        self.options = options
        super().__init__(action, self.options, self._command)

    @property
    def _command(self):
        return f"{self.left_corner} rectangle {self.right_corner};"

    def shift(self, xshift, yshift):
        shifted_corners = shift_coords(
            [self.left_corner, self.right_corner], xshift, yshift
        )
        self.left_corner = shifted_corners[0]
        self.right_corner = shifted_corners[1]

    def scale(self, scale):
        scaled_corners = scale_coords([self.left_corner, self.right_corner], scale)
        self.left_corner = scaled_corners[0]
        self.right_corner = scaled_corners[1]

    def rotate(self, angle, about_pt, radians=False):
        rotated_corners = rotate_coords(
            [self.left_corner, self.right_corner], angle, about_pt, radians
        )
        self.left_corner = rotated_corners[0]
        self.right_corner = rotated_corners[1]