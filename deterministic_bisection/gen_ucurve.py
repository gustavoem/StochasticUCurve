import random

def gen_points (n, max_distance, center):
    """Generates n points from 0 to 1, that differ from each at most max_distance, and 
    describe a u-shape in the return vector. center represents the index of the minimum 
    of the curve"""
    points = [0] * n
    minimum = random.random () / 2
    points[center] = minimum

    for i in xrange (center - 1, 0, -1):
        points[i] = points[i + 1] + \
            min (max_distance * random.random (), (1 - points[i + 1]) * random.random ())

    for i in xrange (center + 1, n):
        points[i] = points[i - 1] + \
            min (max_distance * random.random (), (1 - points[i - 1]) * random.random ())

    return points
