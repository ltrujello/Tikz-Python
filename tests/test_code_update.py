import shutil
import tempfile
import pytest
from tikzpy import TikzPicture
from pathlib import Path
from tikzpy.utils.helpers import replace_code

# Run with: pytest -vv -s test_code_update.py
# The tests make sure the file input and update procedures work correctly.


@pytest.fixture()
def first_environment_text():
    return r"""
\begin{tikzpicture}
    \draw[thin, fill=orange!15] (0, 0) circle (3cm);
\end{tikzpicture}
"""


@pytest.fixture()
def second_environment_text():
    return r"""%!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!
\begin{tikzpicture}
    \draw[thin, fill=orange!15] (0, 0) circle (3cm);
\end{tikzpicture}
\begin{tikzpicture}
    \draw[fill, Green!20] (2, 2) ellipse (4cm and 2cm);
\end{tikzpicture}
"""


@pytest.fixture()
def third_environment_text():
    return r"""%!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!
\begin{tikzpicture}
    \draw[thin, fill=orange!15] (0, 0) circle (3cm);
\end{tikzpicture}
\begin{tikzpicture}
    \draw[fill, Green!20] (2, 2) ellipse (4cm and 2cm);
\end{tikzpicture}
\begin{tikzpicture}
    \draw[<->, thick, dashed] (4, 4) to (4, 0);
\end{tikzpicture}
"""


@pytest.fixture()
def expected_text_before_updating():
    return r"""%!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!
\begin{tikzpicture}
    \draw[fill=red] (0, 0) rectangle (3, 3);
\end{tikzpicture}
"""


@pytest.fixture()
def expected_text_after_updating():
    return r"""%!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!
\begin{tikzpicture}
    \draw[fill=red] (0, 0) rectangle (3, 3);
    \draw[Blue!40] (3, 3) arc [start angle = 20, end angle = 90, radius = 5cm];
\end{tikzpicture}
"""


@pytest.fixture()
def expected_text_multiple_envs():
    return r"""%!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!
\begin{tikzpicture}
    \draw[thin, fill=orange!15] (0, 0) circle (3cm);
\end{tikzpicture}
\begin{tikzpicture}
    \draw[fill, Green!20] (2, 2) ellipse (4cm and 2cm);
\end{tikzpicture}
\begin{tikzpicture}
    \draw[<->, thick, dashed] (4, 4) to (4, 0);
\end{tikzpicture}
"""


@pytest.fixture()
def expected_after_first_update_multiple_envs():
    return r"""%!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!
\begin{tikzpicture}
    \draw[thin, fill=orange!15] (0, 0) circle (3cm);
\end{tikzpicture}
\begin{tikzpicture}
    \draw[fill, Green!20, dashed] (2, 2) ellipse (4cm and 5cm);
    \draw (0, 0) rectangle (1, 1);
\end{tikzpicture}
\begin{tikzpicture}
    \draw[<->, thick, dashed] (4, 4) to (4, 0);
\end{tikzpicture}
"""


@pytest.fixture()
def expected_after_second_update_multiple_envs():
    return r"""%!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!
\begin{tikzpicture}
    \draw[thin, fill=orange!15] (0, 0) circle (3cm);
\end{tikzpicture}
\begin{tikzpicture}
    \draw[fill, Green!20, dashed] (2, 2) ellipse (4cm and 5cm);
    \draw (0, 0) rectangle (1, 1);
\end{tikzpicture}
\begin{tikzpicture}
    \draw[, ->, dashed] (4, 4) to (0, 4);
    \draw (0, 0) arc [start angle = 45, end angle = 90, radius = 2cm];
\end{tikzpicture}
"""


@pytest.fixture()
def expected_after_third_update_multiple_envs():
    return r"""
\begin{tikzpicture}
    \draw[thin, fill=orange!15] (0, 0) circle (1cm);
    \draw (2, 2) to (5, 5);
\end{tikzpicture}
\begin{tikzpicture}
    \draw[fill, Green!20, dashed] (2, 2) ellipse (4cm and 5cm);
    \draw (0, 0) rectangle (1, 1);
\end{tikzpicture}
\begin{tikzpicture}
    \draw[, ->, dashed] (4, 4) to (0, 4);
    \draw (0, 0) arc [start angle = 45, end angle = 90, radius = 2cm];
\end{tikzpicture}
"""


def test_updating_environment(
    expected_text_before_updating, expected_text_after_updating
):
    """Test that making a second change to a Tikz environment, after initially compiling, works correctly."""
    code_dir = Path("test_code_update") / "test_updating_environment"

    TikzPicture.NUM_TIKZS = 0
    with tempfile.TemporaryDirectory() as tmp_dir:
        tikz = TikzPicture(tikz_code_dir=tmp_dir)
        tikz.rectangle((0, 0), (3, 3), options="fill=red")
        tikz.write()

        assert tikz.tikz_file.read_text() == expected_text_before_updating

        # Now update the environment
        tikz.arc((3, 3), start_angle=20, end_angle=90, radius=5, options="Blue!40")
        tikz.write()

        assert tikz.tikz_file.read_text() == expected_text_after_updating


def test_creating_multiple_environments(
    first_environment_text, second_environment_text, third_environment_text
):
    """Test that we can create multiple independent tikz environments in the same process."""
    code_dir = Path("test_code_update") / "test_creating_multiple_environments"

    TikzPicture.NUM_TIKZS = 0
    with tempfile.TemporaryDirectory() as tmp_dir:
        # First environment
        first_tikz = TikzPicture(tikz_code_dir=tmp_dir)
        first_tikz.circle((0, 0), 3, options="thin, fill=orange!15")
        first_tikz.write()  # Writes the Tikz code into a file

        assert first_tikz._id == "@TikzPy__#id__==__(0)"
        assert first_tikz.tikz_file.read_text() == first_environment_text

        # Second environment
        second_tikz = TikzPicture(tikz_code_dir=tmp_dir)
        second_tikz.ellipse((2, 2), 4, 2, options="fill, Green!20")
        second_tikz.write()

        assert second_tikz._id == "@TikzPy__#id__==__(1)"
        assert second_tikz.tikz_file.read_text() == second_environment_text

        # Third environment
        third_tikz = TikzPicture(tikz_code_dir=tmp_dir)
        third_tikz.line((4, 4), (4, 0), options="<->, thick, dashed")
        third_tikz.write()

        assert third_tikz._id == "@TikzPy__#id__==__(2)"
        assert third_tikz.tikz_file.read_text() == third_environment_text


def test_updating_multiple_environments(
    expected_text_multiple_envs,
    expected_after_first_update_multiple_envs,
    expected_after_second_update_multiple_envs,
    expected_after_third_update_multiple_envs,
):
    """Test that we can independently update multiple tikz environments created in one process."""
    TikzPicture.NUM_TIKZS = 0
    with tempfile.TemporaryDirectory() as tmp_dir:
        code_dir = Path("test_code_update") / "test_updating_multiple_environments"

        # First environment
        first_tikz = TikzPicture(tikz_code_dir=tmp_dir)
        circle = first_tikz.circle((0, 0), 3, options="thin, fill=orange!15")
        first_tikz.write()

        # Second environment
        second_tikz = TikzPicture(tikz_code_dir=tmp_dir)
        ellipse = second_tikz.ellipse((2, 2), 4, 2, options="fill, Green!20")
        second_tikz.write()

        # Third environment
        third_tikz = TikzPicture(tikz_code_dir=tmp_dir)
        line = third_tikz.line((4, 4), (4, 0), options="<->, thick, dashed")
        third_tikz.write()

        # Now compile everything
        assert third_tikz.tikz_file.read_text() == expected_text_multiple_envs

        # Test updating second environment
        ellipse.y_axis = 5
        ellipse.options += ", dashed"
        second_tikz.rectangle((0, 0), (1, 1))
        second_tikz.write()
        assert (
            second_tikz.tikz_file.read_text()
            == expected_after_first_update_multiple_envs
        )

        # Test updating third environment
        line.end = (0, 4)
        line.options = ", ->, dashed"
        third_tikz.arc((0, 0), start_angle=45, end_angle=90, radius=2)
        third_tikz.write()
        assert (
            third_tikz.tikz_file.read_text()
            == expected_after_second_update_multiple_envs
        )

        # Test updating first environment
        circle.radius = 1
        first_tikz.line((2, 2), (5, 5))
        first_tikz.write()
        assert (
            first_tikz.tikz_file.read_text()
            == expected_after_third_update_multiple_envs
        )
