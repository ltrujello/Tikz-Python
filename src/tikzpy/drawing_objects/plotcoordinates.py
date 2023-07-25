from typing import List, Tuple, Union
from tikzpy.drawing_objects.point import Point
from tikzpy.drawing_objects.drawing_object import DrawingObject
from tikzpy.utils.helpers import brackets


class PlotCoordinates(DrawingObject):
    """
    A class to create plots in the tikz environment.

    Attributes :
        options (str) : String containing drawing options (e.g., "Blue")
        plot_options (str) : String containing the plot options (e.g., "smooth cycle")
        points (list) : A list of points to be drawn

    """

    def __init__(
        self,
        points: Union[List[Tuple], Point],
        options: str = "",
        plot_options: str = "",
        action: str = "draw",
    ):
        self.points = [Point(point) for point in points]
        self.options = options
        self.plot_options = plot_options
        super().__init__(action, self.options)

    @property
    def _command(self) -> str:
        cmd: str = rf"plot{brackets(self.plot_options)} coordinates {{"
        for pt in self.points:
            cmd += str(pt) + " "
        cmd += "}"
        return cmd

    @property
    def center(self) -> "Point":
        mean_x = 0
        mean_y = 0
        for pt in self.points:
            mean_x += pt.x
            mean_y += pt.y
        mean_x = mean_x / len(self.points)
        mean_y = mean_y / len(self.points)
        return Point(mean_x, mean_y)

    def shift(self, xshift: float, yshift: float) -> None:
        for point in self.points:
            point.shift(xshift, yshift)

    def scale(self, scale: float) -> None:
        for point in self.points:
            point.scale(scale)

    def rotate(
        self,
        angle: float,
        about_pt: Union[Tuple[float, float], None, Point] = None,
        radians: bool = False,
    ) -> None:
        if about_pt is None:
            about_pt = self.center
        for point in self.points:
            point.rotate(angle, about_pt, radians)

    def add_point(self, x, y):
        self.points.append(Point(x, y))
