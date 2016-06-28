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
        mid_block = self.__find_mid_block (mid)
        alpha = self.calculate_alpha (mid)
        beta = alpha - self.blocks[mid_block].p

        if (direction < 0):
            # what does this mean now? 
            if (1 - beta < 1e-8):
                return

            self.split_in (mid, mid_block)
            for i in range (len (self.blocks)):
                if (self.blocks[i].start < mid):
                    self.blocks[i].p *= (pc * (1.0 / beta))
                else:
                    self.blocks[i].p *= (qc * (1.0 / (1 - beta)))

        else:
            if (1 - alpha < 1e-8):
                return

            if (mid == self.blocks[mid_block].end - 1):
                mid_block += 1
            mid = mid + 1
            
            self.split_in (mid, mid_block)
            for i in range (len (self.blocks)):
                if (self.blocks[i].start < mid):
                    self.blocks[i].p *= (qc * (1.0 /  alpha))
                else:
                    self.blocks[i].p *= (pc * (1.0 / (1 - alpha)))


            
    def __find_mid_block (self, mid):
        """ Finds the block that contains the mid element probability """
        block_i = 0
        while (self.blocks[block_i].end < mid):
            block_i += 1
        return block_i
        

    def split_in (self, i, block_i):
        """ Splits the block block_i, which contains the element i in two blocks. The i
        element will be in the first element of the second block """
        # careful here, what does this imply in the later update?
        if (self.blocks[block_i].end - self.blocks[block_i].start < 2):
            return

        old_block = self.blocks[block_i]
        first_block = Block (old_block.p, old_block.start, i)
        second_block = Block (old_block.p, i, old_block.end)
        self.blocks[block_i:block_i + 1] = [first_block, second_block]


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
# alpha = pmf.calculate_alpha (1)
# print (alpha)

# print ("before split: " + pmf.toString ())
# pmf.split_in (2, 0)
# print ("after split: " + pmf.toString ())

print ("before update: " + pmf.toString ())
pmf.update (2, -1, 0.7)
print ("after update: " + pmf.toString ())