from __future__ import annotations
import math
from typing import Tuple, Union
from tikzpy.drawing_objects.point import Point
from tikzpy.drawing_objects.drawing_object import DrawingObject


class Circle(DrawingObject):
    r"""
    A class to create circles in the tikz environment.

    Parameters:
        center: Pair of floats representing the center of the circle
        radius: Length (in cm) of the radius
        options: String containing the drawing options (e.g, "Blue")
        action: The type of TikZ action to use. Default is "draw".
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
        """
        Returns a Point object representing the center of the circle.

        ```python
        from tikzpy import TikzPicture
        tikz = TikzPicture()
        circle = tikz.circle((0,0), 1, options="fill=ProcessBlue!30", action="filldraw")
        tikz.node(circle.center, text="O")
        tikz.show()
        ```

        <img src="../../png/circle_center.png"/> 
        """
        return self._center

    @center.setter
    def center(self, new_center: Union[tuple, Point]) -> None:
        if isinstance(new_center, (tuple, Point)):
            self._center = Point(new_center)
        else:
            raise TypeError(f"Invalid type '{type(new_center)}' for center")

    @property
    def north(self) -> Point:
        """
        Returns a Point object representing the north point on the circle.

        ```python
        from tikzpy import TikzPicture
        tikz = TikzPicture()
        circle = tikz.circle((0,0), 1, options="fill=ProcessBlue!30", action="filldraw")
        tikz.node(circle.north, text="$N$", options="above")
        tikz.show()
        ```

        <img src="../../png/circle_north.png"/> 
        """
        return self._center + (0, self.radius)

    @property
    def east(self) -> Point:
        """
        Returns a Point object representing the east point on the circle.

        ```python
        from tikzpy import TikzPicture
        tikz = TikzPicture()
        circle = tikz.circle((0,0), 1, options="fill=ProcessBlue!30", action="filldraw")
        tikz.node(circle.east, text="$E$", options="right")
        tikz.show()
        ```

        <img src="../../png/circle_east.png"/> 
        """
        return self._center + (self.radius, 0)

    @property
    def south(self) -> Point:
        """
        Returns a Point object representing the south point on the circle.

        ```python
        from tikzpy import TikzPicture
        tikz = TikzPicture()
        circle = tikz.circle((0,0), 1, options="fill=ProcessBlue!30", action="filldraw")
        tikz.node(circle.south, text="$S$", options="below")
        tikz.show()
        ```

        <img src="../../png/circle_south.png"/> 
        """
        return self._center - (0, self.radius)

    @property
    def west(self) -> Point:
        """
        Returns a Point object representing the west point on the circle.

        ```python
        from tikzpy import TikzPicture
        tikz = TikzPicture()
        circle = tikz.circle((0,0), 1, options="fill=ProcessBlue!30", action="filldraw")
        tikz.node(circle.west, text="$W$", options="left")
        tikz.show()
        ```

        <img src="../../png/circle_west.png"/> 
        """
        return self._center - (self.radius, 0)

    @property
    def _command(self) -> str:
        return f"{self._center} circle ({self.radius}cm)"

    def point_at_arg(self, theta: float, radians: bool = False) -> tuple:
        r"""Returns the point on the circle at angle theta. Both degrees and radians can be specified.


        ```python
        from tikzpy import TikzPicture
        tikz = TikzPicture(center=True)
        circle = tikz.circle((0,0), 1, options="fill=ProcessBlue!30", action="filldraw")
        tikz.node(circle.point_at_arg(45), text="$\pi/2$", options="right")
        tikz.node(circle.point_at_arg(135), text="$3\pi/4$", options="left")
        tikz.node(circle.point_at_arg(270), text="$3\pi/2$", options="below")
        tikz.show()
        ```

        <img src="../../png/circle_point_at_arg.png"/> 
        """
        if not radians:
            theta = math.radians(theta)
        return self.center.x + self.radius * math.cos(
            theta
        ), self.center.y + self.radius * math.sin(theta)

    def shift_(self, xshift: float, yshift: float) -> None:
        self._center.shift_(xshift, yshift)

    def scale_(self, scale: float) -> None:
        self._center.scale_(scale)
        self.radius *= scale

    def rotate_(
        self, angle: float, about_pt: Tuple[float, float] = None, radians: bool = False
    ) -> None:
        self._center.rotate_(angle, about_pt, radians)

    def shift(self, xshift: float, yshift: float) -> "Circle":
        new_circle = self.copy()
        new_circle.shift_(xshift, yshift)
        return new_circle

    def scale(self, scale: float) -> "Circle":
        new_circle = self.copy()
        new_circle.scale_(scale)
        return new_circle

    def rotate(
        self, angle: float, about_pt: Tuple[float, float] = None, radians: bool = False
    ) -> "Circle":
        new_circle = self.copy()
        new_circle.rotate_(angle, about_pt, radians)
        return new_circle



