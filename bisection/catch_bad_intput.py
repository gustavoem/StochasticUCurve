from random import random
from gen_ucurve import gen_points
from gen_ucurve import input_noise
from bisection import upb
from math import log
from time import time


input_size = 5100
test_size = 100

points = gen_points (input_size, random ())
input_noise (points, 0)
s = time ()
[result, evaluations] = upb (points, .85)
e = time ()

last_time = e - s
last_input = points


for i in range (test_size):
    points = gen_points (input_size, random ())
    input_noise (points, 0)
    s = time ()
    [result, evaluations] = upb (points, .85)
    e = time ()
    
    current_time = e - s
    if ((current_time - last_time) / last_time > 5000):
        print ("Current time, last time: ", current_time, ", ", last_time)
        input_file1 = open ('bad_input1.txt', 'w')
        input_file2 = open ('bad_input2.txt', 'w')
        for i in range (len (last_input)):
            input_file1.write (str (last_input[i]) + "\n")
        for i in range (len (points)):
            input_file2.write (str (points[i]) + "\n")
        break

    last_input = points
    last_time = current_time

input_file1.close ()
input_file2.close ()