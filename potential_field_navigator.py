import numpy as np

from components import *
from math_utils import normalise, max_normalise

class PotentialFieldNavigator():
    def repulsive(self, env, spaceship_idx):
        return np.zeros((3,))
    
    def attractive(self, env, spaceship_idx):
        cur_pos = env._spaceship_trajectories[spaceship_idx][-1]
        direction = env.spaceships[spaceship_idx].goal - cur_pos
        return 0.1 * direction
    
    def vector(self, env, spaceship_idx):
        """
        Ensure that the vectors are normalised or clipped when
        returned to prevent crazy spaceship trajectories.
        """
        return self.attractive(env, spaceship_idx) + self.repulsive(env, spaceship_idx)
        # return np.array([0., 0., 0])


class BasicPotentialFieldNavigator():
    def repulsive(self, env, spaceship_idx):
        spaceship = env.spaceships[spaceship_idx]
        result = np.zeros((3,))
        safety_dist = 0.2

        for planet in env.planets:
            dist = euclidean_distance(spaceship.position, planet.position)
            if dist < planet.radius + safety_dist:
                result += 1/(spaceship.position - planet.position)

        for asteroid in env.asteroids:
            dist = euclidean_distance(spaceship.position, asteroid.position)
            if dist < asteroid.radius + safety_dist:
                result += 1/(spaceship.position - asteroid.position)

        for other_spaceship in env.spaceships:
            if np.array_equal(other_spaceship.position, spaceship.position):
                continue 

            dist = euclidean_distance(spaceship.position, other_spaceship.position)
            if dist < spaceship.radius + safety_dist:
                result += 1/(spaceship.position - other_spaceship.position)
        
        return result
    
    def attractive(self, env, spaceship_idx):
        cur_pos = env._spaceship_trajectories[spaceship_idx][-1]
        direction = env.spaceships[spaceship_idx].goal - cur_pos
        return 0.05 * direction
    
    def vector(self, env, spaceship_idx):
        """
        Ensure that the vectors are normalised or clipped when
        returned to prevent crazy spaceship trajectories.
        """
        return self.attractive(env, spaceship_idx) + self.repulsive(env, spaceship_idx)


class ProposedPotentialFieldNavigator():
    def repulsive(self, env, spaceship_idx):
        result = np.zeros((3,))
        
        spaceship = env.spaceships[spaceship_idx]
        for planet in env.planets:
            dist = euclidean_distance(spaceship.position, planet.position) - planet.radius - spaceship.radius
            weight = np.exp(-3 * dist)
            result += weight * (spaceship.position - planet.position)

        for asteroid in env.asteroids:
            dist = euclidean_distance(spaceship.position, asteroid.position) - asteroid.radius - spaceship.radius
            weight = np.exp(-3 * dist)
            result += weight * (spaceship.position - asteroid.position)

        for other_spaceship in env.spaceships:
            if np.array_equal(other_spaceship.position, spaceship.position):
                continue 

            dist = euclidean_distance(spaceship.position, other_spaceship.position) - other_spaceship.radius - spaceship.radius
            weight = np.exp(-3 * dist)
            result += weight * (spaceship.position - other_spaceship.position)
        
        return max_normalise(result)

    def attractive(self, env, spaceship_idx):
        cur_pos = env._spaceship_trajectories[spaceship_idx][-1]
        direction = env.spaceships[spaceship_idx].goal - cur_pos
        return normalise(direction)

    def vector(self, env, spaceship_idx):
        return normalise(self.attractive(env, spaceship_idx) + self.repulsive(env, spaceship_idx), scale=0.1)