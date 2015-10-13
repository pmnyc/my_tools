"""
Happy Number
Write an algorithm to determine if a number is "happy".

A happy number is a number defined by the following process:
    Starting with any positive integer, replace the number by the sum of the squares of its digits, 
    and repeat the process until the number equals 1 (where it will stay), 
    or it loops endlessly in a cycle which does not include 1. 
    Those numbers for which this process ends in 1 are happy numbers.

Example: 19 is a happy number


1^2 + 9^2 = 82
8^2 + 2^2 = 68
6^2 + 8^2 = 100
1^2 + 0^2 + 0^2 = 1
"""

import os, sys
import numpy as np


class Solution(object):
    def isHappyNum(self, n):
        if self.sumsqure(n) == 1:
            return True
        else:
            return False

    def sumsqure(self, n):
        # sum_ is the starting point, say sum_=10000
        digits = map(lambda x: int(x), list(str(n)))
        sum_ = sum(map(lambda x: x**2, digits))
        if sum_ >= 10:
            sum_ = self.sumsqure(sum_)
        return sum_

n = 19
Solution().isHappyNum(n)
