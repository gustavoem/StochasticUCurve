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
                new_limit = limit - 1
            [result2, evaluations2] = bisection_min_step (v[i:len (v)], new_limit)
            return [min (result1, result2), evaluations1 + evaluations2 + 3] 


def select_side (v, i):
    """ This function receives a vector v and an index i and, based on the elements
    v[i - 1], v[i] and v[i + 1] decides if the points are decreasing returning 1 if
    they are and -1 if they are increasing """
    l = max (0, i - 1)
    r = min (len(v) - 1, i + 1)
    d = v[l] - v[r]

    if (abs (d) < 1e-10): # if we don't know where to go
        return 0
    
    return int(d / abs (d))


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


def mid_neighbour_bisection (v):
    """ This function receives a vector, that describes approximately u-shaped curve, as
    argument and return the minimum element of this vector """
    #print ("Bisection on v: ", v)
    
    return mid_neighbour_step (v, 1, -1.0 / int_log2 (len (v)))
    

def mid_neighbour_step (v, reliance, reliance_increment):
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
    if lm is rm:
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
        [result1, evaluations1] = mid_neighbour_step (v[0:m], new_reliance, reliance_increment)
        [result2, evaluations2] = mid_neighbour_step (v[m:len(v)], new_reliance, reliance_increment)
        return [min (result1, result2), evaluations1 + evaluations2 + 3]

    # cases:
    #
    # lm       rm
    #    \ m /
    elif (l_slope is -1 and r_slope is 1):
        [result, evaluations] = \
                mid_neighbour_step (v[lm + 1:rm], new_reliance, reliance_increment)
        return [result, evaluations + 3]

    # cases:
    #
    #          rm ,      m -- rm 
    #      m /      lm /            
    # lm /
    elif (l_slope is 1 and (r_slope is 1 or r_slope is 0)):
        [result, evaluations] = \
                mid_neighbour_step (v[0:m + 1], new_reliance, reliance_increment)
        return [result, evaluations + 3]

    # cases:
    #
    # lm            
    #    \ m -- rm 
    elif (l_slope is -1 and r_slope is 0):
        [result, evaluations] =  mid_neighbour_step (v[lm:len(v)], new_reliance, reliance_increment)
        return [result, evaluations + 3]

    # cases:
    #
    # lm -- m
    #         \ rm
    elif (l_slope is 0 and r_slope is 1):
        [result, evaluations] = \
                mid_neighbour_step (v[0:rm], new_reliance, reliance_increment)
        return [result, evaluations + 3]

    # cases:
    #
    # lm            lm -- m 
    #    \ m      ,         \ rm
    #        \ rm
    else:
        [result, evaluations] = \
                mid_neighbour_step (v[m:len (v)], new_reliance, reliance_increment)
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


def upb (v, pc, pmf = []):
    """ U-Curve Probabilistic Bisection 
    This function receives a vector, that describes approximately u-shaped curve, as
    argument and return the minimum element of this vector """
    n = len (v)
    # probability mass function
    # Suppose that the minimum element of v is in v[x*], then, we say that 
    #       P(x* = i) = pmf[i]
    if (pmf == []):
        pmf = [1.0 / n] * n
    
    evaluations = 0
    

    eights = find_eighths (pmf)
    median = eights[4][0]
    alpha = eights[4][1]
    first_qt = eights [2][0]
    third_qt = eights [6][0]

    limit = n
    while ((first_qt is not median and \
           median is not third_qt) and limit > 0):
        evaluations += 3

        #print ("-------------\nIterating...")
        #print ("Initial pmf: ", pmf)
        #print ("v: ", v)
        
        #print ("1st qt: ", first_qt)
        #print ("median, alpha: ", median, ", ", alpha)
        #print ("3rd qt: ", third_qt)

        direction = select_side (v, median)
        if (direction is 0):
            [result, child_eval] = split_upb (v, pc, pmf, median)
            return [result, evaluations + child_eval]
        
        #print ("direction: ", direction)
        update_pmf (pmf, pc, median, alpha, direction)
        #print ("New pmf: ", pmf)
        #print ("pmf sum:", sum(pmf))
        
        eights = find_eighths (pmf)
        median = eights[4][0]
        alpha = eights[4][1]
        first_qt = eights [2][0]
        third_qt = eights [6][0]

        limit -= 1

    evaluations += 3
    return [v[median], evaluations]

def mupb (v, pc, pmf = []):
    """ Mid-neighbour U-Curve Probabilistic Bisection 
    This function receives a vector, that describes approximately u-shaped curve, as
    argument and return the minimum element of this vector """
    n = len (v)
    # probability mass function
    # Suppose that the minimum element of v is in v[x*], then, we say that 
    #       P(x* = i) = pmf[i]
    if (pmf == []):
        pmf = [1.0 / n] * n
    
    evaluations = 0

    eights = find_eighths (pmf)
    median = eights[4][0]
    alpha = eights[4][1]
    first_qt = eights [2][0]
    third_qt = eights [6][0]

    limit = n
    while (first_qt is not median and \
           median is not third_qt and limit > 0):
        evaluations += 3

       #print ("-------------\nIterating...")
       #print ("Initial pmf: ", pmf)
       #print ("v: ", v)
        
       #print ("1st qt: ", first_qt)
       #print ("median, alpha: ", median, ", ", alpha)
       #print ("3rd qt: ", third_qt)
        
        d = float (v[third_qt] - v[first_qt])
        if (abs (d) < 1e-8):
            d = 0
        else:
            d = d / abs (d)
        
       #print ("direction: ", d)

        if (d is 0):
            if (v[median] < v[first_qt]):
                update_pmf (pmf, pc, first_qt, eights [2][1], 1)
                update_pmf (pmf, pc, third_qt, eights [6][1], -1)
            else:
                [result, child_eval] = split_mupb (v, pc, pmf, median)
                return [result, evaluations + child_eval]
        else:
            if (d == 1.0):
                update_pmf (pmf, pc, third_qt, eights [6][1], -1)
            else:
                update_pmf (pmf, pc, first_qt, eights [2][1], 1)
        
       #print ("New pmf: ", pmf)
       #print ("pmf sum:", sum(pmf))
        
        eights = find_eighths (pmf)
        median = eights[4][0]
        alpha = eights[4][1]
        first_qt = eights [2][0]
        third_qt = eights [6][0]

        limit -= 1

    evaluations += 3
    return [v[median], evaluations]



def split_upb (v, pc, pmf, i):
    """ Splits the orginal problem v with pmf in two parts, from 0 to i - 1 and from
    i + 1 to len (v) """
    v1 = v[0:i]
    v2 = v[i + 1:len (v)]
    
    pmf1 = pmf[0:i]
    pmf2 = pmf[i + 1:len (v)]
    normalize_pmf (pmf1)
    normalize_pmf (pmf2)
    
    sol1 = None
    eval1 = 0
    sol2 = None
    eval2 = 0
    if (len (v1) > 0):
        [sol1, eval1] = upb (v1, pc, pmf1)
    if (len (v2) > 0):
        [sol2, eval2] = upb (v2, pc, pmf2)
    
    return [min (min_with_none (sol1, sol2), v[i]), eval1 + eval2]


def split_mupb (v, pc, pmf, i):
    """ Splits the orginal problem v with pmf in two parts, from 0 to i - 1 and from
    i + 1 to len (v) """
    v1 = v[0:i]
    v2 = v[i + 1:len (v)]
    
    pmf1 = pmf[0:i]
    pmf2 = pmf[i + 1:len (v)]
    normalize_pmf (pmf1)
    normalize_pmf (pmf2)
    
    sol1 = None
    eval1 = 0
    sol2 = None
    eval2 = 0
    if (len (v1) > 0):
        [sol1, eval1] = mupb (v1, pc, pmf1)
    if (len (v2) > 0):
        [sol2, eval2] = mupb (v2, pc, pmf2)
    
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
