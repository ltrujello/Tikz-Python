from tikzpy import TikzPicture, Line, Point
import pytest


@pytest.fixture
def tikz_line_from_tikzpicture():
    tikz = TikzPicture()
    line = tikz.line(
        (0, 0),
        (1, 1),
        options="thick, blue",
        control_pts=[(0.25, 0.25), (0.75, 0.75)],
    )
    return line


@pytest.fixture
def tikz_line():
    line = Line(
        (0, 0),
        (1, 1),
        options="thick, blue",
        control_pts=[(0.25, 0.25), (0.75, 0.75)],
    )
    return line


@pytest.fixture
def line_simple():
    line = Line((0, 0), (1, 1))
    return line


@pytest.mark.parametrize(
    "object",
    [
        "tikz_line_from_tikzpicture",
        "tikz_line",
    ],
)
def test_line_construction(object, request):
    line = request.getfixturevalue(object)
    assert line.start.x == 0
    assert line.start.y == 0
    assert line.end.x == 1
    assert line.end.y == 1
    assert line.options == "thick, blue"
    assert line.control_pts[0].x == 0.25
    assert line.control_pts[0].y == 0.25
    assert line.control_pts[1].x == 0.75
    assert line.control_pts[1].y == 0.75
    assert (
        line.code
        == r"\draw[thick, blue] (0, 0) .. controls (0.25, 0.25) and (0.75, 0.75)  .. (1, 1);"
    )


def test_line_point_assignment():
    line = Line((0, 0), (1, 1))
    line.start = (1, 2)
    line.end = (3, 4)
    assert line.start.x == 1
    assert line.start.y == 2
    assert line.end.x == 3
    assert line.end.y == 4
    assert line.code == r"\draw (1, 2) to (3, 4);"


def test_line_scale(line_simple):
    new_line = line_simple.scale(4)
    assert new_line.start == Point(0, 0)
    assert new_line.end == Point(4, 4)


def test_line_scale(line_simple):
    new_line = line_simple.shift(1, 1)
    assert new_line.start == Point(1, 1)
    assert new_line.end == Point(2, 2)
