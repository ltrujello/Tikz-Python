import subprocess
import webbrowser
import tempfile
import re

from pathlib import Path
from typing import List, Optional
from tikzpy.tikz_environments.scope import Scope
from tikzpy.tikz_environments.tikz_environment import TikzEnvironment
from tikzpy.tikz_environments.tikz_style import TikzStyle
from tikzpy.utils.helpers import (
    brackets,
    true_posix_path,
    extract_error_content,
)
from tikzpy.utils.types import CompileError
from tikzpy.templates.tex_file import TEX_FILE


class TikzPicture(TikzEnvironment):
    """
    A class for managing a Tikzpicture environment and associated tex files with tikz code.

    The TikzPicture class acts a canvas in which users can append drawings to.
    In the background, the TikzPicture manages the creation of
    the tikz code.

    Parameters:
        center: True/False if one wants to center their Tikz code
        options: A list of options for the Tikz picture
    """

    def __init__(
        self, center: bool = False, options: str = "", tikz_code_dir=None
    ) -> None:
        super().__init__(options)
        self._preamble = {}
        self._postamble = {}
        self.BASE_DIR = None

        if tikz_code_dir is not None:
            self.BASE_DIR = Path(tikz_code_dir)

        if center:
            self._preamble["center"] = "\\begin{center}\n"
            self._postamble["center"] = "\\end{center}\n"
        else:
            self._preamble["center"] = ""
            self._postamble["center"] = ""

    def code(self) -> str:
        """Returns a string contaning the generated Tikz code."""
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

    def write_tex_file(self, tex_filepath):
        tex_code = TEX_FILE
        tex_file_contents = re.sub("fillme", lambda x: self.code(), tex_code)
        # Update the TeX file
        if self.BASE_DIR is not None:
            tex_filepath = self.BASE_DIR / tex_filepath

        with open(tex_filepath, "w") as f:
            f.write(tex_file_contents)

    def write(self, tikz_code_filepath=None):
        if tikz_code_filepath is None:
            tikz_code_filepath = "tikz_code.tex"

        base_dir: Path = Path.cwd()
        if self.BASE_DIR is not None:
            base_dir = self.BASE_DIR

        tikz_code_filepath = base_dir / tikz_code_filepath
        with open(tikz_code_filepath, "w") as f:
            f.write(self.code())

    def compile(
        self, pdf_destination: Optional[str] = None, quiet: bool = True
    ) -> Path:
        """Compiles the Tikz code and returns a Path to the final PDF.
        If no file path is provided, a default value of "tex_file.pdf" will be used.

        Parameters:
            pdf_destination (str): The file path of the compiled pdf.
            quiet (bool): Parameter to silence latexmk.
        """
        with tempfile.TemporaryDirectory() as tmp_dir:
            tex_filepath = Path(tmp_dir) / "tex_file.tex"
            self.write_tex_file(tex_filepath)

            tex_file_posix_path = true_posix_path(tex_filepath)
            tex_file_parents = true_posix_path(tex_filepath.parent)
            options = ""
            if quiet:
                options += " -quiet "
            cmd = (
                f"latexmk -pdf {options} -output-directory={tex_file_parents} {tex_file_posix_path}",
            )
            completed_process = subprocess.run(cmd, shell=True, capture_output=True)
            if completed_process.returncode != 0:
                logfile = Path(tmp_dir) / "tex_file.log"
                if not logfile.exists():
                    raise CompileError(
                        f"Unexpected compilation error when running {cmd=}. No log file found. Manually compile the tikz code to debug."
                        f"{completed_process.stderr=}"
                    )
                # If there's a log file, try to extract the error from it
                # and return it to the user.
                error_content = extract_error_content(
                    logfile.read_text().splitlines(keepends=True)
                )
                if error_content is None:
                    raise CompileError(
                        f"Unexpected compilation error when running {cmd=}. Failed to parse log file. Manually compile the tikz code and check the .log file."
                        f"{completed_process.stderr=}"
                    )
                raise CompileError(error_content)

            # We move the compiled PDF into the same folder containing the tikz code.
            pdf_file = tex_filepath.with_suffix(".pdf").resolve()
            if pdf_destination is None:
                if self.BASE_DIR is None:
                    moved_pdf_file = Path.cwd() / pdf_file.name
                else:
                    moved_pdf_file = self.BASE_DIR / pdf_file.name
            else:
                moved_pdf_file = Path(pdf_destination)
            pdf_file.replace(moved_pdf_file)
            return moved_pdf_file.resolve()

    def show(self, quiet: bool = False) -> None:
        """Compiles the Tikz code and displays the pdf to the user. Set quiet=True to shut up latexmk.
        This should either open the PDF viewer on the user's computer with the graphic,
        or open the PDF in the user's browser.
        """
        pdf_file = self.compile(quiet=quiet)
        webbrowser.open_new(str(pdf_file.as_uri()))

    def scope(self, options: str = "") -> Scope:
        scope = Scope(options=options)
        self.draw(scope)
        return scope
