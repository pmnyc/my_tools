# -*- coding: utf-8 -*-
"""
Given an input string, reverse the string word by word.

For example,

Given s = "the sky is blue",
return "blue is sky the".
"""


def reverse(s):
    words = s.split(" ")
    length = len(words)
    index_reverse = map(lambda i: length-1-i, range(length))
    return " ".join(map(lambda i: words[i], index_reverse))

s = "the sky is blue"
reverse(s)
