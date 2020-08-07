#!/usr/bin/env python3

import math
import random
import vpython


# Keep track of time globally so we don't have to pass it around everywhere
t = 0
dt = 0.01
tmax = 30


def main():
    global t

    vpython.graph(
        title="Weight on a Spring",
        xtitle="Time (s)",
        ytitle="Displacement (m)",
        fast=False,
    )
    graph = vpython.gcurve(color=vpython.color.red, width=2)

    box = vpython.box(
        pos=vpython.vector(-10, 0, 0),
        width=20,
        length=20,
        height=20,
    )

    x_relax = 10
    x = 5
    r = 1
    k = 1
    m = 1
    v = 0

    spring = vpython.helix(
        pos=vpython.vector(0, 0, 0),
        coils=10,
        axis=vpython.vector(x, 0, 0),
    )

    weight = vpython.sphere(
        pos=vpython.vector(x + r, 0, 0),
        radius=r,
        color=vpython.color.red,
    )

    while t < tmax:

        x_offset = weight.pos.x - weight.radius - x_relax

        graph.plot(t, x_offset)

        force_x = -k*x_offset
        v += force_x*dt/m
        dx = v*dt
        weight.pos.x += dx
        spring.axis.x += dx

        vpython.rate(1/dt)

        t += dt

    return


if __name__ == "__main__":
    main()
