import numpy as np


class Planet:
    def __init__(self, position, radius, mass):
        self.position = position
        self.radius = radius
        self.mass = mass


class Spaceship:
    def __init__(self, position, radius, goal, navigator):
        self.position = position
        self.radius = radius
        self.goal = goal
        self.navigator = navigator


class Asteroid:
    def __init__(self, position, radius, velocity, mass):
        self.position = position
        self.radius = radius
        self.velocity = velocity
        self.mass = mass


class Environment:
    def __init__(self, xlen, ylen, spaceships, asteroids, planets, dt, max_t, navigator):
        self.xlen = xlen
        self.ylen = ylen
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

    def _evaluate_collisions():
        """
        Returns a list of collisions (empty if none take place). Each element of
        the list is a dictionary describing the two colliding objects and the
        location at which they collided.
        """
        pass
    
    def _step_spaceships():
        """
        Given current state of the environment, increment all of the positions of the
        spaceships in the environment.
        """
        for i, spaceship in enumerate(self.spaceships):
            spaceship.position = self.navigator.vector(self, i)
            self._add_spaceship_pos(i, spaceship.position)

    def _step_asteroids():
        """
        Given current state of the environment, increment all of the positions of the
        spaceships in the environment.
        """
        for i, asteroid in enumerate(self.asteroids):
            asteroid.position = asteroid.position + asteroid.velocity * self.dt
            self._add_asteroid_pos(i, asteroid.position)

    def run():

        while self._t < self.max_t:
            self._step_asteroids()
            self._step_spaceships()
            self._t += self.dt

        collisions = self._evaluate_collisions()
        return self._spaceship_trajectories, self._asteroid_trajectories, collisions