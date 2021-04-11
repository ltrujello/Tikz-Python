from __future__ import annotations
from tikzpy.drawing_objects.drawing_object import _DrawingObject
from tikzpy.utils.transformations import shift_coords, scale_coords, rotate_coords


class Rectangle(_DrawingObject):
    """
    A class to create rectangles in the tikz environment

    Attributes :
        left_corner (tuple) : Pair of floats representing the position of the bottom left corner
        right_corner (tuple) : Pair of floats representing the position of the upper right corner
        options (str) : String containing the drawing options, e.g, ("Blue")
    """

    def __init__(
        self,
        left_corner: tuple[float, float],
        right_corner: tuple[float, float],
        options: str = "",
        action: str = "draw",
    ) -> None:

        self.left_corner = left_corner
        self.right_corner = right_corner
        self.options = options
        super().__init__(action, self.options, self._command)

    @property
    def _command(self) -> str:
        return f"{self.left_corner} rectangle {self.right_corner}"

    def shift(self, xshift: float, yshift: float) -> None:
        shifted_corners = shift_coords(
            [self.left_corner, self.right_corner], xshift, yshift
        )
        self.left_corner = shifted_corners[0]
        self.right_corner = shifted_corners[1]

    def scale(self, scale: float) -> None:
        scaled_corners = scale_coords([self.left_corner, self.right_corner], scale)
        self.left_corner = scaled_corners[0]
        self.right_corner = scaled_corners[1]

    def rotate(
        self, angle: float, about_pt: tuple[float, float], radians: bool = False
    ) -> None:
        rotated_corners = rotate_coords(
            [self.left_corner, self.right_corner], angle, about_pt, radians
        )
        self.left_corner = rotated_corners[0]
        self.right_corner = rotated_corners[1]