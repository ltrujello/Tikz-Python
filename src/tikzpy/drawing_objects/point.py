import math
import copy
from numbers import Number
from typing import Tuple, Union, Optional


class Point:
    """A class to handle points for TikzPy.

    The Point class is how TikzPy handles coordinates. All drawing objects, like Line and Circle,
    use the Point class under the hood.

    The Point class is designed to perform arithmetic with instances of itself and with Python tuples.
    The constructor accepts can either accept two numeric arguments, a single tuple of floats argument, or a
    single Point object.

    Parameters:
        first_arg: A number, a tuple, or Point object.
        second_arg: A number, in the case of a 2D point, or None.
        third_arg: A number, in the case of a 3D point, or None.
    """

    def __init__(
        self,
        first_arg: Union[float, Number, tuple, "Point"],
        second_arg: Union[float, Number, None] = None,
        third_arg: Union[float, Number, None] = None,
    ) -> None:
        # Check if attempting to construct from one tuple of two numeric types
        if isinstance(first_arg, tuple) and second_arg is None:
            if len(first_arg) == 2:
                self.x, self.y = (
                    first_arg[0],
                    first_arg[1],
                )
                self.z = None
            elif len(first_arg) == 3:
                self.x, self.y, self.z = (first_arg[0], first_arg[1], first_arg[2])
            else:
                raise ValueError(
                    f"Recieved invalid tuple={first_arg} to Point constructor"
                )

        elif isinstance(first_arg, Point) and second_arg is None:
            self.x = first_arg.x
            self.y = first_arg.y
            self.z = None
            if first_arg.z is not None:
                self.z = first_arg.z

        elif second_arg is not None:
            self.x = first_arg
            self.y = second_arg
            self.z = None
            if third_arg is not None:
                self.z = third_arg
        else:
            raise TypeError(
                f"Invalid non-numeric types {type(first_arg)}, {type(second_arg)} supplied to Point class "
            )

    def distance(self, other_point):
        """
        Calculates the distance between two points.
        """
        if self.z is not None and other_point.z is not None:
            return math.sqrt(
                (self.x - other_point.x) ** 2 +
                (self.y - other_point.y) ** 2 +
                (self.z - other_point.z) ** 2
            )
        else:
            return math.sqrt(
                (self.x - other_point.x) ** 2 +
                (self.y - other_point.y) ** 2
            )

    def copy(self):
        return Point((self.x, self.y, self.z))

    def shift_(
        self, xshift: float, yshift: float, zshift: Optional[float] = None
    ) -> None:
        """Translate the point via x, y offsets. This performs an in-place operation."""
        self.x = self.x + xshift
        self.y = self.y + yshift
        if zshift is not None and zshift is not None:
            self.z = self.z + zshift

    def scale_(self, scale: float) -> None:
        """Scale the point given the scale. This performs an in-place operation."""
        self.x = self.x * scale
        self.y = self.y * scale
        if self.z is not None:
            self.z = self.z * scale

    def rotate_(
        self,
        angle: float,
        about_pt: Union[Tuple[float, float], "Point"],
        radians: bool = False,
    ) -> None:
        """Rotate the point about another point. This performs an in-place operation."""
        if self.z is not None:
            print("Warning: Rotate method for 3D points not yet implemented")
        about_pt = Point(about_pt)
        if not radians:
            angle *= math.pi / 180

        # Shift by about_pt, so that rotation is now relative to that point
        x = self.x - about_pt.x
        y = self.y - about_pt.y

        # Rotate the points
        rotated_x = x * math.cos(angle) - y * math.sin(angle)
        rotated_y = x * math.sin(angle) + y * math.cos(angle)

        # Shift them back by about_pt, truncate the decimal places
        rotated_x += about_pt.x
        rotated_y += about_pt.y

        self.x = rotated_x
        self.y = rotated_y


    def shift(
        self, xshift: float, yshift: float, zshift: Optional[float] = None
    ) -> "Point":
        """Returns a point translated by x, y, z offsets."""
        new_point = self.copy()
        new_point.shift_(xshift, yshift, zshift)
        return new_point

    def scale(self, scale: float) -> "Point":
        """Returns a point scaled by the given scale."""
        new_point = self.copy()
        new_point.scale_(scale)
        return new_point

    def rotate(
        self,
        angle: float,
        about_pt: Union[Tuple[float, float], "Point"],
        radians: bool = False,
    ) -> "Point":
        """Returns a point that is rotated about another point. """
        new_point = self.copy()
        new_point.rotate_(angle, about_pt, radians)
        return new_point

    def to_tuple(self) -> Tuple:
        """Return a tuple of the x, y data."""
        if self.z is None:
            return self.x, self.y
        return self.x, self.y, self.z

    def __iter__(self):
        if self.z is None:
            return iter((self.x, self.y))
        return iter((self.x, self.y, self.z))

    def __add__(self, other) -> "Point":
        if self.z is None:
            if isinstance(other, tuple):
                x, y = other
            elif isinstance(other, Point):
                x, y = other.x, other.y
            else:
                raise TypeError(f"Cannot perform Point object addition with {other} ")
            return Point(self.x + x, self.y + y)

        if isinstance(other, tuple):
            x, y, z = other
        elif isinstance(other, Point):
            x, y, z = other.x, other.y, other.z
        else:
            raise TypeError(f"Cannot perform Point object addition with {other} ")
        return Point(self.x + x, self.y + y, self.z + z)

    def __radd__(self, other) -> "Point":
        if self.z is None:
            if isinstance(other, tuple):
                x, y = other
            elif isinstance(other, Point):
                x, y = other.x, other.y
            else:
                raise TypeError(f"Cannot perform Point object addition with {other} ")
            return Point(self.x + x, self.y + y)

        if isinstance(other, tuple):
            x, y, z = other
        elif isinstance(other, Point):
            x, y, z = other.x, other.y, other.z
        else:
            raise TypeError(f"Cannot perform Point object addition with {other} ")
        return Point(self.x + x, self.y + y, self.z + z)

    def __sub__(self, other):
        if self.z is None:
            if isinstance(other, tuple):
                x, y = other
            elif isinstance(other, Point):
                x, y = other.x, other.y
            else:
                raise TypeError(
                    f"Cannot perform Point object subtraction with {other} "
                )
            return Point(self.x - x, self.y - y)

        if isinstance(other, tuple):
            x, y, z = other
        elif isinstance(other, Point):
            x, y, z = other.x, other.y, other.z
        else:
            raise TypeError(f"Cannot perform Point object subtraction with {other} ")
        return Point(self.x - x, self.y - y, self.z - z)

    def __rsub__(self, other):
        return other + (-1) * self

    def __mul__(self, scale: Number) -> "Point":
        if not isinstance(scale, Number):
            raise TypeError(
                f"Unsupported * between Point object and {scale} of type {type(scale)} (must be numeric)"
            )
        if self.z is None:
            return Point(self.x * scale, self.y * scale)
        return Point(self.x * scale, self.y * scale, self.z * scale)

    def __rmul__(self, scale: float) -> "Point":
        if not isinstance(scale, Number):
            raise TypeError(
                f"Unsupported * between {scale} of type {type(scale)} and Point object (must be numeric)"
            )
        if self.z is None:
            return Point(scale * self.x, scale * self.y)
        return Point(scale * self.x, scale * self.y, scale * self.z)

    def __truediv__(self, scale) -> "Point":
        if not isinstance(scale, Number):
            raise TypeError(
                f"Unsupported / between Point object and {scale} of type {type(scale)}."
            )
        if self.z is None:
            return Point(self.x / scale, self.y / scale)
        return Point(self.x / scale, self.y / scale, self.z / scale)

    def __str__(self):
        if self.z is None:
            return f"({self.x}, {self.y})"

        return f"({self.x}, {self.y}, {self.z})"

    def __repr__(self):
        if self.z is None:
            return f"Point({self.x}, {self.y})"

        return f"Point({self.x}, {self.y}, {self.z})"

    def __eq__(self, other):
        if isinstance(other, Point):
            return self.x == other.x and self.y == other.y and self.z == other.z
        return False
