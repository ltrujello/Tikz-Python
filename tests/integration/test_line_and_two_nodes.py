from tikzpy import TikzPicture
from tikzpy.colors import rainbow_colors

code = r"""\begin{tikzpicture}
    \draw[thick, blue, o-o] (0, 0) to (1, 1);
    \node[below] at (0, 0) { Start! };
    \node[above] at (1, 1) { End! };
\end{tikzpicture}
"""


def test_line_and_two_nodes():
    tikz = TikzPicture()
    line = tikz.line((0, 0), (1, 1), options="thick, blue, o-o")
    start_node = tikz.node(line.start, options="below", text="Start!")
    end_node = tikz.node(line.end, options="above", text="End!")

    assert str(tikz) == code
