#!/usr/bin/env python3

from math import *
from vpython import *

# To make numbers more legible, measure distance in earth orbit radii, time in
# years, and mass in earth masses.
KILOGRAM = 1/(5.97e24)
METER = 1/(1.496e11)
SECOND = 1/(3.154e7)

EARTH_MASS = 5.97e24*KILOGRAM
SUN_MASS = 1.99e30*KILOGRAM
EARTH_ORBIT_RADIUS = 1.496e11*METER
YEAR = 3.154e7*SECOND
G = 6.674e-11*METER**3/KILOGRAM/SECOND**2

# For a circular orbit, we need the force of gravity to match up with the
# centripetal force, mv^2/r. Use that to compute the perpendicular momentum,
# then the orbital angular momentum.
F_GRAV = G*EARTH_MASS*SUN_MASS/EARTH_ORBIT_RADIUS**2
EARTH_MOMENTUM = sqrt(EARTH_ORBIT_RADIUS*EARTH_MASS*F_GRAV)
# The effective potential depends on the reduced mass as well as the orbital
# angular momentum. The easiest way to look at multiple planets is to just mess
# with the radial component of the initial velocity. Leave perpendicular
# velocity and mass consistent.
EARTH_ORBITAL_ANGULAR_MOMENTUM = EARTH_ORBIT_RADIUS*EARTH_MOMENTUM

# Our units are legible... but what do they mean? Figure out what our units of
# energy are.
JOULE = KILOGRAM*METER**2/SECOND**2
print("Energy of 1 corresponds to:", 1/JOULE, "J")

# Non-physical parameter -- how fast do we want the animation to play?
YEARS_PER_SECOND = 0.25


def main():
    init_graph()
    draw_potential()
    planets = get_planets(
        color.green,
        color.blue,
        color.magenta,
        color.red,
        color.orange,
    )
    sun = get_sun()
    # We want to watch years of motion in just a few seconds.
    t = 0
    dt = 0.001*YEAR
    tmax = 10*YEAR
    while t < tmax:
        rate(YEARS_PER_SECOND/dt)
        t += dt
        for planet in planets:
            r = planet.pos - sun.pos
            force = -r.hat * G*planet.mass*sun.mass/r.mag**2
            # Fix the position of the sun. This is slightly inaccurate, but
            # saves us a lot of headaches due to looking at multiple planets at
            # the same time.
            planet.momentum += force*dt
            planet.pos += planet.momentum*dt/planet.mass
            energy = system_energy(sun, planet)
            r = (planet.pos - sun.pos).mag
            planet.curve.plot(r, energy)
    return


def system_energy(body1, body2):
    return (
        0.5*body1.momentum.mag**2/body1.mass +
        0.5*body2.momentum.mag**2/body2.mass +
        -G*body1.mass*body2.mass/(body1.pos - body2.pos).mag
    )


def ugrav(r):
    return -G*EARTH_MASS*SUN_MASS/r


def ucent(r):
    return EARTH_ORBITAL_ANGULAR_MOMENTUM**2/(2*EARTH_MASS*r**2)


def init_graph():
    umin = ugrav(EARTH_ORBIT_RADIUS) + ucent(EARTH_ORBIT_RADIUS)
    return graph(
        title="Energy of Planetary Orbits",
        xtitle="r (Earth orbit radii)",
        ytitle="U (10<sup>32</sup>J)",
        fast=False,
        ymin=1.2*umin,
        ymax=-1.2*umin,
    )
    return


def draw_potential():
    curve_ugrav = gcurve(color=color.black, width=0.5, label="U<sub>g</sub>")
    curve_ucent = gcurve(color=color.black, width=0.5, label="U<sub>cf</sub>")
    curve_ueff = gcurve(color=color.black, width=1, label="U<sub>eff</sub>")
    for i in range(1, 100):
        r = EARTH_ORBIT_RADIUS*i/20
        curve_ugrav.plot(r, ugrav(r))
        curve_ucent.plot(r, ucent(r))
        curve_ueff.plot(r, ugrav(r) + ucent(r))
    return


def get_planets(*colors):
    planets = []
    for i, c in enumerate(colors):
        radial_momentum = i*EARTH_MOMENTUM/len(colors)
        planet = sphere(
            radius=0.05*EARTH_ORBIT_RADIUS,
            color=c,
            pos=vector(0, EARTH_ORBIT_RADIUS, 0),
            mass=EARTH_MASS,
            momentum=vector(EARTH_MOMENTUM, radial_momentum, 0),
            make_trail=True,
            interval=10,
        )
        # Each planet can carry arounds its own graph object.
        planet.curve = gcurve(color=c, width=2)
        planets.append(planet)
    return planets


def get_sun():
    return sphere(
        radius=0.1*EARTH_ORBIT_RADIUS,
        color=color.yellow,
        pos=vector(0, 0, 0),
        mass=SUN_MASS,
        momentum=vector(0, 0, 0),
        make_trail=True,
    )


if __name__ == "__main__":
    main()
