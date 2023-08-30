from __future__ import annotations
from typing import List, Tuple, Union
from abc import ABC, abstractmethod
from tikzpy.drawing_objects.line import Line
from tikzpy.drawing_objects.plotcoordinates import PlotCoordinates
from tikzpy.drawing_objects.circle import Circle
from tikzpy.drawing_objects.node import Node
from tikzpy.drawing_objects.rectangle import Rectangle
from tikzpy.drawing_objects.ellipse import Ellipse
from tikzpy.drawing_objects.arc import Arc
from tikzpy.drawing_objects.point import Point
from tikzpy.drawing_objects.drawing_object import DrawingObject
from tikzpy.tikz_environments.tikz_command import TikzCommand


class TikzEnvironment(ABC):
    def __init__(self, options: str) -> None:
        self.options = options
        self._statements = {}

    @property
    def statements(self) -> dict:
        """A dictionary to keep track of the current Tikz code we've commanded.
        keys : instances of subclasses created (e.g, Line)
        values : the Tikz code of the instance (e.g., Line.code)
        """
        statement_dict = {}
        for draw_obj in self._statements:
            statement_dict[draw_obj] = draw_obj.code
        return statement_dict

    def remove(self, draw_obj: DrawingObject) -> None:
        """Remove a drawing_object from the Tikz environment, e.g., an instance of Line."""
        del self._statements[draw_obj]

    def draw(self, *args: List[DrawingObject]) -> None:
        """Add an arbitrary sequence of drawing objects."""
        for draw_obj in args:
            self._statements[draw_obj] = draw_obj.code

    def add_option(self, option: str) -> None:
        """Add an option to the set of options."""
        if len(self.options) == 0:
            self.options += option
        else:
            self.options += f", {option}"

    def drawing_objects(self) -> list:
        """Returns a list of the currently appended drawing objects in the TikzPicture."""
        return list(self._statements.keys())

    def undo(self) -> None:
        """Remove the last added drawing object from the tikz environment."""
        last_obj = list(self._statements.keys())[-1]
        self.remove(last_obj)

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
        """Draws a line by creating an instance of the Line class.
        Upon creation, we update self._statements with our new code.
        * Key feature: If we update any attributes of our line, the changes
          to the Tikz code are automatically reflected in self._statements.
        """
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
        """Draws a plot coordinates statement by creating an instance of the PlotCoordinates class.
        Updates self._statements when necessary; see above comment under line function above.
        """
        plot = PlotCoordinates(points, options, plot_options, action)
        self.draw(plot)
        return plot

    def circle(
        self,
        center: Union[Tuple[float, float], Point],
        radius: float,
        options: str = "",
        action: str = "draw",
    ) -> Circle:
        """Draws a circle by creating an instance of the Circle class.
        Updates self._statements when necessary; see above comment under line function above.
        """
        circle = Circle(center, radius, options, action)
        self.draw(circle)
        return circle

    def node(
        self,
        position: Union[Tuple[float, float], Point],
        options: str = "",
        text: str = "",
    ) -> Node:
        """Draws a node by creating an instance of the Node class.
        Updates self._statements when necessary; see above comment under line function above.
        """
        node = Node(position, options, text)
        self.draw(node)
        return node

    def rectangle(
        self,
        left_corner: Union[Tuple[float, float], Point] = Point(0, 0),
        right_corner: Union[Tuple[float, float], Point] = Point(0, 0),
        options: str = "",
        action: str = "draw",
    ) -> Rectangle:
        """Draws a rectangle by creating an instance of the Rectangle class.
        Updates self._statements when necessary; see above comment under line function above.
        """
        rectangle = Rectangle(left_corner, right_corner, options, action)
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
        """Draws an ellipse by creating an instance of the Ellipse class.
        Updates self._statements when necessary; see above comment under line function above.
        """
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
        """Draws an arc by creating an instance of the Arc class.
        Updates self._statements when necessary; see above comment under line function above.
        """
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
