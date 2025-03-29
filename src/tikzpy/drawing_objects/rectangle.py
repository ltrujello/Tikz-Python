from __future__ import annotations
from typing import Tuple, Union
from tikzpy.drawing_objects.point import Point
from tikzpy.drawing_objects.drawing_object import DrawingObject


class Rectangle(DrawingObject):
    """
    A class to manage rectangles in a tikz environment

    The `Rectangle` class is used to handle rectangles in TikZ. It is analagous to the TikZ code
    ```
    \draw[<options>] <left_corner> rectangle <right_corner>;
    ```

    Parameters:
        left_corner (tuple or Point) : Position of the left corner
        width (float) : Rectangle width
        height (float) : Rectangle height
        options (str) : String containing the drawing options, e.g, ("Blue")
        action (str) : The type of TikZ action to use. Default is "draw".
    """

    def __init__(
        self,
        left_corner: Union[Tuple[float, float], Point],
        width: float,
        height: float,
        options: str = "",
        action: str = "draw",
    ) -> None:
        self._left_corner: Point = Point(left_corner)
        self.width: float = width
        self.height: float = height
        self.options: str = options
        super().__init__(action, self.options)

    @property
    def _command(self) -> str:
        return f"{self._left_corner} rectangle {self.right_corner}"

    @property
    def center(self) -> Point:
        """Returns the center of the rectangle."""
        return Point(
            self._left_corner.x + self.width / 2,
            self._left_corner.y + self.height / 2,
        )

    @center.setter
    def center(self, center_point: Union[Point, tuple[int, int]]) -> Point:
        """Sets the center of the rectangle."""
        if isinstance(center_point, tuple):
            center_point = Point(center_point)
        self._left_corner = Point(
            center_point.x - self.width / 2, center_point.y - self.height / 2
        )

    @property
    def north(self) -> Point:
        """Returns the north point of the rectangle."""
        return Point(
            self._left_corner.x + self.width / 2,
            self._left_corner.y + self.height,
        )

    @north.setter
    def north(self, north_point: Union[Point, tuple[int, int]]) -> Point:
        """Sets the north point of the rectangle."""
        if isinstance(north_point, tuple):
            north_point = Point(north_point)
        self._left_corner = Point(
            north_point.x - self.width / 2, north_point.y - self.height
        )

    @property
    def east(self) -> Point:
        """Returns the east point of the rectangle."""
        return Point(
            self._left_corner.x + self.width,
            self._left_corner.y + self.height / 2,
        )

    @east.setter
    def east(self, east_point: Union[Point, tuple[int, int]]) -> Point:
        """Sets the east point of the rectangle."""
        if isinstance(east_point, tuple):
            east_point = Point(east_point)
        self._left_corner = Point(
            east_point.x - self.width, east_point.y - self.height / 2
        )

    @property
    def south(self) -> Point:
        """Returns the south point of the rectangle."""
        return Point(
            self._left_corner.x + self.width / 2,
            self._left_corner.y,
        )

    @south.setter
    def south(self, south_point: Union[Point, tuple[int, int]]) -> Point:
        """Sets the south point of the rectangle."""
        if isinstance(south_point, tuple):
            south_point = Point(south_point)
        self._left_corner = Point(south_point.x - self.width / 2, south_point.y)

    @property
    def west(self) -> Point:
        """Returns the west point of the rectangle."""
        return Point(
            self._left_corner.x,
            self._left_corner.y + self.height / 2,
        )

    @west.setter
    def west(self, west_point: Union[Point, tuple[int, int]]) -> Point:
        """Sets the west point of the rectangle."""
        if isinstance(west_point, tuple):
            west_point = Point(west_point)
        self._left_corner = Point(west_point.x, west_point.y - self.height / 2)

    @property
    def left_corner(self) -> Point:
        """Returns the left corner of the rectangle. This attribute is modifiable and can be set."""
        return self._left_corner

    @property
    def right_corner(self) -> Point:
        """Returns the right corner of the rectangle."""
        return self._left_corner + (self.width, self.height)

    @left_corner.setter
    def left_corner(self, new_corner) -> None:
        if isinstance(new_corner, (tuple, Point)):
            self._left_corner = Point(new_corner)
        else:
            raise TypeError(f"Invalid type '{type(new_corner)}' for left corner")

    def shift_(self, xshift: float, yshift: float) -> None:
        self._left_corner.shift_(xshift, yshift)

    def scale_(self, scale: float) -> None:
        self._left_corner.scale_(scale)
        self.width = scale * self.width
        self.height = scale * self.height

    def rotate_(
        self, angle: float, about_pt: Tuple[float, float], radians: bool = False
    ) -> None:
        self._left_corner.rotate_(angle, about_pt, radians)

    def shift(self, xshift: float, yshift: float) -> "Rectangle":
        new_rectangle = self.copy()
        new_rectangle.shift_(xshift, yshift)
        return new_rectangle

    def scale(self, scale: float) -> "Rectangle":
        new_rectangle = self.copy()
        new_rectangle.scale_(scale)
        return new_rectangle

    def rotate(
        self, angle: float, about_pt: Tuple[float, float], radians: bool = False
    ) -> "Rectangle":
        new_rectangle = self.copy()
        new_rectangle.rotate_(angle, about_pt, radians)
        return new_rectangle


def rectangle_from_north(
    north_point: Union[Tuple[float, float], Point],
    width: float = 0,
    height: float = 0,
    options: str = "",
    action: str = "draw",
):
    """Create a Rectangle such that the .north attribute is north_point"""
    north_point = Point(north_point)
    left_corner = Point(north_point.x - width / 2, north_point.y - height)
    return Rectangle(
        left_corner=left_corner,
        width=width,
        height=height,
        options=options,
        action=action,
    )


def rectangle_from_east(
    east_point: Union[Tuple[float, float], Point],
    width: float = 0,
    height: float = 0,
    options: str = "",
    action: str = "draw",
):
    """Create a Rectangle such that the .east attribute is north_point"""
    east_point = Point(east_point)
    left_corner = Point(east_point.x - width, east_point.y - height / 2)
    return Rectangle(
        left_corner=left_corner,
        width=width,
        height=height,
        options=options,
        action=action,
    )


def rectangle_from_south(
    south_point: Union[Tuple[float, float], Point],
    width: float = 0,
    height: float = 0,
    options: str = "",
    action: str = "draw",
):
    """Create a Rectangle such that the .south attribute is north_point"""
    south_point = Point(south_point)
    left_corner = Point(south_point.x - width / 2, south_point.y)
    return Rectangle(
        left_corner=left_corner,
        width=width,
        height=height,
        options=options,
        action=action,
    )


def rectangle_from_west(
    west_point: Union[Tuple[float, float], Point],
    width: float = 0,
    height: float = 0,
    options: str = "",
    action: str = "draw",
):
    """Create a Rectangle such that the .west attribute is west_point"""
    west_point = Point(west_point)
    left_corner = Point(west_point.x, west_point.y - height / 2)
    return Rectangle(
        left_corner=left_corner,
        width=width,
        height=height,
        options=options,
        action=action,
    )


def rectangle_from_center(
    center: Union[Tuple[float, float], Point],
    width: float = 0,
    height: float = 0,
    options: str = "",
    action: str = "draw",
):
    """Create a Rectangle by specifying its center."""
    center = Point(center)
    left_corner = Point(center.x - width / 2, center.y - height / 2)
    return Rectangle(
        left_corner=left_corner,
        width=width,
        height=height,
        options=options,
        action=action,
    )
