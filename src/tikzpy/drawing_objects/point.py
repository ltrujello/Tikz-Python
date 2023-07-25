import math
from numbers import Number
from typing import Tuple, Union


class Point:
    """A class to handle points for TikzPy.
    It is designed to perform arithmetic with instances of itself and with Python tuples.
    The constructor accepts can either accept two numeric arguments, a single tuple of floats argument, or a
    single Point object.
    """

    def __init__(
        self,
        first_arg: Union[float, Number, tuple, "Point"],
        second_arg: Union[float, Number, tuple, "Point", None] = None,
    ) -> None:
        # Check if attempting to construct from one tuple of two numeric types
        if isinstance(first_arg, tuple) and second_arg is None:
            first_arg, second_arg = (
                first_arg[0],
                first_arg[1],
            )  # Careful, this must be a one linear
        # Check if attempting to construct from two numeric types
        if isinstance(first_arg, Number) and isinstance(second_arg, Number):
            self.x = first_arg
            self.y = second_arg
        # Check if attempting to construct from another Point object
        elif isinstance(first_arg, Point) and second_arg is None:
            self.x = first_arg.x
            self.y = first_arg.y
        else:
            raise TypeError(
                f"Invalid non-numeric types {type(first_arg)}, {type(second_arg)} supplied to Point class "
            )

    def shift(self, xshift: float, yshift: float) -> None:
        """Translate the point via x, y offsets."""
        self.x += xshift
        self.y += yshift

    def scale(self, scale: float) -> None:
        """Scale the point given the scale."""
        self.x *= scale
        self.y *= scale

    def rotate(
        self,
        angle: float,
        about_pt: Union[Tuple[float, float], "Point"],
        radians: bool = False,
    ) -> None:
        """Rotate the point about another point."""
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

    def to_tuple(self) -> Tuple:
        """Return a tuple of the x, y data."""
        return self.x, self.y

    def __iter__(self):
        return iter((self.x, self.y))

    def __add__(self, other) -> "Point":
        """Allow Point + tuple and Point + Point arithmetic."""
        if isinstance(other, tuple):
            x, y = other
        elif isinstance(other, Point):
            x, y = other.x, other.y
        else:
            raise TypeError(f"Cannot perform Point object addition with {other} ")
        return Point(self.x + x, self.y + y)

    def __radd__(self, other) -> "Point":
        """Allow tuple + Point arithmetic."""
        if isinstance(other, tuple):
            x, y = other
        elif isinstance(other, Point):
            x, y = other.x, other.y
        else:
            raise TypeError(f"Cannot perform Point object addition with {other} ")
        return Point(self.x + x, self.y + y)

    def __sub__(self, other):
        """Allow tuple + Point arithmetic."""
        if isinstance(other, tuple):
            x, y = other
        elif isinstance(other, Point):
            x, y = other.x, other.y
        else:
            raise TypeError(f"Cannot perform Point object addition with {other} ")
        return Point(self.x - x, self.y - y)

    def __rsub__(self, other):
        return other + (-1) * self

    def __mul__(self, scale: Number) -> "Point":
        """Allow Point * Number arithmetic."""
        if not isinstance(scale, Number):
            raise TypeError(
                f"Unsupported * between Point object and {scale} of type {type(scale)} (must be numeric)"
            )
        return Point(self.x * scale, self.y * scale)

    def __rmul__(self, scale: float) -> "Point":
        """Allow Number * Point arithmetic."""
        if not isinstance(scale, Number):
            raise TypeError(
                f"Unsupported * between {scale} of type {type(scale)} and Point object (must be numeric)"
            )
        return Point(scale * self.x, scale * self.y)

    def __truediv__(self, scale) -> "Point":
        """Allow Point / Number arithmetic."""
        if not isinstance(scale, Number):
            raise TypeError(
                f"Unsupported / between Point object and {scale} of type {type(scale)}."
            )
        return Point(self.x / scale, self.y / scale)

    def __str__(self):
        return f"({self.x}, {self.y})"

    def __repr__(self):
        return f"Point({self.x}, {self.y})"
