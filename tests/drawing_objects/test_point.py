import pytest
from tikzpy import Point


@pytest.mark.parametrize(
    "point, expected",
    [
        (Point(1, 2), (1, 2)),
        (Point(1, 2, 3), (1, 2, 3)),
        (Point((1, 2)), (1, 2)),
        (Point((1, 2, 3)), (1, 2, 3)),
        (Point(Point(1, 2)), (1, 2)),
        (Point(Point(1, 2, 3)), (1, 2, 3)),
    ],
)
def test_point_instantiation(point, expected):
    assert point.x == expected[0]
    assert point.y == expected[1]
    if len(expected) == 3:
        assert point.z == expected[2]
    else:
        print(point, point.z)
        assert point.z is None

def test_point_scale():
    point = Point(1, 4)
    new_point = point.scale(2)
    assert new_point.x == 2
    assert new_point.y == 8


def test_point_shift():
    point = Point(1, 4)
    new_point = point.shift(2, 3)
    assert new_point.x == 3
    assert new_point.y == 7


def test_point_rotate():
    point = Point(1, 0)
    about_point = Point(0, 0)
    new_point = point.rotate(90, about_point)
    assert pytest.approx(new_point.x) == 0
    assert pytest.approx(new_point.y) == 1

