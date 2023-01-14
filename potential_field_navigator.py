import numpy as np

from components import *
from math_utils import normalise

class PotentialFieldNavigator():
    def repulsive(self, env, spaceship_idx):
        pass
    
    def attractive(self, env, spaceship_idx):
        cur_pos = env._spaceship_trajectories[spaceship_idx][-1]
        direction = env.spaceships[spaceship_idx].goal - cur_pos
        return self._normalise(direction)
    
    def vector(self, env, spaceship_idx):
        """
        Ensure that the vectors are normalised or clipped when
        returned to prevent crazy spaceship trajectories.
        """
        # return self.attractive(env, spaceship_idx) + self.repulsive(env, spaceship_idx)
        return np.array([0.1, 0.1, 0])