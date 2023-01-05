import numpy as np


ASTEROID_COLLISION = 0
PLANET_COLLISION = 1
SPACESHIP_COLLISION = 2


class Planet:
    def __init__(self, position, radius, mass):
        self.position = position
        self.radius = radius
        self.mass = mass


class Spaceship:
    def __init__(self, position, radius, goal):
        self.position = position
        self.radius = radius
        self.goal = goal


class Asteroid:
    def __init__(self, position, radius, velocity, mass):
        self.position = position
        self.radius = radius
        self.velocity = velocity
        self.mass = mass


class Environment:
    def __init__(self, xlen, ylen, zlen, spaceships, asteroids, planets, dt, max_t, navigator):
        self.xlen = xlen
        self.ylen = ylen
        self.zlen = zlen
        self.spaceships = spaceships
        self.asteroids = asteroids
        self.planets = planets
        self.dt = dt
        self.max_t = max_t
        self.navigator = navigator
        self._spaceship_trajectories = []
        self._asteroid_trajectories = []
        self._t = 0

    def _add_spaceship_pos(spaceship_idx, pos):
        self._spaceship_trajectories[spaceship_idx].append(pos)
    
    def _add_asteroid_pos(asteroid_idx, pos):
        self._asteroid_trajectories[asteroid_idx].append(pos)

    def _sanitise_position(pos):
        """
        Given a 3D position `pos`, ensures that the position lies witin the
        allowed scope of the environment.
        """
        return np.clip(pos, 
                       [-self.xlen / 2, -self.ylen / 2, -self.zlen / 2],
                       [self.xlen / 2, self.ylen / 2, self.zlen / 2])

    def _check_collision(spaceship_idx, t):
        """
        Returns None if no collision, otherwise returns tuple (spaceship_idx, type, 
        idx, pos) where `type` either indicates whether the spaceship has collided 
        with a Planet, Asteroid or Spaceship, idx represents the index of the 
        colliding object and pos is the position of the collision.
        """

        # Asteroid Collision Check
        for i in range(len(self._asteroid_trajectories)):
            asteroid_pos = self._asteroid_trajectories[i][t/self.dt]
            spaceship_pos = self._spaceship_trajectories[spaceship_idx][t/self.dt]
            dist = np.sqrt(np.sum(np.square(spaceship_pos - asteroid_pos)))

            if dist < self.asteroids[i].radius:
                # We only care about the first collision
                return (spaceship_idx, ASTEROID_COLLISION, i, spaceship_pos)
            
        # Planetary Collision Check
        for i, planet in self.planets:
            spaceship_pos = self._spaceship_trajectories[spaceship_idx][t/self.dt]
            dist = np.sqrt(np.sum(np.square(spaceship_pos - planet.position)))

            if dist < planet.radius:
                return (spaceship_idx, PLANET_COLLISION, i, spaceship_pos)

        # Spaceship Collision Check
        for i, other_spaceship in self.spaceships:
            cur_spaceship_pos = self._spaceship_trajectories[spaceship_idx][t/self.dt]
            other_spaceship_pos = self._spaceship_trajectories[i][t/self.dt]
            dist = np.sqrt(np.sum(np.square(spaceship_pos - other_spaceship_pos)))

            if dist < other_spaceship.radius:
                return (spaceship_idx, SPACESHIP_COLLISION, i, spaceship_pos)
        
        return None

    def _evaluate_collisions():
        """
        Returns a list of collisions (empty if none take place). Each element of
        the list is a dictionary describing the two colliding objects and the
        location at which they collided.
        """
        collisions = []
        for spaceship_idx, spaceship in self.spaceships:
            for t in range(0, self.max_t, self.dt):
                res = self._check_collision(spaceship_idx, t)
                if res:
                    collisions.append(res)
        
        return collisions
    
    def _step_spaceships():
        """
        Given current state of the environment, increment all of the positions of the
        spaceships in the environment.
        """
        for i, spaceship in enumerate(self.spaceships):
            spaceship.position = self._sanitise_position(self.navigator.vector(self, i))
            self._add_spaceship_pos(i, spaceship.position)

    def _step_asteroids():
        """
        Given current state of the environment, increment all of the positions of the
        spaceships in the environment.
        """
        for i, asteroid in enumerate(self.asteroids):
            asteroid.position = self._sanitise_position(asteroid.position + asteroid.velocity * self.dt)
            self._add_asteroid_pos(i, asteroid.position)

    def run():

        while self._t < self.max_t:
            self._step_asteroids()
            self._step_spaceships()
            self._t += self.dt

        collisions = self._evaluate_collisions()
        return self._spaceship_trajectories, self._asteroid_trajectories, collisions