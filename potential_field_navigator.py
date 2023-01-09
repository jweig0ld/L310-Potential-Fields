import numpy as np

from components import *


class PotentialFieldNavigator():
    def repulsive(self, env, spaceship_idx):
        pass
    
    def attractive(self, env, spaceship_idx):
        pass
    
    def vector(self, env, spaceship_idx):
        # return attractive(env, spaceship_idx) + repulsive(env, spaceship_idx)
        return np.array([0, 0, 1])