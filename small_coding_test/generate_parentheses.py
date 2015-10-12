"""
Generate Parentheses

Given n pairs of parentheses, write a function to generate all combinations of well-formed parentheses.
For example, given n = 3, a solution set is:
"((()))", "(()())", "(())()", "()(())", "()()()"

Lessons:
1) This can be done by using classical DFS methods (Depth-First Search)
"""

import os, sys
import numpy as np

class Solution(object):
    def createlist(self, n):
        cand = ''
        res = []
        return self.generateParen(n,n,cand,res)
        
    def generateParen(self, left, right, cand, res):
        # the idea is to start with 3 left ( and 3 right ), and remove one
            # by one until all of them are gone
        # left , right denote # of left right paraentathis
        # cand is the final result of one combination
        # Sample data:
            # left = n, right = n, cand = ''
            # res = [], the starting queue for storing results
        # the elementary idea of using recursion in the DFS is to put everything
             # in the statement and then initialize the first few senarios
        if left < 0 or right < 0:
            return 
        elif left * right == 0:
            if cand not in res:
                res.append(cand)
            return res
        else:
            self.generateParen(left-1, right-1, "("+cand+")", res)
            self.generateParen(left-1, right-1, "()"+cand, res)
            self.generateParen(left-1, right-1, cand+"()", res)
        return res


s = Solution()
print s.createlist(3)

