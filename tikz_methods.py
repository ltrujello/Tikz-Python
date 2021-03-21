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
        # Todo: improve unit tests
        # Todo: check if filename path exists
        # Todo: add an undo method for appending draw objects/tikz environments, but don't make it too powerful
        # Todo: figure out a nice way to implement scope

        # Create a Tikz Environment
        self.filename = filename
        self.options = options
        self.begin = "\\begin{tikzpicture}\n"
        self._statements = {}
        self.end = "\\end{tikzpicture}\n"

        if center == True:
            self.begin = "\\begin{center}\n" + "\t" + self.begin
            self.end = "\t" + self.end + "\\end{center}\n"

        if new_file == True:
            tex_file = open(filename, "w")
            tex_file.close

    def __repr__(self):
        return self.code

    @property
    def statements(self):
        print("accessing statements")
        statement_dict = {}
        for draw_obj in self._statements:
            statement_dict[draw_obj] = draw_obj.code
        return statement_dict

    @statements.setter
    def statements(self, draw_obj):
        print("Setting statements...")
        self._statements[draw_obj] = draw_obj.code

    @property
    def code(self):
        print("writing code")
        code = self.begin + "\n"
        for draw_obj in self.statements:
            code += draw_obj.code + "\n"
        code += self.end + "\n"
        return code

    def add_statement(self, statement):
        # Manually add code to the Tikz Environment
        self.statements[len(self.statements)] = statement

    def scope(self, statements):
        tikz_cmd = "\\begin{scope}\n"
        for statement in statements:
            tikz_cmd += "\t" + statement + "\n"
        tikz_cmd += "\\end{scope}\n"
        self.statements += [tikz_cmd]

    def write(self):
        tex_file = open(self.filename, "a+")
        tex_file.write(self.begin)

        for cmd in self.statements.values():
            tex_file.write("\t" + cmd + "\n")

        tex_file.write(self.end)
        tex_file.close()

    """
        Methods to code in the Tikz Environment
    """

    def line(self, start, end, options="", control_pts=[]):
        line = TikzStatement.Line(self, start, end, options, control_pts)
        self._statements[line] = line.code
        return line

    def plot_coords(self, draw_options, plot_options, points):
        plot_coords = TikzStatement.PlotCoordinates(
            self, draw_options, plot_options, points
        )
        self._statements[plot_coords] = plot_coords.code
        return plot_coords

    def circle(self, position, radius, options=""):
        circle = TikzStatement.Circle(self, position, radius, options)
        self._statements[circle] = circle.code
        return circle

    def node(self, position, content, options=""):
        node = TikzStatement.Node(self, position, content, options)
        self._statements[node] = node.code
        return node

    def rectangle(self, left_corner, right_corner, options=""):
        rectangle = TikzStatement.Rectangle(self, left_corner, right_corner, options)
        self._statements[rectangle] = rectangle.code
        return rectangle

    def ellipse(self, position, horiz_axis, vert_axis):
        ellipse = TikzStatement.Ellipse(self, position, horiz_axis, vert_axis)
        self._statements[ellipse] = ellipse.code
        return ellipse

    def arc(self, position, start_angle, end_angle, radius):
        arc = TikzStatement.Arc(self, position, start_angle, end_angle, radius)
        self._statements[arc] = arc.code
        return arc

    """
        Classes for drawing
    """

    # Class for Lines
    class Line:
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
            # self.tikz_inst.statements[self] = tikz_cmd # this actually helped!

            return tikz_cmd

        def __repr__(self):
            return self.code

    # Class for Plotting
    class PlotCoordinates:
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

        def __repr__(self):
            return self.code

    # Class for Circles
    class Circle:
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

        def __repr__(self):
            return self.code

    # Class for Nodes
    class Node:
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

        def __repr__(self):
            return self.code

    class Rectangle:
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

        tikz.write()
