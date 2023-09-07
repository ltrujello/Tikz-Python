from tikzpy import TikzPicture

code = r"""\begin{tikzpicture}
    \draw[thin, fill=orange!15] (0, 0) circle (3cm);
    \draw[dashed] (3, 0) arc [start angle = 0.0, end angle = 179.99999999999997, x radius = 3cm, y radius = 1.5cm];
    \draw (-3, 0) arc [start angle = 179.99999999999997, end angle = 359.99999999999994, x radius = 3cm, y radius = 1.5cm];
\end{tikzpicture}
"""


def test_basic_circle_example():
    tikz = TikzPicture()
    tikz.circle((0, 0), 3, options="thin, fill=orange!15")

    arc_one = tikz.arc((3, 0), 0, 180, x_radius=3, y_radius=1.5, options=f"dashed")
    arc_two = tikz.arc((-3, 0), 180, 360, x_radius=3, y_radius=1.5)

    assert str(tikz) == code
