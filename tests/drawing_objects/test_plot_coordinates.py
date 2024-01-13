from tikzpy import TikzPicture, PlotCoordinates, Point
import pytest


@pytest.fixture
def plot_coordinates_from_tikzpicture():
    tikz = TikzPicture()
    plot_coordinates = tikz.plot_coordinates(
        options="green",
        plot_options="smooth ",
        points=[(1, 1), (2, 2), (3, 3), (2, -4)],
    )
    return plot_coordinates


@pytest.fixture
def mock_plot_coordinates():
    plot_coordinates = PlotCoordinates(
        options="green",
        plot_options="smooth ",
        points=[(1, 1), (2, 2), (3, 3), (2, -4)],
    )
    return plot_coordinates


@pytest.fixture
def plot_relative_coordinates():
    tikz = TikzPicture()
    plot_coordinates = tikz.plot_relative_coordinates(
        options="green",
        plot_options="smooth ",
        points=[(0, 0), (0, 1), (1, 0), (1, 1)],
    )
    return plot_coordinates


@pytest.mark.parametrize(
    "object",
    [
        "plot_coordinates_from_tikzpicture",
        "mock_plot_coordinates",
    ],
)
def test_plot_coordinates_construction(object, request):
    plot_coordinates = request.getfixturevalue(object)
    assert plot_coordinates.options == "green"
    assert plot_coordinates.plot_options == "smooth "
    assert plot_coordinates.points[0].x == 1
    assert plot_coordinates.points[0].y == 1
    assert plot_coordinates.points[1].x == 2
    assert plot_coordinates.points[1].y == 2
    assert plot_coordinates.points[2].x == 3
    assert plot_coordinates.points[2].y == 3
    assert plot_coordinates.points[3].x == 2
    assert plot_coordinates.points[3].y == -4
    assert (
        plot_coordinates.code
        == r"\draw[green] plot[smooth ] coordinates {(1, 1) (2, 2) (3, 3) (2, -4) };"
    )


def test_plot_relative_coordinates(plot_relative_coordinates):
    assert plot_relative_coordinates.points == [
        Point(0, 0),
        Point(0, 1),
        Point(1, 1),
        Point(2, 2),
    ]
