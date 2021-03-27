import sys
from itertools import combinations

sys.path.append("/Users/luketrujillo/Desktop/github/tikz-python")
from tikz_methods import *

tikz = TikzPicture()


def ven_diagram(*blobs, show_outlines=False):
    """A function that takes in an arbitrary number of 2D blobs and intersects and colors every
    single  intersection area.
    """
    # First we fill in the blobs
    for blob in blobs:
        tikz.draw(blob)
    # Next we compute all of the intersections of the blobs we must make.
    tuple_indices = []
    for tuple_size in range(2, len(blobs) + 1):
        tuple_indices += list(combinations(range(1, len(blobs) + 1), tuple_size))

    # Now we clip and draw the blobs.
    for j, tuple_index in enumerate(tuple_indices):
        scope = tikz.scope()
        clip_draw_blobs = []
        for ind in tuple_index:
            clip_draw_blobs.append(blobs[ind - 1])

        # We create the scope environment
        scope = tikz.scope()
        # Now we clip and draw. We clip all the blobs except the last one, which we draw.
        for i, blob in enumerate(clip_draw_blobs):
            blob_copy = blob.copy()

            if i != len(clip_draw_blobs) - 1:
                scope.clip(blob_copy)
            else:
                blob_copy.options = f"fill = {rainbow_colors(j)}, opacity = 0.7"
                scope.append(blob_copy)

    # We're done, draw the outline
    if show_outlines:
        for blob in blobs:
            draw_blob = blob.copy(options="", action="draw")
            tikz.draw(draw_blob)
    tikz.write()
    tikz.show()


""" Initalize some drawings that we can test the function with.
"""

# Four specific circles
circle1 = Circle((0, 0), 2, options="purple, opacity = 0.7", action="fill")
circle2 = Circle((1, 0), 2, options="ProcessBlue, opacity = 0.7", action="fill")
circle3 = Circle((1, 1), 2, options="Magenta, opacity = 0.7", action="fill")
circle4 = Circle((0, 1), 2, options="ForestGreen, opacity = 0.7", action="fill")

# 9 rainbow circles
circles = []
for i in range(1, 4):
    for j in range(1, 4):
        circ = Circle(
            (i, j),
            1.5,
            options=f"fill = {rainbow_colors(i*j)}, fill opacity = 0.7",
            action="fill",
        )
        circles.append(circ)

# 9 rainbow rectangles
rectangles = []
for i in range(1, 4):
    for j in range(1, 4):
        rect = Rectangle(
            (i, j), (i + 3, j + 0.7), options=f"fill = {rainbow_colors(i*j)}"
        )
        rectangles.append(rect)

# A set of three plots
pts_one = [
    (-2.1, 1.5),
    (-1, 2.5),
    (1.5, 1),
    (4, 0.5),
    (3, -0.5),
    (2.5, -3),
    (0, -0.2),
    (-3, -2.5),
]


pts_two = [
    (-3.5, -0.5),
    (-3, -2.5),
    (-1.5, -3.5),
    (1, -2),
    (3.5, -2.5),
    (3.5, 0.5),
    (2, 2),
    (-0.5, -1.5),
    (-3, 2),
]

pts_three = [(-1.5, 0), (1, 1), (2, 0), (1, -1), (0, -2), (-2, -1)]

plot_options = "smooth, tension=.7, closed hobby"
blob1 = PlotCoordinates(
    pts_one, options="red!80", plot_options=plot_options, action="fill"
)
blob2 = PlotCoordinates(
    pts_two, options="ProcessBlue!80", plot_options=plot_options, action="fill"
)
blob3 = PlotCoordinates(
    pts_three, options="Green!80", plot_options=plot_options, action="fill"
)
