import itertools
import sys
sys.path.append("/Users/luketrujillo/Desktop/github/path_methods")
from tikz_methods import *

path_A = PathStatement()
path_B = PathStatement()
path_C = PathStatement()
path_D = PathStatement()

points = [(14.4, 3.2), (16.0, 3.6), (16.8, 4.8), (16.0, 6.8), (16.4, 8.8), (13.6, 8.8), (12.4, 7.6), (12.8, 5.6), (12.4, 3.6)]

path_A.draw_plot_coords(draw_options = "Blue", plot_options = "smooth, tension=.5, closed hobby", points = points)
path_B.draw_plot_coords(draw_options = "Blue", plot_options = "smooth, tension=.5, closed hobby", points = points)
path_C.draw_plot_coords(draw_options = "Blue", plot_options = "smooth, tension=.5, closed hobby", points = points)
path_D.draw_plot_coords(draw_options = "Blue", plot_options = "smooth, tension=.5, closed hobby", points = points)

paths = [path_A, path_B, path_C, path_D]

for clip_pair in list(itertools.combinations(paths, 2)):
    
