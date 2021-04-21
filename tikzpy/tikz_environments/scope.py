from __future__ import annotations
from typing import List, Tuple
from tikzpy.drawing_objects.drawing_object import DrawingObject
from tikzpy.tikz_environments.clip import Clip
from tikzpy.utils.transformations import shift_coords, scale_coords, rotate_coords
from tikzpy.utils.helpers import brackets


class Scope:
    """A class to create a scope environment."""

    def __init__(self, options: str = "") -> None:
        self.options = options
        self._scope_statements: dict = {}

    @property
    def begin(self) -> str:
        return f"\\begin{{scope}}{brackets(self.options)}\n"

    @property
    def end(self) -> str:
        return "\\end{scope}\n"

    @property
    def scope_statements(self) -> dict:
        """A dictionary to keep track of the current scope statements.
        keys : instances of subclasses created (e.g, Line)
        values : the Tikz code of the instance (e.g., Line.code)
        This makes sure we reflect the changes to the drawing objects the user has made externally.
        """
        statement_dict = {}
        for draw_obj in self._scope_statements:
            statement_dict[draw_obj] = draw_obj.code
        return statement_dict

    @property
    def code(self) -> str:
        """A string contaning the statements in the scope."""
        code = self.begin
        for draw_obj in self.scope_statements:
            code += "\t" + draw_obj.code + "\n"
        code += self.end
        return code

    def __repr__(self) -> str:
        return self.code

    def remove(self, draw_obj: DrawingObject) -> None:
        """Remove a statement from the scope environment"""
        del self._scope_statements[draw_obj]

    def append(self, *args: List[DrawingObject]) -> None:
        """Append a drawing object to the scope statement"""
        for draw_obj in args:
            self._scope_statements[draw_obj] = draw_obj.code

    def clip(self, draw_obj: DrawingObject, draw: bool = False) -> None:
        """Clip a drawing object in the scope environment"""
        clip = Clip(draw_obj, draw=draw)
        self.append(clip)

    # TODO: Test if these three methods work.
    def shift(self, xshift: float, yshift: float) -> None:
        for draw_obj in self._scope_statements:
            draw_obj.shift(xshift, yshift)

    def scale(self, scale: float) -> None:
        for draw_obj in self._scope_statements:
            draw_obj.scale(scale)

    def rotate(
        self, angle: float, about_pt: Tuple[float, float], radians: bool = False
    ) -> None:
        for draw_obj in self._scope_statements:
            draw_obj.rotate(angle, about_pt, radians)