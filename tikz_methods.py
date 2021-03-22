import math
import os
import subprocess
import webbrowser
from pathlib import Path


class TikzPicture:
    """
    A class for a Tikz picture environment.

    Attributes:
        tikz_file (str) : A file path to a desired destination to output the tikz code
        tex_file (str) : A file path to the TeX file which will accept the tikz code
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
        # TODO: figure out a ni ce way to implement scope
        # TODO: If self.options is empty, don't print empty brackets []
        # TODO: Figure out a good way to allow the user to color the tikzpictures by RGB values. Tikz does not support this
        #       and requires the user to manually define the color before using it, so this would save a lot of typing.

        # Create a Tikz Environment
        self.tikz_file = tikz_file
        self.tex_file = tex_file
        self.options = options
        self.center = center
        self._statements = {}

        # Check if the file destination for the Tikz output code exists
        if not os.path.exists(self.tikz_file):
            try:
                os.mkdir(self.tikz_file)
            except:
                print(f"Could not find or create file at {self.tikz_file}")

    @property
    def statements(self):
        """self.statements: A dictionary where
        keys : instances of subclasses created (e.g, Line)
        values : the Tikz code of the instance (e.g., Line.code)
        """
        print("Accessing statements")
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
        list_code.append(f"\\begin{{tikzpicture}}[{self.options}]\n")
        for draw_obj in self.statements:
            list_code.append("\t" + draw_obj.code + "\n")
        list_code.append(f"\\end{{tikzpicture}}\n")
        return list_code

    # Assemble tikz_code as a string (for output readability, see __repr__)
    @property
    def code(self):
        print("Writing code")
        code = ""
        for statement in self.list_statements:
            code += statement
        return code

    def __repr__(self):
        return self.code

    # Remove a code statement from the Tikz environment, e.g., a line
    def remove(self, draw_obj):
        del self._statements[draw_obj]

    # TODO: Manually add code to the Tikz Environment
    def add_statement(self, statement):
        self._statements[len(self._statements)] = statement

    # TODO: Write current Tikz code to the file. But, don't duplicate
    # the code already written there.
    def write(self):
        tex_code = self.code

        # Center the tikzpicture environment
        if self.center:
            tex_code = "\\begin{center}\n" + self.code + "\\end{center}\n"

        tex_file = open(self.tikz_file, "a+")
        tex_file.write(tex_code)
        tex_file.close()

    # TODO: Clear the code that was written to the Tikz file
    # Need to find the chunk of tikz_code in the tikz_file
    # This is potentially dangerous if the user is being careless with their own TeX code.
    # Perhaps make this method private, and don't advertise it.
    def clear(self):
        with open(tikz_file, "r+") as tikz_file:
            lines = tikz_file.readlines()

    # Display the current tikz drawing
    def show(self):
        if not os.path.exists(self.tex_file):
            with open("template/template_tex.tex") as template:
                lines = template.readlines()
                lines = [l for l in lines if "ROW" in l]
                lines = template.readlines()
                with open(self.tex_file, "w") as tex_file:
                    tex_file.writelines(lines)

        pdf_file = self.tex_file[:-4] + ".pdf"

        if not os.path.exists(pdf_file):
            subprocess.run(
                f"latexmk -pdf -pv {self.tex_file}",
                shell=True,
            )
        pdf_path = Path(pdf_file).resolve()
        webbrowser.open_new("file://" + str(pdf_path))

    """
        Methods to code objects in the Tikz Environment
    """

    def line(self, start, end, options="", control_pts=[]):
        line = TikzPicture.Line(self, start, end, options, control_pts)
        self._statements[line] = line.code
        return line

    def plot_coords(self, draw_options, plot_options, points):
        plot_coords = TikzPicture.PlotCoordinates(
            self, draw_options, plot_options, points
        )
        self._statements[plot_coords] = plot_coords.code
        return plot_coords

    def circle(self, position, radius, options=""):
        circle = TikzPicture.Circle(self, position, radius, options)
        self._statements[circle] = circle.code
        return circle

    def node(self, position, content, options=""):
        node = TikzPicture.Node(self, position, content, options)
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

        def shift(self, xshift, yshift):
            shifted = shift_coords([self.start, self.end], xshift, yshift)
            self.start = shifted[0]
            self.end = shifted[1]

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

        def __init__(self, tikz_inst, draw_options, plot_options, points):
            self.draw_options = draw_options
            self.plot_options = plot_options
            self.points = points

        @property
        def code(self):
            tikz_cmd = (
                f"\draw[{self.draw_options}] plot[{self.plot_options}] coordinates {{"
            )
            for pt in self.points:
                tikz_cmd += str(pt) + " "
            tikz_cmd += "};"
            return tikz_cmd

        def shift(self, xshift, yshift):
            self.points = shift_coords(self.points, xshift, yshift)

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

        def __init__(self, tikz_inst, position, radius, options):
            self.position = position
            self.radius = radius
            self.options = options

        @property
        def code(self):
            tikz_cmd = (
                f"\draw[{self.options}] {self.position} circle ({self.radius}cm);"
            )
            return tikz_cmd

        def shift(self, xshift, yshift):
            shifted_coords = shift_coords([self.position], xshift, yshift)
            self.position = shifted_coords[0]

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

        def __init__(self, tikz_inst, position, content, options):
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
            shifted_coords = shift_coords([self.position], xshift, yshift)
            self.position = shifted_coords[0]

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


""" Helper functions
"""


def shift_coords(coords, xshift, yshift):
    shifted_coords = []
    for coord in coords:
        x = coord[0]
        y = coord[1]

        shifted_x = round(x + xshift, 5)
        shifted_y = round(y + yshift, 5)
        shifted_coords.append((shifted_x, shifted_y))
    return shifted_coords


def scale_coords(coords, scale):
    scaled_coords = []
    for coord in coords:
        x = coord[0]
        y = coord[1]

        scale_x = round(scale * x, 5)
        scale_y = round(scale * y, 5)
        scaled_coords.append((scale_x, scale_y))
    return scaled_coords


def rotate_coords(coords, angle):  # rotate counterclockwise; angle is in degrees
    rotated_coords = []
    for coord in coords:
        x = coord[0]
        y = coord[1]

        rotated_x = round(
            x * math.cos(angle * (math.pi / 180))
            - y * math.sin(angle * (math.pi / 180)),
            5,
        )
        rotated_y = round(
            x * math.sin(angle * (math.pi / 180))
            + y * math.cos(angle * (math.pi / 180)),
            5,
        )

        rotated_coords.append((rotated_x, rotated_y))
    return rotated_coords


def shift_and_center_points(coords):
    x_mean = 0
    y_mean = 0
    for point in coords:
        x_mean += point[0]
        y_mean += point[1]

    x_mean /= len(coords)
    y_mean /= len(coords)

    return shift_coords(coords, -x_mean, -y_mean)


def rgb(r, g, b):
    # When calling rgb, it is necessary to specific "color = " or "fill =". This is
    # annoying aspect with Tikz.
    return f"{{ rgb,255:red, {r}; green, {g}; blue, {b} }}"


# Collect xcolor names
colors = []
try:
    with open("misc/xcolors_dvipsnames.txt") as f:
        lines = f.readlines()
        for line in lines:
            colors.append(line.split(",")[0])
except:
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

rainbow_colors = [
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