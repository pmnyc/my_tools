"""
Description:
Count the number of prime numbers less than a non-negative number, n.

Lesson:
1) When return the last funciton's result, make sure, still put return getprime(n-1)
2) When seeing there is blank or NoneType called in the recursion in the error message
    make susure to check if the result return from the previous loop always results in 
    a return.
"""

import os, sys
import numpy as np 

# This is to set the upper limit of the recursion times
sys.setrecursionlimit(5000)

class Solution(object):
    def __init__(self):
        self.out = {}
    
    def getprime(self, n):
        if n < 3:
            print("Not prime numbers less than %s" %str(n))
        if n == 3:
            self.out[n] = [2, 3]
        else:
            que=[]
            if n-1 in self.out.keys():
                chelist = self.out[n-1]
            else:
                self.getprime(n-1)
                chelist = self.out[n-1]
            for i in chelist:
                if n % i == 0:
                    que.append(i)
                    break
            if len(que) == 0:
                self.out[n] = chelist + [n]
            else:
                self.out[n] = chelist

    def listprime(self, n):
        out = self.getprime(n)
        out = self.out[n]
        if n in out:
            out.remove(n)
        return out


Solution().listprime(4000)
