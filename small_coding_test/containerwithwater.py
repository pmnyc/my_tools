"""
Container With Most Water

Given n non-negative integers a1, a2, ..., an, where each represents a 
    point at coordinate (i, ai). n vertical lines are drawn such that 
    the two endpoints of line i is at (i, ai) and (i, 0). Find two lines, 
    which together with x-axis forms a container, such that the container contains the most water.
Note: You may not slant the container.
"""

import os, sys
import numpy as np 


class Solution(object):
    def __init__(self,height):
        self.height = height
    def maxArea(self):
        max_area = 0
        for i in range(len(self.height)):
            for j in range(i+1,len(self.height)):
                area = (j-i) * min(self.height[i], self.height[j])
                max_area = max(max_area, area)
        return max_area
        
        

##
height = [1,4,2,4,5]
self = Solution(height)
self.maxArea()
