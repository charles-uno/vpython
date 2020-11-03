#!/usr/bin/env python3

from math import *
from vpython import *


# Propagation speed
C = 1
# Slinky length
L = 10
# Number of sine waves to use in our solution
N_TERMS = 20

# the math we worked through is continuous, but if we want to plot it we need
# to get discrete. Points are spaced uniformly from 0 to L
N_POINTS = 200

# Wave length and height are used to figure out the initial displacement as
# well as the initial velocity.
WAVE_LENGTH = 2
WAVE_HEIGHT = 3


def main():
    # Based on the initial conditions, figure out how much of each standing
    # wave is present in our initial waveform. We calculate alpha from the
    # initial position and beta from the initial velocity.
    alpha, beta = get_fourier_weights()
    # Rather than repeatedly clearing and re-plotting lines, let's just move a
    # bunch of spheres around.
    dots = []
    for x, u in zip(xarr(), initial_displacement()):
        # Offset by L/2. In our math we worked from 0 to L, but the plot will
        # look nicer if we draw from -L/2 to L/2
        dot = sphere(radius=L/N_POINTS, pos=vector(x - L/2, u, 0))
        dots.append(dot)
    # We're solving for this motion using the wave equation, not forces. Time
    # step is just to make the animation look nice.
    t, dt, tmax = 0, 0.1, 20
    while t < tmax:
        rate(1/dt)
        t += dt
        # Build up u(x, t) as a sum of eigenvectors
        u = [0]*N_POINTS
        for n in range(N_TERMS):
            # The online interpreter doesn't let us import Numpy for proper
            # arrays, and it also doesn't let us define our own classes, so
            # array multiplication is a bit clunky.
            u = array_add(
                    u,
                    array_mult(
                        eigenvector(n),
                        alpha[n]*time_cos(n, t) + beta[n]*time_sin(n, t)
                    )
                )
        # Update the position of our dots.
        for dot, ui in zip(dots, u):
            dot.pos.y = ui
    return


def get_fourier_weights():
    u0 = initial_displacement()
    v0 = initial_velocity()
    alpha, beta = [], []
    for n in range(N_TERMS):
        # Alpha amplitudes correspond to the cosine wave in t, which is at
        # maximum amplitude and zero velocity at t=0
        an = inner_product(u0, eigenvector(n))
        alpha.append(an)
        # Beta amplitudes correspond to the sine wave in t, which accounts for
        # all initial velocity and none of the initial displacement
        omega = (n+1)*pi*C/L
        bn = inner_product(v0, eigenvector(n))/omega
        beta.append(bn)
    return alpha, beta


# Initial displacement. sine squared is nice because it goes to u=0 and u'=0 at
# the edges. Makes the wave look smoother.
def initial_displacement():
    """Sine squared makes for a nice initial displacement because u=0 and u'=0
    at the edge of the pulse.
    """
    u = []
    for xi in xarr():
        if xi < WAVE_LENGTH:
            u.append(WAVE_HEIGHT*sin(pi*xi/WAVE_LENGTH)**2)
        else:
            u.append(0)
    return u


def initial_velocity():
    """Another way of solving the wave equation shows that we can take any
    function we like and swap x -> (x - ct). Do that for the initial
    displacement above (sine squared) and we can take a time derivative. That
    way the displacement and velocity will line up with one another.
    """
    v = []
    for xi in xarr():
        if xi < WAVE_LENGTH:
            v.append(-WAVE_HEIGHT*pi*C*sin(2*pi*xi/WAVE_LENGTH)/WAVE_LENGTH)
        else:
            v.append(0)
    return v


def xarr():
    return [i*L/(N_POINTS - 1) for i in range(N_POINTS)]


def eigenvector(n):
    arr = []
    for xi in xarr():
        arr.append(sin((n+1)*pi*xi/L))
    return arr


def time_sin(n, t):
    return sin((n+1)*pi*C*t/L)


def time_cos(n, t):
    return cos((n+1)*pi*C*t/L)


def inner_product(arr1, arr2):
    # Integrate the two given "functions" from 0 to L, then multiply by 2/L for
    # normality.
    dx = L/N_POINTS
    tally = 0
    for a1, a2 in zip(arr1, arr2):
        tally += a1*a2*dx
    return tally*2/L


def array_add(arr1, arr2):
    arr = []
    for a1, a2 in zip(arr1, arr2):
        arr.append(a1 + a2)
    return arr


def array_mult(arr, num):
    return [a*num for a in arr]


if __name__ == "__main__":
    main()
