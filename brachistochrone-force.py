#!/usr/bin/env python3

import math
import random
import vpython

# Some global variables for convenience

DEG = math.pi/180
RAD = 1/DEG

WHEEL_RADIUS = 100
GRAVITY = 9.81

COLORS = (
    vpython.color.red,
    vpython.color.orange,
    vpython.color.yellow,
    vpython.color.green,
    vpython.color.blue,
    vpython.color.magenta,
)


def main():
    draw_wire()
    init_graph()
    beads = init_beads(6)
    t, dt, tmax = 0, 0.1, 6
    while t < tmax:
        t += dt
        vpython.rate(1/dt)
        all_done = True
        for i, bead in enumerate(beads):
            # Once this bead gets to the bottom, stop updating it. Once all the
            # beads get to the bottom, we're all done.
            if advance_bead(bead, dt):
                all_done = False
            else:
                print("bead", i, "done after %.2f" % t, "s")
            bead.graph.plot(t, 180 - wire_theta(bead.pos.y)*RAD)
        if all_done:
            break
    return


def advance_bead(bead, dt):
    # Short-circuit this bead's motion as soon as it gets to the bottom
    if bead.pos.x > 0:
        return False
    # Figure out the unconstrained velocity first, then project it onto the
    # direction of the wire. Don't bother computing the force of constraint.
    dvdt = vpython.vector(0, -GRAVITY, 0)
    v = bead.v + dvdt*dt
    w_hat = wire_direction(wire_theta(bead.pos.y))
    bead.v = w_hat*v.dot(w_hat)
    bead.pos += bead.v*dt
    return True


def draw_wire():
    theta_min, theta_max = 0, 360*DEG
    dtheta = (theta_max - theta_min)/500
    theta = theta_min
    while theta < theta_max:
        x0, y0 = wire_x(theta), wire_y(theta)
        x1, y1 = wire_x(theta + dtheta), wire_y(theta + dtheta)
        head = vpython.vector(x0, y0, 0)
        tail = vpython.vector(x1, y1, 0)
        vpython.cylinder(
            pos=tail,
            axis=(head - tail),
            radius=0.02*WHEEL_RADIUS,
            texture=vpython.textures.metal,
        )
        theta += dtheta
    return


def init_graph():
    vpython.graph(
        title="Beads on a Cycloid Wire",
        xtitle="Time (s)",
        ytitle="180<sup>o</sup> - Cycloid Angle (<sup>o</sup>)",
        fast=False,
    )
    return


def init_beads(nbeads):
    beads = []
    for i in range(nbeads):
        theta_start = 180*DEG*(i + 0.5)/nbeads
        bead = vpython.sphere(
            pos=vpython.vector(wire_x(theta_start), wire_y(theta_start), 0),
            radius=0.1*WHEEL_RADIUS,
            color=COLORS[i],
        )
        # Use the bead object to keep track of all the dead's data, not just
        # the visual stuff.
        bead.v = vpython.vector(0, 0, 0)
        bead.graph = vpython.gcurve(color=COLORS[i], width=2)
        beads.append(bead)
    return beads


# Some helper functions for keeping track of the shape of the wire. Note
# there's an offset above y=0 because the camera is centered at the origin


def wire_x(theta):
    return WHEEL_RADIUS*(theta - math.sin(theta)) - math.pi*WHEEL_RADIUS


def wire_y(theta):
    return WHEEL_RADIUS*math.cos(theta)


def wire_theta(y):
    # Note: since we're getting theta from y, this will only work for descent
    try:
        return math.acos(y/WHEEL_RADIUS)
    # Numerical jitters may dip us a bit below zero
    except ValueError:
        return math.pi


def wire_direction(theta):
    small = 1e-5
    dy = wire_y(theta + small) - wire_y(theta - small)
    dx = wire_x(theta + small) - wire_x(theta - small)
    return vpython.vector(dx, dy, 0)/math.sqrt(dx*dx + dy*dy)


if __name__ == "__main__":
    main()
