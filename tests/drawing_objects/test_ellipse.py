from tikzpy import TikzPicture, Ellipse, Point
import pytest

@pytest.fixture
def ellipse_from_tikzpicture():
    tikz = TikzPicture()
    ellipse = tikz.ellipse((0, 0), 3, 4, options="fill = purple")
    return ellipse

@pytest.fixture
def mock_ellipse():
    ellipse = Ellipse((0, 0), 3, 4, options="fill = purple")
    return ellipse

@pytest.mark.parametrize(
    "object", [
        "ellipse_from_tikzpicture",
        "mock_ellipse",
    ]
)
def test_ellipse_construction(object, request):
    ellipse = request.getfixturevalue(object)
    assert ellipse.center.x == 0
    assert ellipse.center.y == 0
    assert ellipse.x_axis == 3
    assert ellipse.y_axis == 4
    assert ellipse.options == "fill = purple"
    assert ellipse.code == r"\draw[fill = purple] (0, 0) ellipse (3cm and 4cm);"

def test_center_assignment(mock_ellipse):
    assert mock_ellipse.center == Point(0, 0)
    assert mock_ellipse.north == Point(0, 4)
    assert mock_ellipse.east == Point(3, 0)
    assert mock_ellipse.south == Point(0, -4)
    assert mock_ellipse.west == Point(-3, 0)

    mock_ellipse.center = (1, 1)
    assert mock_ellipse.center == Point(1, 1)
    assert mock_ellipse.north == Point(1, 5)
    assert mock_ellipse.east == Point(4, 1)
    assert mock_ellipse.south == Point(1, -3)
    assert mock_ellipse.west == Point(-2, 1)

def test_ellipse_shift(mock_ellipse):
    mock_ellipse.shift(1, 1)
    assert mock_ellipse.center == Point(1, 1)
    assert mock_ellipse.north == Point(1, 5)
    assert mock_ellipse.east == Point(4, 4)
    assert mock_ellipse.south == Point(1, -3)
    assert mock_ellipse.west == Point(-2, 1)

def test_ellipse_scale(mock_ellipse):
    mock_ellipse.scale(2)
    assert mock_ellipse.center == Point(0, 0)
    assert mock_ellipse.x_axis == 6
    assert mock_ellipse.y_axis == 8


