"""
Given a string of numbers and operators, return all possible results from
computing all the different possible ways to group numbers and operators. The
valid operators are +, - and *.


Example 1
Input: "2-1-1".

((2-1)-1) = 0
(2-(1-1)) = 2
Output: [0, 2]


Example 2
Input: "2*3-4*5"

(2*(3-(4*5))) = -34
((2*3)-(4*5)) = -14
((2*(3-4))*5) = -10
(2*((3-4)*5)) = -10
(((2*3)-4)*5) = 10
Output: [-34, -14, -10, -10, 10]

Lessons:
1) Recursion deals with unknown number of loops and scenarios. The inital values are like math induction

"""

import os, sys
import numpy as np 


class Solution(object):
    def __init__(self):
        self.res = []

    def calculate(self, string):
        print("The %s = %s" %(string, str(eval(string))))
        return eval(string)
    
    def calDiffforms(self, inp):
        res = self.getDiffForms(inp)
        for s in res:
            self.calculate(s)

    def getDiffForms(self, inp):
        operators = set(["+","-","*"])
        if inp is None:
            res = []
        elif inp.isdigit() or inp=="(" or inp==")" :
            res = [inp]
        else:
            res = []
            for i, s in enumerate(inp): #the trick is to find the operator, and make splits
                if s in operators:
                    left = self.getDiffForms(inp[:i]) #list
                    right = self.getDiffForms(inp[i+1:]) #list
                    for l in left:
                        for r in right:
                            string = "(" + l + ")" + s + "("+r+")"
                            res.append(string)
                else:
                    continue
        return res



s=Solution()
s1 = '2*3-4*5'
s2 = '11*2-3+111'
print(s.calDiffforms(s1))
print(s.calDiffforms(s2))
