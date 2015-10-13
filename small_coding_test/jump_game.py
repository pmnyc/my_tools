"""
Given an array of non-negative integers, you are initially positioned at the
first index of the array.

Each element in the array represents your maximum jump length at that
position.

Determine if you are able to reach the last index.

For example:
A = [2,3,1,1,4], return true.

A = [3,2,1,0,4], return false.

Lessons:
1) If the final output is boolean, better use res = True or False to start
    and use recursion.
"""

import os, sys
import numpy as np


class Solution(object):
    def isReachEnd(self, candidates, res):
        # candidates = A
        # res = False #list of list
        n = len(candidates)
        if n <= 1:
            res = True
        elif n == 2:
            res = (candidates[0] >=1)
        elif candidates[0] >= n-1:
            res = True
        else:
            for jump in range(1,candidates[0]+1):
                res = self.isReachEnd(candidates[jump:], res)
        return res


A = [2,3,1,1,4]
#A = [3,2,1,0,4]
Solution().isReachEnd(A,False)
