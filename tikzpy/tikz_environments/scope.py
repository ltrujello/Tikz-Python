from __future__ import annotations
from typing import Tuple
from tikzpy.drawing_objects.drawing_object import DrawingObject
from tikzpy.tikz_environments.tikz_environment import TikzEnvironment
from tikzpy.tikz_environments.clip import Clip
from tikzpy.utils.transformations import shift_coords, scale_coords, rotate_coords
from tikzpy.utils.helpers import brackets


class Scope(TikzEnvironment):
    """A class to create a scope environment."""

    def __init__(self, options: str = "") -> None:
        super().__init__(options)

    @property
    def begin(self) -> str:
        return f"\\begin{{scope}}{brackets(self.options)}\n"

    @property
    def end(self) -> str:
        return "\\end{scope}\n"

    @property
    def code(self) -> str:
        """A string contaning the statements in the scope."""
        code = self.begin
        for draw_obj in self.statements:
            code += "\t" + draw_obj.code + "\n"
        code += self.end
        return code

    def __repr__(self) -> str:
        return self.code

    def clip(self, draw_obj: DrawingObject, draw: bool = False) -> None:
        """Clip a drawing object in the scope environment"""
        clip = Clip(draw_obj, draw=draw)
        self.append(clip)

    def shift(self, xshift: float, yshift: float) -> None:
        for draw_obj in self._statements:
            draw_obj.shift(xshift, yshift)

    def scale(self, scale: float) -> None:
        for draw_obj in self._statements:
            draw_obj.scale(scale)

    def rotate(
        self, angle: float, about_pt: Tuple[float, float], radians: bool = False
    ) -> None:
        for draw_obj in self._statements:
            draw_obj.rotate(angle, about_pt, radians)