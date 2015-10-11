"""
Given an array of integers and an integer k, find out whether there are two
distinct indices i and j in the array such that nums[i] = nums[j] and the
difference between i and j is at most k.
"""

import os, sys
import numpy as np 

class Solution(object):
    def __init__(self, nums, k):
        self.nums = nums
        self.k = k 

    def matchwithink(self):
        blean = False
        for i, num in enumerate(self.nums):
            if i > len(self.nums)-2:
                break
            else:
                u_ = min(len(self.nums)-1,i+4)
                for j in range(i+1,u_):
                    if nums[i] == nums[j]:
                        #print(str(i),str(j))
                        blean = True
                        break
        return blean

##test
nums = [1,9,2,6,0,4,5,6,2,8]
k = 3

self = Solution(nums, k)
self.matchwithink()
