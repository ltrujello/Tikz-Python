import tikzpy

tikz = tikzpy.TikzPicture(center=True)

for i in range(30):
    # i/30-th point on the unit circle
    point = (math.sin(2 * math.pi * i / 30), math.cos(2 * math.pi * i / 30))

    # Create four circles of different radii with center located at point
    tikz.circle(point, 2, "ProcessBlue")
    tikz.circle(point, 2.2, "ForestGreen")
    tikz.circle(point, 2.4, "red")  # xcolor Red is very ugly
    tikz.circle(point, 2.6, "Purple")

tikz.write()
tikz.show()