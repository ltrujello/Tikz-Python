import subprocess
import webbrowser
import pkgutil
from pathlib import Path

from tikzpy.drawing_objects.line import Line
from tikzpy.drawing_objects.plotcoordinates import PlotCoordinates
from tikzpy.drawing_objects.circle import Circle
from tikzpy.drawing_objects.node import Node
from tikzpy.drawing_objects.rectangle import Rectangle
from tikzpy.drawing_objects.ellipse import Ellipse
from tikzpy.drawing_objects.arc import Arc

from tikzpy.tikz_environments.scope import Scope
from tikzpy.tikz_environments.tikz_command import TikzCommand
from tikzpy.tikz_environments.tikz_style import TikzStyle

from tikzpy.utils.helpers import brackets
from tikzpy.utils.helpers import true_posix_path

from tikzpy import NUM_TIKZS

""" NUM_TIKZS: records the number of TikZ environments created.

This global variable is the simplest solution to (1) avoiding making a TeX class 
and (2) designing deletion and update processes of files in such 
a way that even the most careless user will never delete anything 
important on their computer (e.g., a tex document).
"""

# TODO: Create a `clear` function which deletes all Tikz statements with an ID.
# TODO: Create an undo() method which removes the most recently added object.
class TikzPicture:
    """
    A class for a Tikz picture environment.

    Attributes:
        tikz_file (str) : A file path to a desired destination to output the tikz code
        center (bool) : True/False if one wants to center their Tikz code
        options (str) : A list of options for the Tikz picture
        statements (dict) : See docstring for statements below
    """

    def __init__(self, tikz_file="tikz_code/tikz-code.tex", center=False, options=""):
        global NUM_TIKZS
        # Create a Tikz Environment
        self.tikz_file = Path(tikz_file)
        self.options = options
        self._center = center
        self._statements = {}
        self._id = f"@TikzPy__#id__==__({NUM_TIKZS})"  # Cannot have spaces. We later scan and look for this string.
        self.preamble = {"begin_id": f"%__begin__{self._id}\n"}
        self.postamble = {"end_ind": f"%__end__{self._id}\n"}

        # Check if the tikz_file exists. If not, create it.
        if not self.tikz_file.is_file():
            try:
                with open(self.tikz_file.resolve(), "w"):
                    pass
            except:
                print(f"Could not find file at {self.tikz_file}.\n")
                answer = input("Want to make it? (Y/N) ")
                if answer.replace(" ", "") == "y" or answer.replace(" ", "") == "Y":
                    # Make directory, then file
                    self.tikz_file.parent.mkdir(parents=True)
                    with open(self.tikz_file.resolve(), "w+"):
                        pass
                    print(
                        f"File created at {str(self.tikz_file.resolve())}.\nThe tikz_code will output there. \n"
                    )
                else:
                    print("Not created. \n")

    @property
    def center(self):
        return self._center

    @center.setter
    def center(self, bool):
        self._center = bool
        self.center_code()

    def center_code(self):
        if self.center:
            self.preamble["center"] = "\\begin{center}\n"
            self.postamble["center"] = "\\end{center}\n"
        else:
            self.preamble["center"] = ""
            self.postamble["center"] = ""

    @property
    def begin(self):
        """The beginning code of our tikz environment.
        * For each environment we create, we assign an ID that our program can later identify.
          Such an ID is of the form of a TeX comment " % TikzPython id = ({self._id}) "
        * This is to ensure safe, efficient file update and deletion processes.
        """
        begin = []
        for statement in self.preamble.values():
            begin.append(statement)
        begin.append(f"\\begin{{tikzpicture}}{brackets(self.options)}\n")
        return begin

    @property
    def end(self):
        """ End statement for the TikzPicture."""
        end = ["\\end{tikzpicture}\n"]
        for statement in list(
            reversed(list(self.postamble.values()))
        ):  # To accommodate older pythons
            end.append(statement)
        return end

    @property
    def tex_file(self):
        r"""Takes care of the TeX file, containing necessary \usepackage{...} and \usetikzlibrary{...} statements,
        which is used to call the Tikz code and compile it.
        * The TeX file is stored in a folder "/tex", in the same directory as self.tikz_file.
            * This is to make everything easier for the user. They don't have to waste their time with the tedious task
              of sorting and connecting their files together, figuring out full paths, dealing with the stupid .aux, .log... files,
              figuring out \input{...}, etc. This process is automatic.
            * When a PDF compiles, the pdf is moved to the same directory as self.tikz_file
              so the user can see it. (All those moronic .log, .aux files are left behind in the folder,
              another benefit of this approach).
        """
        # Full paths for self.tikz_file and the tex_file
        tikz_file_dir = str(self.tikz_file.resolve().parents[0])
        # Full path for the tex_file
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
                    __name__, "../template/tex_file.tex"
                )
                f.write(template_file_bytes)
            with open(tex_file_path, "r") as f:
                lines = f.readlines()
            # Replace the "\\input{}"" line in tex_file.tex
            with open(tex_file_path, "w") as f:
                for line in lines:
                    if line == "\\input{fillme}\n":
                        f.write(
                            f"\\input{{{tikz_file_path_str}}}"
                        )  # This is what connects the Tikz code to our tex file
                    else:
                        f.write(line)
        return tex_file

    @property
    def statements(self):
        """A dictionary to keep track of the current Tikz code we've commanded. This is for the program.
        keys : instances of subclasses created (e.g, Line)
        values : the Tikz code of the instance (e.g., Line.code)
        This makes sure we reflect the changes to the drawing objects the user has made externally.
        """
        statement_dict = {}
        for draw_obj in self._statements:
            statement_dict[draw_obj] = draw_obj.code
        return statement_dict

    @property
    def code(self):
        """A string contaning our Tikz code. This uses self._statements, and self.code
        gets passed to __repr__.
        """
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

    def __repr__(self):
        """Return a readable string of the current tikz code"""
        readable_code = self.begin[-1]
        for draw_obj in self.statements:
            readable_code += "\t" + draw_obj.code + "\n"
        readable_code += self.end[0]
        return readable_code

    def remove(self, draw_obj):
        """A method to remove a code statement from the Tikz environment, e.g., a line."""
        del self._statements[draw_obj]

    def draw(self, *args):
        """User can also manually add their drawing object. """
        for draw_obj in args:
            self._statements[draw_obj] = draw_obj.code

    def add_command(self, tikz_statement):
        """Manually add a string of valid Tikz code into the Tikz environment."""
        command = TikzCommand(tikz_statement)
        self.draw(command)
        return command

    def tdplotsetmaincoords(self, theta, phi):
        """Specifies the viewing angle for 3D.
        theta: The angle (in degrees) through which the coordinate frame is rotated about the x axis.
        phi: The angle (in degrees) through which the coordinate frame is rotated about the z axis.
        """
        self.tdplotsetmaincoords = (theta, phi)
        if "tdplot_main_coords" not in self.options:
            self.options += "tdplot_main_coords"
        self.preamble[
            "tdplotsetmaincoords"
        ] = f"\\tdplotsetmaincoords{{{theta}}}{{{phi}}}\n"

    def tikzset(self, style_name, style_rules):
        style = TikzStyle(style_name, style_rules)
        self.preamble[f"tikz_style:{style_name}"] = style.code
        return style

    def add_styles(self, *styles):
        for style in styles:
            self.preamble[f"tikz_style:{style.style_name}"] = style.code

    def write(self, overwrite=True):
        """Our method to write the current recorded Tikz code into self.tikz_file, a .tex file somewhere.
        There are two main cases:
        A. This is our first time calling write().
            In this case, we just write into the file.
        B. We've already called .write() before, and we have a TikzPicture environment matching our current ID
        in self.tikz_file.
            In this case, we carefully delete the contents of the old TikzPicture environment. We do this
            by finding our ID. Then we update the environment with our new code.
        If we don't do (2), then we will potentially write duplicate TikzPicture code over and over again.
        Usually, a user won't want this. If for some weird reason they do want this, then they set
        overwrite = False.
        """
        global NUM_TIKZS  # Load in the global to update this variable, in the off chance overwrite = False.
        tikz_file_path = str(self.tikz_file.resolve())
        output_code = self.code

        # If we want to overwrite and update our last TikzPicture environment (in most cases, we do)
        if overwrite:
            begin_ind, end_ind = -1, -1
            # open the tikz_file and obtain its contents
            with open(tikz_file_path, "r") as tikz_file:
                lines = tikz_file.readlines()
            for i, line in enumerate(lines):
                """We look for our old TikzPicture code in the file as follows.
                * Loop over the file lines.
                * For each line, we check if it is our begin statement.
                * If so, we look ahead and search for our end statement.
                """
                if (
                    line.replace(" ", "") == self.begin[0]
                ):  # Search for start of code statement, we remove spaces for comparison
                    begin_ind = i
                    for j, later_lines in enumerate(lines[i:]):
                        if (
                            later_lines.replace(" ", "") == self.end[-1]
                        ):  # Search for end of code statement, we remove spaces for comparison
                            end_ind = i + j
                            break
                    break

            # If we found our begin statement, then we know we've written in the file before.
            if begin_ind != -1:
                assert (
                    end_ind != -1
                ), f"Found code statement at line {begin_ind}, but never found end statement"
                print("Updating Tikz environment with new code")

                # Transfer the text, excluding our old \begin{tikzpicture}\end{tikzpicture} statement.
                new_lines = lines[:begin_ind] + lines[end_ind + 1 :]

                # We create a new file with our desired file contents
                tikz_file_temp = Path(
                    str(self.tikz_file.parents[0])
                    + "/"
                    + self.tikz_file.stem
                    + "_temp.tex"
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
                    tikz_file.write(output_code)
                NUM_TIKZS += 1

        # If for some reason we do not want to overwrite our last TikzPicture
        else:
            with open(tikz_file_path, "a+") as tikz_file:
                tikz_file.write(output_code)
            NUM_TIKZS += 1

    # Display the current tikz drawing
    def show(self, quiet=False):
        """ Compiles the PDF and displays it to the user."""
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
        # We move the PDF up one directory, our of the hidden folder, so the viewer can see it.
        pdf_file = Path(tex_file_parents + "/" + self.tex_file.stem + ".pdf")
        pdf_file_path = str(
            pdf_file.resolve().parents[1] / pdf_file.name
        )  # Desired pdf file path
        pdf_file.rename(pdf_file_path)
        webbrowser.open_new("file://" + pdf_file_path)

    """
        Methods to code objects in the Tikz Environment
    """

    def line(
        self, start, end, options="", to_options="", control_pts=[], action="draw"
    ):
        """Draws a line by creating an instance of the Line class.
        Upon creation, we update self._statements with our new code.
        * Key feature: If we update any attributes of our line, the changes
          to the Tikz code are automatically reflected in self._statements.
        """
        line = Line(start, end, options, to_options, control_pts, action)
        self.draw(line)
        return line

    def plot_coordinates(self, points, options="", plot_options="", action="draw"):
        """Draws a plot coordinates statement by creating an instance of the PlotCoordinates class.
        Updates self._statements when necessary; see above comment under line function above.
        """
        plot = PlotCoordinates(points, options, plot_options, action)
        self.draw(plot)
        return plot

    def circle(self, center, radius, options="", action="draw"):
        """Draws a circle by creating an instance of the Circle class.
        Updates self._statements when necessary; see above comment under line function above.
        """
        circle = Circle(center, radius, options, action)
        self.draw(circle)
        return circle

    def node(self, position, options="", text=""):
        """Draws a node by creating an instance of the Node class.
        Updates self._statements when necessary; see above comment under line function above.
        """
        node = Node(position, options, text)
        self.draw(node)
        return node

    def rectangle(self, left_corner, right_corner, options="", action="draw"):
        """Draws a rectangle by creating an instance of the Rectangle class.
        Updates self._statements when necessary; see above comment under line function above.
        """
        rectangle = Rectangle(left_corner, right_corner, options, action)
        self.draw(rectangle)
        return rectangle

    def ellipse(self, center, horiz_axis, vert_axis, options="", action="draw"):
        """Draws an ellipse by creating an instance of the Ellipse class.
        Updates self._statements when necessary; see above comment under line function above.
        """
        ellipse = Ellipse(center, horiz_axis, vert_axis, options, action)
        self.draw(ellipse)
        return ellipse

    def arc(
        self,
        position,
        start_angle,
        end_angle,
        radius=None,
        x_radius=None,
        y_radius=None,
        options="",
        radians=False,
        draw_from_start=True,
        action="draw",
    ):
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

    def scope(self, options=""):
        scope = Scope(options)
        self.draw(scope)
        return scope