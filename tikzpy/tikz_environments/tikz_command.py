class TikzCommand:
    """A class to handle manually typed Tikz code."""

    def __init__(self, code: str) -> None:
        self.code = code

    def __repr__(self) -> str:
        return self.code
