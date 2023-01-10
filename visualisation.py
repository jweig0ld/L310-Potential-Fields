import matplotlib.pyplot as plt
import numpy as np

from components import *


RESOLUTION = 25
GRID_OFFSET = 0.5


"""
TODO:

1. (DONE). Plot the grid in 2D at z=0. 
2. (DONE). Plot the planets on the grid in 2D, where z=0.
3. (DONE). Plot the asteroids on the grid in 2D, where z=0.
4. (DONE). Plot the trajectories of the asteroids on the grid in 2D, where z=0.
5. (DONE). Plot the spaceships on the grid in 2D, where z=0.
6. (DONE). Plot the trajectories of the spaceships on the grid, where z=0.
7. Plot the vector field of a spaceship where z=0.
8. Allow for the specification of a z value that is not zero. 
"""


def find_circle(c, r, z=0):
    """
    Returns the centre and radius of the circle that results from the
    intersection of the plane z=k and the sphere with centre `c` and 
    radius `r`. If there is no intersection, return (None, None).
    """
    if not (z > c[2] - r and z < c[2] + r):
        return (None, None)

    centre = c.copy()
    centre[2] = z
    d = z - c[2] # Distance between centre of resultant circle and plane z=k.
    radius = np.sqrt(np.square(r) - np.square(d))
    return centre, radius


def plot_walls(env, z=0):
    plt.plot([-env.xlen/2, env.xlen/2], [-env.ylen/2, -env.ylen/2], 'k') # Bottom
    plt.plot([-env.xlen/2, -env.xlen/2], [-env.ylen/2, env.ylen/2], 'k') # Left
    plt.plot([env.xlen/2, env.xlen/2], [-env.ylen/2, env.ylen/2], 'k') # Right
    plt.plot([-env.xlen/2, env.xlen/2], [env.ylen/2, env.ylen/2], 'k') # Top
    plt.axis('equal')
    plt.xlabel('x')
    plt.ylabel('y')
    plt.xlim([-env.xlen/2 - GRID_OFFSET, env.xlen/2 + GRID_OFFSET])
    plt.ylim([-env.ylen/2 - GRID_OFFSET, env.ylen/2 + GRID_OFFSET])


def plot_lines(lst, color_str=None):
    """
    For a list of lists of numpy arrays of 3D points, plot the x 
    and y components of the 3D points in the color `color_str`.
    """
    color_str = color_str if color_str is not None else 'k'
    for line in lst:    
        points = np.stack(line)
        x, y = points[:, 0], points[:, 1]
        plt.plot(x, y, color_str)


def plot_circular_objs(lst, z=0, color_str=None):
    """
    For a list of circular objects `lst` like Planets, Asteroids
    and Spaceships (which MUST have a position and radius), plot
    the circular objects in the color `color_str`.
    """
    for i, circle in enumerate(lst):
        centre, radius = find_circle(circle.position, circle.radius, z)
        if centre is not None: # If there is an intersection, draw planets in green.
            xs = np.linspace(0., 2 * np.pi, RESOLUTION)
            x = np.cos(xs) * radius + centre[0]
            y = np.sin(xs) * radius + centre[1]

            # Default to black if no color specified
            color_str = color_str if color_str is not None else 'k'
            plt.plot(x, y, color_str)


def plot_env(env, z=0, filename=None):
    plot_walls(env, z=z)
    plot_circular_objs(env.planets, z=z, color_str='g')
    plot_circular_objs(env.asteroids, z=z, color_str='r')
    plot_circular_objs(env.spaceships, z=z, color_str='b')
    plot_lines(env._asteroid_trajectories, color_str='r')
    plot_lines(env._spaceship_trajectories, color_str='b')
        
    if filename:
        plt.savefig(filename)


def quiver_2d(env, navigator, spaceship_idx, filename=None):
    """
    Given the current location of a series of planets, asteroids and
    spaceships (and the velocities of the asteroids and spaceships),
    produce a 2D output illustrating the vector field associated with
    one or more spaceships.
    """

    # Potential Field Plotting
    x = np.linspace(-env.xlen/2, env.xlen/2, RESOLUTION)
    y = np.linspace(-env.ylen/2, env.ylen/2, RESOLUTION)
    X, Y = np.meshgrid(x, y)
    U, V = np.zeros_like(X), np.zeros_like(Y)

    for i in range(len(U)):
        for j in range(len(V)):
            # velocity = navigator.vector(env, spaceship_idx)
            velocity = np.array([1., 1.])
            U[i, j] = velocity[0]
            V[i, j] = velocity[1]

    plt.quiver(X, Y, U, V, units='width')
    plt.show()
