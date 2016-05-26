from random import random
from gen_ucurve import gen_points
from deterministic_bisection import bisection_min

max_input_size = 1000
test_size = 100000
corrects = 0
for i in range (test_size):
    n = 1 + int (random () * max_input_size)
    points = gen_points (n, 1.0 / n, int (n * random ()))
    
    if min (points) is bisection_min (points):
        corrects = corrects + 1

print ("Correctness: ", corrects / (test_size * 1.0))
