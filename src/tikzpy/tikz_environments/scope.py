from __future__ import annotations
from typing import Tuple
from tikzpy.drawing_objects.drawing_object import DrawingObject
from tikzpy.tikz_environments.tikz_environment import TikzEnvironment
from tikzpy.tikz_environments.clip import Clip
from tikzpy.utils.helpers import brackets


class Scope(TikzEnvironment):
    r"""A class to create a scope environment.

    The `Scope` class is meant to handle the `scope` environment in TikZ.
    Scoping is useful as it can be used to nest a set of commands in a TikZ picture, or it can be used in conjunction with the TikZ `clip` command to "clip out" drawings.

    This class is analagous to the TikZ command
    ```
    \begin{scope}
        ...
    \end{scope}
    ```
    """

    def __init__(self, options: str = "") -> None:
        super().__init__(options)

    @property
    def code(self) -> str:
        """A string contaning the drawing_objects in the scope."""
        code = f"\\begin{{scope}}{brackets(self.options)}\n"
        for draw_obj in self.drawing_objects:
            code += "\t" + draw_obj.code + "\n"
        code += "\\end{scope}\n"
        return code

    def __repr__(self) -> str:
        return self.code

    def append(self, *args: List[DrawingObject]) -> None:
        """Append a drawing object to the scope statement"""
        for draw_obj in args:
            self.drawing_objects.append(draw_obj)

    def clip(self, draw_obj: DrawingObject, draw: bool = False) -> None:
        """Clip a drawing object in the scope environment"""
        clip = Clip(draw_obj, draw=draw)
        self.draw(clip)

    def shift(self, xshift: float, yshift: float) -> None:
        for draw_obj in self.drawing_objects:
            draw_obj.shift(xshift, yshift)

    def scale(self, scale: float) -> None:
        for draw_obj in self.drawing_objects:
            draw_obj.scale(scale)

    def rotate(
        self, angle: float, about_pt: Tuple[float, float], radians: bool = False
    ) -> None:
        for draw_obj in self.drawing_objects:
            draw_obj.rotate(angle, about_pt, radians)
