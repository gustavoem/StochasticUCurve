from random import random
from gen_ucurve import gen_points
from gen_ucurve import input_noise
from bisection import bisection_min
from bisection import mid_neighbour_bisection 
from bisection import upb
from bisection import mupb
from time import time

max_input_size = 1000
test_size = 100.0


##  Time and evaluations
##
##
time_file = open ('time_data.txt', 'w')
evaluations_file = open ('evaluations_data.txt', 'w')
for j in range (0):
    d_evaluations = 0
    m_evaluations = 0
    s_evaluations = 0
    s2_evaluations = 0
    d_time = 0
    m_time = 0
    s_time = 0
    s2_time = 0

    for i in range (int (test_size)):
        n = max_input_size
        points = gen_points (n, random ())
        input_noise (points, 0)
        
        s = time ()
        [result, evaluations] = bisection_min (points)
        d_evaluations += evaluations / (n * 1.0)
        e = time ()
        d_time += e - s

        s = time ()
        [result, evaluations] = mid_neighbour_bisection (points)
        m_evaluations += evaluations / (n * 1.0)
        e = time ()
        m_time += e - s

        s = time ()
        [result, evaluations] = upb (points, .85)
        s_evaluations += evaluations / (n * 1.0)
        e = time ()
        s_time +=  e - s

        s = time ()
        [result, evaluations] = mupb (points, .85)
        s2_evaluations += evaluations / (n * 1.0)
        e = time ()
        s2_time +=  e - s

    print ("Average percentage of evaluated nodes for traditional bisection: ", d_evaluations / test_size)
    print ("Average percentage of evaluated nodes for mid-neighbour bisection: ", m_evaluations / test_size)
    print ("Average percentage of evaluated nodes for UPB: ", s_evaluations / test_size)
    print ("Average percentage of evaluated nodes for MUPB: ", s2_evaluations / test_size)
    print ("Time used for traditional bisection (seconds): ", d_time)
    print ("Time used for mid-neighbour bisection (seconds): ", m_time)
    print ("Time used for UPB (seconds): ", s_time)
    print ("Time used for MUPB (seconds): ", s2_time)

    evaluations_file.write (str (max_input_size) + " " + str (d_evaluations / test_size) + " " + str (m_evaluations / test_size) + " " + str (s_evaluations / test_size) + " " + str (s2_evaluations / test_size) + "\n")
    time_file.write (str (max_input_size) + " " + str (d_time) + " " + str (m_time) +  " " + str (s_time) + " " + str (s2_time) + " " +"\n")
    
    max_input_size += 500

evaluations_file.close ()
time_file.close ()



# Correctness
#
#
max_input_size = 100
test_size = 1000.0
correctness_file = open ('correctness_data.txt', 'w')
sigma = 0 # input noise parameter
for j in range (10):
    d_corrects = 0
    m_corrects = 0
    s_corrects = 0
    s2_corrects = 0
    s_error = 0.0
    s2_error = 0.0
    for i in range (int (test_size)):
        n = max_input_size
        points = gen_points (n, .25)
        input_noise (points, sigma)
        
        [result, evaluations] = bisection_min (points)
        if abs (min (points) - result) / abs (min (points)) < .05:
            d_corrects = d_corrects + 1

        [result, evaluations] = mid_neighbour_bisection (points)
        if abs (min (points) - result) / abs (min (points)) < .05:
            m_corrects = m_corrects + 1

        [result, evaluations] = upb (points, .8)
        if abs (min (points) - result) / abs (min (points)) < .05:
            s_corrects = s_corrects + 1
        s_error = s_error + abs (min (points) - result) / abs (min (points))

        [result, evaluations] = mupb (points, .85)
        if abs (min (points) - result) / abs (min (points)) < .05:
            s2_corrects = s2_corrects + 1
        s2_error = s2_error + abs (min (points) - result) / abs (min (points))

    print ("Correctness for traditional bisection: ", d_corrects / test_size)
    print ("Correctness for mid-neighbour bisection: ", m_corrects / test_size)
    print ("Correctness for UPB: ", s_corrects / test_size)
    print ("Correctness for MPB: ", s2_corrects / test_size)
    print ("Average relative error of UPB:", s_error / test_size)
    print ("Average relative error of MPB:", s2_error / test_size)
    correctness_file.write (str (sigma) + " " + str (d_corrects / test_size) + " " + str (m_corrects / test_size) + " " + str (s_corrects / test_size) + " " + str (s2_corrects / test_size) + "\n")
    sigma += 1

correctness_file.close ()



# Test different values of pc
#
#
pc_time_file = open ('pc_time_data.txt', 'w')
pc_evaluations_file = open ('pc_evaluations_data.txt', 'w')
max_input_size = 32
for j in range (0):
    p7_evaluations = 0
    p8_evaluations = 0
    p9_evaluations = 0
    p7_time = 0
    p8_time = 0
    p9_time = 0

    for i in range (int (test_size)):
        n = max_input_size
        points = gen_points (n, random ())
        input_noise (points, 0)

        s = time ()
        [result, evaluations] = mupb (points, .7)
        p7_evaluations += evaluations / (n * 1.0)
        e = time ()
        p7_time = p7_time + e - s

        s = time ()
        [result, evaluations] = mupb (points, .8)
        p8_evaluations += evaluations / (n * 1.0)
        e = time ()
        p8_time = p8_time + e - s

        s = time ()
        [result, evaluations] = mupb (points, .9)
        p9_evaluations += evaluations / (n * 1.0)
        e = time ()
        p9_time = p9_time + e - s

    print ("Average percentage of evaluated nodes for pc = .7: ", p7_evaluations / test_size)
    print ("Average percentage of evaluated nodes for pc = .8: ", p8_evaluations / test_size)
    print ("Average percentage of evaluated nodes for pc = .9: ", p9_evaluations / test_size)
    print ("Time used for pc = .7 (seconds): ", p7_time)
    print ("Time used for pc = .8 (seconds): ", p8_time)
    print ("Time used for pc = .9 (seconds): ", p9_time)

    pc_evaluations_file.write (str (max_input_size) + " " + str (p7_evaluations / test_size) + " " + str (p8_evaluations / test_size) + " " + str (p9_evaluations / test_size) + "\n")
    pc_time_file.write (str (max_input_size) + " " + str (p7_time) + " " + str (p8_time) +  " " + str (p9_time) + " " +"\n")
    max_input_size *= 2
pc_time_file.close ()
pc_evaluations_file.close ()
