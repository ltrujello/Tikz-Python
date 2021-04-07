from copy import copy, deepcopy
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

    def __init__(self, position, options="", text=""):
        self.position = position
        self.text = text
        self.options = options

    @property
    def _command(self):
        return fr"at {self.position} {{ {self.text} }}"

    @property
    def code(self):
        return fr"\node{brackets(self.options)} {self._command};"

    def shift(self, xshift, yshift):
        self.position = shift_coords([self.position], xshift, yshift)[0]

    def scale(self, scale):
        self.position = scale_coords([self.position], scale)[0]

    def rotate(self, angle, about_pt, radians=False):
        self.position = rotate_coords([self.position], angle, about_pt, radians)[0]

    # TODO: test if this works
    def __deepcopy__(self, memo):
        """Creates a deep copy of a class object. This is useful since in our classes, we chose to set
        our methods to modify objects, but not return anything.
        """
        draw_obj = Node(
            deepcopy(self.position, memo),
            deepcopy(self.text, memo),
            deepcopy(self.options, memo),
        )
        memo[id(self)] = draw_obj
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