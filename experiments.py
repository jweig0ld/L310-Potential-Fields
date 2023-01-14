import numpy as np

from components import *
from potential_field_navigator import *
from math_utils import normalise

"""
TODO:

1. (DONE). Write a method which checks if a position is inside something
   in the environment – asteroid or planet or equivalent.

2. (DONE). Write a method which samples a position in the environment.

3. (DONE). Write a method which creates an environment according to some
   specification.

4. Write a base experiment which calculates the average success rate of
   each potential field method. I.e. the average number of success rates
   of each spaceship moving toward its goal.
"""


ASTEROID_SCALE = 0.1
PLANET_SCALE = 0.25
SPACESHIP_SCALE = 0.05


def sample_environment(xlen, ylen, zlen, n_planets, n_asteroids, n_spaceships, spaceship_radius, dt, navigator):
    env = Environment(xlen, ylen, zlen, [], [], [], dt, navigator)

    for _ in range(n_planets):
        pos = env.sample_valid_position()
        r = env.sample_valid_radius(pos, PLANET_SCALE)
        env.add_planet(Planet(pos, r))
        print(f'New Planet: Position {pos} with Radius {r}.')

    for _ in range(n_asteroids):
        pos = env.sample_valid_position()
        r = env.sample_valid_radius(pos, ASTEROID_SCALE)
        vel = normalise(np.random.uniform(size=3), scale=dt)
        env.add_asteroid(Asteroid(pos, r, vel))
        print(f'New Asteroid: Position {pos} with Radius {r}.')
    
    for _ in range(n_spaceships):
        pos = env.sample_valid_position()
        goal = env.sample_valid_position()
        r = env.sample_valid_radius(pos, SPACESHIP_SCALE)
        env.add_spaceship(Spaceship(pos, r, goal))
        print(f'New Spaceship: Position {pos} with Radius {r}.')

    return env
    
        
def avg_success_experiment(env):
    pass
