"""
Related to question Excel Sheet Column Title
Given a column title as appear in an Excel sheet, return its corresponding
column number.
For example:
    A -> 1
    B -> 2
    C -> 3
    ...
    Z -> 26
    AA -> 27
    AB -> 28
    AZ -> 26 + 26 = 52
    BA -> 52 + 1 = 53
"""

import os, sys
import numpy as np 

class Solution(object):
    def getColumnum(self, x):
        offset = ord("A")-1
        x_lst = list(x)
        x_length = len(x_lst)
        colmn_num = 0
        for i in range(x_length):
            colmn_num += (26 ** (x_length-i-1)) * (ord(x_lst[i])-offset)
        return colmn_num

x = "BA"
Solution().getColumnum(x)
