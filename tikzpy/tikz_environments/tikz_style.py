class TikzStyle:
    def __init__(self, style_name, style_settings):
        self.style_name = style_name
        self.style_settings = style_settings

    @property
    def code(self):
        return (
            f"\\tikzset{{ {self.style_name}/.style={{ {self.style_settings} }} \n }}\n"
        )

    def __repr__(self):
        return self.code
