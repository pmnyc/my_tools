"""
Letter Combinations of a Phone Number

Given a digit string, return all possible letter combinations that the number could represent.
A mapping of digit to letters (just like on the telephone buttons) is given below.

Input:Digit string "23"
Output: ["ad", "ae", "af", "bd", "be", "bf", "cd", "ce", "cf"].
"""


import os, sys
import numpy as np


def combinationsof2strings(a,b):
    res = []
    for ii in a:
        for jj in b:
            res += [ii + jj]
    return list(set(res))

class Solution(object):
    def getAllCombinations(self,string_list, res):
        digit_letter = {"2":["a","b","c"],
                        "3":["d","e","f"],
                        "4":["g","h","i"],
                        "5":["j","k","l"],
                        "6":["m","n","o"],
                        "7":["p","q","r","s"],
                        "8":["t","u","v"],
                        "9":["w","x","y","z"]}
        # res = []
        if len(string_list) == 0:
            res = res
        elif len(string_list) == 1:
            res = digit_letter[string_list[0]]
        elif len(string_list) == 2:
            res = combinationsof2strings(digit_letter[string_list[0]], digit_letter[string_list[1]])
        else:
            digit1 = string_list[0]
            res_seq = self.getAllCombinations(string_list[1:], [])
            res_seq = combinationsof2strings(digit_letter[digit1],res_seq)
            res += res_seq
        return res
    
    def main(self, string):
        string_list = list(string)
        return self.getAllCombinations(string_list, [])

Solution().main("23")

        