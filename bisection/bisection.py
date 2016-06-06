def bisection_min (v):
    """ This function receives a vector, that describes a u-shaped curve, as argument
    and return the minimum element of this vector """
    i = len (v) // 2
    
    if (valley (v, i)):
        return v[i]
    else:
        direction = select_side (v, i)
        if (direction is 1):
            return bisection_min (v[i:len (v)])
        elif (direction is -1):
            return bisection_min (v[0:i])
        else:
            return min (bisection_min (v[0:i]), bisection_min (v[i:len (v)]))


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

    # minimum of a vector of one element
    if lm is rm:
        return v[m]

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
        return min (mid_neighbour_step (v[0:m], new_reliance, reliance_increment), \
                mid_neighbour_step (v[m:len(v)], new_reliance, reliance_increment))
    # cases:
    #
    # lm       rm
    #    \ m /
    elif (l_slope is -1 and r_slope is 1):
        return mid_neighbour_step (v[lm + 1:rm], new_reliance, reliance_increment)

    # cases:
    #
    #          rm ,      m -- rm 
    #      m /      lm /            
    # lm /
    elif (l_slope is 1 and (r_slope is 1 or r_slope is 0)):
        return mid_neighbour_step (v[0:m + 1], new_reliance, reliance_increment)

    # cases:
    #
    # lm            
    #    \ m -- rm 
    elif (l_slope is -1 and r_slope is 0):
        return mid_neighbour_step (v[lm:len(v)], new_reliance, reliance_increment)

    # cases:
    #
    # lm -- m
    #         \ rm
    elif (l_slope is 0 and r_slope is 1):
        return mid_neighbour_step (v[0:rm], new_reliance, reliance_increment)

    # cases:
    #
    # lm            lm -- m 
    #    \ m      ,         \ rm
    #        \ rm
    else:
        return mid_neighbour_step (v[m:len (v)], new_reliance, reliance_increment)


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


def upb (v):
    """ U-Curve Probabilistic Bisection 
    This function receives a vector, that describes approximately u-shaped curve, as
    argument and return the minimum element of this vector """
    n = len (v)
    # probability mass function
    # Suppose that the minimum element of v is in v[x*], then, we say that 
    #       P(x* = i) = pmf[i]
    pmf = [1.0 / n] * n
    i = 0
    old_i = -1
    limit = 1000
    while (old_i is not i and limit > 0):
        print ("-------------\nIterating...")
        print ("Initial pmf: ", pmf)
        old_i = i
        [i, alpha] = find_median (pmf)
        print ("i, alpha: ", i, ", ", alpha)
        direction = select_side (v, i)
        print ("direction: ", direction)
        update_pmf (pmf, i, alpha, direction)
        #update_pmf2 (pmf, i, direction)
        print ("New pmf: ", pmf)
        print ("pmf sum:", sum(pmf))
        limit -= 1

    return v[i]

def find_median (pmf):
    """ Receives v and pmf and returns the index of v and alpha such that:
        i = argmin {v[i] | P(x* <= i) >= 1/2}, and
        alpha = P(x <= i)
    """
    print (pmf)
    i = 0
    alpha = pmf[i]
    while (alpha < .5):
        i += 1
        alpha += pmf[i]

    return [i, alpha]

def update_pmf (pmf, i, alpha, direction):
    """ if direction >= 0
        pmf_{n+1}(y) = (1/(1 - alpha))*pc*pmf_{n}(y) for y >= x_{n}
        pmf_{n+1}(y) = (1/alpha)*qc*pmf_{n}(y) for y < x_{n}
    and, similarly, for direction = -1 
        pmf_{n+1}(y) = (1/(1 - alpha))*qc*pmf_{n}(y) for y >= x_{n}
        pmf_{n+1}(y) = (1/alpha)*pc*pmf_{n}(y) for y < x_{n}
    """
    pc = .75
    qc = 1 - pc
    
    if (direction < 0):
        pc = 1 - pc
        qc = 1 - qc

    if (alpha > 0.95):
        return [i, 0]

    pmf[0:i] = map (lambda x: (1.0 / alpha) * qc * x, pmf[0:i])
    pmf[i:len (pmf)] = map (lambda x: (1.0 / (1 - alpha)) * pc * x, pmf[i:len (pmf)])

def update_pmf2 (pmf, i, direction):
    pc = .75
    qc = 1 - pc
    if (direction < 0):
        pc = 1 - pc
        qc = 1 - qc

    pmf[0:i] = map (lambda x: qc * x, pmf[0:i])
    pmf[i:len (pmf)] = map (lambda x: pc * x, pmf[i:len (pmf)])
    
    total = sum (pmf)
    pmf[0:len (pmf)] = map (lambda x: x / total, pmf[0:len (pmf)])
