import numpy as np

from components import *
from potential_field_navigator import *


if __name__ == "__main__":
    s_1 = Spaceship(np.array([-0.5, -0.5, -0.5]), 0.05, np.array([0., 0., 0.]))
    spaceships = [s_1]

    # a_1 = Asteroid(np.array([]))
    # asteroids = [a_1]

    # p_1 = Planet()
    # planets = [p_1]

    dt, max_t = 10, 1000
    
    navigator = PotentialFieldNavigator()

    env = Environment(2, 2, spaceships, asteroids, planets, dt, max_t, navigator)