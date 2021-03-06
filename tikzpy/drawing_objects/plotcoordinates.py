from tikzpy.drawing_objects.drawing_object import DrawingObject
from tikzpy.utils.helpers import brackets
from tikzpy.utils.transformations import shift_coords, scale_coords, rotate_coords
from typing import List, Tuple


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
        points: List[Tuple],
        options: str = "",
        plot_options: str = "",
        action: str = "draw",
    ):
        self.points = points
        self.options = options
        self.plot_options = plot_options
        super().__init__(action, self.options)

    @property
    def _command(self) -> str:
        cmd: str = fr"plot{brackets(self.plot_options)} coordinates {{"
        for pt in self.points:
            cmd += str(pt) + " "
        cmd += "}"
        return cmd

    @property
    def center(self) -> Tuple[float, float]:
        mean_x: float = 0
        mean_y: float = 0
        for pt in self.points:
            mean_x += pt[0]
            mean_y += pt[1]
        mean_x = mean_x / len(self.points)
        mean_y = mean_y / len(self.points)
        return (mean_x, mean_y)

    def shift(self, xshift: float, yshift: float) -> None:
        self.points = shift_coords(self.points, xshift, yshift)

    def scale(self, scale: float) -> None:
        self.points = scale_coords(self.points, scale)

    def rotate(
        self, angle: float, about_pt: Tuple[float, float] = None, radians: bool = False
    ) -> None:
        if about_pt is None:
            about_pt = self.center
        self.points = rotate_coords(self.points, angle, about_pt, radians)

    def add_point(self, x, y):
        self.points.append((x, y))
