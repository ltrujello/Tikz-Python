from __future__ import annotations
from typing import Tuple, Union
from tikzpy.drawing_objects.point import Point
from tikzpy.drawing_objects.drawing_object import DrawingObject


class Rectangle(DrawingObject):
    """
    A class to create rectangles in the tikz environment

    Attributes :
        left_corner (tuple) : Pair of floats representing the position of the bottom left corner
        right_corner (tuple) : Pair of floats representing the position of the upper right corner
        options (str) : String containing the drawing options, e.g, ("Blue")
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

    @property
    def north(self) -> Point:
        """Returns the north point of the rectangle."""
        return Point(
            self._left_corner.x + self.width / 2,
            self._left_corner.y + self.height,
        )

    @property
    def east(self) -> Point:
        """Returns the east point of the rectangle."""
        return Point(
            self._left_corner.x + self.width,
            self._left_corner.y + self.height / 2,
        )

    @property
    def south(self) -> Point:
        """Returns the south point of the rectangle."""
        return Point(
            self._left_corner.x + self.width / 2,
            self._left_corner.y,
        )

    @property
    def west(self) -> Point:
        """Returns the west point of the rectangle."""
        return Point(
            self._left_corner.x,
            self._left_corner.y + self.height / 2,
        )

    @property
    def left_corner(self) -> Point:
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

    def shift(self, xshift: float, yshift: float) -> None:
        self._left_corner.shift(xshift, yshift)

    def scale(self, scale: float) -> None:
        self._left_corner.scale(scale)
        self.width = scale * self.width
        self.height = scale * self.height

    def rotate(
        self, angle: float, about_pt: Tuple[float, float], radians: bool = False
    ) -> None:
        self._left_corner.rotate(angle, about_pt, radians)


def rectangle_from_north(
    north_point: Union[Tuple[float, float], Point],
    width: float = 0,
    height: float = 0,
    options: str = "",
    action: str = "draw",
):
    """Create a Rectangle whose such that the .north attribute is north_point"""
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
    """Create a Rectangle whose such that the .east attribute is north_point"""
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
    """Create a Rectangle whose such that the .south attribute is north_point"""
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
    """Create a Rectangle whose such that the .west attribute is north_point"""
    west_point = Point(west_point)
    left_corner = Point(west_point.x, west_point.y - height / 2)
    return Rectangle(
        left_corner=left_corner,
        width=width,
        height=height,
        options=options,
        action=action,
    )
