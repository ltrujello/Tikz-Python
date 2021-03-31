from tikz_py.drawing_object import _DrawingObject
from tikz_py.utils import brackets

# Class for Plotting
class PlotCoordinates(_DrawingObject):
    """
    A class to create plots in the tikz environment

    Attributes :
        options (str) : String containing drawing options (e.g., "Blue")
        plot_options (str) : String containing the plot options (e.g., "smooth cycle")
        points (list) : A list of points to be drawn

    """

    def __init__(self, points, options="", plot_options="", action="draw"):
        self.points = points
        self.options = options
        self.plot_options = plot_options
        super().__init__(action, self.options, self._command)

    @property
    def _command(self):
        cmd = fr"plot{brackets(self.plot_options)} coordinates {{"
        for pt in self.points:
            cmd += str(pt) + " "
        cmd += "};"
        return cmd

    @property
    def center(self):
        mean_x = 0
        mean_y = 0
        for pt in self.points:
            mean_x += pt[0]
            mean_y += pt[1]
        mean_x = round(mean_x / len(self.points), 7)
        mean_y = round(mean_y / len(self.points), 7)
        return (mean_x, mean_y)

    def shift(self, xshift, yshift):
        self.points = shift_coords(self.points, xshift, yshift)

    def scale(self, scale):
        self.points = scale_coords(self.points, scale)

    def rotate(self, angle, about_pt=None, radians=False):
        if about_pt == None:
            about_pt = self.center
        self.points = rotate_coords(self.points, angle, about_pt, radians)