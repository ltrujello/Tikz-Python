from __future__ import annotations
from typing import Tuple, Union
from math import sin, cos, tan, atan2, pi, sqrt
from math import radians as degs_2_rads
from math import degrees as rads_2_degs
from tikzpy.drawing_objects.point import Point
from tikzpy.drawing_objects.drawing_object import DrawingObject


class Arc(DrawingObject):
    r"""
    A class to create arcs in the tikz environment.

    The arc class helps create arcs in Tikz. It is analagous to the TikZ code
    ```
    \draw <center> arc (<start_angle>:<end_angle>:<radius>);
    ```

    Parameters:
        center: Pair of points representing either the center of the arc or the point at which it should begin drawing (see draw_from_start).
        start_angle: The angle (relative to the horizontal) of the start of the arc
        end_angle: The angle (relative to the horizontal) of the end of the arc
        radius: The radius (in cm) of the arc. If this is specified, x_radius and y_radius cannot be specified.
        radians: True if angles are in radians, False otherwise
        draw_from_start: True if position represents the point at which the arc should begin drawing. False if position represents the center of the desired arc.
    """

    def __init__(
        self,
        position: Union[Tuple[float, float], Point],
        start_angle: float,
        end_angle: float,
        radius: float = None,
        x_radius: float = None,
        y_radius: float = None,
        options: str = "",
        radians: bool = False,
        draw_from_start: bool = True,
        action: str = "draw",
    ):
        self._position = Point(position)
        self.start_angle = start_angle
        self.end_angle = end_angle
        self.radius = radius
        self.x_radius = x_radius
        self.y_radius = y_radius
        self.options = options
        self.radians = radians
        self.draw_from_start = draw_from_start

        super().__init__(action, self.options)

    @property
    def _start_angle(self) -> Angle:
        return Angle(self.start_angle, self.radians)

    @property
    def _end_angle(self) -> Angle:
        return Angle(self.end_angle, self.radians)

    def arc_type(self) -> str:
        """Determine the arc type that the user is attempting to create based on their input."""
        if self.radius is not None:
            if self.x_radius is not None or self.y_radius is not None:
                raise ValueError(
                    "Cannot set radius AND x_radius, y_radius at the same time."
                )
            else:
                self.radius_statement = f"radius = {self.radius}cm"
                return "circle"

        else:
            if self.x_radius is None or self.y_radius is None:
                raise ValueError(
                    f"x_radius was set to {self.x_radius}, y_radius was set to {self.y_radius}, but neither should be None."
                )
            if self.x_radius <= 0 or self.y_radius <= 0:
                raise ValueError(
                    f"x_radius is {self.x_radius}, y_radius is {self.y_radius}, but neither can be <= 0."
                )
            else:
                self.radius_statement = (
                    f"x radius = {self.x_radius}cm, y radius = {self.y_radius}cm"
                )
                return "ellipse"

    def draw_start(self) -> Tuple[float, float]:
        """Return the point at which we should begin drawing the arc."""
        if self.draw_from_start:
            start_pos = self._position
        elif self.arc_type() == "circle":
            start_pos = self.start_pos_circle()
        else:
            start_pos = self.start_pos_ellipse()
        return start_pos

    @property
    def position(self):
        return self._position

    @position.setter
    def position(self, new_pos: Tuple[float, float]) -> None:
        self._position = Point(new_pos)

    @property
    def _command(self) -> str:
        if self.arc_type() == "circle":
            start_angle, end_angle = self._start_angle.degs(), self._end_angle.degs()
        else:  # This is for the case the ellipse.
            # We need to calculate the parameter t at which (x_r*cos(self.start_angle), y_r*sin(self.start_angle)) hits
            t_start = self.atan2_for_ellipse(self._start_angle)
            t_end = self.atan2_for_ellipse(self._end_angle)

            start_angle, end_angle = rads_2_degs(t_start), rads_2_degs(t_end)
        return f"{self.draw_start()} arc [start angle = {start_angle}, end angle = {end_angle}, {self.radius_statement}]"

    def start_pos_circle(self) -> Tuple[float, float]:
        """Calculates the point at which the circle should begin
        drawing, given that the user specified what the center, radius,
        start, and end angles of the desired circular arc.
        """
        assert self.arc_type() == "circle"
        # Obtain the angles in radians
        start_angle = self._start_angle.rads()
        # Calculate the point at which the arc should begin drawing
        start_pt_x = self.position.x + self.radius * cos(start_angle)
        start_pt_y = self.position.y + self.radius * sin(start_angle)

        return (start_pt_x, start_pt_y)

    def start_pos_ellipse(self) -> Tuple[float, float]:
        """Calculates the point at which the ellipse arc should begin
        drawing, given that the user specified what the center, x_radius, y_radius,
        start, and end angles of the desired elliptic arc.
        """
        assert self.arc_type() == "ellipse"
        # Obtain the angles in radians
        start_angle = self._start_angle.rads()
        # We calculate r_at_theta, the distance between the origin and the point on the ellipse which occurs at angle self.start_angle.
        r_at_theta = (self.x_radius * self.y_radius) / sqrt(
            (self.y_radius * cos(start_angle)) ** 2
            + (self.x_radius * sin(start_angle)) ** 2
        )
        # We then use r_at_theta to calculate the desired point on the ellipse
        start_pt_x = self.position.x + r_at_theta * cos(start_angle)
        start_pt_y = self.position.y + r_at_theta * sin(start_angle)

        return start_pt_x, start_pt_y

    def shift(self, xshift: float, yshift: float) -> None:
        self._position.shift(xshift, yshift)

    def scale(self, scale: float) -> None:
        self._position.scale(scale)
        self.x_radius *= scale
        self.y_radius *= scale

    def rotate(
        self, angle: float, about_pt: tuple = None, radians: bool = False
    ) -> None:
        if about_pt is None:
            about_pt = self.draw_start()
        self._position.rotate(angle, about_pt, radians)

    def atan2_for_ellipse(self, angle: Angle) -> float:
        """Perform a tangent inverse operation which returns values between 0 and 2pi."""
        theta = angle.rads()
        # The value of t such that (b*cos(t), a*sin(t)) makes angle theta to the axis.
        t = atan2(self.x_radius * tan(theta), self.y_radius)
        if angle.quadrant == 0:
            t += 0
        elif angle.quadrant == 1 or angle.quadrant == 2:
            t += pi
        else:
            t += 2 * pi
        return t


class Angle:
    def __init__(self, angle: float, radians: bool) -> None:
        self.angle = angle
        self.radians = radians
        self.quadrant = self.set_quadrant(angle)

    def degs(self) -> float:
        if self.radians:
            angle = rads_2_degs(self.angle)
        else:
            angle = self.angle
        return angle

    def rads(self) -> float:
        if not self.radians:
            angle = degs_2_rads(self.angle)
        else:
            angle = self.angle

        return angle

    def set_quadrant(self, angle) -> int:
        if self.radians:
            if 0 <= angle <= pi / 2:
                return 0
            elif pi / 2 < angle <= pi:
                return 1
            elif pi < angle <= 3 * pi / 2:
                return 2
            else:
                return 3
        else:
            if 0 <= angle <= 90:
                return 0
            elif 90 < angle <= 180:
                return 1
            elif 180 < angle <= 270:
                return 2
            else:
                return 3
