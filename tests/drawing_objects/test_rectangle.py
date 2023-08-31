from tikzpy import TikzPicture, Rectangle, Point
import pytest

@pytest.fixture
def tikz_rectangle():
    tikz = TikzPicture()
    rectangle = tikz.rectangle((2, 2), (3, 4), options="Blue")
    return rectangle

@pytest.fixture
def mock_rectangle():
    rectangle = Rectangle((2, 2), (3, 4), options="Blue")
    return rectangle


@pytest.mark.parametrize(
    "object", [
        "tikz_rectangle",
        "mock_rectangle",
    ]
)
def test_rectangle_constructor(object, request):
    rectangle = request.getfixturevalue(object)
    assert rectangle.left_corner.x == 2
    assert rectangle.left_corner.y == 2
    assert rectangle.right_corner.x == 3
    assert rectangle.right_corner.y == 4
    assert rectangle.options == "Blue"
    assert rectangle.code == r"\draw[Blue] (2, 2) rectangle (3, 4);"


