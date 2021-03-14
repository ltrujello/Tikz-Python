import sys
sys.path.append("/Users/luketrujillo/Desktop/github/tikz-python")
from tikz_methods import *


def roots_of_unity(n, scale):
    """ Creates a diagram for the n-th roots of unity. 
    """
    new_tikz = TikzStatement(new_tex_file = True)
    
    for i in range(n):
        theta = (2 * math.pi * i)/n
        x, y = scale * math.cos(theta), scale * math.sin(theta)
        new_tikz.draw_line((0,0), (x, y), options = "-o")
        
        # Above y-axis
        if 0 <= theta <= math.pi: 
            new_tikz.draw_node( "above", (x, y), f"$e^{{ ({i} \cdot \pi)/ {n} }}$")
        # Below x-axis
        else:
            new_tikz.draw_node( "below", (x, y), f"$e^{{ ({i} \cdot \pi)/ {n} }}$")
    
    new_tikz.write()