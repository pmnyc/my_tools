"""
Given an array of strings, group anagrams together.

For example, given: ["eat", "tea", "tan", "ate", "nat", "bat"], Return:
[
  ["ate", "eat","tea"],
  ["nat","tan"],
  ["bat"]
]

Note:
For the return value, each inner list's elements must follow the lexicographic
order.

All inputs will be in lower-case.
"""

import os, sys
import numpy as np 


def compare(cand1, cand2):
    if len(cand1) == 0 or len(cand2) == 0:
        return False
    else:
        cand1_ = list(cand1)
        cand1_.sort()
        cand2_ = list(cand2)
        cand2_.sort()
        return cand1_ == cand2_

def group(cand, res):
    # this is for scanning the res queue and see if cand is one of them
        # if not, then create new list for this cand
    if len(res) == 0:
        res.append([cand])
    else:
        res_copy =res[:]
        add_counter = 0
        for i in range(len(res_copy)):
            if compare(cand, res_copy[i][0]):
                add_counter += 1
                if cand not in res_copy[i][0]:
                    res[i].append(cand)
        if add_counter == 0:
            res.append([cand])
    return res

class Solution(object):
    def createAnagrams(self, words):
        res = []    
        for word in words:
            res = group(word, res)
        return res

words = ["eat", "tea", "tan", "ate", "nat", "bat"]
s = Solution()
s.createAnagrams(words)
