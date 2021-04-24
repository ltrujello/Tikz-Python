from __future__ import annotations
from typing import Tuple
from tikzpy.drawing_objects.drawing_object import DrawingObject
from tikzpy.utils.transformations import shift_coords, scale_coords, rotate_coords

# Class for Circles
class Circle(DrawingObject):
    """
    A class to create circles in the tikz environment.

    Attributes :
        position (tuple) : Pair of floats representing the center of the circle
        radius (float) : Length (in cm) of the radius
        options (str) : String containing the drawing options (e.g, "Blue")
    """

    def __init__(
        self,
        center: Tuple[float, float],
        radius: float,
        options: str = "",
        action: str = "draw",
    ) -> None:
        self.center = center
        self.radius = radius
        self.options = options
        super().__init__(action, self.options)

    @property
    def _command(self) -> str:
        return f"{self.center} circle ({self.radius}cm)"

    def shift(self, xshift: float, yshift: float) -> None:
        self.center = shift_coords([self.center], xshift, yshift)[0]

    def scale(self, scale: float) -> None:
        self.center = scale_coords([self.center], scale)[0]

    def rotate(
        self, angle: float, about_pt: Tuple[float, float], radians: bool = False
    ) -> None:
        self.center = rotate_coords([self.center], angle, about_pt, radians)[0]