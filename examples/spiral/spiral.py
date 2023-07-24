import numpy as np
from tikzpy import TikzPicture, PlotCoordinates, Circle

if __name__ == "__main__":
    tikz = TikzPicture(center=True)

    for height in [0, 1.25, 2.5, 3.75]:
        """Idea: No Tikz solution exists for drawing this spiral such that self intersections are drawn with
        a "crossing over" feature. All documented methods (e.g., preaction, decorations, knots library) don't work.
        Instead, we :
            Create two curves, one before the self intersection and one after.
            At the self intersection, we draw a white circle.
            We then draw in the order: first curve half, white circle, second curve half. This provides the necessary crossing over feature.
        """
        curve_under = PlotCoordinates([], plot_options="smooth")  # Curve before cross over
        curve_over = PlotCoordinates([], plot_options="smooth")  # Curve after cross over
        points = []  # Points on the spiral
        under = True  # Controls if we are drawing curve_under or curve_over
        t = 0
        while t < 2 * np.pi / 5 + 0.1:
            x = 2 * np.cos(5 * t)
            y = 2 * np.sin(5 * t) * 0.3 + t + height

            if np.abs(t - 0.1731) < 3.5e-3:  # Draw white space at self intersection
                under = False
                white_space = Circle(
                    (x, y), radius=0.05, options="fill=white", action="fill"
                )

            else:  # Otherwise, collect points on the curve
                if under:
                    curve_under.points.append((x, y))
                else:
                    curve_over.points.append((x, y))
            t += 2 * np.pi / 500

        # Draw everything in this specific order
        tikz.draw(curve_under, white_space, curve_over)

    # Annotations: \\vdots, S^1, x, \mathbb{R}^1
    tikz.node((0, -0.4), text="$\\vdots$")
    tikz.node((-2.8, -0.2), text="$\\vdots$")
    tikz.node((-2.8, 5.3), text="$\\vdots$")
    tikz.node((2.4, -2), text="$S^1$")
    tikz.node((-1.5, -2.6), text="$x$")
    tikz.node((2.4, 0.7), text="$\\mathbb{R}^1$")
    # Arrow
    tikz.line((0, -0.9), (0, -1.2), options="->, =>Stealth")
    # Circles and x's
    for i, math in [(0, "x-1"), (1, "x"), (2, "x+1"), (3, "x+2")]:
        x = -1.5
        y = 0.37 + 1.25 * i
        tikz.circle((x, y), radius=0.05, action="fill")
        tikz.node((x - 1.3, y + 0.2), text=f"${math}$")

    # S^1
    S1 = tikz.ellipse((0, -2), x_axis=2, y_axis=2 * 0.2)
    tikz.circle((-1.5, -2.255), radius=0.05, action="fill")

    tikz.write()
    tikz.show()
