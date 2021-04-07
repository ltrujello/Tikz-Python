from tikzpy.utils.transformations import shift_coords, scale_coords, rotate_coords


class Clip:
    """A class for a clipping code statement."""

    def __init__(self, draw_obj, draw=False):
        if isinstance(
            draw_obj, (Line, PlotCoordinates, Circle, Node, Rectangle, Ellipse, Arc)
        ):
            self.draw_obj = draw_obj
            self.draw = draw
        else:
            raise TypeError(
                f"Clip argument {draw_obj} must be an instance of a drawing class."
            )

    @property
    def code(self):
        if self.draw == True:
            return fr"\clip[preaction = {{draw, {self.draw_obj.options}}}] {self.draw_obj._command};"
        else:
            return fr"\clip {self.draw_obj._command};"

    def shift(self, xshift, yshift):
        self.draw_obj.shift(xshift, yshift)

    def scale(self, scale):
        self.draw_obj.scale(scale)

    def rotate(self, angle, about_pt, radians=False):
        self.draw_obj.rotate(angle, about_pt, radians)
