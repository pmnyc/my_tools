"""
You are a professional robber planning to rob houses along a street. Each
house has a certain amount of money stashed, the only constraint stopping you
from robbing each of them is that adjacent houses have security system
connected and it will automatically contact the police if two adjacent houses
were broken into on the same night.

Given a list of non-negative integers representing the amount of money of each
house, determine the maximum amount of money you can rob tonight without
alerting the police.

This problem is the basic DP problem.
The description can be easily extracted as the following:

1) Given an array of non-negative integers, find the maximum sum of a subset
2) such that no element is adjacent to the other.


"""

import os, sys
import numpy

    
def queues(houses):
    #smaple
    res = []
    # start = 0
    n_houses = len(houses)
    if n_houses ==0:
        res = res
    elif n_houses <=2:
        res_sequences = map(lambda x: [x], houses)
        res_sequences = filter(lambda x: x not in res, res_sequences)
        for s in res_sequences:
            res.append(s)
    else:
        for i, num in enumerate(houses):
            if i +2 > n_houses -1:
                continue
            else:
                res_sequences = queues(houses[i+2:])
                res_sequences = map(lambda x: [num]+x, res_sequences)
                res_sequences = filter(lambda x: x not in res, res_sequences)
                for s in res_sequences:
                    res.append(s)
    return res

class Solution(object):
    def findMaxvalue(self, houses):
        list_= queues(houses)
        max_value = 0
        max_queue = []
        for s in list_:
            if sum(s) > max_value:
                max_value = sum(s)
                max_queue = s
            else:
                continue
        return max_queue

houses = [4, 2, 1, 5, 8, 10, 5]
Solution().findMaxvalue(houses)


## Solution #2 ##s
# DP transition function
# S[i] = max(S[i-2], S[i-3]) + A[i]
#  where A is the list of house values, the S[i] is the max value up to ith-house

class Solution:
    # @param {integer[]} nums
    # @return {integer}
    def rob(self, nums):
        n = len(nums)
        if n==0:
            return 0;
        if n == 1:
            return nums[0]
        s = [0]*(n+1)
        s[1] = nums[0]
        for i in range(2,n+1):
            s[i] = nums[i-1]
         
        for i in range(3,n+1):
            s[i] = max(max(s[i-3:i]), s[i]+max(s[i-3:i-1]))
        return max(s[n],s[n-1])

