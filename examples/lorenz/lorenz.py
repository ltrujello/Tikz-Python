import numpy as np
from scipy.integrate import odeint
from tikzpy import TikzPicture

""" Plots the Lorenz dynamical system. 

    Note: This might not work for some users because of TeX's buffer size parameter, which is a fixed quantity that tells 
    TeX when to quite a process (even if there are no errors with the program). Such a parameter exists 
    because TeX was invented in the late 70s, and not during a time period with quad core 16GB ram computers. 
    
    If one has trouble with this, one could increase their buffer size parameter (a good idea because your computer is in 2021+ 
    and it can definitely handle it) or one could take less iterations in the code below.
"""

tikz = TikzPicture(center=True)
tikz.tdplotsetmaincoords(60, 45)
tikz.options = "tdplot_main_coords"

# lorenz parameters
rho = 28.0
sigma = 10.0
beta = 8.0 / 3.0

# Next state according to the ODEs
def next(state, t):
    x, y, z = state
    return sigma * (y - x), x * (rho - z) - y, x * y - beta * z


# Set initial conditions and time steps
initial = [1.0, 1.0, 1.0]
t = np.arange(
    0.0, 80.0, 0.02
)  # This might need to be changed, e.g., 0.02 to 0.08, to make the program run.

# Solve for the next positions, scale them
states = odeint(next, initial, t)
states = states * 0.25

# We convert points from np.array to tuple for Tikz
tuple_states = []
for state in states:
    tuple_states.append(tuple(state))

# Plot the lorenz system... \tdplotsetmaincoords{60}{45}
lorenz_plot = tikz.plot_coordinates(
    tuple_states, options="ProcessBlue!70", plot_options="smooth"
)
# Annnotate the initial state
tikz.circle(tuple_states[0], radius=0.1, action="fill")
tikz.node(tuple_states[0], options="below", text="Initial: (1,1,1)")

tikz.write()
tikz.show()