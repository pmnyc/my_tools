"""
Given an array of non-negative integers, you are initially positioned at the
first index of the array.

Each element in the array represents your maximum jump length at that
position.

Your goal is to reach the last index in the minimum number of jumps.
For example:

Given array A = [2,3,1,1,4]

The minimum number of jumps to reach the last index is 2. (Jump 1 step from
index 0 to 1, then 3 steps to the last index.)

"""

import os, sys
import numpy as np


def jumps(candidates, prefix, res):
    # res = [] it is a lis to list, and each element is the full result
    # prefix=[2]
    # candidates =[3,1,1,4]
    n = len(candidates)
    if n <= 1:
        if prefix not in res:
            res.append()
    elif n == 2:
        if candidates[0]>=1:
            if prefix+[1] not in res:
                res.append(prefix+[1])
    else:
        num = candidates[0]
        max_jump = min(num,n-1-0)
        for jump in range(1,max_jump+1):
            res_seq = jumps(candidates[jump:], prefix+[jump] ,res)
            res_seq = filter(lambda x: x not in res, res_seq)
            for r in res_seq:
                res.append(r)
    return res
           
class Solution(object):
    def minJumps(self, candidates):
        lists = jumps(candidates, [],[])
        return min(map(lambda x: len(x),lists))

A = [2,3,1,1,4]
jumps(A,[],[])
Solution().minJumps(A)

