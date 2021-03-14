import sys
sys.path.append("/Users/luketrujillo/Desktop/github/tikz-python")
from tikz_methods import *

for i in range(30):
    point = (math.sin(2*math.pi*i/30), math.cos(2*math.pi*i/30))

    tikz.draw_circle(point , 2, "Blue")
    tikz.draw_circle(point , 2.2, "Green")
    tikz.draw_circle(point , 2.4, "Red")
    tikz.draw_circle(point , 2.6, "Purple")