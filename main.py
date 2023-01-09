import numpy as np

from components import *
from potential_field_navigator import *
from visualisation import plot_env


if __name__ == "__main__":
    s1 = Spaceship(np.array([-0.5, -0.5, 0.]), 0.25, np.array([0., 0., 0.]))
    s2 = Spaceship(np.array([2., 0., 0.]), 0.15, np.array([0., 0., 0.]))

    p1 = Planet(np.array([-1.5, 0.5, 0.5]), 1., 0)
    p2 = Planet(np.array([2., 2., 0.]), 1., 0)

    vel = np.array([1., 1., 0.])
    a1 = Asteroid(np.array([-2., -2., 0]), 0.2, vel, 0)
    a2 = Asteroid(np.array([1., -2.5, 0]), 0.1, vel, 0)

    xlen, ylen, zlen = 8, 8, 3
    spaceships = [s1, s2]
    asteroids = [a1, a2]
    planets = [p1, p2]
    dt = 0.01
    navigator = PotentialFieldNavigator()

    env = Environment(xlen, ylen, zlen, spaceships, asteroids, planets, dt, navigator)
    env.run()
    
    plot_env(env, z=0, filename='test.png')
    
