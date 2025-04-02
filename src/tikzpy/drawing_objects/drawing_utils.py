import math
from tikzpy.drawing_objects.line import Line
from tikzpy.drawing_objects.circle import Circle
from tikzpy.drawing_objects.point import Point


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
        (Line, Line): line_line_intersection,
        (Line, Circle): line_circle_intersection,
        (Circle, Line): circle_line_intersection,
    }

    func = intersection_map.get((type(item_a), type(item_b)))
    if func:
        return func(item_a, item_b)
    else:
        raise NotImplementedError(f"No intersection logic for {type(item_a)} and {type(item_b)}")

def circle_circle_intersection(circle_a, circle_b):
    intersections = _circle_circle_intersection(circle_a.center.x, circle_a.center.y, circle_a.radius, circle_b.center.x, circle_b.center.y, circle_b.radius)
    return [Point(pt) for pt in intersections]

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

def line_line_intersection(line_a, line_b):
    intersections = _line_line_intersection(
        line_a.start.x, line_a.start.y, 
        line_a.end.x, line_a.end.y, 
        line_b.start.x, line_b.start.y, 
        line_b.end.x, line_b.end.y
    )
    return [Point(pt) for pt in intersections]


def _line_line_intersection(x1, y1, x2, y2, x3, y3, x4, y4):
    # Compute coefficients A, B, C for both lines in form: Ax + By = C
    A1 = y2 - y1
    B1 = x1 - x2
    C1 = A1 * x1 + B1 * y1

    A2 = y4 - y3
    B2 = x3 - x4
    C2 = A2 * x3 + B2 * y3

    
    det = A1 * B2 - A2 * B1
    # Parallel lines
    if det == 0:
        return None  

    x = (C1 * B2 - C2 * B1) / det
    y = (A1 * C2 - A2 * C1) / det
    return [(x, y)]

def circle_line_intersection(circle, line):
    intersections = line_circle_intersection(line, circle)
    return [Point(pt) for pt in intersections]

def line_circle_intersection(line, circle):
    m = line.slope()
    b = line.y_intercept()
    h, k = circle.center  # Center of the circle
    r = circle.radius
    intersections = _line_circle_intersection(m, b, h, k, r)
    return [Point(pt) for pt in intersections]
    

def _line_circle_intersection(m, b, h, k, r):
    # Quadratic equation coefficients (Ax^2 + Bx + C = 0)
    A = 1 + m**2
    B = 2 * (m * (b - k) - h)
    C = h**2 + (b - k)**2 - r**2
    
    # Discriminant
    D = B**2 - 4 * A * C
    if D < 0:
        # No intersection
        return None 
    elif D == 0:
        # One intersection (tangent)
        x = -B / (2 * A)
        y = m * x + b
        return [(x, y)]
    
    sqrt_D = math.sqrt(D)
    x_1 = (-B + sqrt_D) / (2 * A)
    x_2 = (-B - sqrt_D) / (2 * A)
    y_1 = m * x_1 + b
    y_2 = m * x_2 + b
    
    return [(x_1, y_1), (x_2, y_2)]

