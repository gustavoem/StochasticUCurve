class Block:

    def __init__ (self, p, start, end):
        """ The block represents the value of the pmf of the values in the interval 
        [start, end). """
        self.p = p
        self.start = start
        self.end = end

    def mass (self):
        """ Returns the probability mass of the block """
        return self.p * (self.end - self.start)




class PMF:

    def __init__(self, n, blocks = None):
        """ Creates a PMF represented with blocks with same probability """
        self.__quarters = None

        if (blocks is not None):
            self.__blocks = blocks
            self.normalize_blocks ()
        else:
            self.__blocks = [Block (1.0 / n, 0, n)]
        
        self.find_quarters ()
        self.__median_block = self.find_block (self.__quarters[2][0])


    def normalize_blocks (self):
        """ Used when copying part of a pmf. This normalilzes the pmf so the sum of
        all blocks is one """
        total_mass = 0
        for block in self.__blocks:
            total_mass += block.mass ()

        for i in range (len (self.__blocks)):
            self.__blocks[i].p /= total_mass


    def get_blocks (self):
        """ Return the list of blocks """
        return self.__blocks


    def get_median_block (self):
        """ Return the index of the block that has the median of the PMF """
        return self.__median_block


    def update (self, pc, mid, alpha, direction):
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
        mid_block = self.find_block (mid) ## this will get messed up at some point in the mupb
        beta = alpha - self.__blocks[mid_block].p

        if (direction < 0):
            # what does this mean now? 
            #if (1 - beta < 1e-8):
            #    return

            self.split_in (mid, mid_block)
            for i in range (len (self.__blocks)):
                if (self.__blocks[i].start < mid):
                    self.__blocks[i].p *= (pc * (1.0 / beta))
                else:
                    self.__blocks[i].p *= (qc * (1.0 / (1 - beta)))

        else:
            # if (1 - alpha < 1e-8):
            #     return

            if (mid == self.__blocks[mid_block].end - 1):
                mid_block += 1
            mid = mid + 1
            
            self.split_in (mid, mid_block)
            for i in range (len (self.__blocks)):
                if (self.__blocks[i].start < mid):
                    self.__blocks[i].p *= (qc * (1.0 /  alpha))
                else:
                    self.__blocks[i].p *= (pc * (1.0 / (1 - alpha)))

        # print ("Updated PMF: " + self.toString ())
        self.find_quarters ()


    def find_quarters (self):
        """ Updates the listing of the PMF quarters """
        self.__quarters = [(0, 0)] * 4
        # print ("Finding quarters on these blocks: ")
        # print (len(self.__blocks))
        # print (self.toString ())
        # print ("dump it")
        accumulated = 0
        block_i = 0
        for i in range (1, 4):
            x =  i / 4.0
            while (accumulated + self.__blocks[block_i].mass () < x):
                accumulated += self.__blocks[block_i].mass ()

            if (i == 2):
                self.__median_block = block_i

            remainder = x - accumulated
            block_p = self.__blocks[block_i].p
            intra_block_i = int (remainder / block_p)
            accumulated += block_p * intra_block_i
            self.__quarters[i] = (intra_block_i, accumulated)


    def get_quarter (self, i):
        """ Return the index of the i-th quarter of the PMF """
        return self.__quarters[i][0]


    def get_quarter_mass (self, i):
        """ Return the mass of the i-th quarter of the PMF """
        return self.__quarters[i][1]

            
    def find_block (self, i):
        """ Finds the block that contains the i-th element probability """
        block_i = 0
        while (self.__blocks[block_i].end < i):
            block_i += 1
        return block_i
        

    def split_in (self, i, block_i):
        """ Splits the block block_i, which contains the element i in two blocks. The i
        element will be in the first element of the second block """
        # careful here, what does this imply in the later update?
        if (i - self.__blocks[block_i].start < 1):
            return

        old_block = self.__blocks[block_i]
        first_block = Block (old_block.p, old_block.start, i)
        second_block = Block (old_block.p, i, old_block.end)
        self.__blocks[block_i:block_i + 1] = [first_block, second_block]


    def calculate_alpha (self, mid):
        """ Calculates alpha and beta where:
            alpha = P (i* <= mid) """
        alpha = 0   
        block_i = 0

        while (self.__blocks[block_i].end < mid):
            alpha += self.__blocks[block_i].mass ()
            block_i += 1

        block_start = self.__blocks[block_i].start
        alpha += self.__blocks[block_i].p * (mid - block_start + 1)
        return alpha


    def toString (self):
        s = ""
        for block in self.__blocks:
            s += "-| " + str (block.p) + ": " + str (block.start) + "-" + str (block.end) + " |-"
        return s


pmf = PMF (7)

# print ("before split: " + pmf.toString ())
# pmf.split_in (2, 0)
# print ("after split: " + pmf.toString ())

# print ("before update: " + pmf.toString ())
# pmf.update (4, -1, 0.7)
# pmf.update (2, 1, 0.7)
# print ("after update: " + pmf.toString ())