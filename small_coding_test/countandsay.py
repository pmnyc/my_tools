"""
The count-and-say sequence is the sequence of integers beginning as follows:
1, 11, 21, 1211, 111221, ...
1 is read off as "one 1" or 11.
11 is read off as "two 1s" or 21.
21 is read off as "one 2, then one 1" or 1211.
Given an integer n, generate the nth sequence.
Note: The sequence of integers will be represented as a string.
"""

import os, sys
import numpy as np 
        

class Solution(object):
    def readcurrentstring(self, x):
        x2=list(x)
        node = [0]
        cnt = [1]
        for i in range(1,len(x2)):
            if x2[i] == x2[i-1]:
                cnt[max(node)] += 1
            else:
                node.append(i)
                cnt += [1]
        
        out=""
        for i in range(len(node)):
            out += str(cnt[i])+str(x2[node[i]])
        return out
    
    def countAndSay(self, n):
        if n == 1:
            out ="1"
        else:
            out = self.readcurrentstring(self.countAndSay(n-1))
        return out


s = Solution()
print s.countAndSay(1)
print s.countAndSay(2)
print s.countAndSay(3)
print s.countAndSay(4)
print s.countAndSay(5)