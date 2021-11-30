#!/usr/bin/env python3

from math import *
from vpython import *


EARTH_MASS = 5.97e24
SUN_MASS = 1.99e30
EARTH_ORBIT_RADIUS = 1.496e11
YEAR = 3.154e7
G = 6.674e-11
# Degrees are more legible but the computer uses radians.
DEGREES = pi/180

# For a circular orbit, we need the force of gravity to match up with the
# centripetal force, mv^2/r. Use that to compute the perpendicular momentum,
# then the orbital angular momentum.
F_GRAV = G*EARTH_MASS*SUN_MASS/EARTH_ORBIT_RADIUS**2
EARTH_MOMENTUM = sqrt(EARTH_ORBIT_RADIUS*EARTH_MASS*F_GRAV)
# The effective potential depends on the reduced mass as well as the orbital
# angular momentum. We'll keep this constant across all planets we look at.
EARTH_ORBITAL_ANGULAR_MOMENTUM = EARTH_ORBIT_RADIUS*EARTH_MOMENTUM

# Scale back the trails and graphs to make execution smoother.
PLOT_INTERVAL = 20


def main():
    init_graph()
    draw_potential()
    planets = [
        get_planet(color=color.red, launch_angle=0),
        get_planet(color=color.orange, launch_angle=10*DEGREES),
        get_planet(color=color.yellow, launch_angle=20*DEGREES),
        get_planet(color=color.green, launch_angle=30*DEGREES),
        get_planet(color=color.cyan, launch_angle=40*DEGREES),
    ]
    sun = get_sun()
    # We want to watch years of motion in just a few seconds.
    dt = 0.001*YEAR
    step = 0
    max_steps = 10*YEAR/dt
    while step < max_steps:
        # Play back one year of movement per second.
        rate(1*YEAR/dt)
        step += 1
        for planet in planets:
            r = planet.pos - sun.pos
            force = -r.hat * G*planet.mass*sun.mass/r.mag**2
            # We want each two-body problem to be independent, but they all
            # share the same sun. To avoid any coupling between the planets,
            # fix the position of the sun. This is only a tiny bit inaccurate
            # since the sun is several orders of magnitude more massive than
            # the earth.
            planet.momentum += force*dt
            planet.pos += planet.momentum*dt/planet.mass
            energy = system_energy(sun, planet)
            # To improve performance, don't update the graph every time
            if step % PLOT_INTERVAL == 0:
                planet.curve.plot(r.mag, energy)
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
    print("Potential well depth:", umin)
    return graph(
        title="Energy Trajectories of Planetary Orbits",
        xtitle="Planet-Sun Separation (m)",
        ytitle="System Energy (J)",
        fast=False,
        # We care about the potential well, not asymptotes going to infinity.
        ymin=1.2*umin,
        ymax=-0.6*umin,
    )
    return


def draw_potential():
    curve_ugrav = gcurve(color=color.black, width=0.5, label="U<sub>g</sub>")
    curve_ucent = gcurve(color=color.black, width=0.5, label="U<sub>cf</sub>")
    curve_ueff = gcurve(color=color.black, width=1, label="U<sub>eff</sub>")
    for i in range(1, 100):
        r = EARTH_ORBIT_RADIUS*i/15
        curve_ugrav.plot(r, ugrav(r))
        curve_ucent.plot(r, ucent(r))
        curve_ueff.plot(r, ugrav(r) + ucent(r))
    return


def get_planet(color, launch_angle):
    # The launch angle is relative to the circular orbit.
    radial_momentum = EARTH_MOMENTUM*tan(launch_angle)
    planet = sphere(
        radius=0.05*EARTH_ORBIT_RADIUS,
        color=color,
        pos=vector(0, EARTH_ORBIT_RADIUS, 0),
        mass=EARTH_MASS,
        momentum=vector(EARTH_MOMENTUM, radial_momentum, 0),
        make_trail=True,
        interval=PLOT_INTERVAL,
    )
    kinetic_energy = 0.5*planet.momentum.y**2/planet.mass
    print("Creating planet with radial kinetic energy:", kinetic_energy)
    # We need a curve for each planet object. Might as well attach the
    # curves to the planets rather than storing them somewhere else.
    planet.curve = gcurve(color=color, width=2)
    return planet


def get_sun():
    # For a proper simulation, the sun would move. But that makes our logistics
    # tricky, since we want to just look at two-body systems, and there are
    # multiple planets orbiting the same sun. For simplicity, and since the
    # motion of the sun is a comparatively small source of energy, let's just
    # fix it.
    return sphere(
        radius=0.2*EARTH_ORBIT_RADIUS,
        color=color.white,
        pos=vector(0, 0, 0),
        mass=SUN_MASS,
        momentum=vector(0, 0, 0),
        make_trail=True,
    )


if __name__ == "__main__":
    main()
