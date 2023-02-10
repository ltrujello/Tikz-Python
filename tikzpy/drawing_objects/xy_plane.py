from __future__ import annotations
from typing import List, Tuple
from tikzpy.tikz_environments.scope import Scope
from tikzpy.drawing_objects.line import Line
from tikzpy.drawing_objects.node import Node


class R2_Space:
    def __init__(
        self,
        x_interval: Tuple[float, float],
        y_interval: Tuple[float, float],
        origin: Tuple[float, float] = (0, 0),
        show_ticks: bool = False,
        show_labels: bool = True,
    ):
        self.x_interval = x_interval  # An R^1 interval around 0, e.g., (-2, 3)
        self.y_interval = y_interval  # An R^1 interval around 0
        self.origin = origin
        self.x_axis_options = "Gray!30, <->"
        self.y_axis_options = "Gray!30, <->"
        self.x_label = "$x$"
        self.y_label = "$y$"
        self.nticks = None  # If left to None, no tick marks are shown
        self.show_labels = show_labels

    @property
    def x_axis(self):
        """The x-axis of R^2. The x_axis is specified via self.x_interval."""
        left_pt = self.origin[0] + self.x_interval[0]  # self.x_interval[0] <= 0
        right_pt = self.origin[0] + self.x_interval[1]  # self.x_interval[1] >= 0
        x_axis = Line(
            (left_pt, self.origin[1]),
            (right_pt, self.origin[1]),
            options=self.x_axis_options,
        )
        return x_axis

    @property
    def x_node(self):
        return Node(self.x_axis.end, options="below", text=self.x_label)

    @property
    def y_axis(self):
        """The y-axis of R^2. The y_axis is specified via self.y_interval."""
        down_pt = self.origin[1] + self.y_interval[0]  # self.y_interval[0] <= 0
        up_pt = self.origin[1] + self.y_interval[1]  # self.x_interval[1] >= 0
        y_axis = Line(
            (self.origin[0], down_pt),
            (self.origin[0], up_pt),
            options=self.y_axis_options,
        )
        return y_axis

    @property
    def y_node(self):
        return Node(self.y_axis.end, options="left", text=self.y_label)

    @property
    def code(self):
        xy_plane = Scope()
        xy_plane.draw(self.x_axis, self.y_axis)
        if self.show_labels:
            xy_plane.draw(self.x_node, self.y_node)
        return xy_plane.code

    def __repr__(self):
        return self.code
