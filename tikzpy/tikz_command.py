class TikzCommand:
    """A class to handle manually typed Tikz code. """

    def __init__(self, code):
        self.code = code

    def __repr__(self):
        return self.code
