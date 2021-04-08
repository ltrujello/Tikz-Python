import statistics
import queue
from tikzpy import TikzPicture
from tikzpy.colors import xcolors


def nth_subdivision(n):
    iters = 0
    for i in range(n):
        tikz = TikzPicture(center=True)
        if n > 0:
            iters += 6 ** (i)
            barycentric_subdivision(iters, tikz)
        else:
            barycentric_subdivision(0, tikz)
        tikz.write()

    tikz.show()


def barycentric_subdivision(iterations, tikz):
    pt_one = (0, 0)
    pt_two = (6, 0)
    pt_three = (3, 4.24)

    tikz.line(pt_one, pt_two)
    tikz.line(pt_two, pt_three)
    tikz.line(pt_three, pt_one)

    triangles = queue.Queue()  # queue of lists of tuples
    triangles.put([pt_one, pt_two, pt_three])  # Put goes to the end [... {]}

    while not triangles.empty() and iterations > 0:
        iterations -= 1
        coords = triangles.get()  # Grabs from the front {[} ...]
        new = medians(coords, tikz, iterations)
        for tri in new:
            triangles.put(tri)


def medians(coords, tikz, iteration):
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
        tikz.line(
            (ax, ay),
            (x, y),
            options=f"color={xcolors(iteration)}, line width=0.1mm",
        )
        midpts.append((x, y))

    # get coords of all new triangles created
    for i in range(len(coords)):
        new_triangle.append([centroid, midpts[i], coords[i - 1]])
        new_triangle.append([centroid, midpts[i], coords[i - 2]])

    return new_triangle
