import tikzpy


def roots_of_unity(n, scale):
    """Creates a diagram for the n-th roots of unity."""
    tikz = tikzpy.TikzPicture()

    for i in range(n):
        theta = (2 * math.pi * i) / n
        x, y = scale * math.cos(theta), scale * math.sin(theta)
        content = f"$e^{{ (2 \cdot \pi \cdot {i})/ {n} }}$"

        # Draw line to nth root of unity
        tikz.line((0, 0), (x, y), options="-o")

        if 0 <= theta <= math.pi:
            node_option = "above"
        else:
            node_option = "below"

        # Label the nth root of unity
        tikz.node((x, y), options=node_option, content=content)

    tikz.write()