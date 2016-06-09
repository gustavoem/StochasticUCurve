from random import random

def gen_points (n, max_distance, center):
    """Generates n points from 0 to 1, that differ from each at most max_distance, and 
    describe a u-shape in the return vector. center represents the index of the minimum 
    of the curve"""
    points = [0] * n
    minimum = random () / 2
    points[center] = minimum

    for i in range (center - 1, -1, -1):
        points[i] = points[i + 1] + \
            min (max_distance * random (), (1 - points[i + 1]) * random ())

    for i in range (center + 1, n):
        points[i] = points[i - 1] + \
            min (max_distance * random (), (1 - points[i - 1]) * random ())
    
    # creates some plain sequence of points 
    j = int (n * random ())
    plain_size = int ((n - j) * (random () / 2))
    for k in range (plain_size):
        points[j + k] = points[j]

    return points

def input_noise (v):
    """ Inserts random noise in the points of v with values in
    [-(amplitude / len (v)) * (error_percentage), (amplitude / len (v)) * (error_percentage)] """
    points_amplitude = max (v) - min (v)
    relative_amplitude = points_amplitude / len (v)
    error_percentage = 1
    v[0:len (v)] = map (lambda x: x + ((random () - .5) * relative_amplitude * error_percentage * 2), v[0:len (v)])
    
