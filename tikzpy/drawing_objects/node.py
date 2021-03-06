from __future__ import annotations
from typing import Tuple
from copy import deepcopy
from tikzpy.utils.transformations import shift_coords, scale_coords, rotate_coords
from tikzpy.utils.helpers import brackets


# Class for Nodes
class Node:
    """
    A class to create nodes in the tikz environment.

    Attributes :
        position (tuple) : Pair of floats representing the location of the node
        text (str): Text that will be displayed with the node; can use dollar signs $ for LaTeX
        options (str) : String containing node options (e.g., "above")
    """

    def __init__(
        self, position: Tuple[float, float], options: str = "", text: str = ""
    ) -> None:
        self.position = position
        self.options = options
        self.text = text

    @property
    def _command(self) -> str:
        if self.position is not None:
            return fr"at {self.position} {{ {self.text} }}"
        else:
            return fr"{{ {self.text} }}"

    @property
    def code(self) -> str:
        return fr"\node{brackets(self.options)} {self._command};"

    def shift(self, xshift: float, yshift: float) -> None:
        if self.position is not None:
            self.position = shift_coords([self.position], xshift, yshift)[0]

    def scale(self, scale: float) -> None:
        if self.position is not None:
            self.position = scale_coords([self.position], scale)[0]

    def rotate(
        self, angle: float, about_pt: Tuple[float, float], radians: bool = False
    ) -> None:
        if self.position is not None:
            self.position = rotate_coords([self.position], angle, about_pt, radians)[0]

    def __deepcopy__(self, memo: dict) -> Node:  # TODO: Check this works
        """Creates a deep copy of a class object. This is useful since in our classes, we chose to set
        our methods to modify objects, but not return anything.
        """
        draw_obj = Node(
            deepcopy(self.position),
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
