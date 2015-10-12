"""
Edit Distance

Given two words word1 and word2, find the minimum number of steps required to convert word1 to word2. (each operation is counted as 1 step.)
You have the following 3 operations permitted on a word:

a) Insert a character
b) Delete a character
c) Replace a character

Lessons:
1) This is a typical DP (dynamic progrmaming) problem. It does not need recursion, which usually is quite computationally intensive
2) DP considers the neibors to find the relationship.


The optimal function is:  table[i+1][j+1] = min [table[i][j]+1 or 0 (+0 if word1[i+1]==word2[j+1], else +1),   table[i][j+1]+1, table[i+1][j]+1 ].

Initialization:
table[0][i] = i  i=1:|word1|          here 0 means "", any string convert to "" needs the length of string
table[j][0] = j  i=1:|word2|
table[0][0]=0    "" convert to  "" need 0 steps.
"""

import os, sys
import numpy as np 


class Solution(object):
    def minDistance(self,word1, word2):
        word1 = word1.lower()
        word2 = word2.lower()
        len_1 = len(word1)
        len_2 = len(word2)
        table = map(lambda x: [10**5] * len_2, range(len_1))
        if word1[0] == word2[0]:
            table[0][0] = 0
        else:
            table[0][0] = 1
        for j in range(len_2):
            table[0][j] = j + table[0][0]
        for i in range(len_1):
            table[i][0] = i + table[0][0]
        for i in range(1,len_1):
            for j in range(1,len_2):
                if word1[i] == word2[j]:
                    adder = 0
                else:
                    adder = 1
                
                table[i][j] = min(table[i-1][j-1]+adder,
                                table[i-1][j]+1,
                                table[i][j-1]+1)
        return table[len_1-1][len_2-1]


word1 = "Seattle"
word2 = "Seagle"
Solution().minDistance(word1, word2)
