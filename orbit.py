#!/usr/bin/env python3

import math
import vpython


AU = 1.496e11
M_SUN = 1.988e30
M_EARTH = 5.97e24
SECOND = 1
DAY = 86400
YEAR = 365*DAY
G = 6.674e-11

V_EARTH = 2*math.pi*AU/YEAR


def main():
    sun, earth = init_bodies()
    graphs = init_graphs()
    t, dt, tmax = 0, 1*DAY, 5*YEAR
    while t < tmax:
        t += dt
        # Scale down the rate so 1 year takes 10 seconds
        rate_scale = YEAR/(10*SECOND)
        vpython.rate(rate_scale/dt)
        # Gravitational force needs magnitude and direction of the separation
        # of the bodies
        r_es = sun.pos - earth.pos
        force_magnitude = G*earth.mass*sun.mass/r_es.mag**2
        force = force_magnitude*r_es.hat
        # Equal and opposite! Sun doesn't move much though
        earth.v += force*dt/earth.mass
        sun.v += -force*dt/sun.mass
        earth.pos += earth.v*dt
        sun.pos += sun.v*dt
        earth.path.append(earth.pos)
        # Plot the energy, I guess
        energy_pot = -G*earth.mass*sun.mass/r_es.mag
        energy_kin = (
            0.5*earth.mass*earth.v.mag**2 +
            0.5*sun.mass*sun.v.mag**2
        )
        graphs["potential"].plot(t/DAY, energy_pot)
        graphs["kinetic"].plot(t/DAY, energy_kin)
        graphs["total"].plot(t/DAY, energy_pot + energy_kin)
    return


def init_graphs():
    vpython.graph(
        title="Energy of Earth's Orbit",
        xtitle="Time (days)",
        ytitle="Energy (J)",
        fast=False,
    )
    return {
        "potential": vpython.gcurve(color=vpython.color.blue, width=2),
        "kinetic": vpython.gcurve(color=vpython.color.red, width=2),
        "total": vpython.gcurve(color=vpython.color.magenta, width=2),
    }


def init_bodies():
    sun = vpython.sphere(
        color=vpython.color.yellow,
        pos=vpython.vector(0, 0, 0),
        radius=0.1*AU,
    )
    sun.mass = 1*M_SUN
    sun.v = vpython.vector(0, 0, 0)
    earth = vpython.sphere(
        color=vpython.color.green,
        pos=vpython.vector(1*AU, 0, 0),
        radius=0.02*AU,
    )
    earth.mass = 1*M_EARTH
    earth.v = V_EARTH*vpython.vector(0, 1, 0)*0.8
    earth.path = vpython.curve(
        pos=earth.pos,
        color=vpython.color.white,
    )
    return sun, earth


if __name__ == "__main__":
    main()
