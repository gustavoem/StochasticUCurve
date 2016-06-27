class Block:

    def __init__ (self, p, size):
        self.p = p
        self.size = size

    def mass (self):
        return p * size




class PMF:

    def __init__(self, n):
        self.blocks = [Block (1.0 / n, n)]


    def update (self, mid, direction, pc):
        """ Updates the pfm 
        if direction >= 0
            pmf_{n+1}(y) = (1/(1 - alpha))*pc*pmf_{n}(y) for y >= mid
            pmf_{n+1}(y) = (1/alpha)*qc*pmf_{n}(y) for y < mid
        and, similarly, for direction = -1 
            pmf_{n+1}(y) = (1/(1 - alpha))*qc*pmf_{n}(y) for y >= mid
            pmf_{n+1}(y) = (1/alpha)*pc*pmf_{n}(y) for y < mid 
        Where alpha is the accumulate density of the mid element """
        qc = 1 - pc

        #print ("preferred side: ", direction)
        #print ("sum before: ", sum (pmf))

        # calculates alpha
 

    def calculate_alpha (self, mid):
        alpha = 0
        block_i = 0
        element_i = 0
        print ("pmf: ", self.toString ())

        while (element_i + self.blocks[block_i].size < mid):
            alpha += self.blocks[block_i].mass
            element_i += self.blocks[block_i].size
            block_i += 1

        alpha += self.blocks[block_i].p * (mid - element_i)
        return alpha


    def toString (self):
        s = ""
        for block in self.blocks:
            s += str (block.p) + ": " + str (block.size) + "; "
        return s


pmf = PMF (7)
alpha = pmf.calculate_alpha (4)
print (alpha)
