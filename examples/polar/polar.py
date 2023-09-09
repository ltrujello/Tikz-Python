import numpy as np
from tikzpy import TikzPicture, PlotCoordinates, Circle
from tikzpy.colors import rainbow_colors
from tikzpy.utils.helpers import to_cartesian

def to_cartesian(r, ang):
    """Returns the cartesian coordinates of a polar point."""
    x = r * np.cos(ang)
    y = r * np.sin(ang)
    return x, y


if __name__ == "__main__":
    xy_plane = TikzPicture(options="thick")
    polar_plane = TikzPicture(options="thick")

    # XY_plane
    xy_plane.line((0, 0), (2 * np.pi, 0)).add_node(options="above", text="$x$")
    xy_plane.line((0, 0), (0, 2)).add_node(options="above", text="$y$")

    # Polar Plane: lines and concentric circles
    for ang in np.linspace(0, 2 * np.pi, 16):
        polar_plane.line((0, 0), to_cartesian(2.1, ang), options="Gray!30")

    for radius in [1, 1.5, 2]:
        polar_plane.circle((0, 0), radius=radius, options="Gray!30")

    # Sin curve and Cardioid
    sin_curve = xy_plane.plot_coordinates([], plot_options="smooth")
    cardioid = polar_plane.plot_coordinates([], plot_options="smooth")

    for ang in np.linspace(0, 2 * np.pi, 200):
        x, y = to_cartesian(1 + np.sin(ang), ang)
        sin_curve.add_point(ang, 1 + np.sin(ang))
        cardioid.add_point(x, y)

    # Rainbow points
    for ang in np.linspace(0, 2 * np.pi, 16):
        r = 1 + np.sin(ang)
        x, y = to_cartesian(r, ang)
        color = rainbow_colors(int(ang / (np.pi / 6)))
        xy_plane.circle((ang, r), radius=0.075, options=f"fill={color}", action="fill")
        polar_plane.circle((x, y), radius=0.075, options=f"fill={color}", action="fill")

    xy_plane.write()
    polar_plane.write()
    polar_plane.show()
