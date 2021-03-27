#!/usr/bin/env python3
import math
import subprocess
import webbrowser
from pathlib import Path
from copy import copy, deepcopy

""" _N_TIKZs: records the number of TikZ environments created.

This global variable is the simplest solution to (1) avoiding making a TeX class 
and (2) designing deletion and update processes of files in such 
a way that even the most careless user will never delete anything 
important on their computer (e.g., a tex document).
"""

_N_TIKZs = 0


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
        global _N_TIKZs
        # Create a Tikz Environment
        self.tikz_file = Path(tikz_file)
        self.options = options
        self.center = center
        self._statements = {}
        self._id = _N_TIKZs

        # Check if the tikz_file exists. If not, create it.
        if not self.tikz_file.is_file():
            try:
                with open(self.tikz_file.resolve(), "w"):
                    pass
            except:
                print(f"Could not find file at {self.tikz_file}.")
                answer = input("Want to make it? (Y/N)")
                if answer == "y" or answer == "Y":
                    # Make directory, then file
                    self.tikz_file.parent.mkdir(parents=True)
                    with open(self.tikz_file.resolve(), "w+"):
                        pass
                print(
                    f"File created at {str(self.tikz_file.resolve())}, tikz_code will output there"
                )
            else:
                print("Not created.")
        # Upon successful creation of an object, we create increase the counter
        _N_TIKZs += 1

    @property
    def begin(self):
        """The beginning code of our tikz environment.
        * For each environment we create, we assign an ID that our program can later identify.
          Such an ID is of the form of a TeX comment " % TikzPython id = ({self._id}) "
        * This is to ensure safe, efficient file update and deletion processes.
        """
        return f"\\begin{{tikzpicture}}{braces(self.options)}% TikzPython id = ({self._id}) \n"

    @property
    def end(self):
        """ End statement for the TikzPicture."""
        return "\\end{tikzpicture}\n"

    @property
    def tex_file(self):
        r"""Takes care of the TeX file, containing necessary \usepackage{...} and \usetikzlibrary{...} statements,
        which is used to call the Tikz code and compile it.
        * The TeX file is stored in a folder "/tex", in the same directory as self.tikz_file.
            * This is to make everything easier for the user. They don't have to waste their time with the tedious task
              of sorting and connecting their files together, figuring out full paths, dealing with the stupid .aux, .log... files,
              figuring our \input{...}, etc. This process is automatic.
            * When a PDF compiles, the pdf is moved to the same directory as self.tikz_file
              so the user can see it. (All those moronic .log, .aux files are left behind in the hidden folder,
              another benefit of this approach).
        * The only reason the user will need to change the TeX file is if they change the file name of self.tikz_file.
        Ideally, the program could take care of this. But there isn't a robust way of updating the \input{...} statement in the
        TeX file without risking the user's TeX contents from being wiped (e.g., they may remove some comments that helps the program
        find what line to update). Alternatively, I could warn the user of this, but an
        unwise user could nevertheless put their hard work into such a file and then risk it being wiped.
        """
        # Full paths for self.tikz_file and the tex_file
        tikz_path = str(self.tikz_file.resolve().parents[0])
        # Full path for the hidden tex_file
        tex_file = Path(tikz_path + "/tex/tex_file.tex")
        # Check if the folder exists. If so, create the hidden folder tex/ and populate it with appropriate code using our template
        if not tex_file.exists():
            tex_file.parent.mkdir(parents=True)
            template_file = Path("/template/tex_file.tex")
            with open(str(template_file.resolve())) as f:
                lines = f.readlines()
            with open(tikz_path + "/tex/tex_file.tex", "w") as f:
                for line in lines:
                    if line[:6] == "\\input":
                        f.write(f"\\input{{{str(self.tikz_file.resolve())}}}")
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

    @statements.setter
    def statements(self, draw_obj):
        self._statements[draw_obj] = draw_obj.code

    @property
    def code(self):
        """A string contaning our Tikz code. This uses self._statements, and self.code
        gets passed to __repr__.
        """
        code = self.begin
        for draw_obj in self.statements:
            code += "\t" + draw_obj.code + "\n"
        code += self.end
        return code

    def __repr__(self):
        return self.code

    def remove(self, draw_obj):
        """A method to remove a code statement from the Tikz environment, e.g., a line."""
        del self._statements[draw_obj]

    def draw(self, *args):
        """User can also manually add their drawing object. """
        for draw_obj in args:
            self._statements[draw_obj] = draw_obj.code

    # TODO: Test if this works
    def add_command(self, tikz_statement):
        """Manually add a string of valid Tikz code into the Tikz environment."""
        command = TikzCommand(tikz_statement)
        self.draw(command)
        return command

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
        global _N_TIKZs  # Load in the global to update this variable, in the off chance overwrite = False.
        tikz_file_path = str(self.tikz_file.resolve())
        output_code = self.code

        # Center the tikzpicture environment if necessary
        if self.center:
            output_code = "\\begin{center}\n" + self.code + "\\end{center}\n"

        # If we want to overwrite and update our last TikzPicture environment (in most cases, we do)
        if overwrite:
            begin_ind = -1
            end_ind = -1
            # open the tikz_file and obtain its contents
            with open(tikz_file_path, "r") as tikz_file:
                lines = tikz_file.readlines()
            for i, line in enumerate(lines):
                """We look for our old TikzPicture code in the file as follows.
                * Loop over the file lines.
                * For each line, we check if it is our begin statement.
                * If so, we look ahead and search for our end statement.
                """
                if line == self.begin:
                    begin_ind = i
                    for j, later_lines in enumerate(lines[i:]):
                        if later_lines == self.end:
                            end_ind = i + j
                            break
                    break

            # If we found our begin statement, then we know we've written in the file before.
            if begin_ind != -1:
                assert (
                    end_ind != -1
                ), "Found code statement at line {begin_ind}, but never found end statement"
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
                _N_TIKZs += 1

        # If for some reason we do not want to overwrite our last TikzPicture
        else:
            with open(tikz_file_path, "a+") as tikz_file:
                tikz_file.write(output_code)
            _N_TIKZs += 1

        # Finally, we move onto compiling our PDF.
        tex_file_parents = str(self.tex_file.resolve().parents[0])
        tex_filename = self.tex_file.stem
        tex_file = tex_file_parents + "/" + tex_filename + ".tex"
        # We now compile the PDF
        subprocess.run(
            f"latexmk -pdf -output-directory='{tex_file_parents}' {tex_file}",
            shell=True,
        )
        # We move the PDF up one directory, our of the hidden folder, so the viewer can see it.
        pdf_file = Path(tex_file_parents + "/" + tex_filename + ".pdf")
        pdf_file.rename(pdf_file.resolve().parents[1] / pdf_file.name)

    # Display the current tikz drawing
    def show(self):
        """Displays the pdf of the TikzPicture to the user."""
        pdf_file_path = (
            str(self.tex_file.parents[1]) + "/" + self.tex_file.stem + ".pdf"
        )
        pdf = Path(pdf_file_path).resolve()
        if not pdf.is_file():
            print(
                f"\nCouldn't find the PDF in {pdf_file_path}. Perhaps you forgot to compile it with .write() first? \n"
            )
        webbrowser.open_new("file://" + pdf_file_path)

    """
        Methods to code objects in the Tikz Environment
    """

    def line(self, start, end, options="", to_options="--", control_pts=[]):
        """Draws a line by creating an instance of the Line class.
        Upon creation, we update self._statements with our new code.
        * Key feature: If we update any attributes of our line, the changes
          to the Tikz code are automatically reflected in self._statements.
        """
        line = Line(start, end, options, to_options, control_pts)
        self.draw(line)
        return line

    def plot_coords(self, points, options="", plot_options=""):
        """Draws a plot coordinates statement by creating an instance of the PlotCoordinates class.
        Updates self._statements when necessary; see above comment under line function above.
        """
        plot_coords = PlotCoordinates(points, options, plot_options)
        self.draw(plot_coords)
        return plot_coords

    def circle(self, center, radius, options=""):
        """Draws a circle by creating an instance of the Circle class.
        Updates self._statements when necessary; see above comment under line function above.
        """
        circle = Circle(center, radius, options)
        self.draw(circle)
        return circle

    def node(self, position, options="", content=""):
        """Draws a node by creating an instance of the Node class.
        Updates self._statements when necessary; see above comment under line function above.
        """
        node = Node(position, options, content)
        self.draw(node)
        return node

    def rectangle(self, left_corner, right_corner, options=""):
        """Draws a rectangle by creating an instance of the Rectangle class.
        Updates self._statements when necessary; see above comment under line function above.
        """
        rectangle = Rectangle(left_corner, right_corner, options)
        self.draw(rectangle)
        return rectangle

    def ellipse(self, center, horiz_axis, vert_axis, options=""):
        """Draws an ellipse by creating an instance of the Ellipse class.
        Updates self._statements when necessary; see above comment under line function above.
        """
        ellipse = Ellipse(center, horiz_axis, vert_axis, options)
        self.draw(ellipse)
        return ellipse

    def arc(self, center, start_angle, end_angle, radius, options="", radians=False):
        """Draws an arc by creating an instance of the Arc class.
        Updates self._statements when necessary; see above comment under line function above.
        """
        arc = Arc(center, start_angle, end_angle, radius, options, radians)
        self.draw(arc)
        return arc

    def scope(self, options=""):
        scope = Scope(options)
        self.draw(scope)
        return scope


"""
    Classes for drawing
"""

# TODO: Test if this class works
class TikzCommand:
    """A class to handle manually typed Tikz code. """

    def __init__(self, code):
        self.code = code

    def __repr__(self):
        return self.code


class _DrawingObject:
    """A generic class for our drawing objects to inherit properties from.
    This class serveees"""

    def __init__(self, action, options="", command=""):  # action is usually "draw"
        self.action = action
        self.options = options
        self.command = ""

    @property
    def code(self):
        """Full Tikz code for this drawing object."""
        return f"\{self.action}{braces(self.options)} {self._command}"

    def __deepcopy__(self, memo):
        """Creates a deep copy of a class object. This is useful since in our classes, we chose to set
        our methods to modify objects, but not return anything.
        """
        print("Copied!")
        cls = self.__class__
        draw_obj = cls.__new__(cls)
        memo[id(self)] = draw_obj
        for k, v in self.__dict__.items():
            setattr(draw_obj, k, deepcopy(v, memo))
        return draw_obj

    def copy(self):
        """Wrapper for deepcopy."""
        return deepcopy(self)

    def __repr__(self):
        return self.code


# Class for Lines
class Line(_DrawingObject):
    """
    A class to create lines in the tikz environment

    Attributes :
        tikz_inst (TikzPicture) : An instance of the class TikzPicture so that we may call methods on an instance
        start (tuple) : Pair of floats representing the start of the line
        end (tuple) : Pair of floats representing the end of the line
        options (str) : String containing Tikz drawing options, e.g. "Blue"
        control_pts (list): List of control points for the line
    """

    def __init__(
        self,
        start,
        end,
        options="",
        to_options="to",
        control_pts=[],
        action="draw",
    ):
        self.start = start
        self.end = end
        self.options = options
        self.to_options = to_options
        self.control_pts = control_pts

        super().__init__(action, self.options, self._command)

    @property
    def _command(self):
        """The Tikz code for a line that comes after \draw[self.options]. It is useful for
        us to do this breaking-up of the Tikz code, especially for clipping. However, this
        serves no use to the user, so we make it private (well, it's just bells and whistles).
        """
        if len(self.control_pts) == 0:
            return f"{self.start} to{braces(self.to_options)} {self.end};"
        else:
            control_stmt = ".. controls "
            for pt in self.control_pts:
                control_stmt += f"{pt[0], pt[1]}" + " and "
            control_stmt = control_stmt[:-4] + " .."
            return f"{self.start} {control_stmt} {self.end};"

    @property
    def midpoint(self):
        mid_x = round((self.start[0] + self.end[0]) / 2, 7)
        mid_y = round((self.start[1] + self.end[1]) / 2, 7)
        return (mid_x, mid_y)

    def shift(self, xshift, yshift):
        """Shift start, end, and control_pts"""
        shifted_start_end = shift_coords([self.start, self.end], xshift, yshift)
        shifted_control_pts = shift_coords(self.control_pts, xshift, yshift)

        self.start, self.end = shifted_start_end[0], shifted_start_end[1]
        self.control_pts = shifted_control_pts

    def scale(self, scale):
        """Scale start, end, and control_pts."""
        scaled_start_end = scale_coords([self.start, self.end], scale)
        self.start, self.end = scaled[0], scaled[1]
        self.control_pts = scale_coords(self.control_pts, scale)

    def rotate(self, angle, about_pt=None, radians=False):
        """Rotate start, end, and control_pts"""
        if about_pt == None:
            about_pt = self.midpoint
        rotated_start_end = rotate_coords(
            [self.start, self.end], angle, about_pt, radians
        )

        self.start, self.end = rotated_start_end[0], rotated_start_end[1]
        self.control_pts = rotate_coords(self.control_pts, angle, about_pt, radians)


# Class for Plotting
class PlotCoordinates(_DrawingObject):
    """
    A class to create plots in the tikz environment

    Attributes :
        tikz_inst (TikzPicture) : An instance of the class TikzPicture so that we may call methods on an instance
        options (str) : String containing drawing options (e.g., "Blue")
        plot_options (str) : String containing the plot options (e.g., "smooth cycle")
        points (list) : A list of points to be drawn

    """

    def __init__(self, points, options="", plot_options="", action="draw"):
        self.points = points
        self.options = options
        self.plot_options = plot_options
        super().__init__(action, self.options, self._command)

    @property
    def _command(self):
        cmd = f"plot{braces(self.plot_options)} coordinates {{"
        for pt in self.points:
            cmd += str(pt) + " "
        cmd += "};"
        return cmd

    @property
    def center(self):
        mean_x = 0
        mean_y = 0
        for pt in self.points:
            mean_x += pt[0]
            mean_y += pt[1]
        mean_x = round(mean_x / len(self.points), 7)
        mean_y = round(mean_y / len(self.points), 7)
        return (mean_x, mean_y)

    def shift(self, xshift, yshift):
        self.points = shift_coords(self.points, xshift, yshift)

    def scale(self, scale):
        self.points = scale_coords(self.points, scale)

    def rotate(self, angle, about_pt=None, radians=False):
        if about_pt == None:
            about_pt = self.center
        self.points = rotate_coords(self.points, angle, about_pt, radians)


# Class for Circles
class Circle(_DrawingObject):
    """
    A class to create circles in the tikz environment

    Attributes :
        tikz_inst (TikzPicture) : An instance of the class TikzPicture so that we may call methods on an instance
        position (tuple) : Pair of floats representing the center of the circle
        radius (float) : Length (in cm) of the radius
        options (str) : String containing the drawing options (e.g, "Blue")
    """

    def __init__(self, center, radius, options="", action="draw"):
        self.center = center
        self.radius = radius
        self.options = options
        super().__init__(action, self.options, self._command)

    @property
    def _command(self):
        return f"{self.center} circle ({self.radius}cm);"

    def shift(self, xshift, yshift):
        self.center = shift_coords([self.center], xshift, yshift)[0]

    def scale(self, scale):
        self.center = scale_coords([self.center], scale)

    def rotate(self, angle, about_pt, radians=False):
        self.center = rotate_coords([self.center], angle, about_pt, radians)[0]


# Class for Nodes
class Node(_DrawingObject):
    """
    A class to create lines in the tikz environment

    Attributes :
        tikz_inst (TikzPicture) : An instance of the class TikzPicture so that we may call methods on an instance
        position (tuple) : Pair of floats representing the location of the node
        text (str): Text that will be displayed with the node; can use dollar signs $ for LaTeX
        options (str) : String containing node options (e.g., "above")
    """

    def __init__(self, position, options="", text=""):
        self.position = position
        self.text = text
        self.options = options
        super().__init__("node", self.options, self._command)

    @property
    def _command(self):
        return f"at {self.position} {{ {self.text} }};"

    def shift(self, xshift, yshift):
        self.position = shift_coords([self.position], xshift, yshift)[0]

    def scale(self, scale):
        self.position = scale_coords([self.position], scale)[0]

    def rotate(self, angle, about_pt, radians=False):
        self.position = rotate_coords([self.position], angle, about_pt, radians)[0]


class Rectangle(_DrawingObject):
    """
    A class to create lines in the tikz environment

    Attributes :
        tikz_inst (TikzPicture) : An instance of the class TikzPicture so that we may call methods on an instance
        left_corner (tuple) : Pair of floats representing the position of the bottom left corner
        right_corner (tuple) : Pair of floats representing the position of the upper right corner
        options (str) : String containing the drawing options, e.g, ("Blue")
    """

    def __init__(self, left_corner, right_corner, options="", action="draw"):
        self.left_corner = left_corner
        self.right_corner = right_corner
        self.options = options
        super().__init__(action, self.options, self._command)

    @property
    def _command(self):
        return f"{self.left_corner} rectangle {self.right_corner};"

    def shift(self, xshift, yshift):
        shifted_corners = shift_coords(
            [self.left_corner, self.right_corner], xshift, yshift
        )
        self.left_corner = shifted_corners[0]
        self.right_corner = shifted_corners[1]

    def scale(self, scale):
        scaled_corners = scale_coords([self.left_corner, self.right_corner], scale)
        self.left_corner = scaled_corners[0]
        self.right_corner = scaled_corners[1]

    def rotate(self, angle, about_pt, radians=False):
        rotated_corners = rotate_coords(
            [self.left_corner, self.right_corner], angle, about_pt, radians
        )
        self.left_corner = rotated_corners[0]
        self.right_corner = rotated_corners[1]


class Ellipse(_DrawingObject):
    """
    A class to create lines in the tikz environment

    Attributes :
        tikz_inst (TikzPicture) : An instance of the class TikzPicture so that we may call methods on an instance
        center (tuple) : Pair of floats representing the center of the ellipse
        horiz_axis (float): The length (in cm) of the horizontal axis of the ellipse
        vert_axis (float): The length (in cm) of the vertical axis of the ellipse
    """

    def __init__(self, center, horiz_axis, vert_axis, options="", action="draw"):
        self.center = center
        self.horiz_axis = horiz_axis
        self.vert_axis = vert_axis
        self.options = options
        super().__init__(action, self.options, self._command)

    @property
    def _command(self):
        return f"{self.center} ellipse ({self.horiz_axis}cm and {self.vert_axis}cm);"

    def shift(self, xshift, yshift):
        self.center = shift_coords([self.center], xshift, yshift)[0]

    def scale(self, scale):
        scaled_center = scale_coords([self.center], scale)[0]
        scaled_h = round(self.horiz_axis * scale, 7)
        scaled_v = round(self.vert_axis * scale, 7)

        self.center = scaled_center
        self.horiz_axis = scaled_h
        self.vert_axis = scaled_v

    def rotate(self, angle, about_pt, radians=False):
        self.center = rotate_coords([self.center], angle, about_pt, radians)[0]


class Arc(_DrawingObject):
    """
    A class to create lines in the tikz environment

    Attributes :
        tikz_inst (TikzPicture) : An instance of the class TikzPicture so that we may call methods on an instance
        center (tuple) : Pair of points representing the relative center of the arc
        start_angle (float) : The angle of the start of the arc
        end_angle (float) : The angle of the end of the arc
        radius (float) : The radius (in cm) of the arc
        radians (bool) : Set true if inputting radians. Default behavior is for degrees.
    """

    def __init__(
        self,
        center,
        start_angle,
        end_angle,
        radius,
        options="",
        radians=False,
        action="draw",
    ):
        self.center = center
        self.start_angle = start_angle
        self.end_angle = end_angle
        self.radius = radius
        self.options = options

        if radians:
            self.start_angle = round(self.start_angle, 180 / math.pi, 7)
            self.end_angle = round(self.end_angle, 180 / math.pi, 7)

        super().__init__(action, self.options, self._command)

    @property
    def _command(self):
        return (
            f"{self.center} arc ({self.start_angle}:{self.end_angle}:{self.radius}cm);"
        )

    def shift(self, xshift, yshift):
        self.center = shift_coords([self.center], xshift, yshift)[0]

    def scale(self, scale):
        scaled_center = scale_coords([self.center], scale)
        scaled_radius = round(self.radius * scale, 7)

        self.center = scaled_center[0]
        self.radius = scaled_radius

    def rotate(self, angle, about_pt, radians=False):
        self.center = rotate_coords([self.center], angle, about_pt, radians)[0]


"""
    End of Drawing Object classes
"""


# TODO: Test if this class works
class Scope:
    """A class to create a scope environment."""

    def __init__(self, options=""):
        self.options = ""
        self._scope_statements = {}

    @property
    def begin(self):
        return f"\\begin{{scope}}{braces(self.options)}\n"

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


class Clip:
    """A class for a clipping code statement."""

    def __init__(self, draw_obj, draw=False):
        if isinstance(
            draw_obj, (Line, PlotCoordinates, Circle, Node, Rectangle, Ellipse, Arc)
        ):
            self.draw_obj = draw_obj
            self.draw = draw
        else:
            raise TypeError(
                f"Clip argument {draw_obj} must be an instance of a drawing class."
            )

    @property
    def code(self):
        if self.draw == True:
            return f"\clip[preaction = {{draw, {self.draw_obj.options}}}] {self.draw_obj._command}"
        else:
            return f"\clip {self.draw_obj._command}"

    def shift(self, xshift, yshift):
        self.draw_obj.shift(xshift, yshift)

    def scale(self, scale):
        self.draw_obj.scale(scale)

    def rotate(self, angle, about_pt, radians=False):
        self.draw_obj.rotate(angle, about_pt, radians)


""" Shifting, Scaling, and Rotating calculations called by above methods
"""


def shift_coords(coords, xshift, yshift):
    """Shift a list of 2D-coordinates by "xshift", "yshift".
        Accuracy to 7 decimal places for readability.
    coords (list) : A list of tuples (x, y) with x, y floats
    xshift (float) : An amount to shift the x values
    yshift (float) : An amount to shift the y values
    """

    shifted_coords = []
    for coord in coords:
        x = coord[0]
        y = coord[1]

        shifted_x = round(x + xshift, 7)
        shifted_y = round(y + yshift, 7)
        shifted_coords.append((shifted_x, shifted_y))
    return shifted_coords


def scale_coords(coords, scale):
    """Scale a list of 2D-coordinates by "scale".
        Accuracy to 7 decimal places for readability.
    coords (list) : A list of tuples (x, y) with x, y floats
    scale (float) : An amount to scale the x and y values
    """
    scaled_coords = []
    for coord in coords:
        x = coord[0]
        y = coord[1]

        scale_x = round(scale * x, 7)
        scale_y = round(scale * y, 7)
        scaled_coords.append((scale_x, scale_y))
    return scaled_coords


def rotate_coords(coords, angle, about_pt, radians=False):  # rotate counterclockwise
    """Rotate in degrees (or radians) a list of 2D-coordinates about the point "about_pt".
        Accuracy to 7 decimal places for readability.
    coords (list) : A list of tuples (x, y) with x, y floats
    angle (float) : The angle to rotate the coordinates
    about_pt (tuple) : A point (x,y) of reference for rotation
    radians (bool) : Specify type of angle (radians or degrees)
    """
    if not radians:
        angle *= math.pi / 180

    rotated_coords = []
    for coord in coords:
        x = coord[0]
        y = coord[1]

        # Shift by about_pt, so that rotation is now relative to that point
        x -= about_pt[0]
        y -= about_pt[1]

        # Rotate the points
        rotated_x = x * math.cos(angle) - y * math.sin(angle)
        rotated_y = x * math.sin(angle) + y * math.cos(angle)

        # Shift them back by about_pt, truncate the decimal places
        rotated_x += round(about_pt[0], 7)
        rotated_y += round(about_pt[1], 7)

        rotated_coords.append((rotated_x, rotated_y))
    return rotated_coords


def recenter_to_origin(coords):
    """Shifts a set of 2D points such that their centroid corresponds to the origin.
    This is useful for scaling: One may notice that scaling changes their (x,y) coordinates. Running this before
    scaling can allow them to relatively scale their figure such that the position of the figure does not change.
    """
    x_mean = 0
    y_mean = 0
    for point in coords:
        x_mean += point[0]
        y_mean += point[1]

    x_mean /= len(coords)
    y_mean /= len(coords)

    return shift_coords(coords, -x_mean, -y_mean)


"""
    Functions for colors
"""


def rgb(r, g, b):
    """A wrapper function that outputs xcolor/Tikz code for coloring via rgb values.

    When calling rgb, it is necessary to specify "color = " or "fill =" right before.
    E.g., tikz.line(... options = "color =" + rgb(r,g,b) ...)

    This is an annoying aspect with Tikz.
    """
    return f"{{ rgb,255:red, {r}; green, {g}; blue, {b} }}"


def rainbow_colors(i):
    """A wrapper function for obtaining rainbow colors.
    Any integer can be passed in.
    """
    return rainbow_cols[i % len(rainbow_cols)]


"""
    Miscellaneous Helpers
"""


def braces(string):
    """A helper function for creating tikz code.
    Basically, if the string is empty, we don't obtain brackets [].
    """
    if len(string) != 0:
        return "[" + string + "]"
    else:
        return ""


# Collect xcolor names
xcolors = [
    "Apricot",
    "Aquamarine",
    "Bittersweet",
    "Black",
    "Blue",
    "BlueGreen",
    "BlueViolet",
    "BrickRed",
    "Brown",
    "BurntOrange",
    "CadetBlue",
    "CarnationPink",
    "Cerulean",
    "CornflowerBlue",
    "Cyan",
    "Dandelion",
    "DarkOrchid",
    "Emerald",
    "ForestGreen",
    "Fuchsia",
    "Goldenrod",
    "Gray",
    "Green",
    "GreenYellow",
    "JungleGreen",
    "Lavender",
    "LimeGreen",
    "Magenta",
    "Mahogany",
    "Maroon",
    "Melon",
    "MidnightBlue",
    "Mulberry",
    "NavyBlue",
    "OliveGreen",
    "Orange",
    "OrangeRed",
    "Orchid",
    "Peach",
    "Periwinkle",
    "PineGreen",
    "Plum",
    "ProcessBlue",
    "Purple",
    "RawSienna",
    "Red",
    "RedOrange",
    "RedViolet",
    "Rhodamine",
    "RoyalBlue",
    "RoyalPurple",
    "RubineRed",
    "Salmon",
    "SeaGreen",
    "Sepia",
    "SkyBlue",
    "SpringGreen",
    "Tan",
    "TealBlue",
    "Thistle",
    "Turquoise",
    "Violet",
    "VioletRed",
    "White",
    "WildStrawberry",
    "Yellow",
    "YellowGreen",
    "YellowOrange",
]

rainbow_cols = [
    "{rgb,255:red, 255; green, 0; blue, 0 }",  # red
    "{rgb,255:red, 255; green, 125; blue, 0 }",  # orange
    "{rgb,255:red, 255; green, 255; blue, 0 }",  # yellow
    "{rgb,255:red, 125; green, 255; blue, 0 }",  # spring
    "{rgb,255:red, 0; green, 255; blue, 0 }",  # green
    "{rgb,255:red, 0; green, 255; blue, 125 }",  # turquoise
    "{rgb,255:red, 0; green, 255; blue, 255 }",  # cyan
    "{rgb,255:red, 0; green, 125; blue, 255 }",  # ocean
    "{rgb,255:red, 0; green, 0; blue, 255 }",  # blue
    "{rgb,255:red, 125; green, 0; blue, 255 }",  # violet
    "{rgb,255:red, 255; green, 0; blue, 12 }",  # magenta
    "{rgb,255:red, 255; green, 0; blue, 255 }",  # raspberry
]


if __name__ == "__main__":
    """Quick sanity tests for our classes."""

    tikz = TikzPicture()
    # Line
    line = tikz.line(
        (0, 0),
        (1, 1),
        options="thick, blue",
        control_pts=[(0.25, 0.25), (0.75, 0.75)],
    )
    # Plot
    plot = tikz.plot_coords(
        options="green",
        plot_options="smooth ",
        points=[(1, 1), (2, 2), (3, 3), (2, -4)],
    )
    # Circle
    circle = tikz.circle((1, 1), 1, options="fill = purple")
    # Node
    node = tikz.node(
        position=(3, 3),
        content="I love $ \sum_{x \in \mathbb{R}} f(x^2)$ !",
        options="above",
    )
    # Rectangle
    rectangle = tikz.rectangle((2, 2), (3, 4), options="Blue")
    # Ellipse
    ellipse = tikz.ellipse((0, 0), 3, 4)
    # Arc
    arc = tikz.arc((0, 0), 20, 90, 4)

    def test():
        # Test Line
        assert line.start == (0, 0)
        assert line.end == (1, 1)
        assert line.options == "thick, blue"
        assert line.control_pts == [(0.25, 0.25), (0.75, 0.75)]
        assert (
            line.code
            == "\\draw[thick, blue] (0, 0) .. controls (0.25, 0.25) and (0.75, 0.75)  .. (1, 1);"
        )
        # Test Plot
        assert plot.options == "green"
        assert plot.plot_options == "smooth "
        assert plot.points == [(1, 1), (2, 2), (3, 3), (2, -4)]
        assert (
            plot.code
            == "\\draw[green] plot[smooth ] coordinates {(1, 1) (2, 2) (3, 3) (2, -4) };"
        )
        # Test Circle
        assert circle.center == (1, 1)
        assert circle.radius == 1
        assert circle.options == "fill = purple"
        assert circle.code == "\\draw[fill = purple] (1, 1) circle (1cm);"
        # Test Node
        assert node.position == (3, 3)
        assert node.text == "I love $ \sum_{x \in \mathbb{R}} f(x^2)$ !"
        assert node.options == "above"
        assert (
            node.code
            == "\\node[above] at (3, 3) { I love $ \\sum_{x \\in \\mathbb{R}} f(x^2)$ ! };"
        )
        # Rectangle
        assert rectangle.left_corner == (2, 2)
        assert rectangle.right_corner == (3, 4)
        assert rectangle.options == "Blue"
        assert rectangle.code == "\\draw[Blue] (2, 2) rectangle (3, 4);"
        # Ellipse
        assert ellipse.center == (0, 0)
        assert ellipse.horiz_axis == 3
        assert ellipse.vert_axis == 4
        assert ellipse.code == "\\draw (0, 0) ellipse (3cm and 4cm);"
        # Arc
        assert arc.center == (0, 0)
        assert arc.start_angle == 20
        assert arc.end_angle == 90
        assert arc.radius == 4
        assert arc.code == "\\draw (0, 0) arc (20:90:4cm);"
        print("flying colors!")
