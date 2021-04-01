from tikzpy.drawing_object import _DrawingObject
from tikzpy.utils import brackets

# Class for Lines
class Line(_DrawingObject):
    """
    A class to create lines in the tikz environment

    Attributes :
        start (tuple) : Pair of floats representing the start of the line
        end (tuple) : Pair of floats representing the end of the line
        options (str) : String containing Tikz drawing options, e.g. "Blue"
        control_pts (list): List of control points for the line
    """

    def __init__(
        self,
        start,
        end,
        options="",
        to_options="",
        control_pts=[],
        action="draw",
    ):
        self.start = start
        self.end = end
        self.options = options
        self.to_options = to_options
        self.control_pts = control_pts

        super().__init__(action, self.options, self._command)

    @property
    def _command(self):
        r"""The Tikz code for a line that comes after \draw[self.options]. It is useful for
        us to do this breaking-up of the Tikz code, especially for clipping. However, this
        serves no use to the user, so we make it private (well, it's just bells and whistles).
        """
        if len(self.control_pts) == 0:
            return fr"{self.start} to{brackets(self.to_options)} {self.end};"

        else:
            control_stmt = ".. controls "
            for pt in self.control_pts:
                control_stmt += f"{pt[0], pt[1]}" + " and "
            control_stmt = control_stmt[:-4] + " .."
            return f"{self.start} {control_stmt} {self.end};"

    @property
    def midpoint(self):
        mid_x = round((self.start[0] + self.end[0]) / 2, 7)
        mid_y = round((self.start[1] + self.end[1]) / 2, 7)
        return (mid_x, mid_y)

    def shift(self, xshift, yshift):
        """Shift start, end, and control_pts"""
        shifted_start_end = shift_coords([self.start, self.end], xshift, yshift)
        shifted_control_pts = shift_coords(self.control_pts, xshift, yshift)

        self.start, self.end = shifted_start_end[0], shifted_start_end[1]
        self.control_pts = shifted_control_pts

    def scale(self, scale):
        """Scale start, end, and control_pts."""
        scaled_start_end = scale_coords([self.start, self.end], scale)
        self.start, self.end = scaled_start_end[0], scaled_start_end[1]
        self.control_pts = scale_coords(self.control_pts, scale)

    def rotate(self, angle, about_pt=None, radians=False):
        """Rotate start, end, and control_pts"""
        if about_pt == None:
            about_pt = self.midpoint
        rotated_start_end = rotate_coords(
            [self.start, self.end], angle, about_pt, radians
        )

        self.start, self.end = rotated_start_end[0], rotated_start_end[1]
        self.control_pts = rotate_coords(self.control_pts, angle, about_pt, radians)
