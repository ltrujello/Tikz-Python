import math
import os

class PathStatement:
    def __init__(self):
        self.tikz_statements = []

    def get_tikz_code(self):
        return self.tikz_statements

    def append_draw_statement(self, start, end, options = "", control_pts = []):
        if len(control_pts) == 0:
            tikz_cmd = f"\draw[{options}] {start} -- {end};"
        else:
            control_stmt = ".. controls "
            for pt in control_pts:
                control_stmt += f"{pt[0], pt[1]}" + " and "
            control_stmt = control_stmt[:-4] + " .." 
            tikz_cmd = f"\draw[{options}] {start} {control_stmt} {end};"
        
        self.tikz_statements += [tikz_cmd]

    def append_plot_coords(self, draw_options, plot_options, points):
        tikz_cmd = f"\draw[{draw_options}] plot[{plot_options}] coordinates {{"
        for pt in points:
            tikz_cmd += str(pt) + " "
        tikz_cmd += "};"
        self.tikz_statements += [tikz_cmd]

    def append_circle(self, options, position, radius):
        tikz_cmd = f"\draw[{options}] {position} circle ({radius}cm);"
        self.tikz_statements += [tikz_cmd]

    def append_node(self, options, position, contents):
        tikz_cmd = f"\\node[{options}] at {position} {{ {contents} }};"
        self.tikz_statements += [tikz_cmd]

    """ Nice wrapper functions below.
    """
    # A line
    def path_line(self, start, end, options = "",  control_pts = []):
        self.append_draw_statement(start, end, options, control_pts)

    # A list of points
    def path_plot_coords(self, draw_options = "", plot_options = "", points = []):
        self.append_plot_coords(draw_options, plot_options, points)

    # A circle
    def path_circle(self, position, radius, options = ""):
        self.append_circle(options, position, radius)

    # A node
    def path_node(self, options, position, contents = ""):
        self.append_node(options, position, contents)


""" Helper functions
"""

def shift_coords(coords, xshift, yshift):
    shifted_coords = []
    for coord in coords:
        x = coord[0]
        y = coord[1]

        shifted_x = round(x + xshift, 5)
        shifted_y = round(y + yshift, 5)
        shifted_coords.append( (shifted_x,shifted_y) )
    return shifted_coords

def scale_coords(coords, scale):
    scaled_coords = []
    for coord in coords:
        x = coord[0]
        y = coord[1]

        scale_x = round(scale*x, 5)
        scale_y = round(scale*y, 5) 
        scaled_coords.append( (scale_x, scale_y) )
    return scaled_coords

def rotate_coords(coords, angle): # rotate counterclockwise; angle is in degrees
    rotated_coords = []
    for coord in coords:
        x = coord[0]
        y = coord[1]

        rotated_x = round(x*math.cos(angle*(math.pi/180)) - y*math.sin(angle*(math.pi/180)), 5)
        rotated_y = round(x*math.sin(angle*(math.pi/180)) + y*math.cos(angle*(math.pi/180)), 5)

        rotated_coords.append( (rotated_x, rotated_y))
    return rotated_coords

def shift_and_center_points(coords):
    x_mean = 0
    y_mean = 0
    for point in coords:
        x_mean += point[0]
        y_mean += point[1]

    x_mean /= len(coords)
    y_mean /=len(coords)

    return shift_coords(coords, -x_mean, -y_mean)