from BitHash import BitHash
from BitVector import BitVector


class BloomFilter(object):
    # Return the estimated number of bits needed in a Bloom Filter that 
    # will store numKeys keys, using numHashes hash functions, and that 
    # will have a false positive rate of maxFalsePositive.
    # See Slide 12 for the math needed to do this.    
    def __bitsNeeded(self, numKeys, numHashes, maxFalsePositive):
        val = (1-(maxFalsePositive)**(1 / numHashes))
        bits = (numHashes / (1-(val)**(1 / numKeys)))
        return int(bits)
    
    # Create a Bloom Filter that will store numKeys keys, using 
    # numHashes hash functions, and that will have a false positive 
    # rate of maxFalsePositive.
    # All attributes must be private.
    def __init__(self, numKeys, numHashes, maxFalsePositive):
        # will need to use __bitsNeeded to figure out how big
        # of a BitVector will be needed
        self.__size = self.__bitsNeeded(numKeys, numHashes, maxFalsePositive)
        self.__numKeys = numKeys
        self.__numHashes = numHashes
        self.__maxFalse = maxFalsePositive
        self.__bitVec = BitVector(size = self.__size)
        self.__numBitsSet = 0
        
    
    # insert the specified key into the Bloom Filter.
    # Doesn't return anything, since an insert into 
    # a Bloom Filter always succeeds!
    def insert(self, key):
        seed = 0
        for i in range(self.__numHashes):
            rawHash = BitHash(key, seed)
            hashVal = rawHash % self.__size
            if self.__bitVec[hashVal] != 1:
                self.__bitVec[hashVal] = 1
                self.__numBitsSet += 1
            seed = rawHash
    
    # Returns True if key MAY have been inserted into the Bloom filter. 
    # Returns False if key definitely hasn't been inserted into the BF.   
    def find(self, key):
        seed = 0
        for i in range(self.__numHashes):
            rawHash = BitHash(key, seed)
            hashVal = rawHash % self.__size            
            if self.__bitVec[hashVal] == 0:
                return False
            seed = rawHash
        return True
       
    # Returns the PROJECTED current false positive rate based on the
    # ACTUAL current number of bits set in this Bloom Filter. 
    # This is NOT the same thing as trying to use the Bloom Filter and
    # actually measuring the proportion of false positives that 
    # are actually encountered.
    def falsePositiveRate(self):
        numBitsSet = self.numBitsSet()  # number of bits set to 1
        numBitsZero = self.__size - numBitsSet  # number of bits not set to 1
        prop = numBitsZero / self.__size  # find the proportion
        falsePositiveRate = (1 - prop) ** self.__numHashes
        return falsePositiveRate
       
    # Returns the current number of bits ACTUALLY set in this Bloom Filter
    # WHEN TESTING, MAKE SURE THAT YOUR IMPLEMENTATION DOES NOT CAUSE
    # THIS PARTICULAR METHOD TO RUN SLOWLY.
    def numBitsSet(self):
        return self.__numBitsSet

       

def __main():
    numKeys = 100000
    numHashes = 4
    maxFalse = .05
    
    # create the Bloom Filter
    b = BloomFilter(numKeys, numHashes, maxFalse)
    
    # read the first numKeys words from the file and insert them 
    # into the Bloom Filter. Close the input file.
    text = open("wordlist.txt")
    for i in range(numKeys):
        word = text.readline()
        b.insert(word)
    text.close()

    # Print out what the PROJECTED false positive rate should 
    # THEORETICALLY be based on the number of bits that ACTUALLY ended up being set
    # in the Bloom Filter. Use the falsePositiveRate method.
    print("Theoretical false positive rate", b.falsePositiveRate())

    # Now re-open the file, and re-read the same bunch of the first numKeys 
    # words from the file and count how many are missing from the Bloom Filter, 
    # printing out how many are missing. This should report that 0 words are 
    # missing from the Bloom Filter. Don't close the input file of words since
    # in the next step we want to read the next numKeys words from the file.
    text = open("wordlist.txt")
    missing = 0
    for i in range(numKeys):
        word = text.readline()
        found = b.find(word)
        if not found:
            missing += 1
    print("Missing", missing, "words from BF")

    # Now read the next numKeys words from the file, none of which 
    # have been inserted into the Bloom Filter, and count how many of the 
    # words can be (falsely) found in the Bloom Filter.
    foundWords = 0
    for i in range(numKeys):
        word = text.readline()
        found = b.find(word)
        if found:
            foundWords += 1
    print("Found", foundWords, "words in BF")
    
    # Print out the percentage rate of false positives.
    # THIS NUMBER MUST BE CLOSE TO THE ESTIMATED FALSE POSITIVE RATE ABOVE
    
    percentage  =foundWords/numKeys
    print("The actual false positive rate is ", percentage)

    
if __name__ == '__main__':
    __main()       

