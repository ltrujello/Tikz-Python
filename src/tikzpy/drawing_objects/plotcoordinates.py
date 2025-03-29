from typing import List, Tuple, Union
from tikzpy.drawing_objects.point import Point
from tikzpy.drawing_objects.drawing_object import DrawingObject
from tikzpy.utils.helpers import brackets


class PlotCoordinates(DrawingObject):
    r"""
    A class to manage plots in a tikz environment.

    The PlotCoordinates class is used to represent the plot_coordinates
    functionality in TikZ. It is analagous to the TikZ command
    ```
    \draw plot[<options>] coordinates{ <points> };
    ```

    Parameters:
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
        """Calculates the geometric center (centroid) of a collection of points.

        This property computes the arithmetic mean of the x and y coordinates of all points in the collection.
        The result is a new Point object representing the centroid of these points.

        Returns:
            Point: A Point object representing the geometric center of the collection of points.
        """

        mean_x = 0
        mean_y = 0
        for pt in self.points:
            mean_x += pt.x
            mean_y += pt.y
        mean_x = mean_x / len(self.points)
        mean_y = mean_y / len(self.points)
        return Point(mean_x, mean_y)

    def shift_(self, xshift: float, yshift: float) -> None:
        for point in self.points:
            point.shift_(xshift, yshift)

    def scale_(self, scale: float) -> None:
        for point in self.points:
            point.scale_(scale)

    def rotate_(
        self,
        angle: float,
        about_pt: Union[Tuple[float, float], None, Point] = None,
        radians: bool = False,
    ) -> None:
        if about_pt is None:
            about_pt = self.center
        for point in self.points:
            point.rotate_(angle, about_pt, radians)

    def shift(self, xshift: float, yshift: float) -> None:
        new_plot = self.copy()
        new_plot.shift_(xshift, yshift)
        return new_plot


    def scale(self, scale: float) -> None:
        new_plot = self.copy()
        new_plot.scale_(scale)
        return new_plot

    def rotate(
        self,
        angle: float,
        about_pt: Union[Tuple[float, float], None, Point] = None,
        radians: bool = False,
    ) -> None:
        new_plot = self.copy()
        new_plot.rotate_(angle, about_pt, radians)
        return new_plot

    def add_point(self, x, y):
        """Adds a new point to the points list.

        This method creates a new Point instance with the specified x and y coordinates,
        and appends it to the `points` attribute of the class.

        Args:
            x (int/float): The x-coordinate of the point.
            y (int/float): The y-coordinate of the point.

        Returns:
            None
        """
        self.points.append(Point(x, y))
