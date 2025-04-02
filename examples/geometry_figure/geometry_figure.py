import math
from tikzpy import TikzPicture, Point, Line
from tikzpy.drawing_objects.drawing_utils import calc_intersection


def draw_point(point, text, label_spacing = 0.3):
    tikz.circle(point, radius=0.05, options="fill=black")
    angle = ref_angle(Point(point))
    x_spacing = label_spacing * math.cos(math.radians(angle))
    y_spacing = label_spacing * math.sin(math.radians(angle))
    tikz.node(Point(point) + (x_spacing, y_spacing), text=text)

def ref_angle(point):
    return math.degrees(math.atan2(point.y, point.x))

def angle_between_lines(line_a, line_b):
    m1 = line_a.slope()
    m2 = line_b.slope()
    return math.degrees(math.atan(abs((m2 - m1) / (1 + m1 * m2))))

def arc_between_lines(line_a, line_b, radius):
    intersection = calc_intersection(line_a, line_b)[0]
    a = ref_angle(line_a.end - Point(intersection))
    b = angle_between_lines(line_a, line_b)
    tikz.arc(intersection, a, a + b, radius=radius, draw_from_start=False)

if __name__ == "__main__":
    radius = 3
    tikz = TikzPicture(center=True)
    circle = tikz.circle((0,0), radius)

    # Points on circumference
    A = circle.point_at_arg(110)
    B = circle.point_at_arg(315)
    C = circle.point_at_arg(70)
    D = circle.point_at_arg(215)

    lines = tikz.draw_segments([A, B, C, D])

    X = lines[(D, A)].pos_at_t(0.65)
    
    # Draw intersections
    intersections = calc_intersection(lines[(A, B)], lines[(C, D)])
    M = intersections[0]

    XM_line = tikz.line(X, M)
    intersections = calc_intersection(lines[(B, C)], XM_line)
    Y = intersections[0]

    MY_line = tikz.line(M, Y)
    intersections = calc_intersection(MY_line, circle)
    P, Q = intersections[0], intersections[1]
    tikz.line(P, X)
    tikz.line(Y, Q)

    # Arc between MY and MC
    arc_between_lines(MY_line, Line(M, C), 0.55)
    arc_between_lines(MY_line, Line(M, C), 0.5)

    # Arc between MA and MX
    arc_between_lines(Line(M, A), Line(M, X), 0.35)

    # Arc between MX and MD
    arc_between_lines(Line(M, X), Line(M, D), 0.55)
    arc_between_lines(Line(M, X), Line(M, D), 0.5)

    # Arc between DM and DX 
    arc_between_lines(Line(D, M), Line(D, X), 0.55)
    arc_between_lines(Line(D, M), Line(D, X), 0.5)

    # Arc between BY and BM 
    arc_between_lines(Line(B, Y), Line(B, M), 0.55)
    arc_between_lines(Line(B, Y), Line(B, M), 0.5)

    # Arc between MB and MY 
    arc_between_lines(Line(M, B), Line(M, Y), 0.35)

    # Draw points
    draw_point(A, "$A$",)
    draw_point(B, "$B$",)
    draw_point(C, "$C$",)
    draw_point(D, "$D$",)
    draw_point(X, "$X$",)
    draw_point(Y, "$Y$")
    draw_point(M, "$M$", label_spacing=0.5)
    draw_point(P, "$P$")
    draw_point(Q, "$Q$")

    tikz.show()




