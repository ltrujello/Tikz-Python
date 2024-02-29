from __future__ import annotations
from typing import Tuple
from tikzpy.drawing_objects.line import Line
from tikzpy.drawing_objects.plotcoordinates import PlotCoordinates
from tikzpy.drawing_objects.circle import Circle
from tikzpy.drawing_objects.node import Node
from tikzpy.drawing_objects.rectangle import Rectangle
from tikzpy.drawing_objects.ellipse import Ellipse
from tikzpy.drawing_objects.arc import Arc
from tikzpy.drawing_objects.drawing_object import DrawingObject


class Clip:
    r"""A class for a clipping code statement.

    This class is used to clip a single drawing object draw_obj.
    It is meant to be used in conjunction with the Scope class.
    It is analagous to the tikz code

    ```
    \clip ... # some drawing object
    ```
    """

    def __init__(self, draw_obj: DrawingObject, draw: bool = False) -> None:
        if isinstance(
            draw_obj, (Line, PlotCoordinates, Circle, Node, Rectangle, Ellipse, Arc)
        ):
            self.draw_obj = draw_obj
            self.draw = draw
        else:
            raise TypeError(
                f"Clip argument {draw_obj} must be an instance of a drawing class."
            )

    @property
    def code(self) -> str:
        if self.draw:
            return rf"\clip[preaction = {{draw, {self.draw_obj.options}}}] {self.draw_obj._command};"
        else:
            return rf"\clip {self.draw_obj._command};"

    def shift(self, xshift: float, yshift: float) -> None:
        self.draw_obj.shift(xshift, yshift)

    def scale(self, scale: float) -> None:
        self.draw_obj.scale(scale)

    def rotate(
        self, angle: float, about_pt: Tuple[float, float], radians: bool = False
    ) -> None:
        self.draw_obj.rotate(angle, about_pt, radians)
