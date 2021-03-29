import sys
import pytest

sys.path.append("/Users/luketrujillo/Desktop/github/tikz-python")
from tikz_methods import *

""" We test that our basic class constructors returns the correct Tikz code. 

    We can intialize classes via an instance of TikzPicture, or directly by using 
    a class constructor. Making sure that these are in sync relies on remembering to pair update 
    changes, which is not reliable. Further, when they are not in sync it becomes a hidden bug. Thus 
    it is good to check that these both work separately.
"""

# Initalize via a TikzPicture Class instance
tikz = TikzPicture()
# Line
tikz_line = tikz.line(
    (0, 0),
    (1, 1),
    options="thick, blue",
    control_pts=[(0.25, 0.25), (0.75, 0.75)],
)
# Plot
tikz_plot = tikz.plot_coordinates(
    options="green",
    plot_options="smooth ",
    points=[(1, 1), (2, 2), (3, 3), (2, -4)],
)
# Circle
tikz_circle = tikz.circle((1, 1), 1, options="fill = purple")
# Node
tikz_node = tikz.node(
    position=(3, 3),
    text=r"I love $ \sum_{x \in \mathbb{R}} f(x^2)$ !",
    options="above",
)
# Rectangle
tikz_rectangle = tikz.rectangle((2, 2), (3, 4), options="Blue")
# Ellipse
tikz_ellipse = tikz.ellipse((0, 0), 3, 4)
# Arc
tikz_arc = tikz.arc((0, 0), 20, 90, 4)


# Initalize via class constructors directly
line = Line(
    (0, 0),
    (1, 1),
    options="thick, blue",
    control_pts=[(0.25, 0.25), (0.75, 0.75)],
)
# Plot
plot = PlotCoordinates(
    options="green",
    plot_options="smooth ",
    points=[(1, 1), (2, 2), (3, 3), (2, -4)],
)
# Circle
circle = Circle((1, 1), 1, options="fill = purple")
# Node
node = Node(
    position=(3, 3),
    text=r"I love $ \sum_{x \in \mathbb{R}} f(x^2)$ !",
    options="above",
)
# Rectangle
rectangle = Rectangle((2, 2), (3, 4), options="Blue")
# Ellipse
ellipse = Ellipse((0, 0), 3, 4)
# Arc
arc = Arc((0, 0), 20, 90, 4)


@pytest.mark.order(1)
def test_attributes_assignments():
    """#1 : Test that class constructors via tikz work properly"""
    # Test Line
    assert tikz_line.start == (0, 0)
    assert tikz_line.end == (1, 1)
    assert tikz_line.options == "thick, blue"
    assert tikz_line.control_pts == [(0.25, 0.25), (0.75, 0.75)]
    assert (
        tikz_line.code
        == r"\draw[thick, blue] (0, 0) .. controls (0.25, 0.25) and (0.75, 0.75)  .. (1, 1);"
    )
    # Test Plot
    assert tikz_plot.options == "green"
    assert tikz_plot.plot_options == "smooth "
    assert tikz_plot.points == [(1, 1), (2, 2), (3, 3), (2, -4)]
    assert (
        tikz_plot.code
        == r"\draw[green] plot[smooth ] coordinates {(1, 1) (2, 2) (3, 3) (2, -4) };"
    )
    # Test Circle
    assert tikz_circle.center == (1, 1)
    assert tikz_circle.radius == 1
    assert tikz_circle.options == "fill = purple"
    assert tikz_circle.code == r"\draw[fill = purple] (1, 1) circle (1cm);"
    # Test Node
    assert tikz_node.position == (3, 3)
    assert tikz_node.text == r"I love $ \sum_{x \in \mathbb{R}} f(x^2)$ !"
    assert tikz_node.options == "above"
    assert (
        tikz_node.code
        == r"\node[above] at (3, 3) { I love $ \sum_{x \in \mathbb{R}} f(x^2)$ ! };"
    )
    # Rectangle
    assert tikz_rectangle.left_corner == (2, 2)
    assert tikz_rectangle.right_corner == (3, 4)
    assert tikz_rectangle.options == "Blue"
    assert tikz_rectangle.code == r"\draw[Blue] (2, 2) rectangle (3, 4);"
    # Ellipse
    assert tikz_ellipse.center == (0, 0)
    assert tikz_ellipse.horiz_axis == 3
    assert tikz_ellipse.vert_axis == 4
    assert tikz_ellipse.code == r"\draw (0, 0) ellipse (3cm and 4cm);"
    # Arc
    assert tikz_arc.center == (0, 0)
    assert tikz_arc.start_angle == 20
    assert tikz_arc.end_angle == 90
    assert tikz_arc.radius == 4
    assert tikz_arc.code == r"\draw (0, 0) arc (20:90:4cm);"

    """ Test that directly using the class constructors works properly. 
    """

    assert line.start == (0, 0)
    assert line.end == (1, 1)
    assert line.options == "thick, blue"
    assert line.control_pts == [(0.25, 0.25), (0.75, 0.75)]
    assert (
        line.code
        == r"\draw[thick, blue] (0, 0) .. controls (0.25, 0.25) and (0.75, 0.75)  .. (1, 1);"
    )
    # Test Plot
    assert plot.options == "green"
    assert plot.plot_options == "smooth "
    assert plot.points == [(1, 1), (2, 2), (3, 3), (2, -4)]
    assert (
        plot.code
        == r"\draw[green] plot[smooth ] coordinates {(1, 1) (2, 2) (3, 3) (2, -4) };"
    )
    # Test Circle
    assert circle.center == (1, 1)
    assert circle.radius == 1
    assert circle.options == "fill = purple"
    assert circle.code == r"\draw[fill = purple] (1, 1) circle (1cm);"
    # Test Node
    assert node.position == (3, 3)
    assert node.text == r"I love $ \sum_{x \in \mathbb{R}} f(x^2)$ !"
    assert node.options == "above"
    assert (
        node.code
        == r"\node[above] at (3, 3) { I love $ \sum_{x \in \mathbb{R}} f(x^2)$ ! };"
    )
    # Rectangle
    assert rectangle.left_corner == (2, 2)
    assert rectangle.right_corner == (3, 4)
    assert rectangle.options == "Blue"
    assert rectangle.code == r"\draw[Blue] (2, 2) rectangle (3, 4);"
    # Ellipse
    assert ellipse.center == (0, 0)
    assert ellipse.horiz_axis == 3
    assert ellipse.vert_axis == 4
    assert ellipse.code == r"\draw (0, 0) ellipse (3cm and 4cm);"
    # Arc
    assert arc.center == (0, 0)
    assert arc.start_angle == 20
    assert arc.end_angle == 90
    assert arc.radius == 4
    assert arc.code == r"\draw (0, 0) arc (20:90:4cm);"