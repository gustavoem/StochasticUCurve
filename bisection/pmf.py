class Block:

    def __init__ (self, p, start, end):
        """ The block represents the value of the pmf of the values in the interval 
        [start, end). """
        self.p = p
        self.start = start
        self.end = end

    def mass (self):
        """ Returns the probability mass of the block """
        return p * (end - start)




class PMF:

    def __init__(self, n):
        """ Creates a PMF represented with blocks with same probability """
        self.blocks = [Block (1.0 / n, 0, n)]


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
        # calculates alpha and beta
        mid_block = __find_mid_block (mid)
        alpha = __calculate_alpha (mid)
        beta = alpha - mid_block.p

        if (direction < 0):
            if (1 - beta < 1e-8):
                return



            
    def __find_mid_block (self, mid):
        """ Finds the block that contains the mid element probability """
        block_i = 0
        while (self.blocks[block_i].end < mid):
            block_i += 1
        return block_i
        

    def __split_in (self, i, block_i):
        """ Splits the block block_i, which contains the element i in two blocks. The i
        element will be in the last element of the first block """




    def calculate_alpha (self, mid):
        """ Calculates alpha and beta where:
            alpha = P (i* <= mid) """
        alpha = 0
        block_i = 0

        while (self.blocks[block_i].end < mid):
            alpha += self.blocks[block_i].mass
            block_i += 1

        block_start = self.blocks[block_i].start
        alpha += self.blocks[block_i].p * (mid - block_start + 1)
        return alpha


    def toString (self):
        s = ""
        for block in self.blocks:
            s += "-| " + str (block.p) + ": " + str (block.start) + "-" + str (block.end) + " |-"
        return s


pmf = PMF (7)
alpha = pmf.calculate_alpha (1)
print (alpha)