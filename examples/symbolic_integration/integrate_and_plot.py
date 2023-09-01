#!/bin/bash/python3
import numpy as np
from sympy import *  # Without caution, import * can become a very stupid idea. Here it is okay.
from sympy.abc import x  # Don't name any function, variable, etc, as 'x'.
from tikzpy import TikzPicture
from tikzpy.colors import rainbow_colors

""" Uses Sympy to iteratively calculate n-order integrals. These are then used by tikzpy 
    to plot. 
    Ex: 
        >>> integrate_n_times(poly(x**2), 5)
        >>> integrate_n_times(poly(x**2)-2, 5)
        >>> integrate_n_times(sin(x)+x, 3)
        >>> integrate_n_times(log(x), 3, 0.1, 5)
"""


def integrate_n_times(func, n, x_start=-2.5, x_end=2.5):
    """Given a function func, we integrate and plot each of the i-order integrals of
    func, where i = 1, 2, ... , n.

    func (sympy.core.function.FunctionClass) :  A Sympy function. Ex: sin(x), x**2, log(x), etc.
    n (int) : The number of integrals we would like to see
    x_start : The value of x we should begin plotting
    x_end : The value of x we should stop plotting
    """
    # Create a TikzPicture
    tikz = TikzPicture()
    # x- and y- axis
    tikz.line((-4, 0), (4, 0), options="Gray!40, thick, <->")
    tikz.line((0, -4), (0, 4), options="Gray!40, thick, <->")

    integrals = [(func, [])]
    for i in range(1, n):
        next_int = integrate(integrals[i - 1][0], x)
        integrals.append((next_int, []))

    n_samples = 100
    for i in np.linspace(x_start, x_end, 100):  # 100 samples from (x_start, x_end)
        for integ in integrals:
            integ_val = (i, float(integ[0].subs(x, i)))
            integ[1].append(integ_val)

    for i, integ in enumerate(integrals):
        tikz.plot_coordinates(integ[1], options=f"<->, color= {rainbow_colors(3*i)}")
        if i % 2:
            pos = integ[1][-1]
            options = "right"
        else:
            pos = integ[1][0]
            options = "left"
        tikz.node(pos, options=options, text=f"${latex(integ[0])}$")

    tikz.show()

if __name__ == "__main__":
    integrate_n_times(poly(x**2), 5)

