from copy import copy, deepcopy
from tikz_py.utils import brackets


class _DrawingObject:
    """A generic class for our drawing objects to inherit properties from.
    This class serveees"""

    def __init__(self, action, options="", command=""):  # action is usually "draw"
        self.action = action
        self.options = options
        self.command = ""

    @property
    def code(self):
        """Full Tikz code for this drawing object."""
        return fr"\{self.action}{brackets(self.options)} {self._command}"

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