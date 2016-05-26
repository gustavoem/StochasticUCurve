def bisection_min (v):
    """ This function receives a vector, that describes a u-shaped curve, as argument
    and return the minimum element of this vector """
    n = len (v)
    i = n // 2
    
    while (not valley (v, i)):
        direction = select_side (v, i)
        i = i + direction * (i // 2)

    return v[i]


def select_side (v, i):
    """ This function receives a vector v and an index i and, based on the elements
    v[i - 1], v[i] and v[i + 1] decides if the points are decreasing returning 1 if
    they are and -1 if they are increasing """
    l = max (0, i - 1)
    r = min (len(v) - 1, i + 1)
    d = v[l] - v[r]
    return d / abs (d)


def valley (v, i):
    l = max (0, i - 1)
    r = min (len(v) - 1, i + 1)
    return v[i] <= min (v[l], v[r])
