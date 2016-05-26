from random import random
from gen_ucurve import gen_points
from deterministic_bisection import bisection_min

total_size = 1000
corrects = 0
for i in range (1000):
    n = 1 + int (random () * 1000)
    points = gen_points (n, 1.0 / n, int (n * random ()))
    if min (points) is bisection_min (points):
        corrects = corrects + 1

print ("Correctness: ", corrects / (total_size * 1.0))
