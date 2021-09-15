import subprocess
import webbrowser
import pkgutil
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
        _statements : See docstring for "statements" below
    """

    NUM_TIKZS = 0

    def __init__(self, center: bool = False, options: str = "") -> None:
        super().__init__(options)
        self._center = center
        self._id = f"@TikzPy__#id__==__({TikzPicture.NUM_TIKZS})"
        self._preamble = {"begin_id": f"%__begin__{self._id}\n"}
        self._postamble = {"end_id": f"%__end__{self._id}\n"}
        self.tikz_file = Path("tikz_code/tikz_code.tex")
        TikzPicture.NUM_TIKZS += 1
        self.center_code()

    @property
    def begin(self) -> list:
        """A list of strings containing the beginning of the code block for our tikz environment."""
        begin = []
        for statement in self._preamble.values():
            begin.append(statement)
        begin.append(f"\\begin{{tikzpicture}}{brackets(self.options)}\n")
        return begin

    @property
    def end(self) -> list:
        """A list of strings containing the end of the code block for our tikz environment."""
        end = ["\\end{tikzpicture}\n"]
        for statement in list(
            reversed(list(self._postamble.values()))
        ):  # To accommodate older pythons
            end.append(statement)
        return end

    @property
    def center(self) -> bool:
        return self._center

    @center.setter
    def center(self, centering: bool) -> None:
        self._center = centering
        self.center_code()

    def center_code(self) -> None:
        if self.center:
            print("Centering is true")
            self._preamble["center"], self._postamble["center"] = (
                "\\begin{center}\n",
                "\\end{center}\n",
            )
        else:
            self._preamble["center"], self._postamble["center"] = "", ""

    @property
    def tex_file(self) -> Path:
        r"""Returns a Path object representing the path to our tex file, which we create if it does not exist."""
        tex_file = self.tikz_file.parent / "tex" / "tex_file.tex"
        # Check if the TeX file exists
        if not tex_file.exists():
            # Check if the folder exists
            if not tex_file.parent.exists():
                tex_file.parent.mkdir(parents=True)
            # Gather the template contents
            tex_code = pkgutil.get_data("tikzpy", "templates/tex_file.tex").decode(
                "utf-8"
            )
        else:
            tex_code = tex_file.read_text()
        # Insert the file path to our tikz_file in the template
        tex_file_contents, num_matched = replace_code(
            "\\input{",
            "}",
            tex_code,
            "\\input{" + true_posix_path(self.tikz_file.resolve()) + "}",
        )
        assert num_matched == 1, f"Found {num_matched} many matches"
        # Update the TeX file
        with open(tex_file, "w") as f:
            f.write(tex_file_contents)
        return tex_file

    @property
    def code(self) -> str:
        """A string contaning our Tikz code."""
        code = ""
        # Add the beginning statement
        for stmt in self.begin:
            code += stmt
        # Add the main tikz code
        for draw_obj in self.statements:
            code += "    " + draw_obj.code + "\n"
        # Add the ending statement
        for stmt in self.end:
            code += stmt
        return code

    def __repr__(self) -> str:
        """Return a readable string of the current tikz code"""
        readable_code = self.begin[-1]  # Only return \begin{tikzpicture}[...]
        for draw_obj in self.statements:
            readable_code += "    " + draw_obj.code + "\n"
        readable_code += self.end[0]  # Only return \end{tikzpicture}
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

    def clear(self) -> None:
        """Clear the file contents of the file self.tikz_file.

        Specifically, the function scans the tikz_file for Tikz environments which are autogenerated by Tikz-Python (i.e.,
        those which have an ID) and deletes them. Other contents are left alone.
        """
        with open(self.tikz_file) as f:
            tikz_content = f.read()

        with open(self.tikz_file, "w") as f:
            cleared_content, _ = replace_code(
                self._preamble["begin_id"], self._postamble["end_id"], tikz_content, ""
            )
            f.write(cleared_content)

    def set_tdplotsetmaincoords(self, theta: float, phi: float) -> None:
        """Specify the viewing angle for 3D.

        theta: The angle (in degrees) through which the coordinate frame is rotated about the x axis.
        phi: The angle (in degrees) through which the coordinate frame is rotated about the z axis.
        """
        self.tdplotsetmaincoords = (theta, phi)
        self._preamble[
            "tdplotsetmaincoords"
        ] = f"\\tdplotsetmaincoords{{{theta}}}{{{phi}}}\n"

    def write(self) -> None:
        """Write the currently recorded Tikz code into self.tikz_file.

        One might suspect that calling .write() twice will write down tikz source code twice. Since this
        would make editing pictures very annoying, this is not the default behavior.
        """
        # Check if the tikz_file exists. If not, create it.
        if not self.tikz_file.exists():
            # Make directory, then file
            self.tikz_file.parent.mkdir(parents=True, exist_ok=True)
            # Get the template for new tikz code
            template_file_bytes = pkgutil.get_data("tikzpy", "templates/tikz_code.tex")
            with open(self.tikz_file, "wb") as f:
                f.write(template_file_bytes)
            print(
                f"File created at {str(self.tikz_file.resolve())}.\nThe tikz_code will output there. \n"
            )

        with open(self.tikz_file) as f:
            content = f.read()

        # Updates old code with new code, if any
        new_code, num_matches = replace_code(
            self._preamble["begin_id"],
            self._postamble["end_id"],
            content,
            self.code,
        )
        assert (
            num_matches <= 1
        ), f"# of Code blocks found is {num_matches} but should be 0 or 1"

        # If we found our previous code, then we know we've written in the file before.
        if num_matches == 1:
            print("Updating Tikz environment")
            # We create a temporary file with our updated tikz code
            tikz_file_temp = self.tikz_file.parent / (self.tikz_file.stem + "_temp.tex")
            with open(tikz_file_temp, "w") as f:
                f.write(new_code)
            # Success, so we now rename the file
            tikz_file_temp.replace(self.tikz_file)
            print("Successful write")
        # If we never found our old TikzPicture code, then it was never entered. We are safe to append.
        elif num_matches == 0:
            print("Adding new Tikz environment")
            with open(self.tikz_file, "a+") as f:
                # Always guarantee Tikz-Python ID is on its own new line.
                if len(self.tikz_file.read_text()) > 0:
                    last_char = self.tikz_file.read_text()[-1]
                    if last_char != "\n":
                        f.write("\n")
                f.write(self.code)

    def compile(self, quiet: bool = False) -> Path:
        """Compiles the Tikz code and returns a Path to the final PDF."""
        tex_file = true_posix_path(self.tex_file)
        tex_file_parents = true_posix_path(self.tex_file.parent)
        options = ""
        if quiet:
            options += " -quiet "
        subprocess.run(
            f"latexmk -pdf {options} -output-directory={tex_file_parents} {tex_file}",
            shell=True,
        )
        # We move the compiled PDF up one directory, out of the tex/ folder, so the viewer can see it.
        pdf_file = self.tex_file.with_suffix(".pdf").resolve()
        moved_pdf_file = pdf_file.replace(pdf_file.parents[1] / pdf_file.name)
        return moved_pdf_file

    def show(self, quiet: bool = False) -> None:
        """Compiles the Tikz code and displays the pdf to the user. Set quiet=True to shut up latexmk."""
        self.write()
        pdf_file = self.compile(quiet)
        webbrowser.open_new(str(pdf_file.as_uri()))

    def scope(self, options: str = "") -> Scope:
        scope = Scope(options=options)
        self.draw(scope)
        return scope
