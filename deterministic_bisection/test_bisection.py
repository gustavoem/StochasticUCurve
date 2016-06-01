from random import random
from gen_ucurve import gen_points
from bisection import bisection_min
from bisection import dip_toe_ubisection

max_input_size = 100
test_size = 1000
d_corrects = 0
s_corrects = 0

for i in range (test_size):
    n = 1 + int (random () * max_input_size)
    points = gen_points (n, 1.0 / n, int (n * random ()))
    
#    if min (points) is bisection_min (points):
#        d_corrects = d_corrects + 1

    if min (points) is dip_toe_ubisection (points):
        s_corrects = s_corrects + 1

print ("Correctness for stochastic bisection: ", s_corrects / (test_size * 1.0))
