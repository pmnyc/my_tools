"""
Find the kth largest element in an unsorted array. Note that it is the kth
largest element in the sorted order, not the kth distinct element.

For example,
Given [3,2,1,5,6,4] and k = 2, return 5.

Note: You may assume k is always valid, 1 <= k <= array's length.
"""

import os, sys
import numpy as np

def getmax(A):
    max_ = max(A)
    for i, num in enumerate(A):
        if num == max_:
            break
    return (i, num)

class Solution(object):
    def findkthlargest(self, A, k):
        for i in range(k):
            j, num = getmax(A)
            A = A[:j] + A[j+1:]
        return num
    
A=[3,2,1,5,6,4]
Solution().findkthlargest(A,2)
