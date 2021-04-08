from copy import copy, deepcopy
from tikzpy.utils.helpers import brackets
from tikzpy.drawing_objects.node import Node


class _DrawingObject:
    r"""A generic class for our drawing objects to inherit properties from.

    Attributes :
        action (str) : A string containing either "draw", "filldraw", "fill", or "path". This controls
                       the type of command statement we generate: \draw, \filldraw, \fill, or \path, ...
                       By default, it is draw.
        options (str) : A string of valid Tikz options for the drawing object.
        command (str) : A string consisting of the latter half of our tikz code to create the full statement.
        node (Node object) : A Node object which can be appended to the end of the statement.
    """

    def __init__(self, action="draw", options="", command=""):
        self.action = action
        self.options = options
        self.command = ""
        self.node = None

        if not isinstance(self.action, str):
            raise TypeError(f"The action argument {self.action} is not a string")

        if self.action.replace(" ", "") not in ["draw", "fill", "filldraw", "path"]:
            raise ValueError(
                f"The action {self.action} is not a valid action (draw, fill, filldraw, path). Perhaps you mispelled it."
            )

    @property
    def code(self):
        """Full Tikz code for this drawing object."""
        if self.node is None:
            return fr"\{self.action}{brackets(self.options)} {self._command};"
        else:
            return fr"\{self.action}{brackets(self.options)} {self._command} node{brackets(self.node.options)} {self.node._command};"

    # TODO: Allow one to not specify the position.
    def add_node(self, position=(0, 0), options="", text=""):
        """A method to build a node on a drawing object directly.
        This bypasses having to (1) define a Node object and then (2) use node.setter.
        """
        new_node = Node(position, options, text)
        self.node = new_node

    def __deepcopy__(self, memo):
        """Creates a deep copy of a class object. This is useful since in our classes, we chose to set
        our methods to modify objects, but not return anything.
        """
        print("Copied!")
        cls = self.__class__
        draw_obj = cls.__new__(cls)
        memo[id(self)] = draw_obj
        for attr, value in self.__dict__.items():
            setattr(draw_obj, attr, deepcopy(value, memo))
        return draw_obj

    def copy(self, **kwargs):
        """Allows one to simultaneously make a (deep) copy of a drawing object and modify
        attributes of the drawing object in one step.
        """
        new_copy = deepcopy(self)
        for attr, val in kwargs.items():
            setattr(new_copy, attr, val)
        return new_copy

    def __repr__(self):
        return self.code