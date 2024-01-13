import pytest
from tikzpy import TikzPicture, Point

""" #2
    We test that reassignment of attributes returns the correct Tikz code.
"""

tikz = TikzPicture()
# Line
line = tikz.line((0, 0), (1, 1))
line.start = (-1, 2)
line.end = (4, 4)
line.options = "thick, blue"
line.to_options = "bend right = 45"
line.control_pts = [(0.5, 0.9), (1, -2)]
# Plot
plot = tikz.plot_coordinates(points=[(1, 1), (2, 2), (3, 3), (2, -4)])
plot.points = [Point(0, 0), Point(1, 0), Point(1, 1), Point(0, 1)]
plot.options = "fill=green"
plot.plot_options = "smooth cycle"
# Circle
circle = tikz.circle((1, 1), 1)
circle.center = (2, 2)
circle.radius = 5
circle.options = "fill=purple"
# Node
node = tikz.node(position=(3, 3))
node.position = (4, 4)
node.text = r"Don't forget $+ C$ when $\int$!"
node.options = "below"
# Rectangle
rectangle = tikz.rectangle((2, 2), (3, 4))
rectangle.left_corner = (1, 1)
rectangle.width = 4
rectangle.height = 4
rectangle.options = "fill=purple!50"
# Ellipse
ellipse = tikz.ellipse((0, 0), 3, 4)
ellipse.center = (-1, 2)
ellipse.x_axis = 5
ellipse.y_axis = 3
# Arc
arc = tikz.arc((0, 0), 20, 90, 4)
arc.position = (1, 1)
arc.start_angle = 45
arc.end_angle = 70
arc.radius = 2
arc.options = "fill = Blue!80"
arc.radians = False


@pytest.mark.order(2)
def test_attribute_assignment():
    """#2 : Test that we may reset attributes of already existing class objects properly."""
    # Line
    assert line.start.x == -1
    assert line.start.y == 2
    assert line.end.x == 4
    assert line.end.y == 4
    assert line.options == "thick, blue"
    assert line.to_options == "bend right = 45"
    assert line.control_pts[0].x == 0.5
    assert line.control_pts[0].y == 0.9
    assert line.control_pts[1].x == 1
    assert line.control_pts[1].y == -2
    assert (
        line.code
        == r"\draw[thick, blue] (-1, 2) .. controls (0.5, 0.9) and (1, -2)  .. (4, 4);"
    )
    # Plot
    assert plot.points[0].x == 0
    assert plot.points[0].y == 0
    assert plot.points[1].x == 1
    assert plot.points[1].y == 0
    assert plot.points[2].x == 1
    assert plot.points[2].y == 1
    assert plot.points[3].x == 0
    assert plot.points[3].y == 1
    assert plot.options == "fill=green"
    assert plot.plot_options == "smooth cycle"
    assert (
        plot.code
        == r"\draw[fill=green] plot[smooth cycle] coordinates {(0, 0) (1, 0) (1, 1) (0, 1) };"
    )
    # Circle
    assert circle.center.x == 2
    assert circle.center.y == 2
    assert circle.radius == 5
    assert circle.options == "fill=purple"
    assert circle.code == r"\draw[fill=purple] (2, 2) circle (5cm);"
    # Node
    assert node.position.x == 4
    assert node.position.y == 4
    assert node.text == r"Don't forget $+ C$ when $\int$!"
    assert node.options == "below"
    assert node.code == r"\node[below] at (4, 4) { Don't forget $+ C$ when $\int$! };"
    # Rectangle
    assert rectangle.left_corner.x == 1
    assert rectangle.left_corner.y == 1
    assert rectangle.width == 4
    assert rectangle.height == 4
    assert rectangle.options == "fill=purple!50"
    assert rectangle.code == r"\draw[fill=purple!50] (1, 1) rectangle (5, 5);"
    # Ellipse
    assert ellipse.center.x == -1
    assert ellipse.center.y == 2
    assert ellipse.x_axis == 5
    assert ellipse.y_axis == 3
    assert ellipse.code == r"\draw (-1, 2) ellipse (5cm and 3cm);"
    # Arc
    assert arc.position.x == 1
    assert arc.position.y == 1
    assert arc.start_angle == 45
    assert arc.end_angle == 70
    assert arc.radius == 2
    assert arc.options == "fill = Blue!80"
    assert arc.radians == False
    assert (
        arc.code
        == r"\draw[fill = Blue!80] (1, 1) arc [start angle = 45, end angle = 70, radius = 2cm];"
    )
