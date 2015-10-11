"""
Combination Sum

Given a set of candidate numbers (C) and a target number (T), find all unique combinations in C where the candidate numbers sums to T.
The same repeated number may be chosen from C unlimited number of times.
Note:
All numbers (including target) will be positive integers.
Elements in a combination (a1, a2, … , ak) must be in non-descending order. (ie, a1 ≤ a2 ≤ … ≤ ak).
The solution set must not contain duplicate combinations.
For example, given candidate set 2,3,6,7 and target 7,
A solution set is:
[7]
[2, 2, 3] 

Lessons:
1) Important to use cand[:] instead of cand when doing append to append the list
    without manipulaiton in place
2) The blank return "return " can break the loop and force it to move to next one
"""

import os, sys
import numpy as np 
from copy import copy

class Solution(object):
    def __init__(self, C,T):
        self.c = copy(C)
        self.c.sort(reverse=False) #default value, which is an ascending order
        self.t = T
        self.res = []
    
    def getlist(self):
        self.combineSum(self.c, [], self.t)

    def combineSum(self, candidates, cand, target):
        # target=7
        # candidate = [2]
        # result = []
        if target < 0:
            return
        elif target == 0:
            new = cand[:]
            new.sort()
            self.res.append(new)
        else:
            for i, num in enumerate(candidates):
                # cand is the starting point or list for contining
                cand += [num]
                print(str(cand), str(target))
                self.combineSum(candidates[i:], cand, target-num) #starting from i, not pevious numbers
                cand.pop() #when last number appended failed, which means target<0, then remove that number

#test
C = [2,3,6,7]
T = 7
x = Solution(C,T)
x.getlist()
x.res
