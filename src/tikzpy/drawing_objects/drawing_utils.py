import math
from tikzpy.drawing_objects.line import Line
from tikzpy.drawing_objects.circle import Circle


def line_connecting_circle_edges(circle_a: Circle, circle_b: Circle) -> Line:
    """
    Returns a line that connects the outer edges of circle_a
    to circle_b.
    """
    pos_a = circle_a.center
    pos_b = circle_b.center
    rad_a = circle_a.radius
    rad_b = circle_b.radius

    start, end = calc_start_end_between_nodes(
        pos_a=pos_a, rad_a=rad_a, pos_b=pos_b, rad_b=rad_b
    )
    return Line(start, end)


def calc_start_end_between_nodes(pos_a, rad_a, pos_b, rad_b):
    """
    Given two circles A and B with
    - coordinates pos_a, pos_b
    - radii rad_a, rad_b
    return the start and end coordinates of the shortest
    line that connects A and B.
    """
    x_1, y_1 = pos_a
    x_2, y_2 = pos_b

    # Determine the angle between the points
    if y_1 - y_2 == 0:
        theta = math.pi / 2
    else:
        theta = math.atan(abs(x_2 - x_1) / abs(y_1 - y_2))

    # Use the angle and relative sign of the coordinates to calculate x, y positions
    if y_2 > y_1:
        if x_2 > x_1:
            start = (x_1 + rad_a * math.sin(theta), y_1 + rad_a * math.cos(theta))
            end = (x_2 - rad_b * math.sin(theta), y_2 - rad_b * math.cos(theta))
        else:
            start = (x_1 - rad_a * math.sin(theta), y_1 + rad_a * math.cos(theta))
            end = (x_2 + rad_b * math.sin(theta), y_2 - rad_b * math.cos(theta))
    else:
        if x_2 > x_1:
            start = (x_1 + rad_a * math.sin(theta), y_1 - rad_a * math.cos(theta))
            end = (x_2 - rad_b * math.sin(theta), y_2 + rad_b * math.cos(theta))
        else:
            start = (x_1 - rad_a * math.sin(theta), y_1 - rad_a * math.cos(theta))
            end = (x_2 + rad_b * math.sin(theta), y_2 + rad_b * math.cos(theta))
    return start, end
