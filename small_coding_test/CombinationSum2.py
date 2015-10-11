"""
Combination Sum II

Given a collection of candidate numbers (C) and a target number (T), find all unique combinations in C where the candidate numbers sums to T.
Each number in C may only be used once in the combination.
Note:
All numbers (including target) will be positive integers.
Elements in a combination (a1, a2, … , ak) must be in non-descending order. (ie, a1 ≤ a2 ≤ … ≤ ak).
The solution set must not contain duplicate combinations.
For example, given candidate set 10,1,2,7,6,1,5 and target 8,
A solution set is:
[1, 7]
[1, 2, 5]
[2, 6]
[1, 1, 6] 

"""

import os, sys
import numpy as np 


class Solution(object):
    def __init__(self, C,T):
        self.c = C[:]
        self.c = sorted(self.c)
        self.t = T
        self.res = []

    def getList(self):
        self.combineSum(self.c, [], self.t)

    def combineSum(self, candidates, cand, target):
        if target <0:
            return
        elif target == 0 and cand[:] not in self.res:
            self.res.append(cand[:])
        else:
            for i, num in enumerate(candidates):
                cand.append(num)
                print(str(cand), str(target))
                self.combineSum(candidates[i+1:],cand,target-num)
                cand.pop()


### test
C=[10,1,2,7,6,1,5]
T=8
self = Solution(C,T)
self.getList()
self.res
