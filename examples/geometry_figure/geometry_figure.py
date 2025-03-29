import math
from tikzpy import TikzPicture, Point


def draw_segements(points, circular=True):
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

        line = tikz.line(first_pt, second_pt)
        lines[(first_pt, second_pt)] = line
        idx += 1

    return lines

def line_intersection(line_a, line_b):
    return intersection_point(
        line_a.start.x, line_a.start.y, 
        line_a.end.x, line_a.end.y, 
        line_b.start.x, line_b.start.y, 
        line_b.end.x, line_b.end.y
    )

def line_circle_intersection(line, circle):
    m = line.slope()
    b = line.y_intercept()
    r = circle.radius

    x_1 = -m*b + math.sqrt((r - b)*(r + b) + m**2 * r**2) / (1 + m**2)
    x_2 = -m*b - math.sqrt((r - b)*(r + b) + m**2 * r**2) / (1 + m**2)

    y_1 = m * x_1 + b
    y_2 = m * x_2 + b

    return (x_1, y_1), (x_2, y_2)


def intersection_point(x1, y1, x2, y2, x3, y3, x4, y4):
    # Compute coefficients A, B, C for both lines in form: Ax + By = C
    A1 = y2 - y1
    B1 = x1 - x2
    C1 = A1 * x1 + B1 * y1

    A2 = y4 - y3
    B2 = x3 - x4
    C2 = A2 * x3 + B2 * y3

    # Determinant (denominator)
    det = A1 * B2 - A2 * B1

    if det == 0:
        return None  # Lines are parallel (should not happen per function assumption)

    # Solve for x and y
    x = (C1 * B2 - C2 * B1) / det
    y = (A1 * C2 - A2 * C1) / det

    return (x, y)


def draw_point(point, text):
    tikz.circle(point, radius=0.05, options="fill=black")
    label_spacing = .3
    angle = ref_angle(Point(point))
    x_spacing = label_spacing * math.cos(math.radians(angle))
    y_spacing = label_spacing * math.sin(math.radians(angle))
    tikz.node(Point(point) + (x_spacing, y_spacing), text=text)

def ref_angle(point):
    return math.degrees(math.atan2(point.y, point.x))

if __name__ == "__main__":
    radius = 3
    tikz = TikzPicture()
    circle = tikz.circle((0,0), radius)

    A = circle.point_at_arg(110)
    B = circle.point_at_arg(315)
    C = circle.point_at_arg(70)
    D = circle.point_at_arg(215)

    lines = draw_segements([A, B, C, D])

    X = lines[(D, A)].pos_at_t(0.65)
    M = line_intersection(lines[(A, B)], lines[(C, D)])

    XM_line = tikz.line(X, M)
    Y = line_intersection(lines[(B, C)], XM_line)

    XM_line = tikz.line(M, Y)
    P, Q = line_circle_intersection(XM_line, circle)
    tikz.line(P, X)
    tikz.line(Y, Q)

    draw_point(A, "$A$",)
    draw_point(B, "$B$",)
    draw_point(C, "$C$",)
    draw_point(D, "$D$",)
    draw_point(X, "$X$",)
    draw_point(Y, "$Y$")
    draw_point(M, "$M$")
    draw_point(P, "$P$")
    draw_point(Q, "$Q$")

    tikz.show()




