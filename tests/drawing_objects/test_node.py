from tikzpy import TikzPicture, Node, Point
import pytest


@pytest.fixture
def node_from_tikzpicture():
    tikz = TikzPicture()
    node = tikz.node(
        position=(3, 3),
        text=r"I love $ \sum_{x \in \mathbb{R}} f(x^2)$ !",
        options="above",
    )
    return node


@pytest.fixture
def mock_node():
    node = Node(
        position=(3, 3),
        text=r"I love $ \sum_{x \in \mathbb{R}} f(x^2)$ !",
        options="above",
    )
    return node


@pytest.mark.parametrize(
    "object",
    [
        "node_from_tikzpicture",
        "mock_node",
    ],
)
def test_node_construction(object, request):
    node = request.getfixturevalue(object)
    assert node.position.x == 3
    assert node.position.y == 3
    assert node.text == r"I love $ \sum_{x \in \mathbb{R}} f(x^2)$ !"
    assert node.options == "above"
    assert (
        node.code
        == r"\node[above] at (3, 3) { I love $ \sum_{x \in \mathbb{R}} f(x^2)$ ! };"
    )


def test_node_position_assignment(mock_node):
    assert mock_node.position == Point(3, 3)
    mock_node.position = (4, 4)
    assert mock_node.position == Point(4, 4)


def test_node_shift(mock_node):
    mock_node.shift(1, 1)
    assert mock_node.position == Point(4, 4)


def test_node_scale(mock_node):
    mock_node.scale(2)
    assert mock_node.position == Point(8, 8)
