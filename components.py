import numpy as np


G = 6.67 * 10^-11 # Newtonian Constant of Gravity


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
    def __init__(self, xlen, ylen, spaceships, asteroids, planets, dt):
        self.xlen = xlen
        self.ylen = ylen
        self.spaceships = spaceships
        self.asteroids = asteroids
        self.planets = planets
        self.dt = dt

    def step():
        _step_asteroid()
        _step_spaceship()
    
    def _step_asteroid():
        for asteroid in self.asteroids:
            f_res = np.zeros(3)

            # Compute new asteroid velocity
            for planet in self.planets:
                r = asteroid.position - planet.position
                distance = np.sqrt(np.sum(np.square(r)))
                r_hat = r / np.linalg.norm(r)
                f_res += ((G * planet.mass * asteroid.mass) / distance) * r_hat
                
            # Update position and velocity based on new velocity
            dp = asteroid.velocity * dt + (f_res / (2 * asteroid.mass)) * self.dt ** 2
            asteroid.position += dp
            asteroid.velocity = asteroid.velocity + (f_res / asteroid.mass) * self.dt