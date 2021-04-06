import pytest
import tikzpy
import math
from tikzpy.utils.transformations import (
    shift_coords,
    scale_coords,
    rotate_coords,
)

tikz = tikzpy.TikzPicture()
# Line
line = tikz.line((0, 0), (1, 1))
line.start = (-1, 2)
line.end = (4, 4)
line.options = "thick, blue"
line.to_options = "bend right = 45"
line.control_pts = [(0.5, 0.9), (1, -2)]
# Plot
plot = tikz.plot_coordinates(points=[(1, 1), (2, 2), (3, 3), (2, -4)])
plot.points = [(0, 0), (1, 0), (1, 1), (0, 1)]
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
rectangle.right_corner = (5, 5)
rectangle.options = "fill=purple!50"
# Ellipse
ellipse = tikz.ellipse((0, 0), 3, 4)
ellipse.center = (-1, 2)
ellipse.horiz_axis = 5
ellipse.vert_axis = 3
# Arc
arc = tikz.arc((0, 0), 20, 90, 4)
arc.center = (1, 1)
arc.start_angle = 45
arc.end_angle = 70
arc.radius = 2
arc.options = "fill = Blue!80"
arc.radians = True

drawing_objects = [line, plot, circle, node, rectangle, ellipse, arc]
transformed_drawing_objects = []

for draw_obj in drawing_objects:
    transformed = {}
    shifted = draw_obj.copy()
    shifted.shift(-2, 3)
    scaled = draw_obj.copy()
    scaled.scale(2)
    rotated = draw_obj.copy()
    rotated.rotate(3 * math.pi / 2, about_pt=(0, 0), radians=True)
    transformed[draw_obj] = [shifted, scaled, rotated]
