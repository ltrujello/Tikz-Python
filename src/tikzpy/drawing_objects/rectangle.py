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
        left_corner: Union[Tuple[float, float], Point] = Point(0, 0),
        right_corner: Union[Tuple[float, float], Point] = Point(0, 0),
        options: str = "",
        action: str = "draw",
    ) -> None:
        self._left_corner = Point(left_corner)
        self._right_corner = Point(right_corner)
        self.options = options
        super().__init__(action, self.options)

    @property
    def _command(self) -> str:
        return f"{self._left_corner} rectangle {self._right_corner}"

    @property
    def height(self) -> float:
        """Returns the height of the rectangle"""
        return abs(self._right_corner.y - self._left_corner.y)

    @property
    def width(self) -> float:
        """Returns the width of the rectangle"""
        return abs(self._right_corner.x - self._left_corner.x)

    @property
    def center(self):
        """Returns the center of the rectangle."""
        return Point(
            (self._left_corner.x + self._right_corner.x) / 2,
            (self._left_corner.y + self._right_corner.y) / 2,
        )

    @property
    def north(self):
        return self._right_corner - (self.width / 2, 0)

    @property
    def east(self):
        return self._right_corner - (0, self.height / 2)

    @property
    def south(self):
        return self._left_corner + (self.width / 2, 0)

    @property
    def west(self):
        return self._left_corner + (0, self.height / 2)

    @property
    def left_corner(self) -> Point:
        return self._left_corner

    @left_corner.setter
    def left_corner(self, new_corner) -> None:
        if isinstance(new_corner, (tuple, Point)):
            self._left_corner = Point(new_corner)
        else:
            raise TypeError(f"Invalid type '{type(new_corner)}' for left corner")

    @property
    def right_corner(self) -> Point:
        return self._right_corner

    @right_corner.setter
    def right_corner(self, new_corner) -> None:
        if isinstance(new_corner, (tuple, Point)):
            self._right_corner = Point(new_corner)
        else:
            raise TypeError(f"Invalid type '{type(new_corner)}' for right corner")

    def set_north(
        self,
        north_point: Union[Tuple[float, float], Point],
        height: float,
        width: float,
    ):
        """Set the left and right corners such that their .north attribute is north_point"""
        north_point = Point(north_point)
        self._left_corner = Point(north_point.x - width / 2, north_point.y - height)
        self._right_corner = Point(north_point.x + width / 2, north_point.y)
        return self

    def set_east(
        self,
        east_point: Union[Tuple[float, float], Point],
        height: float,
        width: float,
    ):
        """Set the left and right corners such that their .east attribute is east_point"""
        east_point = Point(east_point)
        self._left_corner = Point(east_point.x - width, east_point.y - height / 2)
        self._right_corner = Point(east_point.x, east_point.y + height / 2)
        return self

    def set_south(
        self,
        south_point: Union[Tuple[float, float], Point],
        height: float,
        width: float,
    ):
        """Set the left and right corners such that their .south attribute is south_point"""
        south_point = Point(south_point)
        self._left_corner = Point(south_point.x - width / 2, south_point.y)
        self._right_corner = Point(south_point.x + width / 2, south_point.y + height)
        return self

    def set_west(
        self,
        west_point: Union[Tuple[float, float], Point],
        height: float,
        width: float,
    ):
        """Set the left and right corners such that their .west attribute is west_point"""
        west_point = Point(west_point)
        self._left_corner = Point(west_point.x, west_point.y - height / 2)
        self._right_corner = Point(west_point.x + width, west_point.y + height / 2)
        return self

    def shift(self, xshift: float, yshift: float) -> None:
        self._left_corner.shift(xshift, yshift)
        self._right_corner.shift(xshift, yshift)

    def scale(self, scale: float) -> None:
        self._left_corner.scale(scale)
        self._right_corner.scale(scale)

    def rotate(
        self, angle: float, about_pt: Tuple[float, float], radians: bool = False
    ) -> None:
        self._left_corner.rotate(angle, about_pt, radians)
        self._right_corner.rotate(angle, about_pt, radians)
