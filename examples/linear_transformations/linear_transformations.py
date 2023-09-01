import numpy as np
from tikzpy import TikzPicture
from tikzpy.colors import rainbow_colors

""" Plots the image of a 3 x 2 matrix in R^3 acting on R^2. 
    Vectors in R^3 which lie below the positive Z-axis are drawn with lower opacity to aid the eye.

    Usage: Plug a 3x2 numpy array into plot_linear_transformation. 
        Ex: 
            >>> matrix = np.array([[0, 1], [1, 1], [0, 1]])
            >>> plot_linear_transformation(matrix)
        
            >>> matrix = np.array([[2, 0], [1, 1], [1, 1]])
            >>> plot_linear_transformation(matrix)
        
            >>> matrix = np.array([[2, 0], [1, 0], [1, 1]])
            >>> plot_linear_transformation(matrix)
        etc. 
"""


def build_scene():
    """Creates a Tikz Environment with two scope environments displayed side by side.
    The left scope environment displays R^2, while the right scope environment displays R^3.
    """
    tikz = TikzPicture(options=">=stealth")

    # xy plane
    xy_plane = tikz.scope(options="xshift=-8cm")  # 2D plane
    axis_len = 2.5  # 2D axes length
    xy_plane.line((-axis_len, 0), (axis_len, 0)).add_node(
        options="right, ->", text="$x$"
    )  # X axis
    xy_plane.line((0, -axis_len), (0, axis_len)).add_node(
        options="above, ->", text="$y$"
    )  # Y axis

    # xyz space
    tikz.set_tdplotsetmaincoords(60, 110)  # 3D perspective
    xyz_space = tikz.scope("tdplot_main_coords")
    O_xyz = (0, 0, 0)  # 3D origin
    axis_len = 5  # 3D axes length
    X = (axis_len, 0, 0)
    Y = (0, axis_len - 1, 0)
    Z = (0, 0, axis_len - 2)
    # X, Y, Z axes
    xyz_space.line(O_xyz, X).add_node(options="below, ->", text="$x$")  # X axis
    xyz_space.line(O_xyz, Y).add_node(options="right, ->", text="$y$")  # Y axis
    xyz_space.line(O_xyz, Z).add_node(options="above, ->", text="$z$")  # Z axis

    return tikz, xy_plane, xyz_space


# Main function
def plot_linear_transformation(matrix, num_vecs=40):
    """Plots a list of vectors in 2D and then displays their matrix product in 3D."""

    tikz, xy_plane, xyz_space = build_scene()
    O_xy = (0, 0)  # 2D origin
    O_xyz = (0, 0, 0)  # 3D origin

    for i in np.linspace(0, 2 * np.pi, num_vecs):
        i_x = 2 * np.cos(i)
        i_y = 2 * np.sin(i)
        color = "color=" + rainbow_colors(int(i / (2 * np.pi) * num_vecs))
        xy_plane.line(O_xy, (i_x, i_y), options=f"->, {color}")

        M = tuple(np.matmul(matrix, np.array([i_x, i_y])))  # The matrix calculation

        vec = xyz_space.line(O_xyz, M, options=f"->, {color}")
        if M[2] < 0:  # If the Z-coordinate is negative, color it with low opacity
            vec.options += ", opacity=0.2"

    tikz.show()

if __name__ == "__main__":
    matrix = np.array([[2, 0], [1, 1], [1, 1]])
    plot_linear_transformation(matrix)
