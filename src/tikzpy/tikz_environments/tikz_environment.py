from __future__ import annotations
from typing import List, Tuple, Union
from abc import ABC, abstractmethod
from tikzpy.drawing_objects.line import Line
from tikzpy.drawing_objects.plotcoordinates import PlotCoordinates
from tikzpy.drawing_objects.circle import Circle
from tikzpy.drawing_objects.node import Node
from tikzpy.drawing_objects.rectangle import (
    Rectangle,
    rectangle_from_north,
    rectangle_from_east,
    rectangle_from_south,
    rectangle_from_west,
    rectangle_from_center,
)
from tikzpy.drawing_objects.ellipse import Ellipse
from tikzpy.drawing_objects.arc import Arc
from tikzpy.drawing_objects.point import Point
from tikzpy.drawing_objects.drawing_object import DrawingObject
from tikzpy.tikz_environments.tikz_command import TikzCommand
from tikzpy.drawing_objects.drawing_utils import line_connecting_circle_edges, draw_segments


class TikzEnvironment(ABC):
    def __init__(self, options: str) -> None:
        self.options = options
        self.drawing_objects = []

    def draw(self, *args: List[DrawingObject]) -> None:
        """Add an arbitrary sequence of drawing objects."""
        for draw_obj in args:
            self.drawing_objects.append(draw_obj)

    def add_option(self, option: str) -> None:
        """Add an option to the set of options."""
        if len(self.options) == 0:
            self.options += option
        else:
            self.options += f", {option}"

    def add_command(self, tikz_statement: str) -> TikzCommand:
        """Add a string of valid Tikz code into the Tikz environment."""
        command = TikzCommand(tikz_statement)
        self.draw(command)
        return command

    """
        Methods to code objects in the Tikz Environment
    """

    def line(
        self,
        start: Union[Tuple[float, float], Point],
        end: Union[Tuple[float, float], Point],
        options: str = "",
        to_options: str = "",
        control_pts: list = [],
        action: str = "draw",
    ) -> Line:
        """Draws a line by creating an instance of the Line class."""
        line = Line(start, end, options, to_options, control_pts, action)
        self.draw(line)
        return line

    def plot_coordinates(
        self,
        points: Union[List[tuple], List[Point]],
        options: str = "",
        plot_options: str = "",
        action: str = "draw",
    ) -> PlotCoordinates:
        """Draws a plot coordinates statement by creating an instance of the PlotCoordinates class."""
        plot = PlotCoordinates(points, options, plot_options, action)
        self.draw(plot)
        return plot

    def plot_relative_coordinates(
        self,
        points: Union[List[tuple], List[Point]],
        options: str = "",
        plot_options: str = "",
        action: str = "draw",
    ) -> PlotCoordinates:
        """Draws a (relative) plot coordinates statement by creating an instance of the PlotCoordinates class."""
        last_point = points[0]
        new_points = [last_point]
        for point in points[1:]:
            new_point = last_point + Point(point)
            new_points.append(new_point)
            last_point = new_point

        plot = PlotCoordinates(new_points, options, plot_options, action)
        self.draw(plot)
        return plot

    def circle(
        self,
        center: Union[Tuple[float, float], Point],
        radius: float,
        options: str = "",
        action: str = "draw",
    ) -> Circle:
        """Draws a circle by creating an instance of the Circle class."""
        circle = Circle(center, radius, options, action)
        self.draw(circle)
        return circle

    def connect_circle_edges(
        self,
        circle_a,
        circle_b,
        options="",
        src_delta=0,
        dst_delta=0
    ) -> Line:
        """Draws a line connecting the edges of two circles. This is useful for drawing
        graphs, diagrams, neural networks, etc.

        ```python
        from tikzpy import TikzPicture

        tikz = TikzPicture()
        radius = 0.3
        centers = [(0,2), (2, 4), (4,2), (6,5)]
        circles = [tikz.circle(x, radius, options="ProcessBlue!50", action="filldraw") for x in centers]
        for idx in range(len(circles) - 1):
            line = tikz.connect_circle_edges(circles[idx], circles[idx + 1])
            line.options = "->"
        tikz.show()
        ```
        <img src="../../png/connect_circles.png"/> 

        """
        line = line_connecting_circle_edges(circle_a, circle_b, options, src_delta, dst_delta)
        self.draw(line)
        return line

    def draw_segments(self, points, circular=True, options=""):
        """
        Given a list of points, draw a sequence of line segments between the points.

        ```python
        from tikzpy import TikzPicture
        tikz = TikzPicture(center=True)
        circle = tikz.circle((0,0), 3, options="fill=ProcessBlue!30", action="filldraw")
        num_points = 7
        points = []
        for num in range(num_points):
            angle = 360/num_points*num
            points.append(circle.point_at_arg(angle))
        draw_segments(tikz, points, options="thick")
        tikz.show()
        ```

        <img src="../../png/draw_segments.png"/> 
        """
        lines = draw_segments(self, points, circular, options)
        return lines

    def node(
        self,
        position: Union[Tuple[float, float], Point],
        options: str = "",
        text: str = "",
    ) -> Node:
        """Draws a node by creating an instance of the Node class."""
        node = Node(position, options, text)
        self.draw(node)
        return node

    def rectangle(
        self,
        left_corner: Union[Tuple[float, float], Point],
        width: float = 0,
        height: float = 0,
        options: str = "",
        action: str = "draw",
    ) -> Rectangle:
        """Draws a rectangle by creating an instance of the Rectangle class."""
        rectangle = Rectangle(left_corner, width, height, options, action)
        self.draw(rectangle)
        return rectangle

    def rectangle_from_north(
        self,
        north_point: Union[Tuple[float, float], Point],
        width: float = 0,
        height: float = 0,
        options: str = "",
        action: str = "draw",
    ) -> Rectangle:
        """
        Creates and draws a rectangle using the northernmost point as a reference.

        This method allows for the creation of a rectangle by specifying its north point,
        width, and height.

        Args:
            north_point: The northernmost point of the
                rectangle. This can be a tuple of floats representing the coordinates, or
                a Point object.
            width: The width of the rectangle. Defaults to 0.
            height: The height of the rectangle. Defaults to 0.
            options: A string representing additional options for the
                rectangle's creation or manipulation. Defaults to an empty string.
            action: Specifies the TikZ action to be taken with the rectangle
                once created. Defaults to "draw".
        """
        rectangle = rectangle_from_north(
            north_point=north_point,
            width=width,
            height=height,
            options=options,
            action=action,
        )
        self.draw(rectangle)
        return rectangle

    def rectangle_from_east(
        self,
        east_point: Union[Tuple[float, float], Point],
        width: float = 0,
        height: float = 0,
        options: str = "",
        action: str = "draw",
    ) -> Rectangle:
        """
        Creates and draws a rectangle using the east point as a reference.

        This method allows for the creation of a rectangle by specifying its east point,
        width, and height.

        Args:
            east_point: The east point of the rectangle.
                This can be a tuple of floats representing the coordinates, or a Point object.
            width: The width of the rectangle. Defaults to 0.
            height: The height of the rectangle. Defaults to 0.
            options: A string representing additional options for the
                rectangle's creation or manipulation. Defaults to an empty string.
            action: Specifies the TikZ action to be taken with the rectangle
                once created. Defaults to "draw".
        """
        rectangle = rectangle_from_east(east_point, width, height, options, action)
        self.draw(rectangle)
        return rectangle

    def rectangle_from_south(
        self,
        south_point: Union[Tuple[float, float], Point],
        width: float = 0,
        height: float = 0,
        options: str = "",
        action: str = "draw",
    ) -> Rectangle:
        """
        Creates and draws a rectangle using the south point as a reference.

        This method allows for the creation of a rectangle by specifying its south point,
        width, and height.

        Args:
            south_point: The south point of the rectangle.
                This can be a tuple of floats representing the coordinates, or a Point object.
            width: The width of the rectangle. Defaults to 0.
            height: The height of the rectangle. Defaults to 0.
            options: A string representing additional options for the
                rectangle's creation or manipulation. Defaults to an empty string.
            action: Specifies the TikZ action to be taken with the rectangle
                once created. Defaults to "draw".
        """
        rectangle = rectangle_from_south(south_point, width, height, options, action)
        self.draw(rectangle)
        return rectangle

    def rectangle_from_west(
        self,
        west_point: Union[Tuple[float, float], Point],
        width: float = 0,
        height: float = 0,
        options: str = "",
        action: str = "draw",
    ) -> Rectangle:
        """
        Creates and draws a rectangle using the west point as a reference.

        This method allows for the creation of a rectangle by specifying its west point,
        width, and height.

        Args:
            west_point: The west point of the rectangle.
                This can be a tuple of floats representing the coordinates, or a Point object.
            width: The width of the rectangle. Defaults to 0.
            height: The height of the rectangle. Defaults to 0.
            options: A string representing additional options for the
                rectangle's creation or manipulation. Defaults to an empty string.
            action: Specifies the TikZ action to be taken with the rectangle
                once created. Defaults to "draw".
        """
        rectangle = rectangle_from_west(west_point, width, height, options, action)
        self.draw(rectangle)
        return rectangle

    def rectangle_from_center(
        self,
        center: Union[Tuple[float, float], Point],
        width: float = 0,
        height: float = 0,
        options: str = "",
        action: str = "draw",
    ) -> Rectangle:
        rectangle = rectangle_from_center(center, width, height, options, action)
        self.draw(rectangle)
        return rectangle

    def ellipse(
        self,
        center: Union[Tuple[float, float], Point],
        x_axis: float,
        y_axis: float,
        options: str = "",
        action: str = "draw",
    ) -> Ellipse:
        """Draws an ellipse by creating an instance of the Ellipse class."""
        ellipse = Ellipse(center, x_axis, y_axis, options, action)
        self.draw(ellipse)
        return ellipse

    def arc(
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
    ) -> Arc:
        """Draws an arc by creating an instance of the Arc class."""
        arc = Arc(
            position,
            start_angle,
            end_angle,
            radius,
            x_radius,
            y_radius,
            options,
            radians,
            draw_from_start,
            action,
        )
        self.draw(arc)
        return arc
