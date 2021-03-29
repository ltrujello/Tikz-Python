import math

""" Shifting, Scaling, and Rotating calculations called by above methods
"""


def shift_coords(coords, xshift, yshift):
    """Shift a list of 2D-coordinates by "xshift", "yshift". Accuracy to 7 decimal places for readability.
    coords (list) : A list of tuples (x, y) with x, y floats
    xshift (float) : An amount to shift the x values
    yshift (float) : An amount to shift the y values
    """

    shifted_coords = []
    for coord in coords:
        x = coord[0]
        y = coord[1]

        shifted_x = round(x + xshift, 7)
        shifted_y = round(y + yshift, 7)
        shifted_coords.append((shifted_x, shifted_y))
    return shifted_coords


def scale_coords(coords, scale):
    """Scale a list of 2D-coordinates by "scale". Accuracy to 7 decimal places for readability.
    coords (list) : A list of tuples (x, y) with x, y floats
    scale (float) : An amount to scale the x and y values
    """
    scaled_coords = []
    for coord in coords:
        x = coord[0]
        y = coord[1]

        scale_x = round(scale * x, 7)
        scale_y = round(scale * y, 7)
        scaled_coords.append((scale_x, scale_y))
    return scaled_coords


def rotate_coords(coords, angle, about_pt, radians=False):  # rotate counterclockwise
    """Rotate in degrees (or radians) a list of 2D-coordinates about the point "about_pt". Accuracy to 7 decimal places for readability.
    coords (list) : A list of tuples (x, y) with x, y floats
    angle (float) : The angle to rotate the coordinates
    about_pt (tuple) : A point (x,y) of reference for rotation
    radians (bool) : Specify type of angle (radians or degrees)
    """
    if not radians:
        angle *= math.pi / 180

    rotated_coords = []
    for coord in coords:
        x = coord[0]
        y = coord[1]

        # Shift by about_pt, so that rotation is now relative to that point
        x -= about_pt[0]
        y -= about_pt[1]

        # Rotate the points
        rotated_x = x * math.cos(angle) - y * math.sin(angle)
        rotated_y = x * math.sin(angle) + y * math.cos(angle)

        # Shift them back by about_pt, truncate the decimal places
        rotated_x += round(about_pt[0], 7)
        rotated_y += round(about_pt[1], 7)

        rotated_coords.append((rotated_x, rotated_y))
    return rotated_coords


def recenter_to_origin(coords):
    """Shifts a set of 2D points such that their centroid corresponds to the origin.
    This is useful for scaling: One may notice that scaling changes their (x,y) coordinates. Running this before
    scaling can allow them to relatively scale their figure such that the position of the figure does not change.
    """
    x_mean = 0
    y_mean = 0
    for point in coords:
        x_mean += point[0]
        y_mean += point[1]

    x_mean /= len(coords)
    y_mean /= len(coords)

    return shift_coords(coords, -x_mean, -y_mean)