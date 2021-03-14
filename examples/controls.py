import sys
sys.path.append("/Users/luketrujillo/Desktop/github/tikz-python")
from tikz_methods import *

new_tikz = TikzStatement()
    pts = list(range(0,10))
    for i in pts:
        new_tikz.draw_line((i, 0),\
                            (0, 5),\
                            options = "blue!" + str(100 * i // len(pts)),\
                            control_pts = [(i-2, -1), (i+2, -2)],\
                            )
    new_tikz.write()