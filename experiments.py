import numpy as np

from components import *
from potential_field_navigator import *
from math_utils import normalise


ASTEROID_SCALE = 0.1
PLANET_SCALE = 0.25
SPACESHIP_SCALE = 0.05


def sample_environment(xlen, ylen, zlen, n_planets, n_asteroids, n_spaceships, spaceship_radius, dt, navigator):
    env = Environment(xlen, ylen, zlen, [], [], [], dt, navigator)

    for _ in range(n_planets):
        r = 2.
        pos = env.sample_valid_position(radius=r)
        env.add_planet(Planet(pos, r))
        # print(f'New Planet: Position {pos} with Radius {r}.')

    for _ in range(n_asteroids):
        r = 0.5
        pos = env.sample_valid_position(radius=r)
        vel = normalise(np.random.uniform(size=3), scale=dt)
        env.add_asteroid(Asteroid(pos, r, vel))
        # print(f'New Asteroid: Position {pos} with Radius {r}.')
    
    for _ in range(n_spaceships):
        pos = env.sample_valid_position(radius=spaceship_radius)
        goal = env.sample_valid_position()
        env.add_spaceship(Spaceship(pos, r, goal))
        # print(f'New Spaceship: Position {pos} with Radius {r}.')

    return env
    
        
def collision_rate_experiment(config):
    """
    Returns the rate of collisions between spaceships and other
    obstacles the for the total number of runs in the environment.
    """
    success, fail = 0, 0
    a_collisions, s_collisions, p_collisions = 0, 0, 0

    for run in range(config['n_runs']):
        env = sample_environment(config['xlen'], 
                                 config['ylen'],
                                 config['zlen'], 
                                 config['n_planets'], 
                                 config['n_asteroids'],
                                 config['n_spaceships'],
                                 config['spaceship_radius'],
                                 config['dt'],
                                 config['navigator'])
        _, _, collisions = env.run()

        if not collisions:
            # Did all of the spaceships reach their destinations?
            single_fail = False
            for spaceship in env.spaceships:
                if not spaceship.at_goal():
                    fail += 1
                    single_fail = True
                    break

            # All spaceships made it successfully
            if not single_fail:
                success += 1
        else:
            for (spaceship_idx, type, i, pos) in collisions:
                if type == ASTEROID_COLLISION:
                    a_collisions += 1
                elif type == PLANET_COLLISION:
                    p_collisions += 1
                elif type == SPACESHIP_COLLISION:
                    s_collisions += 1
            fail += 1
    
    return {
        'success': success/config['n_runs'],
        'fail': fail/config['n_runs'],
        'asteroid': a_collisions/config['n_runs'],
        'spaceship': s_collisions/config['n_runs'],
        'planet': p_collisions/config['n_runs'],
        'minima':(fail - a_collisions - s_collisions - p_collisions)/config['n_runs']
    }
