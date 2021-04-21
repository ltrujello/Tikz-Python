import subprocess
import webbrowser
import pkgutil
from pathlib import Path
from typing import List, Tuple
from tikzpy.drawing_objects.line import Line
from tikzpy.drawing_objects.plotcoordinates import PlotCoordinates
from tikzpy.drawing_objects.circle import Circle
from tikzpy.drawing_objects.node import Node
from tikzpy.drawing_objects.rectangle import Rectangle
from tikzpy.drawing_objects.ellipse import Ellipse
from tikzpy.drawing_objects.arc import Arc
from tikzpy.drawing_objects.drawing_object import DrawingObject
from tikzpy.tikz_environments.scope import Scope
from tikzpy.tikz_environments.tikz_command import TikzCommand
from tikzpy.tikz_environments.tikz_style import TikzStyle
from tikzpy.utils.helpers import brackets, true_posix_path


class TikzPicture:
    """
    A class for a Tikz picture environment.

    Attributes:
        tikz_file : A file path to a desired destination to output the tikz code
        center : True/False if one wants to center their Tikz code
        options : A list of options for the Tikz picture
        statements : See docstring for "statements" below
    """

    NUM_TIKZS = 0

    def __init__(self, center: bool = False, options: str = "") -> None:
        self.tikz_file: Path = Path("tikz_code/tikz_code.tex")
        self.options: str = options
        self._center: bool = center
        self._statements: dict = {}
        self._id: str = f"@TikzPy__#id__==__({self.NUM_TIKZS})"
        self._preamble: dict = {"begin_id": f"%__begin__{self._id}\n"}
        self._postamble: dict = {"end_ind": f"%__end__{self._id}\n"}

    @property
    def center(self) -> bool:
        return self._center

    @center.setter
    def center(self, centering) -> None:
        self._center = centering
        self.center_code()

    def center_code(self) -> None:
        if self.center:
            self._preamble["center"], self._postamble["center"] = (
                "\\begin{center}\n",
                "\\end{center}\n",
            )
        else:
            self._preamble["center"], self._postamble["center"] = "", ""

    @property
    def begin(self) -> list:
        """A list of strings containing the beginning code of our tikz environment.

        For each environment we assign an ID that our program can later identify.
        Such an ID is of the form of a TeX comment. This is to ensure safe, efficient file update and deletion processes.
        """
        begin = []
        for statement in self._preamble.values():
            begin.append(statement)
        begin.append(f"\\begin{{tikzpicture}}{brackets(self.options)}\n")
        return begin

    @property
    def end(self) -> list:
        """ A list of strings containing the ending code of our tikz environment."""
        end = ["\\end{tikzpicture}\n"]
        for statement in list(
            reversed(list(self._postamble.values()))
        ):  # To accommodate older pythons
            end.append(statement)
        return end

    @property
    def tex_file(self) -> Path:
        r"""A pathlib.Path object representing the path to our tex file, which
        contains our necessary \usepackage{...} and \usetikzlibrary{...} statements and is used for compiling.
        """
        # Full paths for self.tikz_file and the tex_file
        tikz_file_dir = str(self.tikz_file.resolve().parents[0])
        tex_file_path = tikz_file_dir + "/tex/tex_file.tex"
        tex_file = Path(tex_file_path)
        # Check if the TeX file exists
        if not tex_file.exists():
            tikz_file_path = self.tikz_file.resolve()
            tikz_file_path_str = true_posix_path(tikz_file_path)
            # Check if the folder exists
            if not tex_file.parents[0].exists():
                tex_file.parent.mkdir(parents=True)
            # The folder has been created. We now gather our template contents and write it into the new tex_file.tex
            with open(tex_file_path, "wb") as f:
                template_file_bytes = pkgutil.get_data(
                    "tikzpy", "templates/tex_file.tex"
                )
                f.write(template_file_bytes)
            with open(tex_file_path, "r") as f:
                lines = f.readlines()
            # Replace the "\\input{}"" line in tex_file.tex
            with open(tex_file_path, "w") as f:
                for line in lines:
                    if line == "\\input{fillme}\n":
                        # This is what connects the Tikz code to our tex file
                        f.write(f"\\input{{{tikz_file_path_str}}}")
                    else:
                        f.write(line)
        return tex_file

    @property
    def statements(self) -> dict:
        """A dictionary to keep track of the current Tikz code we've commanded. This is for the program.
        keys : instances of subclasses created (e.g, Line)
        values : the Tikz code of the instance (e.g., Line.code)
        """
        statement_dict = {}
        for draw_obj in self._statements:
            statement_dict[draw_obj] = draw_obj.code
        return statement_dict

    @property
    def code(self) -> str:
        """A string contaning our Tikz code."""
        code = ""
        # Add the beginning statement
        for stmt in self.begin:
            code += stmt
        # Add the main tikz code
        for draw_obj in self.statements:
            code += "\t" + draw_obj.code + "\n"
        # Add the ending statement
        for stmt in self.end:
            code += stmt
        return code

    def __repr__(self) -> str:
        """Return a readable string of the current tikz code"""
        readable_code = self.begin[-1]  # Only return \begin{tikzpicture}[...]
        for draw_obj in self.statements:
            readable_code += "\t" + draw_obj.code + "\n"
        readable_code += self.end[0]  # Only return \end{tikzpicture}
        return readable_code

    def remove(self, draw_obj: DrawingObject) -> None:
        """Remove a drawing_object from the Tikz environment, e.g., an instance of Line."""
        del self._statements[draw_obj]

    def draw(self, *args: List[DrawingObject]) -> None:
        """Add an arbitrary sequence of drawing objects. """
        for draw_obj in args:
            self._statements[draw_obj] = draw_obj.code

    def drawing_objects(self) -> list:
        """Returns a list of the currently appended drawing objects in the TikzPicture."""
        return list(self._statements.keys())

    def undo(self) -> None:
        """ Remove the last added drawing object from the tikz environment. """
        last_obj = list(self._statements.keys())[-1]
        self.remove(last_obj)

    def add_command(self, tikz_statement: str) -> TikzCommand:
        """Add a string of valid Tikz code into the Tikz environment."""
        command = TikzCommand(tikz_statement)
        self.draw(command)
        return command

    def tikzset(self, style_name: str, style_rules: TikzStyle) -> TikzStyle:
        """Create and add a TikzStyle object with name "style_name" and tikzset syntax "style_rules" """
        style = TikzStyle(style_name, style_rules)
        add_styles(style)
        return style

    def add_styles(self, *styles: List[TikzStyle]) -> None:
        """Add a TikzStyle object to the environment. """
        for style in styles:
            self._preamble[f"tikz_style:{style.style_name}"] = style.code

    def clear(self) -> None:
        """Clear the file contents of the file self.tikz_file.

        Specifically, the function scans the tikz_file for Tikz environments which are autogenerated by Tikz-Python (i.e.,
        those which have an ID) and deletes them. Other contents are left alone.
        """
        tikz_file_path = str(self.tikz_file.resolve())
        with open(tikz_file_path) as tikz_file:
            lines = tikz_file.readlines()

        new_lines = []
        i = 0
        while i < len(lines):
            line = lines[i]
            if line.replace(" ", "") == self.begin[0]:
                for j, later_lines in enumerate(lines[i:]):
                    if later_lines.replace(" ", "") == self.end[-1]:
                        k = i + j
                i = k + 1
            else:
                true_content = line.replace(" ", "").replace("\n", "")
                if len(true_content) != 0:
                    new_lines.append(line)
                i += 1

        with open(tikz_file_path, "w") as tikz_file:
            tikz_file.writelines(new_lines)

    def set_tdplotsetmaincoords(self, theta: float, phi: float) -> None:
        """Specify the viewing angle for 3D.

        theta: The angle (in degrees) through which the coordinate frame is rotated about the x axis.
        phi: The angle (in degrees) through which the coordinate frame is rotated about the z axis.
        """
        self.tdplotsetmaincoords = (theta, phi)
        if "tdplot_main_coords" not in self.options:
            self.options += "tdplot_main_coords"
        self._preamble[
            "tdplotsetmaincoords"
        ] = f"\\tdplotsetmaincoords{{{theta}}}{{{phi}}}\n"

    def write(self, overwrite: bool = True) -> None:
        """Write the currently recorded Tikz code into self.tikz_file.

        One might suspect that calling .write() twice will write down tikz source code twice. Since this is on
        average undesirable behavior, this is not the default behavior. Thus overwrite = True by default.
        If for some weird reason one wishes to literally write code twice, then they can set overwrite = False.
        """
        tikz_file_path = str(self.tikz_file.resolve())
        output_code = self.code

        # Check if the tikz_file exists. If not, create it.
        if not self.tikz_file.is_file():
            try:
                with open(tikz_file_path, "w"):
                    pass
            except:
                print(f"Could not find file at {self.tikz_file}.\n")
                answer = input("Want to make it? (Y/N) ")
                if answer.replace(" ", "") == "y" or answer.replace(" ", "") == "Y":
                    # Make directory, then file
                    self.tikz_file.parent.mkdir(parents=True)
                    with open(tikz_file_path, "wb") as f:
                        template_file_bytes = pkgutil.get_data(
                            "tikzpy", "templates/tikz_code.tex"
                        )
                        f.write(template_file_bytes)
                    print(
                        f"File created at {str(self.tikz_file.resolve())}.\nThe tikz_code will output there. \n"
                    )
                else:
                    print("Not created. \n")

        # If we want to overwrite and update our last TikzPicture environment (in most cases, we do)
        if overwrite:
            begin_ind, end_ind = -1, -1
            # open the tikz_file and obtain its contents
            with open(tikz_file_path) as tikz_file:
                lines = tikz_file.readlines()
            # We look for our old TikzPicture code in the file.
            for i, line in enumerate(lines):
                # Search for start of code statement, we remove spaces for comparison
                if line.replace(" ", "") == self.begin[0]:
                    begin_ind = i
                    for j, later_lines in enumerate(lines[i:]):
                        # Search for end of code statement. We remove spaces for comparison
                        if later_lines.replace(" ", "") == self.end[-1]:
                            end_ind = i + j
                            break
                    break

            # If we found our begin statement, then we know we've written in the file before.
            if begin_ind != -1:
                assert (
                    end_ind != -1
                ), f"Found code statement at line {begin_ind}, but never found end statement"
                print("Updating Tikz environment with new code")

                # We create a new file with our desired file contents
                new_lines = lines[:begin_ind] + lines[end_ind + 1 :]
                tikz_file_temp = Path(
                    str(self.tikz_file.parents[0]), self.tikz_file.stem + "_temp.tex"
                )
                tikz_file_temp_path = str(tikz_file_temp.resolve())
                with open(tikz_file_temp_path, "w") as f:
                    # Write everything before our begin statement
                    for line in lines[:begin_ind]:
                        f.write(line)
                    # Substitute in our updated code
                    f.write(output_code)
                    # Write everything after our end statement
                    for line in lines[end_ind + 1 :]:
                        f.write(line)
                # Now rename the file
                tikz_file_temp.replace(tikz_file_path)
                print("Successful write")

            # If we never found our old TikzPicture code, then it was never entered. We are safe to append.
            else:
                print("Adding new Tikz environment")
                with open(tikz_file_path, "a+") as tikz_file:
                    # Always guarantee Tikz-Python ID is on its own new line.
                    if self.NUM_TIKZS > 0:
                        last_char = self.tikz_file.read_text()[-1]
                        if last_char != "\n":
                            tikz_file.write("\n")
                    tikz_file.write(output_code)
                self.NUM_TIKZS += 1

        # If for some reason we do not want to overwrite our last TikzPicture
        else:
            with open(tikz_file_path, "a+") as tikz_file:
                tikz_file.write(output_code)
            self.NUM_TIKZS += 1

    def show(self, quiet: bool = False) -> None:
        """Compiles the PDF and displays it to the user.

        Set quiet=True to shut up latexmk, false otherwise.
        """
        tex_file_parents = true_posix_path(self.tex_file.resolve().parents[0])
        tex_filename = Path(tex_file_parents, self.tex_file.stem + ".tex")
        tex_file = true_posix_path(tex_filename)
        # We now compile the PDF
        if quiet:
            compile_cmd = (
                f"latexmk -pdf -quiet -output-directory={tex_file_parents} {tex_file}"
            )
        else:
            compile_cmd = (
                f"latexmk -pdf -output-directory={tex_file_parents} {tex_file}"
            )
        subprocess.run(compile_cmd, shell=True)
        # We move the compiled PDF up one directory, out of the tex/ folder, so the viewer can see it.
        pdf_file = Path(tex_file_parents, self.tex_file.stem + ".pdf")
        pdf_file_path = str(pdf_file.resolve().parents[1] / pdf_file.name)
        pdf_file.replace(pdf_file_path)
        webbrowser.open_new("file://" + pdf_file_path)

    """
        Methods to code objects in the Tikz Environment
    """

    def line(
        self,
        start: Tuple[float, float],
        end: Tuple[float, float],
        options: str = "",
        to_options: str = "",
        control_pts: list = [],
        action: str = "draw",
    ) -> Line:
        """Draws a line by creating an instance of the Line class.
        Upon creation, we update self._statements with our new code.
        * Key feature: If we update any attributes of our line, the changes
          to the Tikz code are automatically reflected in self._statements.
        """
        line = Line(start, end, options, to_options, control_pts, action)
        self.draw(line)
        return line

    def plot_coordinates(
        self,
        points: tuple,
        options: str = "",
        plot_options: str = "",
        action: str = "draw",
    ) -> PlotCoordinates:
        """Draws a plot coordinates statement by creating an instance of the PlotCoordinates class.
        Updates self._statements when necessary; see above comment under line function above.
        """
        plot = PlotCoordinates(points, options, plot_options, action)
        self.draw(plot)
        return plot

    def circle(
        self,
        center: Tuple[float, float],
        radius: float,
        options: str = "",
        action: str = "draw",
    ) -> Circle:
        """Draws a circle by creating an instance of the Circle class.
        Updates self._statements when necessary; see above comment under line function above.
        """
        circle = Circle(center, radius, options, action)
        self.draw(circle)
        return circle

    def node(
        self, position: Tuple[float, float], options: str = "", text: str = ""
    ) -> Node:
        """Draws a node by creating an instance of the Node class.
        Updates self._statements when necessary; see above comment under line function above.
        """
        node = Node(position, options, text)
        self.draw(node)
        return node

    def rectangle(
        self,
        left_corner: Tuple[float, float],
        right_corner: Tuple[float, float],
        options: str = "",
        action: str = "draw",
    ) -> Rectangle:
        """Draws a rectangle by creating an instance of the Rectangle class.
        Updates self._statements when necessary; see above comment under line function above.
        """
        rectangle = Rectangle(left_corner, right_corner, options, action)
        self.draw(rectangle)
        return rectangle

    def ellipse(
        self,
        center: Tuple[float, float],
        horiz_axis: float,
        vert_axis: float,
        options: str = "",
        action: str = "draw",
    ) -> Ellipse:
        """Draws an ellipse by creating an instance of the Ellipse class.
        Updates self._statements when necessary; see above comment under line function above.
        """
        ellipse = Ellipse(center, horiz_axis, vert_axis, options, action)
        self.draw(ellipse)
        return ellipse

    def arc(
        self,
        position: Tuple[float, float],
        start_angle: float,
        end_angle: float,
        radius: float = None,
        x_radius: float = None,
        y_radius: float = None,
        options: str = "",
        radians: bool = False,
        draw_from_start: bool = True,
        action: str = "draw",
    ) -> Arc:
        """Draws an arc by creating an instance of the Arc class.
        Updates self._statements when necessary; see above comment under line function above.
        """
        arc = Arc(
            position,
            start_angle,
            end_angle,
            radius,
            x_radius,
            y_radius,
            options,
            radians,
            draw_from_start,
            action,
        )
        self.draw(arc)
        return arc

    def scope(self, options: str = "") -> Scope:
        scope = Scope(options)
        self.draw(scope)
        return scope