import math
from tikzpy.drawing_objects.line import Line
from tikzpy.drawing_objects.circle import Circle


def line_connecting_circle_edges(circle_a: Circle, circle_b: Circle, options="", src_delta=0, dst_delta=0) -> Line:
    """
    Returns a line that connects the outer edges of circle_a
    to circle_b.
    """
    pos_a = circle_a.center
    pos_b = circle_b.center
    rad_a = circle_a.radius + src_delta
    rad_b = circle_b.radius + dst_delta

    start, end = calc_start_end_between_nodes(
        pos_a=pos_a, rad_a=rad_a, pos_b=pos_b, rad_b=rad_b
    )
    return Line(start, end, options=options)


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

def draw_segments(tikz, points, circular=True, options=""):
    """
    Given a list of points, draw a sequence of line segments between the points.
    Returns a dictionary collection of the lines for later modification if necessary.
    """
    idx = 0
    lines = {}
    while idx < len(points):
        if idx == len(points) - 1:
            if not circular:
                break
            first_pt = points[-1]
            second_pt = points[0]
        else:
            first_pt = points[idx]
            second_pt = points[idx + 1]

        line = tikz.line(first_pt, second_pt, options=options)
        lines[(first_pt, second_pt)] = line
        idx += 1
    return lines

def calc_intersection(item_a, item_b):
    intersection_map = {
        (Circle, Circle): circle_circle_intersection,
    }

    func = intersection_map.get((type(item_a), type(item_b)))
    if func:
        return func(item_a, item_b)
    else:
        raise NotImplementedError(f"No intersection logic for {type(item_a)} and {type(item_b)}")

def circle_circle_intersection(circle_a, circle_b):
    return _circle_circle_intersection(circle_a.center.x, circle_a.center.y, circle_a.radius, circle_b.center.x, circle_b.center.y, circle_b.radius)

def _circle_circle_intersection(x1, y1, r1, x2, y2, r2):
    # Distance between circle centers
    d = math.sqrt((x2 - x1) ** 2 + (y2 - y1) ** 2)
    
    # No solutions if circles are separate or one completely contains the other
    if d > r1 + r2 or d < abs(r1 - r2) or d == 0:
        return None  # No intersection

    # Find a and h for intersection calculations
    a = (r1 ** 2 - r2 ** 2 + d ** 2) / (2 * d)
    h = math.sqrt(r1 ** 2 - a ** 2)

    # Find the point P2, which is the base point of the perpendicular
    x3 = x1 + a * (x2 - x1) / d
    y3 = y1 + a * (y2 - y1) / d

    # Intersection points
    x_int1 = x3 + h * (y2 - y1) / d
    y_int1 = y3 - h * (x2 - x1) / d

    x_int2 = x3 - h * (y2 - y1) / d
    y_int2 = y3 + h * (x2 - x1) / d

    # One intersection if circles touch at one point, otherwise two
    if d == r1 + r2 or d == abs(r1 - r2):
        return [(x_int1, y_int1)]  
    return [(x_int1, y_int1), (x_int2, y_int2)]  


