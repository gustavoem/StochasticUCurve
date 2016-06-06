from random import random
from gen_ucurve import gen_points
from bisection import bisection_min
from bisection import mid_neighbour_bisection 
from time import time

max_input_size = 8000
test_size = 10000.0

d_corrects = 0
s_corrects = 0
d_time = 0
s_time = 0
s_error = 0.0

for i in range (int (test_size)):
    n = 1 + int (random () * max_input_size)
    points = gen_points (n, 1.0 / n, int (n * random ()))
    
    s = time ()
    result = bisection_min (points)
    e = time ()
    d_time = d_time + e - s
    if min (points) is result:
        d_corrects = d_corrects + 1

    s = time ()
    result = mid_neighbour_bisection (points)
    e = time ()
    s_time = s_time + e - s
    if min (points) is result:
        s_corrects = s_corrects + 1
    else:
        s_error = s_error + abs (min (points) - result) / min (points)



print ("Correctness for mid-neighbour bisection: ", s_corrects / test_size)
print ("Correctness for traditional bisection: ", d_corrects / test_size)
print ("Time used for mid-neighbour bisection (seconds): ", s_time)
print ("Time used for traditional bisection (seconds): ", d_time)
print ("Average relative error of mid-neighour bisection: ", s_error / max (test_size - s_corrects, 1))
