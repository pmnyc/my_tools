
"""
You are climbing a stair case. It takes n steps to reach to the top.
Each time you can either climb 1 or 2 steps. In how many distinct ways can you
climb to the top?

Lesson:
1) Use recursion. Here, if we store the queue in the memory, the speed is significantly faster
    as what the self.y shows below.
"""

import os, sys
import numpy as np 

class Solution(object):
    def __init__(self):
        self.y = {}
    
    def calSteps(self, n):
        n = int(n)
        if n < 1:
            raise Exception("You need to have at least 1 stair")
        elif n == 1:
            self.y[n] = 1
        elif n == 2:
            self.y[n] = 3
        else:
            if n-1 in self.y.keys(): #check the queque first before running full recursion
                a = self.y[n-1]
            else:
                a = self.calSteps(n-1)[n-1]
            if n-2 in self.y.keys(): #check the queque again if this component is part of recursion
                b = self.y[n-2]
            else:
                b = self.calSteps(n-2)[n-2]
            self.y[n] = a+b
        return self.y

if __name__ == "__main__":
    n =800
    print("There are %s of steps" %str(Solution().calSteps(n)[n]))
