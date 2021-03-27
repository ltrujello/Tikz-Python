import sys

sys.path.append("/Users/luketrujillo/Desktop/github/tikz-python")
from tikz_methods import *

tikz = TikzPicture()

pts_one = [
    (-1.5, -2.1),
    (-1, -1.0),
    (-1.4, 1.5),
    (-0.5, 3.0),
    (0.5, 2.0),
    (0.75, 0.5),
    (2.0, -0.0),
    (2.5, -2.1),
    (-1, -3),
]
pts_two = [
    (0.5, -3.5),
    (2.5, -3.0),
    (3.5, -1.5),
    (2.5, 1.0),
    (3.0, 3.5),
    (-0.5, 3.5),
    (-2.0, 2.0),
    (-1.5, -0.5),
    (-2.0, -3.0),
]
pts_three = [
    (-0.51303, -1.40954),
    (-0.59767, 1.28),
    (2.25, 3.5),
    (1.75, 1),
    (2, -1),
    (0.25565, -2.22141),
]


def ven_diagram(pts_one, pts_two, pts_three):
    plot_options = "smooth, tension=.7, closed hobby"

    # First we fill in blobs with some color
    blob1 = PlotCoordinates(
        pts_one, options="red!60", plot_options=plot_options, action="fill"
    )
    blob2 = PlotCoordinates(
        pts_two, options="ProcessBlue!60", plot_options=plot_options, action="fill"
    )
    blob3 = PlotCoordinates(
        pts_three, options="Green!60", plot_options=plot_options, action="fill"
    )

    tikz.draw(blob2.copy(), blob1.copy(), blob3.copy())

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
    blob1 = PlotCoordinates(pts_one, plot_options=plot_options)
    blob2 = PlotCoordinates(pts_two, plot_options=plot_options)
    blob3 = PlotCoordinates(pts_three, plot_options=plot_options)

    tikz.draw(blob1, blob2, blob3)

    tikz.write()
    tikz.show()


ven_diagram(pts_one, pts_two, pts_three)