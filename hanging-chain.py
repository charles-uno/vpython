#!/usr/bin/env python3

from math import *
from vpython import *

LINK_MASS = 1
GRAVITY = 9.8

POST_HEIGHT = 20
POST_BOTTOM = -POST_HEIGHT/2
POST_TOP = POST_BOTTOM + POST_HEIGHT
POST_WIDTH = 20
POST_LEFT = -POST_WIDTH/2
POST_RIGHT = POST_LEFT + POST_WIDTH

CHAIN_LENGTH = 40
# Put a motionless dummy link at each end of the chain. Then spring n will be
# between link n and link n+1.
N_SPRINGS = 20
N_LINKS = N_SPRINGS + 1

# A stiffer spring will be less stretched at the end. A looser spring will
# relax more quickly.
SPRING_CONSTANT = 10000
SPRING_LENGTH_RELAX = CHAIN_LENGTH/N_SPRINGS

# For no damping, set this to zero. In that case, the springs will oscillate
# forever rather than relaxing. Setting it to 0.1 means we artificially
# decrease the velocity of each link by 10% every time step to help it relax
# into its lowest energy state.
FRICTION = 0.05

# For real time, use 1. For 10x speed fast-forwarding, use 10.
SPEED = 10


def main():
    draw_posts()
    links = get_chain()
    relax_chain(links)
    init_graph()
    plot_chain(links)
    # The springs will always end up a little bit stretched, which means the
    # chain will always be a little bit longer than we expected initially.
    # Figure out the actual length here.
    length = get_length(links)
    plot_catenary(length)
    plot_parabola(length)
    print("target length:", CHAIN_LENGTH)
    print("actual length:", length)
    return


def draw_posts():
    for x in [POST_LEFT, POST_RIGHT]:
        cylinder(
            pos=vector(x, POST_BOTTOM, 0),
            axis=vector(0, POST_HEIGHT, 0),
            radius=0.1,
        )
    return


def get_chain():
    links = []
    # To start, let's just uniformly space the links. This means our springs
    # will be squished to start. They'll stretch out as we go.
    for i in range(N_LINKS):
        # The function range(n) counts from 0 to n-1. We want the 0th link at
        # the left edge and the n-1st link on the right edge.
        x = POST_LEFT + i*POST_WIDTH/(N_LINKS - 1)
        link = sphere(
            pos=vector(x, POST_TOP, 0),
            radius=0.5*POST_WIDTH/N_LINKS,
            color=color.magenta,
            mass=LINK_MASS,
            velocity=vector(0,0,0),
        )
        links.append(link)
    return links


def relax_chain(links):
    t = 0
    dt = 0.01
    tmax = 20
    while t < tmax:
        t += dt
        rate(SPEED/dt)
        # If we update positions as we go, the left neighbor will always be a
        # time step ahead of the right neighbor. Better to go through once and
        # figure out the forces, then go through again and update positions.
        next_pos = [None]*N_LINKS
        for i in range(N_LINKS):
            # First and lat links are fixed.
            if i == 0 or i == N_LINKS-1:
                next_pos[i] = links[i].pos
                continue
            # Gravity pulls equally on each link
            f_gravity = vector(0, -links[i].mass*GRAVITY, 0)
            f_net = f_gravity
            # Look at position compared to left and right neighbors to figure
            # out spring forces.
            for neighbor in (links[i-1], links[i+1]):
                spring_axis = links[i].pos - neighbor.pos
                stretch = spring_axis.mag - SPRING_LENGTH_RELAX
                f_spring = -SPRING_CONSTANT*stretch*spring_axis.hat
                f_net += f_spring
            links[i].velocity += f_net*dt/links[i].mass
            # If energy is conserved, this will oscillate forever. We want to
            # let it relax into its lowest energy state. So every time step,
            # apply some "friction" to slightly reduce the energy. Note that
            # the form of this friction may not be physical!
            links[i].velocity = links[i].velocity*(1 - FRICTION)
            next_pos[i] = links[i].pos + links[i].velocity*dt
#            links[i].pos += links[i].velocity*dt
        # Go back through and apply all the new positions at once.
        for pos, link in zip(next_pos, links):
            link.pos = pos
    return


def get_length(links):
    length = 0
    for i in range(N_LINKS):
        # Each link looks at its left neighbor. Note the first link doesn't
        # have a left neighbor!
        if i == 0:
            continue
        length += (links[i].pos - links[i-1].pos).mag
    return length


def plot_chain(links):
    curve = gdots(color=color.black, width=1, label="Chain")
    for link in links:
        curve.plot(link.pos.x, link.pos.y)
    return


def plot_catenary(length):
    # There is no analytical way to go from chain length to alpha (the
    # steepness of the catenary) so we solve for it numerically. This can also
    # be done by hand, in Mathematica, etc.
    alpha = bisection_search(length, catenary_length, guess=1/CHAIN_LENGTH)
    y0 = POST_TOP - cosh(alpha*POST_WIDTH/2)/alpha
    curve = gcurve(color=color.blue, width=1, label="Catenary")
    npoints = 1000
    for i in range(npoints):
        x = POST_LEFT + i*POST_WIDTH/npoints
        y = cosh(alpha*x)/alpha + y0
        curve.plot(x, y)
    return


def plot_parabola(length):
    # There is no analytical way to go from chain length to the steepness of a
    # parabola, so we solve for it numerically. This can also be done by hand,
    # in Mathematica, etc.
    curve = gcurve(color=color.red, width=1, label="Parabola")
    a = bisection_search(length, parabola_length, guess=1/CHAIN_LENGTH)
    y0 = POST_TOP - 0.5*a*(POST_WIDTH/2)**2
    npoints = 1000
    for i in range(npoints):
        x = POST_LEFT + i*POST_WIDTH/npoints
        y = 0.5*a*x**2 + y0
        curve.plot(x, y)
    return


def catenary_length(alpha):
    # Return the length of a catenary with the given alpha between our posts
    return 2*sinh(alpha*POST_WIDTH/2)/alpha


def parabola_length(a):
    # Return the curve length of a parabola 0.5at^2 between our posts.
    t = a*POST_WIDTH/2
    return (t*sqrt(1 + t**2) + log(t + sqrt(1 + t**2)))/a


def bisection_search(target, func, guess):
    # Finds x such that
    #    func(x) = target
    # Using a bisection search. This was not expected. It would also be fine to
    # figure out the solution by hand, use Mathematica, etc.
    guess_min = 0.01*guess
    guess_max = 100*guess
    for _ in range(50):
        guess_med = 0.5*(guess_min + guess_max)
        target_med = func(guess_med)
        if target > target_med:
            guess_min = guess_med
        else:
            guess_max = guess_med
    return guess_med


def init_graph():
    return graph(
        title="Shape of a Hanging Chain",
        xtitle="X",
        ytitle="Y",
        fast=False,
    )


if __name__ == "__main__":
    main()
