#!/usr/bin/env python3

"""
Ball on a Spring
Charles Fyfe
Fall 2020
"""

# You may be used to "from vpython import *"
# Best practice is to instead import the whole namespace. This makes debugging
# a lot easier. What would happen, for example, if you imported two libraries
# with two different definitions of the "vector" object?


import vpython


def main():
    graph = init_graph()
    spring, ball = init_setup()
    # Outsourcing setup to helper functions keeps our main function legible!
    t, dt, tmax = 0, 0.1, 30
    while t < tmax:
        t += dt
        # Slow down to show movement in real time
        vpython.rate(1/dt)
        # VPython vector objects have nice helper methods for when we need
        # magnitudes and unit vectors.
        stretch = spring.axis.mag - spring.x0
        direction = spring.axis.hat
        # Physics happens here.
        force = -spring.k*stretch*direction
        ball.v += force*dt/ball.m
        ball.pos += ball.v*dt
        # Update the spring to stay connected to the ball
        spring.axis = ball.pos - spring.pos
        # Add a point to the graph every iteration
        graph.plot(t, ball.pos.x)
    return


def init_graph():
    vpython.graph(
        title="Ball on a Spring",
        xtitle="Time (s)",
        ytitle="Displacement (m)",
        fast=False,
    )
    return vpython.gcurve(color=vpython.color.red, width=2)


def init_setup():
    # No need to return the box object, since it doesn't change
    box_size = 20
    vpython.box(
        pos=vpython.vector(-0.5*box_size, 0, 0),
        width=box_size,
        length=box_size,
        height=box_size,
        texture=vpython.textures.stucco,
    )
    # VPython objects are initialized with their display attributes. We can
    # then add additional attributes for convenient bookkeeping.
    spring_length_relax = 10
    spring_length_start = 5
    spring = vpython.helix(
        pos=vpython.vector(0, 0, 0),
        coils=10,
        axis=vpython.vector(spring_length_start, 0, 0),
    )
    spring.k = 1
    spring.x0 = spring_length_relax
    # Same deal for the ball. Position, radius, and color are all we need to
    # draw the initial object. Additional values are used later.
    ball_radius = 1
    ball = vpython.sphere(
        pos=spring.axis,
        radius=ball_radius,
        color=vpython.color.red,
    )
    ball.m = 1
    ball.v = vpython.vector(0, 0, 0)
    return spring, ball


if __name__ == "__main__":
    main()
