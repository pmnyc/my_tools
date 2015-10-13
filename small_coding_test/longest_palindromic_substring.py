"""
Longest Palindromic Substring
Given a string S, find the longest palindromic substring in S. 
    You may assume that the maximum length of S is 1000, 
    and there exists one unique longest palindromic substring.
"""

def isPalingdrom(x):
    # x = "abba"
    x = x.replace(" ","")
    len_ = len(x)
    if len_ <=1:
        res = False
    else:
        idx = range(len_)
        idx_reverse = map(lambda x: len_-1-x, idx)
        res = True
        for i in idx:
            if x[idx[i]] != x[idx_reverse[i]]:
                res = False
                break
    return res

class Solution(object):
    def longestPalindrome(self, a):
        queue = []
        for i in range(len(a)-1):
            for j in range(1+i, len(a)):
                if isPalingdrom(a[i:j+1]):
                    if a[i:j+1] not in queue:
                        queue.append(a[i:j+1])
        max_length = 0
        max_string = ""
        for q in queue:
            if len(q) > max_length:
                max_length = len(q)
                max_string = q
        return max_length, max_string


a = 'akaa2baakcbbc'
s = Solution()
s.longestPalindrome(a)
