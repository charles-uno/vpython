GlowScript 3.0 VPython

"""
Ball on a Spring
Charles Fyfe
Fall 2020

Numerical values are arbitrary. Don't be shy about modifying initial size,
velocity, spring constant, etc.
"""


def main():
    graph = init_graph()
    spring, ball = init_spring_and_ball()
    # Outsourcing setup to helper functions keeps our main function legible!
    t, dt, tmax = 0, 0.1, 30
    while t < tmax:
        t += dt
        # Slow down to show movement in real time
        rate(1/dt)
        # VPython vector objects have nice helper methods for when we need
        # magnitudes and unit vectors.
        length = spring.axis.mag
        stretch = length - spring.length_relax
        direction = spring.axis.hat
        # Physics happens here.
        force = -spring.spring_constant*stretch*direction
        ball.velocity += force*dt/ball.mass
        ball.pos += ball.velocity*dt
        # Update the spring to stay connected to the ball
        spring.axis = ball.pos - spring.pos
        # Add a point to the graph every iteration
        graph.plot(t, ball.pos.x)
    return


def init_graph():
    graph(
        title="Ball on a Spring",
        xtitle="Time (s)",
        ytitle="Displacement (m)",
        fast=False,
    )
    return gcurve(color=color.red, width=2)


def init_spring_and_ball():
    # Draw a box to anchor the spring, but don't bother naming or returning it.
    # It does not change over time.
    box_size = 20
    # Position is the center of the box. We want the edge at the origin.
    box_center = vector(-0.5*box_size, 0, 0)
    box(
        # Position is the center of the box. We want the edge at the origin.
        pos=box_center,
        width=box_size,
        length=box_size,
        height=box_size,
        texture=textures.stucco,
    )
    # VPython objects are initialized with their display attributes. We can
    # then add additional attributes for convenient bookkeeping.
    spring_length_relax = 10
    spring_length_start = 5
    spring_axis = vector(spring_length_start, 0, 0)
    spring = helix(
        pos=vector(0, 0, 0),
        coils=10,
        axis=spring_axis,
    )
    spring.spring_constant = 1
    spring.length_relax = spring_length_relax
    # Same deal for the ball. Position, radius, and color are all we need to
    # draw the initial object. Additional values are used later.
    ball_radius = 1
    ball = sphere(
        pos=spring.axis,
        radius=ball_radius,
        color=color.red,
    )
    ball.mass = 1
    ball.velocity = vector(0, 0, 0)
    return spring, ball


# This is a pretty typical setup for a Python script: we define a bunch of
# functions up top, then call main at the bottom to start actually doing the
# work. Notably, main only gets called if we run this script directly. If we
# import it into another script (for example, to reuse the helper functions)
# then this will not call main.
if __name__ == "__main__":
    main()
