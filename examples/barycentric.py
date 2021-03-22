import statistics
import queue
import sys

sys.path.append("/Users/luketrujillo/Desktop/github/tikz-python")
from tikz_methods import *

tikz = TikzPicture(new_file=True)


def nth_subdivision(n):
    new_tikz = TikzPicture()
    iters = 0
    if n > 0:
        for i in range(n):
            iters += 6 ** (i)
            barycentric_subdivision(iters, new_tikz)
    else:
        barycentric_subdivision(0, new_tikz)

    new_tikz.write()


def barycentric_subdivision(iterations, new_tikz):
    pt_one = (0, 0)
    pt_two = (6, 0)
    pt_three = (3, 4.24)
    init_coords = [pt_one, pt_two, pt_three]

    new_tikz.line(pt_one, pt_two)
    new_tikz.line(pt_two, pt_three)
    new_tikz.line(pt_three, pt_one)

    triangles = queue.Queue()  # queue of lists of tuples
    triangles.put(init_coords)  # Put goes to the end [... {]}

    while not triangles.empty() and iterations > 0:
        iterations -= 1
        coords = triangles.get()  # Grabs from the front {[} ...]
        new = medians(coords, new_tikz, iterations)
        for tri in new:
            triangles.put(tri)


def medians(coords, new_tikz, iteration):
    centroid = (
        statistics.mean([x[0] for x in coords]),
        statistics.mean([x[1] for x in coords]),
    )
    new_triangle = []  # save coords of new triangles

    # get median coordinates for all edges
    midpts = []
    for i in range(-len(coords), 0):
        ax, ay = coords[i]
        bx, by = coords[i + 1]
        cx, cy = coords[i + 2]

        # get median coords, draw median
        x = statistics.mean([bx, cx])
        y = statistics.mean([by, cy])
        new_tikz.line((ax, ay), (x, y), colors[iteration % len(colors)])  # tikz
        midpts.append((x, y))

    # get coords of all new triangles created
    for i in range(len(coords)):
        new_triangle.append([centroid, midpts[i], coords[i - 1]])
        new_triangle.append([centroid, midpts[i], coords[i - 2]])

    return new_triangle
