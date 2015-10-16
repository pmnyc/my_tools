# -*- coding: utf-8 -*-
"""
Test Justification

Given an array of words and a length L, format the text such that each line has exactly L characters and is fully (left and right) justified.
You should pack your words in a greedy approach; that is, pack as many words as you can in each line. Pad extra spaces ' ' when necessary so that each line has exactly L characters.
Extra spaces between words should be distributed as evenly as possible. If the number of spaces on a line do not divide evenly between words, the empty slots on the left will be assigned more spaces than the slots on the right.
For the last line of text, it should be left justified and no extra space is inserted between words.
For example,

words: ["This", "is", "an", "example", "of", "text", "justification."]
L: 16.

Return the formatted lines as:
[
   "This    is    an",
   "example  of text",
   "justification.  "
]
Note: Each word is guaranteed not to exceed L in length.
Corner Cases:
A line other than the last line might contain only one word. What should you do in this case?
In this case, that line should be left-justified.

"""

import math

def textlength(words, n):
    # get the length of n words if they are combined
    w = words[:n]
    sentence = " ".join(w)
    return len(sentence)

def firstrow(words, L):
    # This is to get the first row of words given the limit of L characters
    w_lens = map(lambda x: len(x), words)
    j = 1
    for i in range(1, len(w_lens)):
        new_lengths = map(lambda x: x+1, w_lens[:i]) + [w_lens[i]]
        if sum(new_lengths) >= L:
            j = i-1
            break
        else:
            j = i
    res = words[:j+1]
    return res

def getWords(x, L):
    """
    This will need more refined modification
    """
    # x=['a','b']
    if len(x) == 1:
        return x[0]
    length_1 = textlength(x,len(x))
    left_length = L - length_1
    space_insert = int(math.ceil(left_length /(len(x)-1)))
    word = " ".join(x)
    word = word.replace(" "," "*(space_insert+1))
    res = word
    while len(res) > L:
        res = res[:res.index(" ")] + res[res.index(" ")+1:]
    return res

def getFullText(candidates, cand, L, res=[]):
    # candidates=["text",'justfify']
    # cand = ["this","is"]
    if len(candidates) == 0:
        res = res
    elif firstrow(candidates, L) == candidates:
        res += [getWords(candidates, L)]
    else:
        row_words = firstrow(candidates, L)
        start= [getWords(row_words, L)]
        cand_new = cand + row_words
        candidates_new = candidates[len(row_words):]
        res_new = getFullText(candidates_new, cand_new, L, start)
        res += res_new
    return res
        
    
words = "Extra spaces between words should be distributed as evenly as possible. If the number of spaces on a line do not divide evenly between words, the empty slots on the left will be assigned more spaces than the slots on the right."
words = words.split()
L=32
x = getFullText(words, [], L)
