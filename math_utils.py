import numpy as np


def euclidean_distance(a, b):
    return np.sqrt(np.sum(np.square(a - b)))


def normalise(v, scale=1.):
    norm = np.linalg.norm(v)
    if norm == 0: 
        return v
    return scale * (v / norm)


def max_normalise(v):
    norm = np.linalg.norm(v)
    if norm < 1: 
        return v
    return (v / norm)


def find_circle(c, r, z=0):
    """
    Returns the centre and radius of the circle that results from the
    intersection of the plane z=k and the sphere with centre `c` and 
    radius `r`. If there is no intersection, return (None, None).
    """
    if not (z > c[2] - r and z < c[2] + r):
        return (None, None)

    centre = c.copy()
    centre[2] = z
    d = z - c[2] # Distance between centre of resultant circle and plane z=k.
    radius = np.sqrt(np.square(r) - np.square(d))
    return centre, radius


def spherical_collision(sphere1, sphere2, r1=None, r2=None):
    """
    Given two spherical objects (both which have a `position` attr),
    return True if there is overlap between the spheres at their
    current positions i.e. there is a collision and False otherwise.
    """
    pos1, pos2, radius1, radius2 = None, None, None, None
    radius_msg = "If you provide a pos array you must also provide a radius."
    
    if isinstance(sphere1, np.ndarray):
        pos1 = sphere1
        assert r1 is not None, radius_msg
        radius1 = r1
    else:
        pos1 = sphere1.position
        radius1 = sphere1.radius

    if isinstance(sphere2, np.ndarray):
        pos2 = sphere2
        assert r2 is not None, radius_msg
        radius2 = r2
    else:
        pos2 = sphere2.position
        radius2 = sphere2.radius
        
    dist = euclidean_distance(pos1, pos2)
    return (dist <= radius1 + radius2)