class TikzStyle:
    def __init__(self, style_name: str, style_settings: str) -> None:
        self.style_name = style_name
        self.style_settings = style_settings

    @property
    def code(self) -> str:
        return (
            f"\\tikzset{{ {self.style_name}/.style={{ {self.style_settings} }} \n }}\n"
        )

    def __repr__(self) -> str:
        return self.code
