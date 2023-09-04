from __future__ import annotations
from typing import List, Tuple, Union
from tikzpy.drawing_objects.point import Point
from tikzpy.drawing_objects.drawing_object import DrawingObject
from tikzpy.utils.helpers import brackets


class Line(DrawingObject):
    """
    A class to create lines in the tikz environment.

    Attributes :
        start (tuple) : Pair of floats representing the start of the line
        end (tuple) : Pair of floats representing the end of the line
        options (str) : String containing Tikz drawing options, e.g. "Blue"
        control_pts (list): List of control points for the line
    """

    def __init__(
        self,
        start: Union[Tuple[float, float], Point],
        end: Union[Tuple[float, float], Point],
        options: str = "",
        to_options: str = "",
        control_pts: List[Tuple] = [],
        action: str = "draw",
    ) -> None:
        self._start = Point(start)
        self._end = Point(end)
        self.options = options
        self.to_options = to_options
        self._control_pts = [Point(point) for point in control_pts]

        super().__init__(action, self.options)

    @property
    def control_pts(self):
        return self._control_pts

    @control_pts.setter
    def control_pts(self, new_control_pts):
        self._control_pts = [Point(point) for point in new_control_pts]

    @property
    def _command(self) -> str:
        r"""The Tikz code for a line that comes after \draw[self.options]. It is useful for
        us to do this breaking-up of the Tikz code, especially for clipping. However, this
        serves no use to the user, so we make it private (well, it's just bells and whistles).
        """
        if len(self.control_pts) == 0:
            return rf"{self.start} to{brackets(self.to_options)} {self.end}"

        else:
            control_stmt = ".. controls "
            for pt in self.control_pts:
                if pt.z is None:
                    control_stmt += f"{pt.x, pt.y}" + " and "
                else:
                    control_stmt += f"{pt.x, pt.y, pt.z}" + " and "
            control_stmt = control_stmt[:-4] + " .."
            return f"{self.start} {control_stmt} {self.end}"

    @property
    def start(self) -> Point:
        return self._start

    @property
    def end(self) -> Point:
        return self._end

    @start.setter
    def start(self, new_start: Union[Tuple, Point]) -> None:
        if isinstance(new_start, (tuple, Point)):
            self._start = Point(new_start)
        else:
            raise TypeError(f"Invalid type '{type(new_start)}' for start")

    @end.setter
    def end(self, new_end: Union[Tuple, Point]) -> None:
        if isinstance(new_end, (tuple, Point)):
            self._end = Point(new_end)
        else:
            raise TypeError(f"Invalid type '{type(new_end)}' for end")

    def pos_at_t(self, t: float) -> Point:
        """Returns the point on the line that lies at "time t", on a scale from 0 to 1."""
        x_1, y_1 = self._start
        x_2, y_2 = self._end
        return Point(x_1 * (1 - t) + x_2 * t, y_1 * (1 - t) + y_2 * t)

    def midpoint(self) -> Point:
        return self.pos_at_t(0.5)

    def shift(self, xshift: float, yshift: float) -> None:
        """Shift start, end, and control_pts"""
        self._start.shift(xshift, yshift)
        self._end.shift(xshift, yshift)
        for point in self.control_pts:
            point.shift(xshift, yshift)

    def scale(self, scale: float) -> None:
        """Scale start, end, and control_pts."""
        self._start.scale(scale)
        self._end.scale(scale)
        for point in self.control_pts:
            point.scale(scale)

    def rotate(
        self, angle: float, about_pt: Tuple[float, float] = None, radians: bool = False
    ) -> None:
        """Rotate start, end, and control_pts. By default, the rotation is done relative to the midpoint
        of the line."""
        if about_pt is None:
            about_pt = self.midpoint
        self._start.rotate(angle, about_pt, radians)
        self._end.rotate(angle, about_pt, radians)

        for point in self.control_pts:
            point.rotate(angle, about_pt, radians)
