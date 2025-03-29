from tikzpy import TikzPicture, Circle, Point
import pytest


@pytest.fixture
def circle_from_tikzpicture():
    tikz = TikzPicture()
    circle = tikz.circle((1, 1), 1, options="fill = purple")
    return circle


@pytest.fixture
def mock_circle():
    circle = Circle((1, 1), 1, options="fill = purple")
    return circle


@pytest.mark.parametrize(
    "object",
    [
        "circle_from_tikzpicture",
        "mock_circle",
    ],
)
def test_circle_construction(object, request):
    circle = request.getfixturevalue(object)
    assert circle.center.x == 1
    assert circle.center.y == 1
    assert circle.radius == 1
    assert circle.options == "fill = purple"
    assert circle.code == r"\draw[fill = purple] (1, 1) circle (1cm);"


def test_center_assignment(mock_circle):
    assert mock_circle.center == Point(1, 1)
    assert mock_circle.north == Point(1, 2)
    assert mock_circle.east == Point(2, 1)
    assert mock_circle.south == Point(1, 0)
    assert mock_circle.west == Point(0, 1)

    mock_circle.center = (3, 4)
    assert mock_circle.center == Point(3, 4)
    assert mock_circle.north == Point(3, 5)
    assert mock_circle.east == Point(4, 4)
    assert mock_circle.south == Point(3, 3)
    assert mock_circle.west == Point(2, 4)


def test_circle_shift(mock_circle):
    new_circle = mock_circle.shift(1, 1)
    assert new_circle.center == Point(2, 2)
    assert new_circle.north == Point(2, 3)
    assert new_circle.east == Point(3, 2)
    assert new_circle.south == Point(2, 1)
    assert new_circle.west == Point(1, 2)


def test_circle_scale(mock_circle):
    new_circle = mock_circle.scale(2)
    assert new_circle.center == Point(2, 2)
    assert new_circle.north == Point(2, 4)
    assert new_circle.east == Point(4, 2)
    assert new_circle.south == Point(2, 0)
    assert new_circle.west == Point(0, 2)
