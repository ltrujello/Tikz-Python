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


@pytest.mark.parametrize(
    "object",
    [
        "plot_coordinates_from_tikzpicture",
        "mock_plot_coordinates",
    ],
)
def test_plot_coordinates_construction(object, request):
    plot_coordinates = request.getfixturevalue(object)
    assert tikz_plot.options == "green"
    assert tikz_plot.plot_options == "smooth "
    assert tikz_plot.points[0].x == 1
    assert tikz_plot.points[0].y == 1
    assert tikz_plot.points[1].x == 2
    assert tikz_plot.points[1].y == 2
    assert tikz_plot.points[2].x == 3
    assert tikz_plot.points[2].y == 3
    assert tikz_plot.points[3].x == 2
    assert tikz_plot.points[3].y == -4
    assert (
        tikz_plot.code
        == r"\draw[green] plot[smooth ] coordinates {(1, 1) (2, 2) (3, 3) (2, -4) };"
    )
