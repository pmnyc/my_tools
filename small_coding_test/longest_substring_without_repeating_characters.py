"""
Longest Substring Without Repeating Characters

Given a string, find the length of the longest substring without repeating characters. 
    For example, the longest substring without repeating letters for "abcabcbb" is "abc", 
    which the length is 3. For "bbbbb" the longest substring is "b", with the length of 1.
"""


def isReapeat(x):
    #x = "aba"
    x_list = list(x)
    if len(x_list) != len(list(set(x_list))):
        res = True
    else:
        res = False
    return res

class Solution(object):
    def getLongestNonRepeat(self, a):
        length = len(a)
        queue = []
        for i in range(length-1):
            for j in range(1,length):
                sub_str = a[i:j+1]
                if not(isReapeat(sub_str)) and sub_str not in queue:
                    queue.append(sub_str)
        max_length = 0
        max_str = ""
        for c in queue:
            if len(c) > max_length:
                max_length = len(c)
                max_str = c
        return max_length, max_str

a = "abcabcbb"
Solution().getLongestNonRepeat(a)
