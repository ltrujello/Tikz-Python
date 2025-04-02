from tikzpy import TikzPicture 
from tikzpy.drawing_objects.drawing_utils import calc_intersection

tikz = TikzPicture(center=True)

# Draw nodes A, B
A = tikz.node((0,0), options="left", text="$A$")
B = tikz.node((1.25, 0.25), options="right", text="$B$")

# Draw circle about A, B
AB_dist = A.position.distance(B.position) # Calc distance between A and B
circle_A = tikz.circle(A.position, radius=AB_dist)
circle_B = tikz.circle(B.position, radius=AB_dist)

# Calculate intersection points between two circles
intersections = calc_intersection(circle_A, circle_B)

# Draw nodes C, D, E
C = tikz.node(intersections[1], options="above", text="$C$")
C_prime = tikz.node(intersections[0], options="below", text="$C'$")
D = tikz.node(circle_A.west, text="$D$", options="left")
E = tikz.node(circle_B.east, text="$E$", options="right")

# Draw lines
line_a = tikz.line(A.position, B.position)
line_b = tikz.line(C.position, C_prime.position, options="red")

# Draw intersection
intersections = calc_intersection(line_a, line_b)
tikz.node(intersections[0], options="fill=red,inner sep=1pt")

tikz.show(quiet=False)

