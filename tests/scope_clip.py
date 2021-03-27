import sys
from itertools import combinations

sys.path.append("/Users/luketrujillo/Desktop/github/tikz-python")
from tikz_methods import *

tikz = TikzPicture()

# pts_one = [
#     (-1.5, -2.1),
#     (-1, -1.0),
#     (-1.4, 1.5),
#     (-0.5, 3.0),
#     (0.5, 2.0),
#     (0.75, 0.5),
#     (2.0, -0.0),
#     (2.5, -2.1),
#     (-1, -3),
# ]
# pts_two = [
#     (0.5, -3.5),
#     (2.5, -3.0),
#     (3.5, -1.5),
#     (2.5, 1.0),
#     (3.0, 3.5),
#     (-0.5, 3.5),
#     (-2.0, 2.0),
#     (-1.5, -0.5),
#     (-2.0, -3.0),
# ]
# pts_three = [
#     (-0.51303, -1.40954),
#     (-0.59767, 1.28),
#     (2.25, 3.5),
#     (1.75, 1),
#     (2, -1),
#     (0.25565, -2.22141),
# ]


def ven_diagram(blob1, blob2, blob3, show_outlines=False):
    # First we fill in blobs with some color
    tikz.draw(blob2, blob1, blob3)

    # We create various scope environments, performing clippings and drawings
    for j, blob_tuple in enumerate(
        [(blob1, blob2), (blob1, blob3), (blob2, blob3), (blob1, blob2, blob3)]
    ):
        scope = tikz.scope()

        for i, blob in enumerate(blob_tuple):
            blob_copy = blob.copy()
            if i != len(blob_tuple) - 1:
                scope.clip(blob_copy)
            else:
                blob_copy.options = f"fill = {rainbow_colors(j)}"
                scope.append(blob_copy)

    # We're done, draw the outline
    if show_outlines:
        blob1 = blob1.copy(options="", action="draw")
        blob2 = blob2.copy(options="", action="draw")
        blob3 = blob3.copy(options="", action="draw")

        tikz.draw(blob1, blob2, blob3)

    tikz.write()
    tikz.show()


def ven_diagram(blob1, blob2, blob3, blob4, show_outlines=False):
    # First we fill in blobs with some color
    tikz.draw(blob1, blob2, blob3, blob4)

    # We create various scope environments, performing clippings and drawings
    for j, blob_tuple in enumerate(
        [
            (blob1, blob2),
            (blob1, blob3),
            (blob1, blob4),
            (blob2, blob3),
            (blob2, blob4),
            (blob3, blob4),
            (blob1, blob2, blob3),
            (blob1, blob2, blob4),
            (blob1, blob3, blob4),
            (blob2, blob3, blob4),
            (blob1, blob2, blob3, blob4),
        ]
    ):
        scope = tikz.scope()

        for i, blob in enumerate(blob_tuple):
            blob_copy = blob.copy()
            if i != len(blob_tuple) - 1:
                scope.clip(blob_copy)
            else:
                blob_copy.options = f"fill = {rainbow_colors(j)}"
                scope.append(blob_copy)

    # We're done, draw the outline
    if show_outlines:
        blob1 = blob1.copy(options="", action="draw")
        blob2 = blob2.copy(options="", action="draw")
        blob3 = blob3.copy(options="", action="draw")
        blob4 = blob4.copy(options="", action="draw")
        tikz.draw(blob1, blob2, blob3, blob4)
    tikz.write()
    tikz.show()
