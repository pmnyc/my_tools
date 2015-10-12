"""
leetcode Question 27: Distinct Subsequences
Distinct Subsequences

Given a string S and a string T, count the number of distinct subsequences of T in S.

A subsequence of a string is a new string which is formed from the original string by deleting some (can be none) of the characters without disturbing the relative positions of the remaining characters. (ie, "ACE" is a subsequence of "ABCDE"while "AEC" is not).
Here is an example:

S = "rabbbit", T = "rabbit"
Return 3.

Lessons:
1) Try not use to .remove in the recursion that can modify even the original input values

"""


def numDistinct(S, T):
    if len(S) < len(T):
        return 0
    n = len(S)
    m = len(T)
    t = [0 for i in range(m + 1)]
    t[0] = 1
    for i in range(1, n + 1):
        # j = m ... 1
        for k in range(m):
            j = m - k
            if S[i - 1] == T[j - 1]:
                t[j] += t[j - 1]
    return t[m]

numDistinct(S,T)


def subseq(s_interval, k):
    if k < 1:
        return
    elif k == 1:
        queque = map(lambda x: [x], s_interval)
        return queque
    else:
        queque = []
        for i, num in enumerate(s_interval):
            singlelist = [num]
            for sub in subseq(s_interval[i+1:] , k-1):
                new_ = singlelist+sub
                new_.sort()
                if new_ not in queque:
                    queque.append(new_)
    return queque

class Solution(object):
    def countSubsequence(self, S,T):
        s_length = len(S)
        t_length = len(T)
        S = S.lower()
        T = T.lower()
        s_interval = range(s_length)
        counter = 0
        for idx in subseq(s_interval, t_length):
            S_ = map(lambda i: S[i], idx)
            S_ = "".join(S_)
            if S_ == T:
                counter += 1
        return counter


S = "raaabbbiirit"
T = "rabbit"
Solution().countSubsequence(S,T)

