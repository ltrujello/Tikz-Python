from __future__ import annotations
from typing import Tuple
from tikzpy.drawing_objects.drawing_object import DrawingObject
from tikzpy.utils.transformations import shift_coords, scale_coords, rotate_coords


class Ellipse(DrawingObject):
    """
    A class to create ellipses in the tikz environment.

    Attributes :
        center (tuple) : Pair of floats representing the center of the ellipse
        x_axis (float): The length (in cm) of the horizontal axis of the ellipse
        y_axis (float): The length (in cm) of the vertical axis of the ellipse
    """

    def __init__(
        self,
        center: Tuple[float, float],
        x_axis: float,
        y_axis: float,
        options: str = "",
        action: str = "draw",
    ) -> None:

        self.center = center
        self.x_axis = x_axis
        self.y_axis = y_axis
        self.options = options
        super().__init__(action, self.options)

    @property
    def _command(self) -> str:
        return f"{self.center} ellipse ({self.x_axis}cm and {self.y_axis}cm)"

    def shift(self, xshift: float, yshift: float) -> None:
        self.center = shift_coords([self.center], xshift, yshift)[0]

    def scale(self, scale: float) -> None:
        scaled_center = scale_coords([self.center], scale)[0]
        scaled_h = self.x_axis * scale
        scaled_v = self.y_axis * scale

        self.center = scaled_center
        self.x_axis = scaled_h
        self.y_axis = scaled_v

    def rotate(
        self, angle: float, about_pt: Tuple[float, float], radians: bool = False
    ) -> None:
        self.center = rotate_coords([self.center], angle, about_pt, radians)[0]
