import math
import subprocess
import webbrowser
from pathlib import Path

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
        tex_file (str) : A file path to the TeX file which will accept the tikz code.
        center (bool) : True/False if one wants to center their Tikz code
        options (str) : A list of options for the Tikz picture
        statements (dict) : See docstring for statements below
    """

    def __init__(
        self,
        tikz_file="tikz_code/tikz-code.tex",
        tex_file="tex/tex_file.tex",
        center=False,
        options="",
    ):
        # TODO: improve unit tests (verify shift and scale work, ...)
        # TODO: add an undo method for appending draw objects/tikz environments, but don't make it too powerful
        # TODO: figure out a nice way to implement scope
        # TODO: If self.options is empty, don't print empty brackets []
        global _N_TIKZs
        # Create a Tikz Environment
        self.tikz_file = Path(tikz_file)
        self.tex_file = Path(tex_file)
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
                print(f"Could not find or create file at {self.tikz_file}")
            else:
                print(
                    f"File created at {str(self.tikz_file.resolve())}, tikz_code will output there"
                )
        # Upon successful creation of an object, we create increase the counter
        _N_TIKZs += 1

    @property
    def begin(self):
        return (
            f"\\begin{{tikzpicture}}[{self.options}]% TikzPython id = ({self._id}) \n"
        )

    @property
    def end(self):
        return f"\\end{{tikzpicture}}\n"

    @property
    def statements(self):
        """self.statements: A dictionary where
        keys : instances of subclasses created (e.g, Line)
        values : the Tikz code of the instance (e.g., Line.code)
        """
        statement_dict = {}
        for draw_obj in self._statements:
            statement_dict[draw_obj] = draw_obj.code
        return statement_dict

    @statements.setter
    def statements(self, draw_obj):
        self._statements[draw_obj] = draw_obj.code

    # Assemble tikz_code in a list format (for ease in handling)
    @property
    def list_statements(self):
        list_code = []
        list_code.append(self.begin)

        for draw_obj in self.statements:
            list_code.append("\t" + draw_obj.code + "\n")

        list_code.append(self.end)
        return list_code

    # Assemble tikz_code as a string (for output readability, see __repr__)
    @property
    def code(self):
        code = ""
        for statement in self.list_statements:
            code += statement
        return code

    def __repr__(self):
        print(self.code)
        return ""

    # Remove a code statement from the Tikz environment, e.g., a line
    def remove(self, draw_obj):
        del self._statements[draw_obj]

    # TODO: Manually add code to the Tikz Environment
    def add_statement(self, statement):
        self._statements[len(self._statements)] = statement

    def write(self, overwrite=True):
        global _N_TIKZs

        tikz_file_path = str(self.tikz_file.resolve())
        tex_code = self.code
        # Center the tikzpicture environment if necessary
        if self.center:
            tex_code = "\\begin{center}\n" + self.code + "\\end{center}\n"

        if not overwrite:
            with open(tikz_file_path, "a+") as tikz_file:
                tikz_file.write(tex_code)
            _N_TIKZs += 1
        else:
            begin_ind = -1
            # open the file, grab the file lines
            with open(tikz_file_path, "r") as tikz_file:
                lines = tikz_file.readlines()
            # Loop over the file lines to find our old code
            for i, line in enumerate(lines):
                # Look for our begin statement
                if line == self.begin:
                    begin_ind = i
                    # Look ahead of our statement
                    for j, later_lines in enumerate(lines[i:]):
                        # Look later for the end statement
                        if later_lines == self.end:
                            end_ind = i + j
                            break
                    break
            # If we never found our id, then we are safe to write
            if begin_ind == -1:
                print("Adding new Tikz environment")
                with open(tikz_file_path, "a+") as tikz_file:
                    tikz_file.write(tex_code)
                _N_TIKZs += 1
            # Otherwise, we found the \begin{tikzpicture}\end{tikzpicture} statement.
            else:
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
                with open(tikz_file_temp_path, "w") as new_tikz_file:
                    # Write everything before what needed to be replaced
                    for line in lines[:begin_ind]:
                        new_tikz_file.write(line)
                    # Substitute in our updated code
                    new_tikz_file.write(self.code)
                    # Write everything after what needed to be replaced
                    for line in lines[end_ind + 1 :]:
                        new_tikz_file.write(line)
                # Now rename the file
                tikz_file_temp.replace(tikz_file_path)
                print("Successful write")

    # Display the current tikz drawing
    def show(self):
        """Displays the pdf of the TikzPicture to the user."""
        tex_file_path = str(self.tex_file.resolve())
        # Check if TeX exists, if not, create it using our template
        if not self.tex_file.is_file():
            with open("template/template_tex.tex") as template:
                lines = template.readlines()
                lines = [l for l in lines if "ROW" in l]
                with open(tex_file_path, "w") as tex_file:
                    for line in lines:
                        tex_file.writelines(line)
        # Find the pdf
        pdf_file = Path(self.tex_file.parent.name + "/" + self.tex_file.stem + ".pdf")
        # If we cannot find it, it has not been compiled. Thus, we compile it.
        if not pdf_file.is_file():
            subprocess.run(
                f"latexmk -pdf -pv {tex_file_path}",
                shell=True,
            )
        # Show the user the TikzPicture
        webbrowser.open_new("file://" + str(pdf_file.resolve()))

    """
        Methods to code objects in the Tikz Environment
    """

    def line(self, start, end, options="", control_pts=[]):
        line = TikzPicture.Line(self, start, end, options, control_pts)
        self._statements[line] = line.code
        return line

    def plot_coords(self, points, draw_options, plot_options):
        plot_coords = TikzPicture.PlotCoordinates(
            self, points, draw_options, plot_options
        )
        self._statements[plot_coords] = plot_coords.code
        return plot_coords

    def circle(self, position, radius, options=""):
        circle = TikzPicture.Circle(self, position, radius, options)
        self._statements[circle] = circle.code
        return circle

    def node(self, position, options="", content):
        node = TikzPicture.Node(self, position, options, content)
        self._statements[node] = node.code
        return node

    def rectangle(self, left_corner, right_corner, options=""):
        rectangle = TikzPicture.Rectangle(self, left_corner, right_corner, options)
        self._statements[rectangle] = rectangle.code
        return rectangle

    def ellipse(self, position, horiz_axis, vert_axis):
        ellipse = TikzPicture.Ellipse(self, position, horiz_axis, vert_axis)
        self._statements[ellipse] = ellipse.code
        return ellipse

    def arc(self, position, start_angle, end_angle, radius):
        arc = TikzPicture.Arc(self, position, start_angle, end_angle, radius)
        self._statements[arc] = arc.code
        return arc

    """
        Classes for drawing
    """

    # Class for Lines
    class Line:
        """
        A subclass of TikzPicture to create lines in the tikz environment

        Attributes :
            tikz_inst (TikzPicture) : An instance of the class TikzPicture so that we may call methods on an instance
            start (tuple) : Pair of floats representing the start of the line
            end (tuple) : Pair of floats representing the end of the line
            options (str) : String containing Tikz drawing options, e.g. "Blue"
            control_pts (list): List of control points for the line
        """

        def __init__(self, tikz_inst, start, end, options, control_pts):
            self.tikz_inst = tikz_inst
            self.start = start
            self.end = end
            self.options = options
            self.control_pts = control_pts

        @property
        def code(self):
            if len(self.control_pts) == 0:
                tikz_cmd = f"\draw[{self.options}] {self.start} -- {self.end};"
            else:
                control_stmt = ".. controls "
                for pt in self.control_pts:
                    control_stmt += f"{pt[0], pt[1]}" + " and "
                control_stmt = control_stmt[:-4] + " .."
                tikz_cmd = (
                    f"\draw[{self.options}] {self.start} {control_stmt} {self.end};"
                )
            return tikz_cmd

        @property
        def midpoint(self):
            mid_x = round((self.start[0] + self.end[0]) / 2, 7)
            mid_y = round((self.start[1] + self.end[1]) / 2, 7)
            return (mid_x, mid_y)

        def shift(self, xshift, yshift):
            shifted_start_end = shift_coords([self.start, self.end], xshift, yshift)
            shifted_control_pts = shift_coords(self.control_pts, xshift, yshift)

            self.start, self.end = shifted_start_end[0], shifted_start_end[1]
            self.control_pts = shifted_control_pts

        def scale(self, scale):
            scaled = scale_coords([self.start, self.end], scale)
            self.start, self.end = scaled[0], scaled[1]

        def rotate(self, angle, about_pt=None, radians=False):
            if about_pt == None:
                about_pt = self.midpoint
            rotated = rotate_coords([self.start, self.end], angle, about_pt, radians)
            self.start, self.end = rotated[0], rotated[1]

        def __repr__(self):
            return self.code

    # Class for Plotting
    class PlotCoordinates:
        """
        A subclass of TikzPicture to create plots in the tikz environment

        Attributes :
            tikz_inst (TikzPicture) : An instance of the class TikzPicture so that we may call methods on an instance
            draw_options (str) : String containing drawing options (e.g., "Blue")
            plot_options (str) : String containing the plot options (e.g., "smooth cycle")
            points (list) : A list of points to be drawn

        """

        def __init__(self, tikz_inst, points, draw_options, plot_options):
            self.points = points
            self.draw_options = draw_options
            self.plot_options = plot_options

        @property
        def code(self):
            tikz_cmd = (
                f"\draw[{self.draw_options}] plot[{self.plot_options}] coordinates {{"
            )
            for pt in self.points:
                tikz_cmd += str(pt) + " "
            tikz_cmd += "};"
            return tikz_cmd

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

        def __repr__(self):
            return self.code

    # Class for Circles
    class Circle:
        """
        A subclass of TikzPicture to create circles in the tikz environment

        Attributes :
            tikz_inst (TikzPicture) : An instance of the class TikzPicture so that we may call methods on an instance
            position (tuple) : Pair of floats representing the center of the circle
            radius (float) : Length (in cm) of the radius
            options (str) : String containing the drawing options (e.g, "Blue")
        """

        def __init__(self, tikz_inst, center, radius, options):
            self.center = center
            self.radius = radius
            self.options = options

        @property
        def code(self):
            tikz_cmd = (
                f"\draw[{self.options}] {self.center} circle ({self.radius}cm);"
            )
            return tikz_cmd

        def shift(self, xshift, yshift):
            self.center = shift_coords([self.center], xshift, yshift)[0]

        def scale(self, scale):
            self.center = scale_coords([self.center], scale)

        def rotate(self, angle, about_pt, radians=False):
            self.center = rotate_coords([self.center], angle, about_pt, radians)[0]

        def __repr__(self):
            return self.code

    # Class for Nodes
    class Node:
        """
        A subclass of TikzPicture to create lines in the tikz environment

        Attributes :
            tikz_inst (TikzPicture) : An instance of the class TikzPicture so that we may call methods on an instance
            position (tuple) : Pair of floats representing the location of the node
            content (str): Text that will be displayed with the node; can use dollar signs $ for LaTeX
            options (str) : String containing node options (e.g., "above")
        """

        def __init__(self, tikz_inst, position, options, content):
            self.position = position
            self.content = content
            self.options = options

        @property
        def code(self):
            tikz_cmd = (
                f"\\node[{self.options}] at {self.position} {{ {self.content} }};"
            )
            return tikz_cmd

        def shift(self, xshift, yshift):
            self.position = shift_coords([self.position], xshift, yshift)

        def scale(self, scale):
            self.position = scale_coords([self.position], scale)

        def rotate(self, angle, about_pt, radians=False):
            self.position = rotate_coords([self.position], angle, about_pt, radians)[0]

        def __repr__(self):
            return self.code

    class Rectangle:
        """
        A subclass of TikzPicture to create lines in the tikz environment

        Attributes :
            tikz_inst (TikzPicture) : An instance of the class TikzPicture so that we may call methods on an instance
            left_corner (tuple) : Pair of floats representing the position of the bottom left corner
            right_corner (tuple) : Pair of floats representing the position of the upper right corner
            options (str) : String containing the drawing options, e.g, ("Blue")
        """

        def __init__(self, tikz_inst, left_corner, right_corner, options):
            self.left_corner = left_corner
            self.right_corner = right_corner
            self.options = options

        @property
        def code(self):
            tikz_cmd = f"\draw[{self.options}] {self.left_corner} rectangle {self.right_corner};"
            return tikz_cmd

        def __repr__(self):
            return self.code

    class Ellipse:
        """
        A subclass of TikzPicture to create lines in the tikz environment

        Attributes :
            tikz_inst (TikzPicture) : An instance of the class TikzPicture so that we may call methods on an instance
            position (tuple) : Pair of floats representing the center of the ellipse
            horiz_axis (float): The length (in cm) of the horizontal axis of the ellipse
            vert_axis (float): The length (in cm) of the vertical axis of the ellipse
        """

        def __init__(self, tikz_inst, position, horiz_axis, vert_axis):
            self.position = position
            self.horiz_axis = horiz_axis
            self.vert_axis = vert_axis

        @property
        def code(self):
            tikz_cmd = f"\draw {self.position} ellipse ({self.horiz_axis}cm and {self.vert_axis}cm);"
            return tikz_cmd

        def __repr__(self):
            return self.code

    class Arc:
        """
        A subclass of TikzPicture to create lines in the tikz environment

        Attributes :
            tikz_inst (TikzPicture) : An instance of the class TikzPicture so that we may call methods on an instance
            position (tuple) : Pair of points representing the relative center of the arc
            start_angle (float) : The angle (in degrees) of the start of the arc
            end_angle (float) : The angle (in degrees) of the end of the arc
            radius (float) : The radius (in cm) of the arc
        """

        def __init__(self, tikz_inst, position, start_angle, end_angle, radius):
            self.position = position
            self.start_angle = start_angle
            self.end_angle = end_angle
            self.radius = radius

        @property
        def code(self):
            tikz_cmd = f"\draw {self.position} arc ({self.start_angle}:{self.end_angle}:{self.radius}cm);"
            return tikz_cmd

        def __repr__(self):
            return self.code


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


# Collect xcolor names
colors = [
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
        (0, 0), (1, 1), options="thick, blue", control_pts=[(0.25, 0.25), (0.75, 0.75)]
    )
    # Plot
    plot = tikz.plot_coords(
        draw_options="green",
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
        assert plot.draw_options == "green"
        assert plot.plot_options == "smooth "
        assert plot.points == [(1, 1), (2, 2), (3, 3), (2, -4)]
        assert (
            plot.code
            == "\\draw[green] plot[smooth ] coordinates {(1, 1) (2, 2) (3, 3) (2, -4) };"
        )
        # Test Circle
        assert circle.position == (1, 1)
        assert circle.radius == 1
        assert circle.options == "fill = purple"
        assert circle.code == "\\draw[fill = purple] (1, 1) circle (1cm);"
        # Test Node
        assert node.position == (3, 3)
        assert node.content == "I love $ \sum_{x \in \mathbb{R}} f(x^2)$ !"
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
        assert ellipse.position == (0, 0)
        assert ellipse.horiz_axis == 3
        assert ellipse.vert_axis == 4
        assert ellipse.code == "\\draw (0, 0) ellipse (3cm and 4cm);"
        # Arc
        assert arc.position == (0, 0)
        assert arc.start_angle == 20
        assert arc.end_angle == 90
        assert arc.radius == 4
        assert arc.code == "\\draw (0, 0) arc (20:90:4cm);"
        print("flying colors!")
