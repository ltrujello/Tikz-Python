from tikzpy.drawing_object import _DrawingObject

# Class for Circles
class Circle(_DrawingObject):
    """
    A class to create circles in the tikz environment

    Attributes :
        position (tuple) : Pair of floats representing the center of the circle
        radius (float) : Length (in cm) of the radius
        options (str) : String containing the drawing options (e.g, "Blue")
    """

    def __init__(self, center, radius, options="", action="draw"):
        self.center = center
        self.radius = radius
        self.options = options
        super().__init__(action, self.options, self._command)

    @property
    def _command(self):
        return f"{self.center} circle ({self.radius}cm);"

    def shift(self, xshift, yshift):
        self.center = shift_coords([self.center], xshift, yshift)[0]

    def scale(self, scale):
        self.center = scale_coords([self.center], scale)[0]

    def rotate(self, angle, about_pt, radians=False):
        self.center = rotate_coords([self.center], angle, about_pt, radians)[0]