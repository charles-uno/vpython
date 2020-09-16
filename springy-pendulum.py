GlowScript 3.0 VPython

"""
Springy Pendulum
Charles Fyfe
Fall 2020
"""


GRAVITY = 9.8


def main():
    graphs = init_graphs()
    spring, ball = init_spring_and_ball()
    # Give the ball a little kick to get it started.
    ball.velocity = vector(5, 0, 0)
    # Note that the springy pendulum requires a pretty small time step for
    # stability! With a larger time step, energy is not conserved.
    t, dt, tmax = 0, 0.01, 30
    while t < tmax:
        t += dt
        rate(1/dt)
        # VPython vector objects have nice helper methods for when we need
        # magnitudes and unit vectors.
        length = spring.axis.mag
        stretch = length - spring.length_relax
        direction = spring.axis.hat
        # Physics happens here.
        force_spring = -spring.spring_constant*stretch*direction
        force_gravity = ball.mass*vector(0, -GRAVITY, 0)
        force_net = force_spring + force_gravity
        ball.velocity += force_net*dt/ball.mass
        ball.pos += ball.velocity*dt
        # Update the spring to stay connected to the ball
        spring.axis = ball.pos - spring.pos
        # Update the graphs every iteration
        energy_spring = 0.5*spring.spring_constant*stretch**2
        energy_grav = ball.mass*GRAVITY*ball.pos.y
        energy_kinetic = 0.5*ball.mass*ball.velocity.mag**2
        energy_total = energy_spring + energy_kinetic + energy_grav
        graphs["kinetic"].plot(t, energy_kinetic)
        graphs["spring"].plot(t, energy_spring)
        graphs["grav"].plot(t, energy_grav)
        graphs["total"].plot(t, energy_total)
    return


def init_graphs():
    graph(
        title="Energy of a Springy Pendulum",
        xtitle="Time (s)",
        ytitle="Energy (J)",
        fast=False,
    )
    # Return the graphs in a dictionary so we can easily keep track of what's
    # what. Also make sure the curves have labels!
    graph_kinetic = gcurve(color=color.red, width=2, label="Kinetic Energy")
    graph_spring = gcurve(color=color.blue, width=2, label="Spring Energy")
    graph_grav = gcurve(color=color.green, width=2, label="Gravitational Energy")
    graph_total = gcurve(color=color.black, width=2, label="Total Energy")
    return {
        "kinetic": graph_kinetic,
        "grav": graph_grav,
        "spring": graph_spring,
        "total": graph_total,
    }


def init_spring_and_ball():
    # Draw a box to anchor the spring, but don't bother naming or returning it.
    # It does not change over time.
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
    # VPython objects are initialized with their display attributes. We can
    # then add additional attributes for convenient bookkeeping.
    spring_length_relax = 10
    spring_length_start = 5
    spring_axis = vector(0, -spring_length_start, 0)
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


if __name__ == "__main__":
    main()
