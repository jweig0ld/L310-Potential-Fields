import numpy as np

from components import *
from potential_field_navigator import *
from math_utils import normalise


ASTEROID_SCALE = 0.1
PLANET_SCALE = 0.25
SPACESHIP_SCALE = 0.05


def sample_environment(xlen, ylen, zlen, n_planets, n_asteroids, n_spaceships, spaceship_radius, dt, navigator, asteroid_radius=None, planet_radius=None):
    env = Environment(xlen, ylen, zlen, [], [], [], dt, navigator)

    for _ in range(n_planets):
        r = planet_radius if planet_radius is not None else 2.
        pos = env.sample_valid_position(radius=r)
        env.add_planet(Planet(pos, r))
        # print(f'New Planet: Position {pos} with Radius {r}.')

    for _ in range(n_asteroids):
        r = asteroid_radius if asteroid_radius is not None else 0.75
        pos = env.sample_valid_position(radius=r)
        vel = normalise(np.random.uniform(size=3))
        env.add_asteroid(Asteroid(pos, r, vel))
        # print(f'New Asteroid: Position {pos} with Radius {r}.')
    
    for _ in range(n_spaceships):
        pos = env.sample_valid_position(radius=spaceship_radius)
        goal = env.sample_valid_position(radius=spaceship_radius)
        env.add_spaceship(Spaceship(pos, spaceship_radius, goal))
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
                                 config['navigator'],
                                 asteroid_radius=config['asteroid_radius'],
                                 planet_radius=config['planet_radius'])
        _, _, collisions = env.run()
        
        # We can fail because there was a collision
        if collisions:
            for collision in collisions:
                spaceship_idx, type, i, pos = collision
                if type == ASTEROID_COLLISION:
                    a_collisions += 1
                elif type == PLANET_COLLISION:
                    p_collisions += 1
                elif type == SPACESHIP_COLLISION:
                    s_collisions += 1
            fail += 1
        # ... or not all of the spaceships reached their destination
        else:
            single_fail = False
            for spaceship in env.spaceships:
                if not spaceship.at_goal():
                    fail += 1
                    single_fail = True
                    break

            # All spaceships made it successfully
            if not single_fail:
                success += 1

                # # Calculate how long it took for the experiment
                # # to become successful
                # for spaceship in env.spacehips:
    
    return {
        'success': success/config['n_runs'],
        'fail': fail/config['n_runs'],
        'asteroid': a_collisions/config['n_runs'],
        'spaceship': s_collisions/config['n_runs'],
        'planet': p_collisions/config['n_runs'],
        'minima':(fail - a_collisions - s_collisions - p_collisions)/config['n_runs']
    }
