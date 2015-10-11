"""
Given an array S of n integers, find three integers in S such that the sum is
closest to a given number, target. Return the sum of the three integers. You
may assume that each input would have exactly one solution.
    For example, given array S = {-1 2 1 -4}, and target = 1.
    The sum that is closest to the target is 2. (-1 + 2 + 1 = 2).
"""

import os, sys
import numpy as np 
from copy import copy

class Solution(object):
    def findTriplet(self, S, traget):
        diff_from_target = 3 * max(map(lambda x: abs(x), S)) + abs(target)
        for i in range(len(S)-2):
            for j in range(i+1, len(S)-1):
                for jj in range(j+1, len(S)):
                    triplet = [S[i],S[j],S[jj]]
                    diff_from_target_new = abs(sum(triplet) - target)
                    if diff_from_target_new < diff_from_target:
                        triplet_final = triplet

        print "The sum that is cloest to the target %s is %s. \
            The triplet is %s" %(str(target), str(sum(triplet_final)), str(tuple(triplet_final)))

if __name__ == '__main__':
    S=(-1, 2, 1, -4)
    target=1
    Solution().findTriplet(S,target)
