from tikzpy import TikzPicture, Arc, Point
import pytest


@pytest.fixture
def arc_from_tikzpicture():
    tikz = TikzPicture()
    arc = tikz.arc((0, 0), 20, 90, 4)
    return arc


@pytest.fixture
def mock_arc():
    arc = Arc((0, 0), 20, 90, 4)
    return arc


@pytest.mark.parametrize(
    "object",
    [
        "arc_from_tikzpicture",
        "mock_arc",
    ],
)
def test_arc_construction(object, request):
    arc = request.getfixturevalue(object)
    assert arc.position.x == 0
    assert arc.position.y == 0
    assert arc.start_angle == 20
    assert arc.end_angle == 90
    assert arc.radius == 4
    assert (
        arc.code
        == r"\draw (0, 0) arc [start angle = 20, end angle = 90, radius = 4cm];"
    )
