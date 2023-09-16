import tempfile
from pathlib import Path
from tikzpy import TikzPicture
from tikzpy.styles import arrows_along_path_style

code = r"""\begin{tikzpicture}[thick]
    \draw[arrows_along_path=red] plot[smooth, tension=.5, closed hobby] coordinates {(-3, -0.5) (-1, -1.5) (2, -1.5) (4, -1.5) (5, 0) (3, 2.4) (-1, 2.6) (-3, 2) };
    \draw[arrows_along_path=blue] (3, -0.3) circle (0.7cm);
    \draw[arrows_along_path=blue] (1.3, 1.3) circle (0.7cm);
    \draw[arrows_along_path=blue] (-0.4, -0.2) circle (0.7cm);
    \draw[arrows_along_path=blue] (-2, 1.1) circle (0.7cm);
    \draw[bend left, <-] (3.7, -0.5) to (4.6, -1);
    \draw[bend right, <-] (1.4, 0.6) to (2.3, -0.3);
    \draw[bend left, <-] (-0.25, 0.5) to (0.6, 1.4);
    \draw[bend left, <-] (-1.29, 1.1) to (-0.6, 0.46);
    \draw[bend left, ->] (-2.5, 1.6) to (-2.8, 2.15);
    \fill (3, -0.3) circle (0.05cm);
    \node[right] at (3, -0.3) { $a_1$ };
    \fill (1.3, 1.3) circle (0.05cm);
    \node[right] at (1.3, 1.3) { $a_2$ };
    \fill (-0.4, -0.2) circle (0.05cm);
    \node[right] at (-0.4, -0.2) { $a_3$ };
    \fill (-2, 1.1) circle (0.05cm);
    \node[right] at (-2, 1.1) { $a_4$ };
\end{tikzpicture}
"""


def test_cauchy_residue_example():
    tikz = TikzPicture()

    points = [
        (-3, -0.5),
        (-1, -1.5),
        (2, -1.5),
        (4, -1.5),
        (5, 0),
        (3, 2.4),
        (-1, 2.6),
        (-3, 2),
    ]

    tikz.add_styles(*arrows_along_path_style)
    tikz.options = "thick"

    # Draws the main boundary
    plot = tikz.plot_coordinates(
        options="arrows_along_path=red",
        plot_options="smooth, tension=.5, closed hobby",
        points=points,
        action="draw",
    )

    # Draws the inner circles
    singularity_1 = tikz.circle((3, -0.3), 0.7, "arrows_along_path=blue")
    singularity_2 = tikz.circle((1.3, 1.3), 0.7, "arrows_along_path=blue")
    singularity_3 = tikz.circle((-0.4, -0.2), 0.7, "arrows_along_path=blue")
    singularity_4 = tikz.circle((-2, 1.1), 0.7, "arrows_along_path=blue")

    # Draws the paths that connect the circles
    tikz.line((3.7, -0.5), (4.6, -1), options="bend left, <-")
    tikz.line((1.4, 0.6), (2.3, -0.3), options="bend right, <-")
    tikz.line((-0.25, 0.5), (0.6, 1.4), options="bend left, <-")
    tikz.line((-1.29, 1.1), (-0.6, 0.46), options="bend left, <-")
    tikz.line((-2.5, 1.6), (-2.8, 2.15), options="bend left, ->")

    # Draws and labels the points a_1, a_2, a_3, and a_4.
    for ind, singularity in enumerate(
        [singularity_1, singularity_2, singularity_3, singularity_4]
    ):
        tikz.circle(singularity.center, 0.05, action="fill")
        tikz.node(singularity.center, options="right", text=f"$a_{ind+1}$")

    with tempfile.NamedTemporaryFile() as fp:
        temp_path = Path(fp.name)
        tikz.compile(temp_path, quiet=True)

    assert str(tikz) == code
