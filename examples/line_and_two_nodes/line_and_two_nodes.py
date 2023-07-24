#!/bin/bash/python3
from tikzpy import TikzPicture

""" Draws a line and two nodes.
"""

if __name__ == "__main__":
    tikz = TikzPicture()
    line = tikz.line((0, 0), (1, 1), options="thick, blue, o-o")
    start_node = tikz.node(line.start, options="below", text="Start!")
    end_node = tikz.node(line.end, options="above", text="End!")

    tikz.write()
    tikz.show()
