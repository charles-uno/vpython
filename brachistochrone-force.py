#!/usr/bin/env python3

import math
import random
import vpython

# Some global variables for convenience

DEG = math.pi/180

WHEEL_RADIUS = 1
GRAVITY = 9.81
BEAD_MASS = 1

COLORS = (
    vpython.color.red,
    vpython.color.orange,
    vpython.color.yellow,
    vpython.color.green,
    vpython.color.blue,
    vpython.color.magenta,
)


# Keep track of time globally so we don't have to pass it around everywhere
t = 0
dt = 0.001
tmax = 2


def main():
    draw_wire()
    init_graph()
    beads = init_beads(6)
    # Keep looping until the advance_beads function returns False

    sample_counter = 0

    while advance_beads(beads):

        dt_sample = 0.05
        sample_rate = dt_sample/dt

        if sample_counter % sample_rate == 0:
            stamp = "%03.0f" % (1000*t)
            print(f"saving: brac-{stamp}.png")
            vpython.scene.capture(f"brac-{stamp}.png")
        sample_counter += 1

    return


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
            radius=0.02,
            texture=vpython.textures.metal,
        )
        theta += dtheta
    return


GRAPHS = []


def init_graph():
    vpython.graph(
        title="Beads on a Cycloid Wire",
        xtitle="Time (s)",
        ytitle="Height (m)",
        fast=False,
    )
    for i, color in enumerate(COLORS):
        GRAPHS.append(
            vpython.gcurve(color=COLORS[i], width=2)
        )
    return


def init_beads(nbeads):
    beads = []
    for i in range(nbeads):
        theta_start = 180*DEG*(i + 0.5)/nbeads
        bead = vpython.sphere(
            pos=vpython.vector(wire_x(theta_start), wire_y(theta_start), 0),
            radius=0.1,
            color=COLORS[i],
        )
        # Track velocity along with position
        bead.v = vpython.vector(0, 0, 0)
        beads.append(bead)
    return beads


def advance_beads(beads):
    global t
    t += dt
    vpython.rate(1/dt)
    all_done = True
    for i, bead in enumerate(beads):
        f_g = vpython.vector(0, -BEAD_MASS*GRAVITY, 0)
        # Compute the unconstrained velocity first, then take the component
        # along the direction of the wire. Normal force will be whatever makes
        # that happen.
        v = bead.v + f_g*dt/BEAD_MASS
        w_hat = wire_direction(wire_theta(bead.pos))
        bead.v = w_hat*(v.x*w_hat.x + v.y*w_hat.y)

        if bead.v.y == 0:
            continue


        bead.pos += bead.v*dt

        if t < tmax:
            all_done = False

        GRAPHS[i].plot(t, bead.pos.y + WHEEL_RADIUS)
    return not all_done


# Some helper functions for keeping track of the shape of the wire. Note
# there's an offset above y=0 because the camera is centered at the origin


def wire_x(theta):
    return WHEEL_RADIUS*(theta - math.sin(theta)) - math.pi*WHEEL_RADIUS


def wire_y(theta):
    return WHEEL_RADIUS*math.cos(theta)


def wire_theta(pos):
    try:
        theta = math.acos(pos.y/WHEEL_RADIUS)
        return theta if pos.x < 0 else 2*math.pi - theta
    # Possible that we'll dip slightly below the wire numerically
    except ValueError:
        return math.pi

    # Alternatively, try to figure this out numerically. This lets us climb
    # back up after bottoming out, though it's a pretty big hammer.
    t0, t1 = 0, 2*math.pi
    for _ in range(30):
        if wire_error(t0, pos) < wire_error(t1, pos):
            t1 = (t0 + t1)/2
        else:
            t0 = (t0 + t1)/2
    return (t0 + t1)/2


def wire_error(theta, pos):
    x, y = wire_x(theta), wire_y(theta)
    return math.sqrt((pos.x - x)**2 + (pos.y - y)**2)







def wire_direction(theta):
    small = 1e-5
    dy = wire_y(theta + small) - wire_y(theta - small)
    dx = wire_x(theta + small) - wire_x(theta - small)
    return vpython.vector(dx, dy, 0)/math.sqrt(dx*dx + dy*dy)


if __name__ == "__main__":
    main()
