from tikz_py.drawing_object import _DrawingObject

# Class for Nodes
class Node(_DrawingObject):
    """
    A class to create lines in the tikz environment

    Attributes :
        position (tuple) : Pair of floats representing the location of the node
        text (str): Text that will be displayed with the node; can use dollar signs $ for LaTeX
        options (str) : String containing node options (e.g., "above")
    """

    def __init__(self, position, options="", text=""):
        self.position = position
        self.text = text
        self.options = options
        super().__init__("node", self.options, self._command)

    @property
    def _command(self):
        return fr"at {self.position} {{ {self.text} }};"

    def shift(self, xshift, yshift):
        self.position = shift_coords([self.position], xshift, yshift)[0]

    def scale(self, scale):
        self.position = scale_coords([self.position], scale)[0]

    def rotate(self, angle, about_pt, radians=False):
        self.position = rotate_coords([self.position], angle, about_pt, radians)[0]
