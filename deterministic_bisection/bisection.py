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


def dip_toe_ubisection (v):
    """ This function receives a vector, that describes approximately u-shaped curve, as
    argument and return the minimum element of this vector """
    #print ("Bisection on v: ", v)
    
    return dip_toe_step (v, 1, -1.0 / int_log2 (len (v)))
    

def dip_toe_step (v, reliance, reliance_increment):
    """ This function receives """
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
        return min (dip_toe_step (v[0:m], new_reliance, reliance_increment), \
                dip_toe_step (v[m:len(v)], new_reliance, reliance_increment))
    # cases:
    #
    # lm       rm
    #    \ m /
    elif (l_slope is -1 and r_slope is 1):
        return dip_toe_step (v[lm + 1:rm], new_reliance, reliance_increment)

    # cases:
    #
    #          rm ,      m -- rm ,           rm
    #      m /      lm /           lm -- m / 
    # lm /
    elif ((l_slope is 1 and (r_slope is 1 or r_slope is 0)) or (l_slope is 0 and r_slope is 1)):
        return dip_toe_step (v[0:m], new_reliance, reliance_increment)


    # cases:
    #
    # lm            lm             lm -- m 
    #    \ m      ,    \ m -- rm ,         \ rm
    #        \ rm
    else:
        return dip_toe_step (v[m:len (v)], new_reliance, reliance_increment)


def abstract_slope (d, reliance):
    alpha = d * reliance
    if (abs (alpha) < 1e-3):
        return 0
    else:
        return int (d / abs (d))



def int_log2 (x):
    x = int (x)
    i = 0
    while (x > 0):
        x = x // 2
        i = i + 1
    return i
