#!/usr/bin/env python3

from math import *
from vpython import *


L = 10
# Propagation speed
C = 3

# Number of sine waves to use in our solution. Change this!
N_TERMS = 30

# the math we worked through is continuous, but if we want to plot it we need
# to get discrete. Points are spaced uniformly from 0 to L.
N_POINTS = 200


class Array(tuple):
    """We can't import numpy on glowscript. This is a tuple that can be added
    to other tuples and multiplied by numbers.
    """

    def __mul__(self, num):
        ret = []
        for elt in self:
            ret.append(num*elt)
        return Array(ret)

    def __add__(self, other):
        ret = []
        for s, o in zip(self, other):
            ret.append(s+o)
        return Array(ret)


def empty_array(n=N_POINTS):
    return Array([0]*n)


XVALS = []
for i in range(N_POINTS):
    XVALS.append(i*L/(N_POINTS - 1))
XVALS = Array(XVALS)


# Define initial displacement here. Triangle wave to get us started.
U0 = []
for x in XVALS:
    if x < L/8:
        U0.append(2*x)
    elif x < L/4:
        U0.append(L/2-2*x)
    else:
        U0.append(0)
U0 = Array(U0)


def eigenvector(n):
    vec = []
    for x in XVALS:
        vec.append(sin((n+1)*pi*x/L))
    return Array(vec)


def timefactor(n, t):
    return cos((n+1)*pi*C*t/L)


def inner_product(vec1, vec2):
    # Integrates the two given "functions" from 0 to L, then multiplies by 2/L
    tally = 0
    dx = L/N_POINTS
    for v1, v2 in zip(vec1, vec2):
        tally += v1*v2*dx
    return tally*2/L


def main():
    # Based on the initial conditions, figure out how much of each standing
    # wave is present in our initial waveform. We calculate alpha from the
    # initial position and beta from the initial velocity.
    alpha = []
    beta = []

    for n in range(N_TERMS):
        a = inner_product(U0, eigenvector(n))
        print("amplitude of mode", n, "is:", a)
        alpha.append(a)





    # Draw the jumprope using a sequence of spheres.
    dots = []
    for x, u in zip(XVALS, U0):
        dot = sphere(radius=L/N_POINTS, pos=vector(x-L/2, u, 0))
        dots.append(dot)
    # We're solving for this motion using the wave equation, not forces. Time
    # step is just to make the animation look nice.
    t = 0
    dt = 0.1
    tmax = 10
    while t < tmax:
        rate(1/dt)
        t += dt
        # Build up u(x, t) as a sum of eigenvectors
        u = empty_array()
        for n in range(N_TERMS):
            # Careful with order of operations here. We can do Array*number,
            # but number*Array isn't defined.
            u = eigenvector(n)*alpha[n]*timefactor(n, t) + u
        # Update the position of our dots.
        for dot, ui in zip(dots, u):
            dot.pos.y = ui
    return


if __name__ == "__main__":
    main()
