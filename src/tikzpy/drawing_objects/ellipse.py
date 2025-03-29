from __future__ import annotations
from typing import Tuple, Union
from tikzpy.drawing_objects.point import Point
from tikzpy.drawing_objects.drawing_object import DrawingObject


class Ellipse(DrawingObject):
    r"""
    A class to create ellipses in the tikz environment.

    The ellipse class handles ellipses in Tikz. It it analagous to the Tikz command
    ```
    \draw[options] <center> ellipse (<x_radius> and <y_radius>);
    ```

    Parameters:
        center: Position of the center of the ellipse
        x_axis: The length (in cm) of the horizontal axis of the ellipse
        y_axis: The length (in cm) of the vertical axis of the ellipse
        options: TikZ options to draw with
        action: The type of TikZ action to use. Default is "draw"
    """

    def __init__(
        self,
        center: Union[Tuple[float, float], Point],
        x_axis: float,
        y_axis: float,
        options: str = "",
        action: str = "draw",
    ) -> None:
        self._center = Point(center)
        self.x_axis = x_axis
        self.y_axis = y_axis
        self.options = options
        super().__init__(action, self.options)

    @property
    def center(self):
        return self._center

    @center.setter
    def center(self, new_center: Union[tuple, Point]) -> None:
        if isinstance(new_center, (tuple, Point)):
            self._center = Point(new_center)
        else:
            raise TypeError(f"Invalid type '{type(new_center)}' for center")

    @property
    def north(self) -> Point:
        """Returns the north point of the ellipse."""
        return self._center + (0, self.y_axis)

    @property
    def east(self) -> Point:
        """Returns the east point of the ellipse."""
        return self._center + (self.x_axis, 0)

    @property
    def south(self) -> Point:
        """Returns the south point of the ellipse."""
        return self._center - (0, self.y_axis)

    @property
    def west(self) -> Point:
        """Returns the west point of the ellipse."""
        return self._center - (self.x_axis, 0)

    @property
    def _command(self) -> str:
        return f"{self.center} ellipse ({self.x_axis}cm and {self.y_axis}cm)"

    def shift_(self, xshift: float, yshift: float) -> None:
        self._center.shift_(xshift, yshift)

    def scale_(self, scale: float) -> None:
        self._center.scale_(scale)
        self.x_axis *= scale
        self.y_axis *= scale

    def rotate_(
        self, angle: float, about_pt: Tuple[float, float], radians: bool = False
    ) -> None:
        self._center.rotate_(angle, about_pt, radians)

    def shift(self, xshift: float, yshift: float) -> "Ellipse":
        new_ellipse = self.copy()
        new_ellipse.shift_(xshift, yshift)
        return new_ellipse

    def scale(self, scale: float) -> "Ellipse":
        new_ellipse = self.copy()
        new_ellipse.scale_(scale)
        return new_ellipse

    def rotate(
        self, angle: float, about_pt: Tuple[float, float], radians: bool = False
    ) -> "Ellipse":
        new_ellipse = self.copy()
        new_ellipse.rotate_(angle, about_pt, radians)
        return new_ellipse
