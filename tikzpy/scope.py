from tikzpy.utils import brackets

# TODO: Test if this class works
class Scope:
    """A class to create a scope environment."""

    def __init__(self, options=""):
        self.options = ""
        self._scope_statements = {}

    @property
    def begin(self):
        return f"\\begin{{scope}}{brackets(self.options)}\n"

    @property
    def end(self):
        return "\\end{scope}\n"

    @property
    def scope_statements(self):
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
    def code(self):
        """A string contaning the statements in the scope."""
        code = self.begin
        for draw_obj in self.scope_statements:
            code += "\t" + draw_obj.code + "\n"
        code += self.end
        return code

    def __repr__(self):
        return self.code

    def remove(self, draw_obj):
        """Remove a statement from the scope environment"""
        del self._scope_statements[draw_obj]

    def append(self, *args):
        """Append a drawing object to the scope statement"""
        for draw_obj in args:
            self._scope_statements[draw_obj] = draw_obj.code

    def clip(self, draw_obj, draw=False):
        """Clip a drawing object in the scope environment"""
        clip = Clip(draw_obj, draw=draw)
        self.append(clip)

    # TODO: Test if these three methods work.
    def shift(self, xshift, yshift):
        for draw_obj in self._scope_statements:
            draw_obj.shift(xshift, yshift)

    def scale(self, scale):
        for draw_obj in self._scope_statements:
            draw_obj.scale(scale)

    def rotate(self, angle, about_pt, radians=False):
        for draw_obj in self._scope_statements:
            draw_obj.rotate(angle, about_pt, radians)