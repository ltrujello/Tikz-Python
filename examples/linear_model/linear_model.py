#!/bin/bash/python3
import math
from tikzpy import TikzPicture, Point
tikz = TikzPicture()
radius = 0.25

if __name__ == "__main__"
    x_2 = 6
    y_2 = 2
    epsilon = 0.2
    for i in range(5):
        x_1 = 0
        y_1 = 4 - i
        if y_1 - y_2 == 0:
            theta = math.pi/2
        else:
            theta = math.atan(abs(x_2 - x_1) / abs(y_1 - y_2))
        if y_2 > y_1:
            start = (x_1 + radius * math.sin(theta), y_1 + radius* math.cos(theta))
            end = (x_2 - radius * math.sin(theta), y_2 - radius * math.cos(theta))
        else:
            start = (x_1 + radius * math.sin(theta), y_1 - radius* math.cos(theta))
            end = (x_2 - radius * math.sin(theta), y_2 + radius * math.cos(theta))

        line = tikz.line(start, end, options="->")
        tikz.circle((x_1, y_1), radius)
        # Draw the input x_i
        tikz.node((x_1, y_1 + radius + epsilon), text=f"$x_{i}$")
        # Draw the weight w_i
        tikz.node(line.pos_at_t(0.3), options="above", text=f"$w_{i}$")

    # Draw the output node
    tikz.circle((x_2, y_2), radius)
    # Draw label for output node
    tikz.node((x_2, y_2 + radius + epsilon), text="$y$")
