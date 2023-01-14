from __future__ import annotations

import numpy as np

from math_utils import euclidean_distance, spherical_collision


ASTEROID_COLLISION = 0
PLANET_COLLISION = 1
SPACESHIP_COLLISION = 2


class Planet:
    def __init__(self, position, radius):
        self.position = position
        self.radius = radius


class Spaceship:
    def __init__(self, position, radius, goal):
        self.position = position
        self.radius = radius
        self.goal = goal

    def set_position(self, new_position):
        self.position = new_position

    def at_goal(self):
        return euclidean_distance(self.position, self.goal) < 0.1


class Asteroid:
    def __init__(self, position, radius, velocity):
        self.position = position
        self.radius = radius
        self.velocity = velocity

    def set_position(self, new_position):
        self.position = new_position


class Environment:
    def __init__(self, xlen, ylen, zlen, spaceships, asteroids, planets, dt, navigator):
        self.xlen = xlen
        self.ylen = ylen
        self.zlen = zlen
        self.spaceships = spaceships
        self.asteroids = asteroids
        self.planets = planets
        self.dt = dt
        self.navigator = navigator
        self._spaceship_trajectories = [[s.position] for s in spaceships]
        self._asteroid_trajectories = [[a.position] for a in asteroids]
        self._t = 0

    def _add_spaceship_pos(self, spaceship_idx, pos):
        self._spaceship_trajectories[spaceship_idx].append(pos)
    
    def _add_asteroid_pos(self, asteroid_idx, pos):
        self._asteroid_trajectories[asteroid_idx].append(pos)

    def _inside_obj(self, pos):
        """
        Returns True if `pos` is inside a Planet, Asteroid or Spaceship.
        """
        for planet in self.planets:
            if euclidean_distance(pos, planet.position) < planet.radius:
                return True
        
        for asteroid in self.asteroids:
            if euclidean_distance(pos, asteroid.position) < asteroid.radius:
                return True
            
        for spaceship in self.spaceships:
            if euclidean_distance(pos, spaceship.position) < spaceship.radius:
                return True

        return False

    def _inside_planet(self, pos):
        """
        Returns True if `pos` is inside a planet. False otherwise.
        """
        for planet in self.planets:
            dist = euclidean_distance(pos, planet.position)
            if dist < planet.radius:
                return True
        
        return False

    def _can_move(self, pos):
        """
        Returns False if an object is either on the edge of one of the
        dimensions of the environment or is inside a planet. True
        otherwise.
        """
        if (pos[0] == abs(self.xlen/2) or \
            pos[1] == abs(self.ylen/2) or \
            pos[2] == abs(self.zlen/2)):
            return False

        if self._inside_planet(pos):
            return False

        return True

    def _sanitise_position(self, pos):
        """
        Given a 3D position `pos`, ensures that the position lies witin the
        allowed scope of the environment.
        """
        return np.clip(pos, 
                       [-self.xlen / 2, -self.ylen / 2, -self.zlen / 2],
                       [self.xlen / 2, self.ylen / 2, self.zlen / 2])

    def _check_collision(self, spaceship_idx, t):
        """
        Returns None if no collision, otherwise returns tuple (spaceship_idx, type, 
        idx, pos) where `type` either indicates whether the spaceship has collided 
        with a Planet, Asteroid or Spaceship, idx represents the index of the 
        colliding object and pos is the position of the collision.
        """
        index = int(t/self.dt)
        spaceship_pos = self._spaceship_trajectories[spaceship_idx][index]
        spaceship_radius = self.spaceships[spaceship_idx].radius

        # Asteroid Collision Check
        for i, asteroid in enumerate(self.asteroids):
            asteroid_pos = self._asteroid_trajectories[i][index]
            if spherical_collision(spaceship_pos, asteroid_pos, r1=spaceship_radius, r2=asteroid.radius):
                return (spaceship_idx, ASTEROID_COLLISION, i, spaceship_pos)
                
            
        # Planetary Collision Check
        for i, planet in enumerate(self.planets):
            if spherical_collision(planet, spaceship_pos, r2=spaceship_radius):
                return (spaceship_idx, PLANET_COLLISION, i, spaceship_pos)
                

        # Spaceship Collision Check
        for i, other_spaceship in enumerate(self.spaceships):
            if i == spaceship_idx:
                continue

            other_spaceship_pos = self._spaceship_trajectories[i][index]
            if spherical_collision(spaceship_pos, other_spaceship_pos, r1=spaceship_radius, r2=other_spaceship.radius):
                return (spaceship_idx, SPACESHIP_COLLISION, i, spaceship_pos)
        
        return None

    def _evaluate_collisions(self):
        """
        Returns a list of collisions (empty if none take place). Each element of
        the list is a dictionary describing the two colliding objects and the
        location at which they collided.
        """
        collisions = []
        for spaceship_idx, spaceship in enumerate(self.spaceships):
            for t in np.arange(0., 1., self.dt):
                res = self._check_collision(spaceship_idx, t)
                if res is not None:
                    collisions.append(res)
                    break
        
        return collisions
    
    def _step_spaceships(self):
        """
        Given current state of the environment, increment all of the positions of the
        spaceships in the environment.
        """
        for i, spaceship in enumerate(self.spaceships):

            if not self._can_move(spaceship.position):
                self._add_spaceship_pos(i, spaceship.position)
                continue

            new_position = spaceship.position + self.navigator.vector(self, i)
            spaceship.set_position(self._sanitise_position(new_position))
            self._add_spaceship_pos(i, spaceship.position)

    def _step_asteroids(self):
        """
        Given current state of the environment, increment all of the positions of the
        asteroids in the environment.
        """
        for i, asteroid in enumerate(self.asteroids):

            if not self._can_move(asteroid.position):
                self._add_asteroid_pos(i, asteroid.position)
                continue

            new_position = asteroid.position + asteroid.velocity * self.dt
            asteroid.set_position(self._sanitise_position(new_position))
            self._add_asteroid_pos(i, asteroid.position)

    def sample_valid_position(self):
        """
        Return a random position inside the environment which is 
        not inside an existing object.
        """
        low = [-self.xlen/2, -self.ylen/2, -self.zlen/2]
        high = [self.xlen/2, self.ylen/2, self.zlen/2]

        sample = np.random.uniform(low=low, high=high, size=3)
        while self._inside_obj(sample):
            sample = np.random.uniform(low=low, high=high, size=3)
        
        return sample

    def sample_valid_radius(self, pos, scale):
        """
        For a spherical object centered at pos, sample a radius
        which is less than the distance to the nearest other
        object in the environment. The `scale` parameter [0,1]
        is a number which controls how much space you want there
        to be between the objects in the environment, and thus
        indirectly how large the objects are.
        """
        planet_dists = [euclidean_distance(planet.position, pos) for planet in self.planets]
        asteroid_dists = [euclidean_distance(asteroid.position, pos) for asteroid in self.asteroids]
        spaceship_dists = [euclidean_distance(spaceship.position, pos) for spaceship in self.spaceships]
        dists = [*planet_dists, *asteroid_dists, *spaceship_dists]
        
        if not planet_dists and not asteroid_dists and not spaceship_dists:
            return np.random.uniform(high=self.xlen/4 * scale)
            
        min_dist = np.amin(np.array(dists))

        return np.random.uniform(high=min_dist * scale)

    def add_spaceship(self, spaceship):
        self.spaceships.append(spaceship)
        self._spaceship_trajectories.append([spaceship.position])

    def add_asteroid(self, asteroid):
        self.asteroids.append(asteroid)
        self._asteroid_trajectories.append([asteroid.position])
    
    def add_planet(self, planet):
        self.planets.append(planet)

    def state_at_time(self, t) -> Environment:
        """
        Given a time `t`, returns an Environment instance representing the state
        of the calling environment at time `t`.
        """
        shorten = lambda lst, i : lst[:int(i/self.dt)]
        a_trajectories = shorten(self._asteroid_trajectories, t)
        s_trajectories = shorten(self._spaceship_trajectories, t)
        new_env = Environment(self.xlen,
                           self.ylen,
                           self.zlen,
                           self.spaceships,
                           self.asteroids,
                           self.planets,
                           self.dt,
                           self.navigator)
        new_env._asteroid_trajectories = a_trajectories
        new_env._spaceship_trajectories = s_trajectories
        return new_env

    def run(self):

        while self._t < 1:
            self._step_asteroids()
            self._step_spaceships()
            self._t += self.dt

        collisions = self._evaluate_collisions()
        return self._spaceship_trajectories, self._asteroid_trajectories, collisions