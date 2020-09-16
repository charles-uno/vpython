#!/usr/bin/env python3

from math import *
from vpython import *

# Degrees are more legible, but trig functions use radians.
DEG = pi/180
RAD = 1/DEG

WHEEL_RADIUS = 100
GRAVITY = 9.81
BEAD_MASS = 1


def main():
    init_wire()
    init_graph()
    # Create a handful of color-coded beads, each starting at a different angle
    beads = [
        init_bead(color=color.red, angle=15*DEG),
        init_bead(color=color.orange, angle=45*DEG),
        init_bead(color=color.yellow, angle=75*DEG),
        init_bead(color=color.green, angle=105*DEG),
        init_bead(color=color.blue, angle=135*DEG),
        init_bead(color=color.magenta, angle=165*DEG),
    ]
    # We'll loop until we get to the bottom, but set tmax as a precaution.
    # Don't want to spin our wheels forever if something goes wrong.
    t, dt, tmax = 0, 0.1, 20
    while t < tmax:
        t += dt
        rate(1/dt)
        for bead in beads:
            # Use energy conservation to figure out kinetic energy. That whole
            # kinetic energy is velocity along the direction of the wire.
            energy_kinetic = bead.energy_initial - bead.mass*GRAVITY*bead.pos.y
            direction = wire_direction(wire_theta(bead.pos.y))
            velocity = sqrt(2*energy_kinetic/bead.mass)*direction
            bead.pos += velocity*dt
            # Let's plot angle along the cycloid curve rather than the vertical
            # component of the position. The angle goes from 0 to 180 degrees,
            # which is pretty easy to eyeball, whereas the vertical position is
            # scaled to the arbitrary wheel radius.
            bead.graph.plot(t, 180 - wire_theta(bead.pos.y)*RAD)
            # Stop updating as soon as any bead gets to the bottom. In theory,
            # they should all get there at pretty much the same time.
            if bead.pos.x > 0:
                break
    return


def init_wire():
    # Trace the cycloid curve, drawing a bunch of tiny cylinders as we go, to
    # draw the wire.
    theta_min, theta_max = 0, 360*DEG
    dtheta = (theta_max - theta_min)/500
    theta = theta_min
    while theta < theta_max:
        x0, y0 = wire_x(theta), wire_y(theta)
        x1, y1 = wire_x(theta + dtheta), wire_y(theta + dtheta)
        head = vector(x0, y0, 0)
        tail = vector(x1, y1, 0)
        cylinder(
            pos=tail,
            axis=(head - tail),
            radius=0.02*WHEEL_RADIUS,
            texture=textures.metal,
        )
        theta += dtheta
    return


def init_graph():
    graph(
        title="Beads on a Cycloid Wire",
        xtitle="Time (s)",
        ytitle="180<sup>o</sup> - Cycloid Angle (<sup>o</sup>)",
        fast=False,
    )
    return


def init_bead(color, angle):
    bead = sphere(
        pos=vector(wire_x(angle), wire_y(angle), 0),
        radius=0.1*WHEEL_RADIUS,
        color=color,
        mass=BEAD_MASS,
    )
    # Use the bead object to keep track of all the dead's data, not just the
    # visual stuff.
    bead.graph = gcurve(color=color, width=2)
    # Keep track of the initial energy so we can later map from position to
    # velocity. Also need to give each bead a tiny kick to get going. Otherwise
    # the initial velocity will be zero and nothing will ever move.
    bead.energy_initial = bead.mass*GRAVITY*bead.pos.y + 1e-5
    return bead


# Some helper functions for keeping track of the shape of the wire. Note
# there's an offset above y=0 because the camera is centered at the origin
def wire_x(theta):
    return WHEEL_RADIUS*(theta - sin(theta)) - pi*WHEEL_RADIUS


def wire_y(theta):
    return WHEEL_RADIUS*cos(theta)


def wire_theta(y):
    # Note: due to the domain of acos, this will only work on the descent
    try:
        return acos(y/WHEEL_RADIUS)
    # Numerical jitters may dip us a bit below zero
    except ValueError:
        return pi


def wire_direction(theta):
    small = 1e-5
    dy = wire_y(theta + small) - wire_y(theta - small)
    dx = wire_x(theta + small) - wire_x(theta - small)
    return vector(dx, dy, 0)/sqrt(dx*dx + dy*dy)


if __name__ == "__main__":
    main()
