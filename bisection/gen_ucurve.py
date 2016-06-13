import random
from datetime import datetime

def gen_points (n, max_distance, center):
    """Generates n points from 0 to 1, that differ from each at most max_distance, and 
    describe a u-shape in the return vector. center represents the index of the minimum 
    of the curve"""
    points = [0] * n
    minimum = random.random () / 2
    points[center] = minimum

    for i in range (center - 1, -1, -1):
        points[i] = points[i + 1] + \
            min (max_distance * random.random (), (1 - points[i + 1]) * random.random ())

    for i in range (center + 1, n):
        points[i] = points[i - 1] + \
            min (max_distance * random.random (), (1 - points[i - 1]) * random.random ())
    
    # creates some plain sequence of points 
    j = int (n * random.random ())
    plain_size = int ((n - j) * (random.random () / 2))
    for k in range (plain_size):
        points[j + k] = points[j]

    return points

def input_noise (v, sigma):
    """ Inserts random noise in the points of v with values in
    [-(amplitude / len (v)) * (alpha), (amplitude / len (v)) * (alpha)]  where alpha
    is a random variable with gaussian distribution with mean zero and standard deviation
    sigma """
    curve_amplitude = max (v) - min (v)
    relative_amplitude = curve_amplitude / len (v)
    v[0:len (v)] = map (lambda x: x + ((random.gauss (0, sigma)) * relative_amplitude), v[0:len (v)])
   
random.seed (datetime.now ())
f = open ('curve_data.txt', 'w')
v = gen_points (100, 1.0 / 100, 50)
input_noise (v, 2)
for x in v:
   f.write (str (x) + "\n")
f.close ()

