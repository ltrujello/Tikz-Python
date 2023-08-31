import subprocess
import webbrowser
import pkgutil
import tempfile
import re
from pathlib import Path
from typing import List
from tikzpy.tikz_environments.scope import Scope
from tikzpy.tikz_environments.tikz_environment import TikzEnvironment
from tikzpy.tikz_environments.tikz_style import TikzStyle
from tikzpy.utils.helpers import brackets, true_posix_path, replace_code


class TikzPicture(TikzEnvironment):
    """
    A class for managing a Tikzpicture environment and associated tex files with tikz code.

    Attributes:
        tikz_file : A file path to the destination of the output tikz code
        center : True/False if one wants to center their Tikz code
        options : A list of options for the Tikz picture
        drawing_objects : List of DrawingObjects appened to curr tikz env
    """

    def __init__(
        self, center: bool = False, options: str = "", tikz_code_dir=None
    ) -> None:
        super().__init__(options)
        self._preamble = {}
        self._postamble = {}
        if tikz_code_dir is not None:
            self.BASE_DIR = Path(tikz_code_dir)
            self.tikz_file = self.BASE_DIR / Path("tikz_code.tex")
            self.tex_file = self.BASE_DIR / "tex" / "tex_file.tex"
        else:
            self.BASE_DIR = None
            self.tikz_file = None
            self.tex_file = None

        if center:
            self._preamble["center"] = "\\begin{center}\n"
            self._postamble["center"] = "\\end{center}\n"
        else:
            self._preamble["center"] = ""
            self._postamble["center"] = ""

    def code(self) -> str:
        """A string contaning our Tikz code."""
        code = ""
        # Add the beginning statement
        for stmt in self._preamble.values():
            code += stmt
        code += f"\\begin{{tikzpicture}}{brackets(self.options)}\n"

        # Add the main tikz code
        for draw_obj in self.drawing_objects:
            code += "    " + draw_obj.code + "\n"

        # Add the ending statement
        code += "\\end{tikzpicture}\n"
        for stmt in list(reversed(list(self._postamble.values()))):
            code += stmt
        return code

    def __repr__(self) -> str:
        """Return a readable string of the current tikz code"""
        readable_code = f"\\begin{{tikzpicture}}{brackets(self.options)}\n"

        for draw_obj in self.drawing_objects:
            readable_code += "    " + draw_obj.code + "\n"

        readable_code += "\\end{tikzpicture}\n"
        return readable_code

    def tikzset(self, style_name: str, style_rules: TikzStyle) -> TikzStyle:
        """Create and add a TikzStyle object with name "style_name" and tikzset syntax "style_rules" """
        style = TikzStyle(style_name, style_rules)
        self.add_styles(style)
        return style

    def add_styles(self, *styles: List[TikzStyle]) -> None:
        """Add a TikzStyle object to the environment."""
        for style in styles:
            self._preamble[f"tikz_style:{style.style_name}"] = style.code

    def set_tdplotsetmaincoords(self, theta: float, phi: float) -> None:
        """Specify the viewing angle for 3D.

        theta: The angle (in degrees) through which the coordinate frame is rotated about the x axis.
        phi: The angle (in degrees) through which the coordinate frame is rotated about the z axis.
        """
        self.tdplotsetmaincoords = (theta, phi)
        self._preamble[
            "tdplotsetmaincoords"
        ] = f"\\tdplotsetmaincoords{{{theta}}}{{{phi}}}\n"

    def save_tex_code(self, tex_filepath):
        tex_code = pkgutil.get_data("tikzpy", "templates/tex_file.tex").decode("utf-8")
        tex_file_contents = re.sub("fillme", lambda x: self.code(), tex_code)
        # Update the TeX file
        with open(tex_filepath, "w") as f:
            f.write(tex_file_contents)

    def compile(self, quiet: bool = True) -> Path:
        """Compiles the Tikz code and returns a Path to the final PDF."""
        with tempfile.TemporaryDirectory() as tmp_dir:
            tex_filepath = Path(tmp_dir) / "tex_file.tex"
            self.save_tex_code(tex_filepath)

            tex_file_posix_path = true_posix_path(tex_filepath)
            tex_file_parents = true_posix_path(tex_filepath.parent)
            options = ""
            if quiet:
                options += " -quiet "
            subprocess.run(
                f"latexmk -pdf {options} -output-directory={tex_file_parents} {tex_file_posix_path}",
                shell=True,
            )

            # We move the compiled PDF into the same folder containing the tikz code.
            pdf_file = tex_filepath.with_suffix(".pdf").resolve()
            if self.BASE_DIR is None:
                moved_pdf_file = Path.cwd() / pdf_file.name
            else:
                moved_pdf_file = self.BASE_DIR / pdf_file.name
            pdf_file.replace(moved_pdf_file)
            return moved_pdf_file.resolve()

    def show(self, quiet: bool = False) -> None:
        """Compiles the Tikz code and displays the pdf to the user. Set quiet=True to shut up latexmk."""
        pdf_file = self.compile(quiet)
        webbrowser.open_new(str(pdf_file.as_uri()))

    def scope(self, options: str = "") -> Scope:
        scope = Scope(options=options)
        self.draw(scope)
        return scope
