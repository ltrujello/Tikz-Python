from __future__ import annotations
import math
from typing import Tuple, Union
from tikzpy.drawing_objects.point import Point
from tikzpy.drawing_objects.drawing_object import DrawingObject


class Circle(DrawingObject):
    """
    A class to create circles in the tikz environment.

    Attributes :
        position (Point) : Pair of floats representing the center of the circle
        radius (float) : Length (in cm) of the radius
        options (str) : String containing the drawing options (e.g, "Blue")
    """

    def __init__(
        self,
        center: Union[Tuple[float, float], Point],
        radius: float,
        options: str = "",
        action: str = "draw",
    ) -> None:
        self._center = Point(center)
        self.radius = radius
        self.options = options
        super().__init__(action, self.options)

    @property
    def center(self) -> Point:
        return self._center

    @center.setter
    def center(self, new_center: Union[tuple, Point]) -> None:
        if isinstance(new_center, (tuple, Point)):
            self._center = Point(new_center)
        else:
            raise TypeError(f"Invalid type '{type(new_center)}' for center")

    @property
    def north(self):
        return self._center + (0, self.radius)

    @property
    def east(self):
        return self._center + (self.radius, 0)

    @property
    def south(self):
        return self._center - (0, self.radius)

    @property
    def west(self):
        return self._center - (self.radius, 0)

    @property
    def _command(self) -> str:
        return f"{self._center} circle ({self.radius}cm)"

    def point_at_arg(self, theta: float, radians: bool = False) -> tuple:
        """Returns the point on the circle at angle theta."""
        if not radians:
            theta = math.radians(theta)
        return self.center.x + self.radius * math.cos(
            theta
        ), self.center.y + self.radius * math.sin(theta)

    def shift(self, xshift: float, yshift: float) -> None:
        self._center.shift(xshift, yshift)

    def scale(self, scale: float) -> None:
        self._center.scale(scale)

    def rotate(
        self, angle: float, about_pt: Tuple[float, float] = None, radians: bool = False
    ) -> None:
        self._center.rotate(angle, about_pt, radians)
