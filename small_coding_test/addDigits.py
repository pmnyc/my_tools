"""
Given a non-negative integer num, repeatedly add all its digits until the
result has only one digit.
For example:
Given num = 38, the process is like: 3 + 8 = 11, 1 + 1 = 2. Since 2 has only
one digit, return it.
Follow up:
Could you do it without any loop/recursion in O(1) runtime?

Lessons:
1) The trick is to use recursion
"""

import os, sys
import numpy as np 

class Solution(object):
    def sumUp(self,num):
        num_ = str(num)
        num_list = list(num_)
        sum_ = sum(map(lambda x: int(x),num_list))
        # this is for getting single digit
        if len(str(sum_)) > 1:
            sum_ = self.sumUp(sum_)
        else:
            print("Final single digit is %s" %str(sum_))
        return sum_

if __name__ == "__main__":
    num = 38
    Solution().sumUp(num)
