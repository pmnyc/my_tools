"""
Given n non-negative integers representing the histogram's bar height where the width of each bar is 1, 
    find the area of largest rectangle in the histogram.

Above is a histogram where width of each bar is 1, given height = [2,1,5,6,2,3].

The largest rectangle is shown in the shaded area, which has area = 10 unit.

For example,
Given height = [2,1,5,6,2,3],
return 10.
"""

import os, sys
import numpy as np


def choosek(index, k, res):
    # res = [] is the list of list
    if len(index) == 0 or len(index) < k:
        res = res
    elif k==1:
        res = map(lambda x: [x], index)
    else:
        for i, num in enumerate(index):
            res_more = choosek(index[:i]+index[i+1:], k-1, []) #tricky part, needs to use [] for case not matching it
            res_more = map(lambda x: sorted([num] + x), res_more)
            res_more = filter(lambda x: x not in res, res_more)
            for r in res_more:
                if r not in res:
                    res.append(r)
    return res


def getArea(A, index):
    length = max(index) - min(index) + 1
    min_height = min(map(lambda i: A[i],index))
    area = min_height * length
    return area

class Solution(object):
    def getMaxArea(self,A):
        index = range(len(A))
        max_area = 0
        max_index = []
        for k in range(2,len(A)+1):
            list_index = choosek(index, k, res=[])
            for idx in list_index:
                if getArea(A, idx) > max_area:
                    max_area = getArea(A, idx)
                    max_index = idx
        return max_area, max_index
    

A = [2,1,5,6,2,3]
Solution().getMaxArea(A)

