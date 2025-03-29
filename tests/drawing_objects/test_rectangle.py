from tikzpy import TikzPicture, Rectangle, Point
import pytest


@pytest.fixture
def tikz_rectangle():
    tikz = TikzPicture()
    rectangle = tikz.rectangle((2, 2), 1, 2, options="Blue")
    return rectangle


@pytest.fixture
def mock_rectangle():
    rectangle = Rectangle((2, 2), 1, 2, options="Blue")
    return rectangle


@pytest.mark.parametrize(
    "object",
    [
        "tikz_rectangle",
        "mock_rectangle",
    ],
)
def test_rectangle_constructor(object, request):
    rectangle = request.getfixturevalue(object)
    assert rectangle.left_corner.x == 2
    assert rectangle.left_corner.y == 2
    assert rectangle.options == "Blue"
    assert rectangle.height == 2
    assert rectangle.width == 1

    assert rectangle.center == Point(2.5, 3.0)
    assert rectangle.north == Point(2.5, 4)
    assert rectangle.east == Point(3, 3)
    assert rectangle.south == Point(2.5, 2)
    assert rectangle.west == Point(2, 3)

    assert rectangle.code == r"\draw[Blue] (2, 2) rectangle (3, 4);"


def test_left_corner_assignment(mock_rectangle):
    mock_rectangle.left_corner = (0, 0)
    assert mock_rectangle.left_corner == Point(0, 0)
    assert mock_rectangle.height == 2
    assert mock_rectangle.width == 1
    assert mock_rectangle.code == r"\draw[Blue] (0, 0) rectangle (1, 2);"


def test_rectangle_shift(mock_rectangle):
    new_rectangle = mock_rectangle.shift(1, 1)
    assert new_rectangle.left_corner == Point(3, 3)
    assert new_rectangle.right_corner == Point(4, 5)
    assert new_rectangle.code == r"\draw[Blue] (3, 3) rectangle (4, 5);"


def test_rectangle_scale(mock_rectangle):
    new_rectangle = mock_rectangle.scale(2)
    assert new_rectangle.left_corner == Point(4, 4)
    assert new_rectangle.right_corner == Point(6, 8)
    assert new_rectangle.code == r"\draw[Blue] (4, 4) rectangle (6, 8);"
