"""
Note: This is an extension of House Robber.

After robbing those houses on that street, the thief has found himself a new
place for his thievery so that he will not get too much attention. This time,
all houses at this place are arranged in a circle. That means the first house
is the neighbor of the last one. Meanwhile, the security system for these
houses remain the same as for those in the previous street.

Given a list of non-negative integers representing the amount of money of each
house, determine the maximum amount of money you can rob tonight without
alerting the police.

Lessons:
1) 
"""

import os, sys
import numpy as np 

def add_index_in_circle(i,step,n):
    # n is the last index in line
    # step = 1, -1 2, -2, etc.
    i += 100 * (n+1)
    return (i+step) % (n+1)

def queque0(houses):
    res = []
    n = len(houses)
    if n == 0:
        res = res
    elif n <=2:
        res = map(lambda x: [x], houses)
    else:
        for i, num in enumerate(houses):
            res_seq = queque0(houses[i+2:])
            res_seq = map(lambda x: [num] + x, res_seq)
            for s in res_seq:
                res.append(s)
    return res

def queque(houses):
    res = []
    n = len(houses)
    if n == 0:
        res = res
    elif n <= 3:
        res_seq = map(lambda x: [x], houses)
        res_seq = filter(lambda x: x not in res, res_seq)
        for s in res_seq:
            res.append(s)
    elif n == 4:
        res_seq = [[houses[0],houses[2]],[houses[1],houses[3]]]
        res_seq = filter(lambda x: x not in res, res_seq)
        for s in res_seq:
            res.append(s)
    else:
        for i, num in enumerate(houses):
            left_ = add_index_in_circle(i,2,n-1)
            right_ = add_index_in_circle(i,-2,n-1)
            if left_ <= right_:
                idx = range(left_, right_+1)
            else:
                idx = range(left_,n) + range(right_+1)
            res_seq = queque0(map(lambda i: houses[i],idx))
            res_seq = map(lambda x: [num] + x, res_seq)
            res_seq = filter(lambda x: x not in res, res_seq)
            for s in res_seq:
                res.append(s)
    return res

class Solution(object):
    def findMaxseq(self, houses):
        seq = queque(houses)
        max_value = 0
        max_seq = []
        for s in seq:
            if sum(s) > max_value:
                max_value = sum(s)
                max_seq = s
        return max_seq

houses = [4, 1, 6, 10, 5, 13, 2, 7]
Solution().findMaxseq(houses)


###### Solutions #2

class Solution(object):
    def rob(self, nums):
        """
        :type nums: List[int]
        :rtype: int
        """
        n = len(nums)
        if n == 0:
            return 0
        elif n == 1:
            return nums[0]
        return max(self.rob_aux(nums, 0), self.rob_aux(nums, 1))

    def rob_aux(self, nums, left):
        n = len(nums) - 1
        t = [0 for i in range(n + 1)]
        if n == 0:
            return t[n]
        t[1] = nums[left]
        if n <= 1:
            return t[n]
        t[2] = max(nums[left: left + 2])
        for i in range(3, n + 1):
            t[i] = max(t[i - 2] + nums[left + i - 1], t[i - 1])
        return t[n]

a1 = [1]
a2 = [4, 1, 6, 10, 5, 13, 2, 7]
s = Solution()
print(s.rob(a1))
print(s.rob(a2))

