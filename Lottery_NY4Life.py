"""
Year: 2014
@author: pm
@Lottery Type: Lottery_NY4Life
@Remark: Use Lucky Years to Create Sequences
"""

import numpy as np, random

class RandSeq:
    def __init__(self,range_upperbound=60,count=5,seed=None):
        self.range_upperbound = range_upperbound
        self.count = count
        self.seed = seed
        #print 'Sequence Upper Bound is', self.range_upperbound
        #print 'Sequence has', self.count, 'numbers ranging from 1 to',range_upperbound
    def createrange(self):
        rgn = range(self.range_upperbound + 1)
        rgn.pop(0)
        return rgn
        
    def generate_numofLoops(self):
        random.seed(None)
        loopnum1 = np.random.uniform(low=0.0, high=2012, size=10)
        random.seed(None)
        loopnum2 = np.random.uniform(low=0.0, high=1980, size=10)
        loopnum = int(np.ceil(np.min(loopnum1) + np.min(loopnum2)))
        #print 'There are',loopnum,'loops used for generation of random sequence'
        return loopnum
        
    def randomshuffle(self):
        random.seed(None)
        rgn = self.createrange()
        np.random.shuffle(rgn)
        random.seed(None)
        np.random.shuffle(rgn)
        idx = range(len(rgn))
        random.seed(None)
        np.random.shuffle(idx)
        rgn = [rgn[k] for k in idx]
        return rgn
        
    def generate_numbers(self):
        numLoops = self.generate_numofLoops()
        a = [None] * numLoops
        b = [None] * numLoops
        for i in range(numLoops):
            x = self.randomshuffle()
            b[i] = x[:self.count]
        return b

    def getnumwithleastcount(self,yy):
        z = np.array(np.array(zip(yy,map(yy.count,yy))))
        z2 = z[z[:,1]==np.min(z[:,1])].tolist()
        idx = range(len(z2))
        random.seed(None)
        np.random.shuffle(idx)
        idx = idx[0]
        z_final = z2[idx][0]
        return z_final
        
    def finalSeq(self):
        xx = self.generate_numbers()
        c = [None] * self.count
        for i in range(self.count):
            yy=[x[i] for x in xx]
            c[i] = self.getnumwithleastcount(yy)
        return c

x=RandSeq(60,5).finalSeq()
y=RandSeq(4,1).finalSeq()
print "*" * 50
print "Two Sequences are:",x," "*5, y
print "*" * 50
