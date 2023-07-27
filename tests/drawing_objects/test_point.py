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
