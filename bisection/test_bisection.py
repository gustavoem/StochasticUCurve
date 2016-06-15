from random import random
from gen_ucurve import gen_points
from gen_ucurve import input_noise
from bisection import bisection_min
from bisection import mid_neighbour_bisection 
from bisection import upb
from time import time

max_input_size = 1000
test_size = 500.0



time_file = open ('time_data.txt', 'w')
evaluations_file = open ('evaluations_data.txt', 'w')
for j in range (0):
    d_evaluations = 0
    m_evaluations = 0
    s_evaluations = 0
    d_time = 0
    m_time = 0
    s_time = 0

    for i in range (int (test_size)):
        #n = 1 + int (random () * max_input_size)
        n = max_input_size
        points = gen_points (n, random ())
        input_noise (points, 0)
        
        s = time ()
        [result, evaluations] = bisection_min (points)
        d_evaluations += evaluations / (n * 1.0)
        e = time ()
        d_time = d_time + e - s

        s = time ()
        [result, evaluations] = mid_neighbour_bisection (points)
        m_evaluations += evaluations / (n * 1.0)
        e = time ()
        m_time = m_time + e - s

        s = time ()
        [result, evaluations] = upb (points)
        s_evaluations += evaluations / (n * 1.0)
        e = time ()
        s_time = s_time + e - s

    print ("Average percentage of evaluated nodes for traditional bisection: ", d_evaluations / test_size)
    print ("Average percentage of evaluated nodes for mid-neighbour bisection: ", m_evaluations / test_size)
    print ("Average percentage of evaluated nodes for stochastic bisection: ", s_evaluations / test_size)
    print ("Time used for traditional bisection (seconds): ", d_time)
    print ("Time used for mid-neighbour bisection (seconds): ", m_time)
    print ("Time used for probabilistic bisection (seconds): ", s_time)

    evaluations_file.write (str (max_input_size) + " " + str (d_evaluations / test_size) + " " + str (m_evaluations / test_size) + " " + str (s_evaluations / test_size) + "\n")
    time_file.write (str (max_input_size) + " " + str (d_time) + " " + str (m_time) +  " " + str (s_time) + " " +"\n")
    
    max_input_size += 1000

evaluations_file.close ()
time_file.close ()

max_input_size = 100
test_size = 1000.0
correctness_file = open ('correctness_data.txt', 'w')
# input noise parameter
sigma = 0
for j in range (11):
    d_corrects = 0
    m_corrects = 0
    s_corrects = 0
    s_error = 0.0
    for i in range (int (test_size)):
        #n = 1 + int (random () * max_input_size)
        n = max_input_size
        points = gen_points (n, .5)
        input_noise (points, sigma)
        
        
        [result, evaluations] = bisection_min (points)
        if min (points) is result:
            d_corrects = d_corrects + 1

        [result, evaluations] = mid_neighbour_bisection (points)
        if min (points) is result:
            m_corrects = m_corrects + 1

        [result, evaluations] = upb (points)
        if abs (min (points) - result) / abs (min (points)) < .05:
            s_corrects = s_corrects + 1
        
        s_error = s_error + abs (min (points) - result) / abs (min (points))

    print ("Correctness for traditional bisection: ", d_corrects / test_size)
    print ("Correctness for mid-neighbour bisection: ", m_corrects / test_size)
    print ("Correctness for probabilistic bisection: ", s_corrects / test_size)
    print ("Average relative error of probabilistic bisection", s_error / test_size)
    correctness_file.write (str (sigma) + " " + str (d_corrects / test_size) + " " + str (m_corrects / test_size) + " " + str (s_corrects / test_size) + "\n")
    
    sigma += 1

correctness_file.close ()
