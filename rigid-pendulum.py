#!/usr/bin/env python3

"""
Rigid Pendulum
Charles Fyfe
Fall 2020

Start a rigid pendulum from rest at some height. Plot a comparison with the
small angle approximation. The larger the initial height, the worse they line
up with one another.
"""


from vpython import *


GRAVITY = 9.8
# Trig functions work in radians, but degrees are more legible for input and
# graphs. These global variables let us go back and forth easily.
DEG = pi/180
RAD = 1/DEG


def main():
    init_box()
    graphs = init_graphs()
    # Change this value to start the ball higher or lower
    angle_initial = 45*DEG
    wire, ball = init_wire_and_ball(angle=angle_initial)
    # Smaller time step means more accuracy, but also means the computer has to
    # do that much more work.
    t, dt, tmax = 0, 0.01, 30
    while t < tmax:
        t += dt
        rate(1/dt)
        # Break gravity into radial and perpendicular components.
        f_gravity = ball.mass*vector(0, -GRAVITY, 0)
        f_gravity_radial = wire.axis.hat*dot(f_gravity, wire.axis.hat)
        f_gravity_tangent = f_gravity - f_gravity_radial
        # In order to maintain a circular path, the net radial force must be
        # mv^2/r. The tension will be whatever it needs to be to make that
        # happen. You can think of it like a really really stiff spring:
        # sometimes it pushes, sometimes it pulls, but it always maintains the
        # same length.
        f_centripetal = -wire.axis.hat*ball.mass*ball.velocity.mag**2/wire.length
        f_net = f_gravity_tangent + f_centripetal
        ball.velocity += f_net*dt/ball.mass
        ball.pos += ball.velocity*dt
        wire.axis = ball.pos
        # Trig functions deal with radians, so we multiply by 180/pi to get
        # degrees, which are more legible.
        ball_angle = atan(ball.pos.x/ball.pos.y)*RAD
        ideal_angle = angle_initial*cos(sqrt(wire.length/GRAVITY)*t)*RAD
        graphs["ball"].plot(t, ball_angle)
        graphs["sine"].plot(t, ideal_angle)
    return


def init_graphs():
    graph(
        title="Pendulum Model vs Small Angle Approximation",
        xtitle="Time (s)",
        ytitle="Oscillation Angle (<sup>o</sup>)",
        fast=False,
    )
    ball_curve = gcurve(color=color.red, width=2, label="Pendulum")
    sine_curve = gcurve(color=color.blue, width=2, label="sqrt(L/g)")
    return {"sine": sine_curve, "ball": ball_curve}


def init_wire_and_ball(angle):
    wire_length = 10
    pos_initial = wire_length*vector(-sin(angle), -cos(angle), 0)
    ball = sphere(
        pos=pos_initial,
        radius=1,
        color=color.red,
        mass=1,
        velocity=vector(0, 0, 0),
    )
    wire = cylinder(
        pos=vector(0, 0, 0),
        axis=ball.pos,
        radius=0.1,
    )
    return wire, ball


def init_box():
    # No need to name or return the box, since it does not change.
    box_size = 20
    # Position is the center of the box. We want the edge at the origin.
    box_center = vector(0, 0.5*box_size, 0)
    box(
        pos=box_center,
        width=box_size,
        length=box_size,
        height=box_size,
        texture=textures.stucco,
    )
    return


if __name__ == "__main__":
    main()
