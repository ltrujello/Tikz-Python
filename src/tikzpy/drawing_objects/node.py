from __future__ import annotations
from typing import Tuple, Union
from copy import deepcopy
from tikzpy.drawing_objects.point import Point
from tikzpy.utils.helpers import brackets


class Node:
    """
    A class to create nodes in the tikz environment.

    Attributes :
        position (tuple) : Pair of floats representing the location of the node
        text (str): Text that will be displayed with the node; can use dollar signs $ for LaTeX
        options (str) : String containing node options (e.g., "above")
    """

    def __init__(
        self,
        position: Union[Tuple[float, float], Point],
        options: str = "",
        text: str = "",
    ) -> None:
        self._position = Point(position) if position is not None else None
        self.options = options
        self.text = text

    @property
    def _command(self) -> str:
        if self.position is not None:
            return rf"at {self.position} {{ {self.text} }}"
        else:
            return rf"{{ {self.text} }}"

    @property
    def position(self):
        return self._position

    @position.setter
    def position(self, new_pos: Union[Tuple[float, float], Point]) -> None:
        if isinstance(new_pos, (tuple, Point)):
            self._position = Point(new_pos)
        else:
            raise TypeError(f"Invalid type '{type(new_pos)}' for node position")

    @property
    def code(self) -> str:
        return rf"\node{brackets(self.options)} {self._command};"

    def shift(self, xshift: float, yshift: float) -> None:
        if self._position is not None:
            self._position.shift(xshift, yshift)

    def scale(self, scale: float) -> None:
        if self._position is not None:
            self._position.scale(scale)

    def rotate(
        self, angle: float, about_pt: Tuple[float, float], radians: bool = False
    ) -> None:
        if self._position is not None:
            self._position.rotate(angle, about_pt, radians)

    def __deepcopy__(self, memo: dict) -> Node:  # TODO: Check this works
        """Creates a deep copy of a class object. This is useful since in our classes, we chose to set
        our methods to modify objects, but not return anything.
        """
        draw_obj = Node(
            deepcopy(self._position),
            deepcopy(self.options),
            deepcopy(self.text),
        )
        memo[id(self)] = draw_obj
        return draw_obj

    def copy(self, **kwargs: dict) -> Node:
        """Allows one to simultaneously make a (deep) copy of a drawing object and modify
        attributes of the drawing object in one step.
        """
        new_copy = deepcopy(self)
        for attr, val in kwargs.items():
            setattr(new_copy, attr, val)
        return new_copy

    def __repr__(self) -> str:
        return self.code
