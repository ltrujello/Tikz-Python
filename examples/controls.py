import sys

sys.path.append("/Users/luketrujillo/Desktop/github/tikz-python")
from tikz_methods import *

tikz = TikzPicture()
for i in range(0, 15):
    line = tikz.line((i, 0), (0, 5))
    line.options = f"color={rainbow_colors(i)}"
    line.control_pts = [(i - 2, -1), (i + 2, -2)]

tikz.write()
