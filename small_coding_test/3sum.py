"""
Given an array S of n integers, are there elements a, b, c in S such that a +
b + c = 0? Find all unique triplets in the array which gives the sum of zero.
Note:
Elements in a triplet (a,b,c) must be in non-descending order. (ie, a ≤ b ≤ c)
The solution set must not contain duplicate triplets.
    For example, given array S = {-1 0 1 2 -1 -4},
    A solution set is:
    (-1, 0, 1)
    (-1, -1, 2)
"""

import os, sys
import numpy as np 
from copy import copy

class Solution(object):
    @staticmethod
    def reordertriplet(x):
        #sample
        # x = (-1, 2, -1)
        x = list(x)
        x.sort()
        return tuple(x)

    def Solve(self, S):
        outs = []
        for i in range(len(S)-2):
            for j in range(i+1,len(S)-1):
                s_copy = copy(S)
                nums_ = (S[i],S[j])
                znum = (-1) * (sum(nums_))
                if znum in map(lambda jj: S[jj], range(i+2,len(S))):
                    output = self.reordertriplet([S[i],S[j],znum])
                    if output not in outs:
                        outs.append(output)
                        print "One triplet is %s" %str(output)

if __name__ == "__main__":
    import sys
    #S = sys.argv[1]
    S = (-1, 0, 1, 2, -1, -4)
    Solution().Solve(S)
