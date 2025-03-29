from __future__ import annotations
from abc import ABC, abstractmethod
from typing import Tuple
from copy import deepcopy
from tikzpy.utils.helpers import brackets
from tikzpy.drawing_objects.node import Node


class DrawingObject(ABC):
    r"""A generic class for our drawing objects to inherit properties from.

    Attributes :
        action (str) : A string containing either "draw", "filldraw", "fill", or "path". This controls
                       the type of command statement we generate: \draw, \filldraw, \fill, or \path, ...
                       By default, it is draw.
        options (str) : A string of valid Tikz options for the drawing object.
        command (str) : A string consisting of the latter half of our tikz code to create the full statement.
        node (Node object) : A Node object which can be appended to the end of the statement.
    """

    def __init__(self, action: str = "draw", options: str = "") -> None:
        self.action = action
        self.options = options
        self.node: Node = None

        if not isinstance(self.action, str):
            raise TypeError(f"The action argument {self.action} is not of type str")

        if self.action.replace(" ", "") not in ["draw", "fill", "filldraw", "path"]:
            raise ValueError(
                f"The action {self.action} is not a valid action ('draw', 'fill', 'filldraw', 'path'). Perhaps you mispelled it."
            )

    @property
    @abstractmethod
    def _command(self) -> str:
        r"""The latter half of the Tikz Code for the drawing object.
        E.g.: For a Line with code "\draw (0,0) to (1,1), _command corresponds to "(0,0) to (1,1)".
        """

    @abstractmethod
    def shift(self, xshift: float, yshift: float) -> "DrawingObject":
        """Shift the coordinates of the drawing object by (xshift, yshift)"""

    @abstractmethod
    def scale(self, scale: float) -> "DrawingObject":
        """Scale the coordinates of the drawing object by amount "scale"."""

    @abstractmethod
    def rotate(
        self, angle: float, about_pt: Tuple[float, float] = None, radians: bool = False
    ) -> "DrawingObject":
        """Rotate the coordinates of the drawing object (counterclockwise) by "angle" about the
        point "about_pt".
        """

    @property
    def code(self) -> str:
        """Full Tikz code for this drawing object."""
        draw_cmd = f"\\{self.action}{brackets(self.options)} {self._command}"
        if self.node is None:
            return f"{draw_cmd};"
        else:
            return f"{draw_cmd} node{brackets(self.node.options)} {self.node._command};"

    def add_node(
        self, position: tuple = None, options: str = "", text: str = ""
    ) -> None:
        """A method to build a node on a drawing object directly.
        This bypasses having to (1) define a Node object and then (2) use node.setter.
        """
        new_node = Node(position, options, text)
        self.node = new_node

    def __deepcopy__(self, memo: dict) -> DrawingObject:
        """Creates a deep copy of a class object. This is useful since in our classes, we chose to set
        our methods to modify objects, but not return anything.
        """
        cls = self.__class__
        draw_obj = cls.__new__(cls)
        memo[id(self)] = draw_obj
        for attr, value in self.__dict__.items():
            setattr(draw_obj, attr, deepcopy(value, memo))
        return draw_obj

    def copy(self, **kwargs: dict) -> DrawingObject:
        """Allows one to simultaneously make a (deep) copy of a drawing object and modify
        attributes of the drawing object in one step.
        """
        new_copy = deepcopy(self)
        for attr, val in kwargs.items():
            setattr(new_copy, attr, val)
        return new_copy

    def __repr__(self) -> str:
        return self.code
