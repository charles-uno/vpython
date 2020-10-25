#!/usr/bin/env python3

from math import *
from vpython import *


SPRING_CONSTANTS = [1, 1, 1]
BLOCK_MASSES = [1, 1]
BLOCK_POSITIONS = [2, 2]
N_BLOCKS = len(BLOCK_MASSES)

# Relaxed length is a cosmetic detail so we might as well keep it consistent.
RELAXED_LENGTH = 10


def main():
    init_graph()
    # Even though there are only a few masses, it's still convenient to keep
    # track of the movement of the masses in a list, just like we did for the
    # hanging chain. That way we can use a loop to iterate over them, rather
    # than copy-pasting code that's pretty much the same. Note that we also
    # treat the left and right walls as fixed chain links, just like we did for
    # the hanging chain.
    blocks = init_blocks()
    springs = init_springs(blocks)
    t = 0
    tmax = 100
    dt = 0.01
    while t < tmax:
        rate(1/dt)
        t += dt
        # Figure out all the forces first, then go through and apply them. This
        # way we don't have to worry about moving one block while we're still
        # making calculations for its neighbor.
        forces = get_forces(blocks, springs)
        for i in range(len(forces)):
            # Don't bother with the walls.
            if i == 0 or i > N_BLOCKS:
                continue
            blocks[i].p += forces[i]*dt
            blocks[i].pos += blocks[i].p*dt/blocks[i].m
            blocks[i].curve.plot(t, blocks[i].pos.x)
        redraw_springs(blocks, springs)
    return


def get_forces(blocks, springs):
    # Block 0 is the left wall, which does not move. Block 1 moved, and is
    # between spring 0 and spring 1. The last block is also fixed, since it's
    # the right wall.
    forces = []
    for i in range(len(blocks)):
        forces.append(vector(0, 0, 0))
        if i == 0 or i > N_BLOCKS:
            continue
        # When j=-1, we're looking at left neighbors. When j=1 we're looking at
        # right neighbors.
        for j in [-1, 1]:
            neighbor_distance = blocks[i+j].pos - blocks[i].pos
            stretch = neighbor_distance.mag - RELAXED_LENGTH
            # The index of -1 refers to the last entry in the list.
            forces[-1] += springs[i-1].k*stretch*neighbor_distance.hat
    return forces


def redraw_springs(blocks, springs):
    # Walls are blocks, so spring i lives between block i and block i+1.
    for i in range(N_BLOCKS+1):
        springs[i].pos = blocks[i].pos
        springs[i].axis = blocks[i+1].pos - springs[i].pos
    return


def init_blocks():
    left_edge = vector(-1.5*RELAXED_LENGTH, 0, 0)
    right_edge = vector(1.5*RELAXED_LENGTH, 0, 0)
    # The first and last "blocks" are walls fixed on the left and right.
    walls = []
    for x in [left_edge, right_edge]:
        wall = box(
            pos=x,
            size=vector(RELAXED_LENGTH/10, RELAXED_LENGTH, RELAXED_LENGTH/3),
            texture=textures.stucco,
            m=1,
            p=vec(0, 0, 0),
        )
        walls.append(wall)
    # In between the walls are a pair of moving masses.
    colors = [color.blue, color.red]
    balls = []
    for i in range(N_BLOCKS):
        relaxed_pos = left_edge + (i+1)*vector(RELAXED_LENGTH, 0, 0)
        ball = sphere(
            pos=relaxed_pos + vector(BLOCK_POSITIONS[i], 0, 0),
            radius=0.2*RELAXED_LENGTH,
            color=colors[i],
            m=BLOCK_MASSES[i],
            p=vector(0, 0, 0),
        )
        ball.curve = gcurve(color=colors[i], width=2)
        balls.append(ball)
    # Return them in the correct order!
    return walls[0], balls[0], balls[1], walls[1]


def init_springs(blocks):
    springs = []
    for i, k in enumerate(SPRING_CONSTANTS):
        # Spring i will go from block i to block i+1
        left = blocks[i].pos
        right = blocks[i+1].pos
        spring = helix(
            pos=left,
            axis=right - left,
            color=color.white,
            loops=10,
            radius=0.05*RELAXED_LENGTH,
            k=k,
        )
        springs.append(spring)
    return springs


def init_graph():
    return graph(
        title="Coupled Oscillators",
        xtitle="Time (s)",
        ytitle="Displacement (m)",
        fast=False,
    )


if __name__ == "__main__":
    main()
