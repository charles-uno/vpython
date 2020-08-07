#!/usr/bin/env python3

from vpython import *

deg = pi/180

r = 1
dtheta = 5*deg
length = 10
z = -length/2

loops = 20
dz_dtheta = length/(loops*360*deg)

theta = 0

while z < length/2:

    head = vector(z, r*sin(theta), r*cos(theta))
    theta += dtheta
    z += dz_dtheta*dtheta
    tail = vector(z, r*sin(theta), r*cos(theta))
    cylinder(
        pos=tail,
        axis=(head - tail),
        radius=0.05,
        texture=textures.metal,
    )
