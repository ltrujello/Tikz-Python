import math
import os


class TikzStatement:
    def __init__(
        self,
        filename="tikz_code/tikz-code.tex",
        new_file=False,
        center=False,
        options="",
    ):
        """Example:
        LaTeX:
            \begin{tikzpicture}
            \end{tikzpicture}
        Python:
            tikz = TikzStatement()
        """

        # Create a Tikz Environment
        self.filename = filename
        self.options = options
        self.begin = "\\begin{tikzpicture}\n"
        self.tikz_statements = []
        self.end = "\\end{tikzpicture}\n"

        if new_file == True:
            tex_file = open(filename, "w")
            tex_file.close

        if center == True:
            self.begin = "\\begin{center}\n" + "\t" + self.begin
            self.end = "\t" + self.end + "\\end{center}\n"

    def __repr__(self):
        return self.get_code()

    def add_statement(self, statements):
        # Adds code to the Tikz Environment
        for statement in statements:
            self.tikz_statements.append(statement)

    def write_tikz_code(self):
        code = self.begin + "\n"
        for cmd in self.tikz_statements:
            code += cmd + "\n"
        code += self.end + "\n"
        return code

    def scope(self, statements):
        tikz_cmd = "\\begin{scope}\n"
        for statement in statements:
            tikz_cmd += "\t" + statement + "\n"
        tikz_cmd += "\\end{scope}\n"
        self.tikz_statements += [tikz_cmd]

    def write(self):
        tex_file = open(self.filename, "a+")
        tex_file.write(self.begin)

        for cmd in self.tikz_statements:
            tex_file.write("\t" + cmd + "\n")

        tex_file.write(self.end)
        tex_file.close()

    """
        Methods to code in the Tikz Environment
    """

    def draw_line(self, start, end, options="", control_pts=[]):
        return TikzStatement.Line(self, start, end, options, control_pts)

    def draw_plot_coords(self, draw_options, plot_options, points):
        return TikzStatement.PlotCoords(self, draw_options, plot_options, points)

    def draw_circle(self, position, radius, options=""):
        return TikzStatement.Circle(self, position, radius, options)

    def draw_node(self, position, content, options=""):
        return TikzStatement.Node(self, position, content, options)

    def draw_rectangle(self, left_corner, right_corner, options=""):
        return TikzStatement.Rectangle(self, left_corner, right_corner, options)

    def draw_ellipse(self, position, horiz_axis, vert_axis):
        return TikzStatement.Ellipse(self, position, horiz_axis, vert_axis)

    def draw_arc(self, position, start_angle, end_angle, radius):
        return TikzStatement.Arc(self, position, start_angle, end_angle, radius)

    """
        Classes for drawing
    """

    # Class for Lines
    class Line:
        """Example:
        LaTeX:
            \draw[thick, blue] (0,0) -- (1,1);
        Python:
            tikz.draw_line( (0,0), (1,1), options = "thick, blue")
        """

        def __init__(self, tikz_inst, start, end, options, control_pts):
            self.tikz_inst = tikz_inst
            self.start = start
            self.end = end
            self.options = options
            self.control_pts = control_pts
            self.code = self.create_draw_statement()
            tikz_inst.add_statement([self.code])  # May want to be dependent on if/else?

        def create_draw_statement(self):
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

        def __repr__(self):
            return self.code

    # Class for Plotting
    class PlotCoords:
        """Ex
        LaTeX:
            \draw plot[smooth cycle] coordinates {(4.9, 9) (3.7, 8.3) (2.3, 8.5) };
        Python:
            points = [(4.9, 9), (3.7, 8.3), (2.3, 8.5)]
            tikz.draw_plot_coords(draw_options = "Red", plot_options = "smooth cycle", points = points)
        """

        def __init__(self, tikz_inst, draw_options, plot_options, points):
            self.draw_options = draw_options
            self.plot_options = plot_options
            self.points = points
            self.code = self.create_plot_statement()
            tikz_inst.add_statement([self.code])

        def create_plot_statement(self):
            tikz_cmd = (
                f"\draw[{self.draw_options}] plot[{self.plot_options}] coordinates {{"
            )
            for pt in self.points:
                tikz_cmd += str(pt) + " "
            tikz_cmd += "};"
            return tikz_cmd

        def __repr__(self):
            return self.code

    # Class for Circles
    class Circle:
        """Ex
        LaTeX:
            \draw[fill = blue] (0,0) circle (2cm);
        Python:
            tikz.draw_circle( (0,0), 2, options = "fill = blue")
        """

        def __init__(self, tikz_inst, position, radius, options):
            self.position = position
            self.radius = radius
            self.options = options
            self.code = self.create_circle_statement()
            tikz_inst.add_statement([self.code])

        def create_circle_statement(self):
            tikz_cmd = (
                f"\draw[{self.options}] {self.position} circle ({self.radius}cm);"
            )
            return tikz_cmd

        def __repr__(self):
            return self.code

    # Class for Nodes
    class Node:
        """Example:
        LaTeX:
            \node[above] at (0,0) {I am a node!};
        Python:
            tikz.node((0,0), "I am a node!", "above")
        """

        def __init__(self, tikz_inst, position, content, options):
            self.position = position
            self.content = content
            self.options = options
            self.code = self.create_node_statement()
            tikz_inst.add_statement([self.code])

        def create_node_statement(self):
            tikz_cmd = (
                f"\\node[{self.options}] at {self.position} {{ {self.content} }};"
            )
            return tikz_cmd

        def __repr__(self):
            return self.code

    class Rectangle:
        """Example:
        LaTeX:
            \draw[blue] (0,0) rectangle (5, 6);
        Python:
            tikz.rectangle( (0,0), (5,6), options = "Blue")
        """

        def __init__(self, tikz_inst, left_corner, right_corner, options):
            self.left_corner = left_corner
            self.right_corner = right_corner
            self.options = options
            self.code = self.create_rectangle_statement()
            tikz_inst.add_statement([self.code])

        def create_rectangle_statement(self):
            tikz_cmd = f"\draw[{self.options}] {self.left_corner} rectangle {self.right_corner};"
            return tikz_cmd

        def __repr__(self):
            return self.code

    class Ellipse:
        """Example:
        LaTeX:
            \draw (0,0) ellipse (2cm and 4cm)
        Python:
            tikz.ellipse( (0,0), 2, 4)
        """

        def __init__(self, tikz_inst, position, horiz_axis, vert_axis):
            self.position = position
            self.horiz_axis = horiz_axis
            self.vert_axis = vert_axis
            self.code = self.create_ellipse_statement()
            tikz_inst.add_statement([self.code])

        def create_ellipse_statement(self):
            tikz_cmd = f"\draw {self.position} ellipse ({self.horiz_axis}cm and {self.vert_axis}cm);"
            return tikz_cmd

        def __repr__(self):
            return self.code

    class Arc:
        """Example:
        LaTeX:
            \draw (1,1) arc (45:90:5cm)
        Python:
            tikz.arc( (1,1), 45, 90, 5)
        """

        def __init__(self, tikz_inst, position, start_angle, end_angle, radius):
            self.position = position
            self.start_angle = start_angle
            self.end_angle = end_angle
            self.radius = radius
            self.code = self.create_arc_statement()
            tikz_inst.add_statement([self.code])

        def create_arc_statement(self):
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


# def compile(filname = "tikz-code.tex"):

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
    "red",
    "Orange",
    "BurntOrange",
    "Yellow",
    "Green",
    "ForestGreen",
    "ProcessBlue",
    "Blue",
    "Plum",
]

if __name__ == "__main__":
    """Quick sanity tests for our classes."""

    tikz = TikzStatement(new_file=True)
    # Line
    line = tikz.draw_line(
        (0, 0), (1, 1), options="thick, blue", control_pts=[(0.25, 0.25), (0.75, 0.75)]
    )
    # Plot
    plot = tikz.draw_plot_coords(
        draw_options="green",
        plot_options="smooth ",
        points=[(1, 1), (2, 2), (3, 3), (2, -4)],
    )
    # Circle
    circle = tikz.draw_circle((1, 1), 1, options="fill = purple")
    # Node
    node = tikz.draw_node(
        position=(3, 3),
        content="I love $ \sum_{x \in \mathbb{R}} f(x^2)$ !",
        options="above",
    )
    # Rectangle
    rectangle = tikz.draw_rectangle((2, 2), (3, 4), options="Blue")
    # Ellipse
    ellipse = tikz.draw_ellipse((0, 0), 3, 4)
    # Arc
    arc = tikz.draw_arc((0, 0), 20, 90, 4)

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

    tikz.write()
