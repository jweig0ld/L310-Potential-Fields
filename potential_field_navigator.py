import numpy as np

from components import *


class PotentialFieldNavigator():
    def repulsive(self, env, spaceship_idx):
        pass
    
    def attractive(self, env, spaceship_idx):
        pass
    
    def vector(self, env, spaceship_idx):
        """
        Ensure that the vectors are normalised or clipped when
        returned to prevent crazy spaceship trajectories.
        """
        # return attractive(env, spaceship_idx) + repulsive(env, spaceship_idx)
        return np.array([0.5, 1, 0])