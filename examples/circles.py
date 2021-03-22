import sys

sys.path.append("/Users/luketrujillo/Desktop/github/tikz-python")
from tikz_methods import *

tikz = TikzPicture(new_file=True)

for i in range(30):
    point = (math.sin(2 * math.pi * i / 30), math.cos(2 * math.pi * i / 30))

    tikz.circle(point, 2, "Blue")
    tikz.circle(point, 2.2, "Green")
    tikz.circle(point, 2.4, "Red")
    tikz.circle(point, 2.6, "Purple")

tikz.write()