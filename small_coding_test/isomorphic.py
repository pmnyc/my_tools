"""
Given two strings s and t, determine if they are isomorphic.

Two strings are isomorphic if the characters in s can be replaced to get t.

All occurrences of a character must be replaced with another character while
preserving the order of characters. No two characters may map to the same
character but a character may map to itself.

For example,
Given "egg", "add", return true.

Given "foo", "bar", return false.

Given "paper", "title", return true.

Note:
You may assume both s and t have the same length.
"""


import os, sys
import numpy as np


class Solution(object):
    def isIsomorphic(self, s,t):
        if len(s) != len(t) or len(s) == 0 or len(t) == 0:
            res = False
        else:
            s_list = list(s)
            t_list = list(t)
            for i in range(len(s_list)):
                c = s_list[i]
                s = s.replace(c,t_list[i])
            if s == t:
                res = True
            else:
                res = False
        return res

    
# another trick is to use the dictionary to record the words that need to be replaced if replace function is not used

s="paper"
t="title"
Solution().isIsomorphic(s,t)
