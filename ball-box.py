#!/usr/bin/env python3

import math
import random
import vpython


GRAVITY = -9.81


def main():
    box_size = 10
    box_thickness = 1
    ball_radius = 0.5
    # Set the axis of each side to be a perpendicular unit vector pointing into
    # the box. That'll allow us to handle all the walls in a loop, rather than
    # spelling them out
    axes = [
        vpython.vector(1, 0, 0),
        vpython.vector(-1, 0, 0),
        vpython.vector(0, 1, 0),
    ]
    box_sides = []
    for axis in axes:
        side = vpython.box(
            pos=-0.5*box_size*axis,
            axis=axis,
            height=box_size,
            width=box_size,
        )
        box_sides.append(side)

        vpython.arrow(
            pos=-0.5*box_size*axis,
            axis=axis,
            color=vpython.color.blue,
        )

    # Initial position chosen randomly inside the box
    x0 = vpython.vector(
        random.random()*box_size - 0.5*box_size,
        random.random()*box_size - 0.5*box_size,
        0,
    )
    # Initial velocity small enough that we should not escape
    v_max = math.sqrt(-2*GRAVITY*(0.5*box_size - x0.y))
    v0 = vpython.vector(
        random.random()*v_max,
        random.random()*v_max,
        0,
    )
    # Initialize the ball. Python also lets us attach an extra attribute, in
    # this case velocity, to the ball object.
    ball = vpython.sphere(
        pos=x0,
        color=vpython.color.red,
        radius=ball_radius,
    )
    ball.v = v0
    ball.m = 1
    # Set up the graph pane and each curve we want in it
    vpython.graph(
        title="Ball in a Box",
        xtitle="Time (s)",
        ytitle="Energy (J)",
        fast=False,
    )
    graph_pot = vpython.gcurve(color=vpython.color.blue, width=2, label="Potential Energy")
    graph_kin = vpython.gcurve(color=vpython.color.red, width=2, label="Kinetic Energy")
    graph_tot = vpython.gcurve(color=vpython.color.magenta, width=2, label="Total Energy")
    # Time loop! Handle gravity and collisions
    t, dt, tmax = 0, 0.001, 10
    while t < tmax:
        t += dt
        vpython.rate(1/dt)
        dvdt = -GRAVITY*vpython.vector(0, -1, 0)
        ball.v += dvdt*dt
        ball.pos += ball.v*dt
        # Check for collisions
        for side in box_sides:
            # Vector from the center of the ball to the center of the wall
            center_to_center = ball.pos - side.pos
            # Project onto the wall's perpendicular unit vector to get distance
            distance = center_to_center.dot(side.axis)
            # If it's a collision, flip the component of the ball's velocity
            # that's perpendicular to the wall
            if distance < (ball.radius + 0.5*box_thickness):
                dv = -2*side.axis.dot(ball.v)
                ball.v += side.axis*dv
        energy_pot = -ball.m*GRAVITY*ball.pos.y
        energy_kin = 0.5*ball.m*ball.v.dot(ball.v)
        graph_pot.plot(t, energy_pot)
        graph_kin.plot(t, energy_kin)
        graph_tot.plot(t, energy_pot + energy_kin)
    return


if __name__ == "__main__":
    main()
