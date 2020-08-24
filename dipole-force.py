#!/usr/bin/env python3

"""
Motion of a charged particle in the equatorial plane of a dipole magnetic field.
"""

import vpython

# Characteristic scales are not necessarily physical. They are chosen for
# visibility.
R0 = 1
B0 = 2
M0 = 1
Q0 = 2
V0 = 1

T = 0
DT = 0.001
TMAX = 10


# For looking at the difference between the euler method and the midpoint
# method. Midpoint method is stable at DT=0.01, while euler method is unstable
# even at a tenth of that.
USE_MIDPOINT = False


def main():
    global T
    earth = vpython.sphere(
        color=vpython.color.green,
        radius=0.2*R0,
        pos=vpython.vector(0, 0, 0),
    )
    ion = vpython.sphere(
        color=vpython.color.magenta,
        radius=0.05*R0,
        pos=vpython.vector(0, R0, 0),
        make_trail=True,
        interval=10,
    )
    # Tack some physical (but non-displaying) parameters onto the ion object
    ion.v = vpython.vector(V0, 0, 0)
    ion.v_prev = ion.v
    ion.q = Q0
    ion.m = M0
    while T < TMAX:
        T += DT
        vpython.rate(1/DT)
        # Print out the velocity once per second to keep an eye out for
        # numerical instability. If this changes a lot, something is wrong.
        if int(T + DT) > int(T):
            print("v:", ion.v.mag)
            if ion.pos.mag > 100*R0:
                print("UH OH")
                break
            if ion.v.mag > 2.5*V0:
                print("UH OH")
                break
        force = get_force(ion)
        ion.v += force*DT/ion.m
        ion.pos += ion.v*DT
    return


def get_force(ion):
    # Velocity is tracked half a time step behind position and magnetic field.
    # That is, we have r(0), and so we also have B(0). But to jump from r(-1)
    # to r(0), we used v(-0.5). In order to get F(0), we interpolate v(0) from
    # v(-0.5) and v(-1.5).
    if USE_MIDPOINT:
        v_int = 1.5*ion.v - 0.5*ion.v_prev
    # Alternatively, skip the interpolation.
    else:
        v_int = ion.v
    ion.v_prev = ion.v
    b = get_b(ion.pos)
    # This force will take us from v(-0.5) to v(0.5), then we'll use v(0.5) to
    # go from r(0) to r(1).
    return ion.q*v_int.cross(b)


def get_b(pos):
    return B0*(pos.mag/R0)**3*vpython.vector(0, 0, -1)


if __name__ == "__main__":
    main()
