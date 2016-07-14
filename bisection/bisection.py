from pmf import PMF
from math import log
from math import floor
from math import exp
from time import time

def bisection_min (v, limit = None):
    #print (limit)
    return bisection_min_step (v, limit)

def bisection_min_step (v, limit = None):
    """ This function receives a vector, that describes a u-shaped curve, as argument
    and return the minimum element of this vector """
    i = len (v) // 2

    if (valley (v, i) or (limit is not None and limit <= 0)):
        return [v[i], 3]
    else:
        direction = select_side (v, i)
        new_limit = None
        if (direction is 1):
            if (limit is not None):
                new_limit = limit - 1
            [result, evaluations] = bisection_min_step (v[i:len (v)], new_limit)
            return [result, evaluations + 3]
        elif (direction is -1):
            if (limit is not None):
                new_limit = limit - 1
            [result, evaluations] = bisection_min_step (v[0:i], new_limit)
            return [result, evaluations + 3]
        else:
            if (limit is not None):
                new_limit = limit - 1
            [result1, evaluations1] = bisection_min_step (v[0:i], new_limit)
            if (limit is not None):
                new_limit = limit - evaluations1
            [result2, evaluations2] = bisection_min_step (v[i:len (v)], new_limit)
            return [min (result1, result2), evaluations1 + evaluations2 + 3] 


def select_side (v, i):
    """ This function receives a vector v and an index i and, based on the elements
    v[i - 1], v[i] and v[i + 1] decides if the points are decreasing returning 1 if
    they are and -1 if they are increasing """
    l = i - 1
    if (l < 0):
        l = 0
    r = i + 1
    if (r >= len (v)):
        r = len (v) - 1

    d = v[l] - v[r]
    if (abs (d) < 1e-20): # if we don't know where to go
        return 0
    
    return int (d / abs (d))


def valley (v, i):
    """ This function verifies if the element on index i of v is a valley, i.e if the 
    element on index i of v is strictly less than its neighbours """
    if (len (v) is 1):
        return True
    
    # from now on we can assume we have at least two elements
    if (i > 0):
        vl = v[i - 1]
    else: # just reflect the other neighbour if we are in the extreme
        vl = v[i + 1]
    if (i < len (v) - 1):
        vr = v[i + 1]
    else:
        vr = v[i - 1]

    return v[i] < min (vl, vr)


def mid_neighbour_bisection (v, limit = None):
    """ This function receives a vector, that describes approximately u-shaped curve, as
    argument and return the minimum element of this vector """
    return mid_neighbour_step (v, 1, -1.0 / int_log2 (len (v)), limit)
    

def mid_neighbour_step (v, reliance, reliance_increment, limit = None):
    """ Receives a vector v, a reliance and a reliance increment. This function divides
    the vector in 4 equal pieces with 3 different points lm, m and rm. The value of the 
    vector is calculated in these points and an abstract slope is calculated. This 
    abstract slope considers the difference between simple difference of the three points
    and also the reliance value to decide wheter the function grows, decreases or 
    is a plain (which is the same case as when the reliance is too low). Based on these 3
    cases we can prune the vector until we get a solution.
    The reliance is updated in a way that when the vector gets smaller, the difference 
    between the points get less reliable to decide whether the function is increasing or 
    decreasing. When the difference * reliance is too low we treat it as a plain area 
    and calculate both 'sides' of the vector separately to avoid prunning the minimum"""
    #print ("Bisection step on: ", v)
    #print ("reliance: ", reliance)
    m = (len (v) // 2) 
    lm = m // 2
    rm = m + (len (v) - m) // 2
    #print ("lm, m, rm: ", lm, ", ", m, ", ", m)

    # minimum of a vector of one element
    if (lm is rm or (limit is not None and limit <= 0)):
        return [v[m], 0]

    ld = v[m] - v[lm]
    rd = v[rm] - v[m]
    l_slope = abstract_slope (ld, reliance)
    r_slope = abstract_slope (rd, reliance)
    new_reliance = max (reliance + reliance_increment, 0)
    #print ("l_slope, r_slope: ", l_slope, ", ", r_slope)
    
    # cases:
    #    
    #      m    ,   lm -- m -- rm 
    # lm /   \ rm
    if ((l_slope is 1 and r_slope is -1) or (l_slope is 0 and r_slope is 0)):
        if (limit is not None):
            limit -= 1
        [result1, evaluations1] = \
                mid_neighbour_step (v[0:m], new_reliance, reliance_increment, limit)
        if (limit is not None):
            limit -= evaluations1
        [result2, evaluations2] = \
                mid_neighbour_step (v[m:len(v)], new_reliance, reliance_increment, limit)
        return [min (result1, result2), evaluations1 + evaluations2 + 3]

    # cases:
    #
    # lm       rm
    #    \ m /
    elif (l_slope is -1 and r_slope is 1):
        if (limit is not None):
            limit -= 1
        [result, evaluations] = \
                mid_neighbour_step (v[lm + 1:rm], new_reliance, reliance_increment, limit)
        return [result, evaluations + 3]

    # cases:
    #
    #          rm ,      m -- rm 
    #      m /      lm /            
    # lm /
    elif (l_slope is 1 and (r_slope is 1 or r_slope is 0)):
        if (limit is not None):
            limit -= 1
        [result, evaluations] = \
                mid_neighbour_step (v[0:m + 1], new_reliance, reliance_increment, limit)
        return [result, evaluations + 3]

    # cases:
    #
    # lm            
    #    \ m -- rm 
    elif (l_slope is -1 and r_slope is 0):
        if (limit is not None):
            limit -= 1
        [result, evaluations] = \
                mid_neighbour_step (v[lm:len(v)], new_reliance, reliance_increment, limit)
        return [result, evaluations + 3]

    # cases:
    #
    # lm -- m
    #         \ rm
    elif (l_slope is 0 and r_slope is 1):
        if (limit is not None):
            limit -= 1
        [result, evaluations] = \
                mid_neighbour_step (v[0:rm], new_reliance, reliance_increment, limit)
        return [result, evaluations + 3]

    # cases:
    #
    # lm            lm -- m 
    #    \ m      ,         \ rm
    #        \ rm
    else:
        if (limit is not None):
            limit -= 1
        [result, evaluations] = \
                mid_neighbour_step (v[m:len (v)], new_reliance, reliance_increment, limit)
        return [result, evaluations + 3]



def abstract_slope (d, reliance):
    """ Calculates the abstract slope used in mid_neighbour """
    alpha = d * reliance
    if (abs (alpha) < 1e-3):
        return 0
    else:
        return int (d / abs (d))

def int_log2 (x):
    """ Calculates the base 2 logarithm of an integer x """
    x = int (x)
    i = 0
    while (x > 0):
        x = x // 2
        i = i + 1
    return i


def upb (v, pc, pmf = None, limit = None):
    """ U-Curve Probabilistic Bisection 
    This function receives a vector, that describes approximately u-shaped curve, as
    argument and return the minimum element of this vector """
    n = len (v)

    total_s = time ()
    update_time = 0
    nof_updates = 0
    
    # Probability Mass Function
    if (pmf is None):
        pmf = PMF (n)
    
    evaluations = 0
    if (limit is None):
        # limit = n 
        limit = 1 + 2 * int_log2 (n) * int_log2 (n)

    first_qt = pmf.get_quarter (1)
    median = pmf.get_quarter (2)
    third_qt = pmf.get_quarter (3)
    while ((first_qt is not median and \
           median is not third_qt) and limit > 0):
        evaluations += 3

        direction = select_side (v, median)
        if (direction is 0):
            if (median - first_qt > third_qt - median):
                direction = -1
            else:
                direction = 1
        
        alpha = pmf.get_quarter_mass (2)
        pmf.update (pc, median, alpha, direction)
        first_qt = pmf.get_quarter (1)
        median = pmf.get_quarter (2)
        third_qt = pmf.get_quarter (3)
        limit -= 1

    return [v[median], evaluations]

def mupb (v, pc, pmf = None, limit = None):
    """ Mid-neighbour U-Curve Probabilistic Bisection 
    This function receives a vector, that describes approximately u-shaped curve, as
    argument and return the minimum element of this vector """
    n = len (v)
    
    # Probability Mass Function
    if (pmf is None):
        pmf = PMF (n)
    
    evaluations = 0
    if (limit is None):
        # limit = 1 + 2 * int_log2 (n) * int_log2 (n)
        limit = n

    first_qt = pmf.get_quarter (1)
    median = pmf.get_quarter (2)
    third_qt = pmf.get_quarter (3)
    while (first_qt is not median or \
           median is not third_qt and limit > 0):
        evaluations += 3

        # print (v)
        d = float (v[third_qt] - v[first_qt])
        if (abs (d) < 1e-8):
            d = 0
        else:
            d = d / abs (d)

        if (d is 0):
            if (v[median] < v[first_qt]):
                pmf.update (pc, first_qt, pmf.get_quarter_mass (1), 1)
                if (pmf.get_quarter (1) != pmf.get_quarter (2) and \
                    pmf.get_quarter (3) != pmf.get_quarter (2)):
                    pmf.update (pc, third_qt, pmf.get_quarter_mass (3), -1)
            else:
                if (median - first_qt > third_qt - median):
                    pmf.update (pc, first_qt, pmf.get_quarter_mass (1), 1)
                else:
                    pmf.update (pc, third_qt, pmf.get_quarter_mass (3), -1)
                # [result, sub_eval] = split_mupb (v, pc, pmf, median, limit)
                # return [result, evaluations + sub_eval]
        else:
            if (d > 0):
                pmf.update (pc, third_qt, pmf.get_quarter_mass (3), -1)
            else:
                pmf.update (pc, first_qt, pmf.get_quarter_mass (1), 1)
        
        first_qt = pmf.get_quarter (1)
        median = pmf.get_quarter (2)
        third_qt = pmf.get_quarter (3)
        limit -= 1

    return [v[median], evaluations]



def split_upb (v, pc, pmf, i, limit):
    """ Splits the orginal problem v with pmf in two parts, from 0 to i - 1 and from
    i + 1 to len (v) """
    pmf.split_in (pmf.get_quarter (2), pmf.get_median_block ())

    # print ("Splitting")

    blocks = pmf.get_blocks ()
    half_size = len (blocks) // 2
    # print ("Dividing: ")
    blocks1 = blocks[0:half_size]
    blocks2 = blocks[half_size:len (blocks)]
    translate_blocks (blocks1)
    translate_blocks (blocks2)
    
    n1 = sum ((block.end - block.start) for block in blocks1)
    n2 = len (v) - n1
    v1 = v[0:n1]
    v2 = v[n1:len (v)]
    # print ("n = ", len (v), ", |blocks| = ", len (blocks), ", half_size = ", half_size, ", n1 = ", n1, ", n2 = ", n2)
    
    pmf1 = PMF (n1, blocks1)
    pmf2 = PMF (n2, blocks2)
    
    sol1 = None
    eval1 = 0
    sol2 = None
    eval2 = 0
    if (len (v1) > 0):
        [sol1, eval1] = upb (v1, pc, pmf1, limit)
        limit -= eval1
    if (len (v2) > 0):
        [sol2, eval2] = upb (v2, pc, pmf2, limit)
    
    return [min (min_with_none (sol1, sol2), v[i]), eval1 + eval2]


def translate_blocks (blocks):
    offset = blocks[0].start
    for i in range (len (blocks)):
        blocks[i].start -= offset
        blocks[i].end -= offset

def split_mupb (v, pc, pmf, i, limit):
    """ Splits the orginal problem v with pmf in two parts, from 0 to i - 1 and from
    i + 1 to len (v) """
    pmf.split_in (pmf.get_quarter (2), pmf.get_median_block ())

    # print ("Splitting")

    blocks = pmf.get_blocks ()
    half_size = len (blocks) // 2
    # print ("Dividing: ")
    blocks1 = blocks[0:half_size]
    blocks2 = blocks[half_size:len (blocks)]
    translate_blocks (blocks1)
    translate_blocks (blocks2)
    
    n1 = sum ((block.end - block.start) for block in blocks1)
    n2 = len (v) - n1
    v1 = v[0:n1]
    v2 = v[n1:len (v)]
    # print ("n = ", len (v), ", |blocks| = ", len (blocks), ", half_size = ", half_size, ", n1 = ", n1, ", n2 = ", n2)
    
    pmf1 = PMF (n1, blocks1)
    pmf2 = PMF (n2, blocks2)
    
    sol1 = None
    eval1 = 0
    sol2 = None
    eval2 = 0
    if (len (v1) > 0):
        [sol1, eval1] = mupb (v1, pc, pmf1, limit)
        limit -= eval1
    if (len (v2) > 0):
        [sol2, eval2] = mupb (v2, pc, pmf2, limit)
    
    return [min (min_with_none (sol1, sol2), v[i]), eval1 + eval2]



def min_with_none (a, b):
    """ Same as the built in min function, except that this one handles None elements """
    if (a is None):
        return b
    if (b is None):
        return a
    return min (a, b)

    

def normalize_pmf (pmf):
    """ Makes sum (pmf) = 1 and keep the proportion of it's elements """
    total = sum (pmf)
    pmf[0:len (pmf)] = map (lambda x: x / total, pmf[0:len (pmf)])
    


def find_eighths (pmf):
    """ Returns a vector of size 9 where the index i of the vector contains the 
    "information" of the element x such that x is the smallest-indexed element where 
    F (x) >= 8 / i, i.e it fetches the eights of the pmf. The information is a pair with
    [i, alpha] where i is the index of x in the pmf and alpha is F(x) """
    eights = [[0, 0]] * 9
    i = 0
    alpha = pmf[i]
    
    for j in range (1, 7):
        x = j / 8.0
        while (alpha < x):
            i += 1
            alpha += pmf[i]
        eights[j] = [i, alpha]
    return eights

def update_pmf (pmf, pc, i, alpha, direction):
    """ if direction >= 0
        pmf_{n+1}(y) = (1/(1 - alpha))*pc*pmf_{n}(y) for y >= x_{n}
        pmf_{n+1}(y) = (1/alpha)*qc*pmf_{n}(y) for y < x_{n}
    and, similarly, for direction = -1 
        pmf_{n+1}(y) = (1/(1 - alpha))*qc*pmf_{n}(y) for y >= x_{n}
        pmf_{n+1}(y) = (1/alpha)*pc*pmf_{n}(y) for y < x_{n} """
    qc = 1 - pc

    #print ("preferred side: ", direction)
    #print ("sum before: ", sum (pmf))
    
    if (direction < 0):
        # beta = P (x* < X_n)
        # beta < 1 
        beta = alpha - pmf[i]
        #print ("alpha: ", alpha, "| beta: ", beta, "| pmf[i]: ", pmf[i])
        if (1 - beta < 1e-8):
            return
        
        pmf[i:len (pmf)] = map (lambda x: (1.0 / (1 - beta)) * qc * x, pmf[i:len (pmf)])
        pmf[0:i] = map (lambda x: (1.0 / beta) * pc * x, pmf[0:i])
    else:
        # alpha = P (x* <= X_n)
        if (1 - alpha < 1e-8):
            return

        pmf[i + 1:len (pmf)] = \
                map (lambda x: (1.0 / (1 - alpha)) * pc * x, pmf[i + 1: len (pmf)])
        pmf[0:i + 1] = map (lambda x: (1.0 / alpha) * qc * x, pmf[0:i + 1])

    #print ("sum after: ", sum (pmf))


def mbb (v, sigma, limit = None):
    m = len (v) // 2
    lm = m // 2
    rm = m + (len (v) - m) // 2

    acceptance = .9

    # print ("v: ", v)

    if (lm is rm or (limit is not None and limit <= 0)):
        return [v[m], 0]

    if (limit is not None):
        limit -= 1

    # print ("lm: ", lm, " | m: ", m, " | rm: ", rm)
    # print ("v[lm]: ", v[lm], " | v[m]: ", v[m], " | v[rm]: ", v[rm])

    if (v[lm] < v[rm]):
        min_point = lm
        if (v[lm] > v[m]):
            min_point = m

        alpha = v[min_point] - v[rm]
        # print ("L Alpha: ", alpha, ", sigma: ", sigma)
        if (alpha < -2 * sigma):
            [sol, evaluations] = mbb (v[0:rm], sigma, limit)
            return [sol, evaluations + 2]
        else:
            [sol1, evaluations1] = mbb (v[0:m], sigma, limit)
            if (limit is not None):
                limit -= evaluations1
            [sol2, evaluations2] = mbb (v[m:len (v)], sigma, limit)
            return [min (sol1, sol2), evaluations1 + evaluations2 + 2]
    else:
        min_point = rm
        if (v[rm] > v[m]):
            min_point = m

        alpha = v[min_point] - v[lm]
        # print ("R Alpha: ", alpha, ", sigma: ", sigma)
        if (alpha < -2 * sigma):
            [sol, evaluations] = mbb (v[lm + 1:len (v)], sigma, limit)
            return [sol, evaluations + 2]
        else:
            [sol1, evaluations1] = mbb (v[0:m], sigma, limit)
            if (limit is not None):
                limit -= evaluations1
            [sol2, evaluations2] = mbb (v[m:len (v)], sigma, limit)
            return [min (sol1, sol2), evaluations1 + evaluations2 + 2]
