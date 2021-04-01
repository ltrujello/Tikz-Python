import tikzpy
import numpy as np
from sympy import integrate, poly, latex
from sympy.abc import x

# Create a TikzPicture
tikz = tikzpy.TikzPicture(center=True)
# x- and y- axis
tikz.line((-4, 0), (4, 0), options="Gray!40, thick, <->")
tikz.line((0, -4), (0, 4), options="Gray!40, thick, <->")


def integrate_n_times(func, n_integrals):
    p = poly(func)
    integrals = [(p, [])]
    for i in range(1, n_integrals):
        next_int = integrate(integrals[i - 1][0], x)
        integrals.append((next_int, []))

    n_samples = 100
    for i in np.linspace(-2.5, 2.5, 100):  # 100 samples from (-3, 3)
        for integ in integrals:
            integ_val = (i, float(integ[0].subs(x, i)))
            integ[1].append(integ_val)

    for i, integ in enumerate(integrals):
        tikz.plot_coordinates(
            integ[1], options=f"<->, color= {tikzpy.rainbow_colors(3*i)}"
        )
        if i % 2:
            tikz.node(
                integ[1][-1],
                options="right",
                text=f"${latex(integ[0].expr)}$",
            )
        else:
            tikz.node(
                integ[1][0],
                options="left",
                text=f"${latex(integ[0].expr)}$",
            )

    tikz.write()
    tikz.show()