import numpy as np

from components import *
from potential_field_navigator import *
from visualisation import plot_env


if __name__ == "__main__":
    # s_1 = Spaceship(np.array([-0.5, -0.5, -0.5]), 0.05, np.array([0., 0., 0.]))
    # spaceships = [s_1]

    # a_1 = Asteroid(np.array([]))
    # asteroids = [a_1]

    p1 = Planet(np.array([-1.5, 0.5, 0.5]), 1., 0)
    p2 = Planet(np.array([2., 2., 0.]), 1., 0)

    xlen, ylen, zlen = 8, 8, 3
    spaceships = []
    asteroids = []
    planets = [p1, p2]
    dt, max_t = 10, 1000
    navigator = None

    env = Environment(xlen, ylen, zlen, spaceships, asteroids, planets, dt, max_t, navigator)
    plot_env(env, z=0, filename='test.png')
    
