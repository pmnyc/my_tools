"""
Minimum Window Substring

Given a string S and a string T, find the minimum window in S which will contain all the characters in T in complexity O(n).

For example,
S = "ADOBECODEBANC"
T = "ABC"
Minimum window is "BANC".
"""

def miniWindow(S,T):
    n_s = len(S)
    n_t = len(T)
    queue = []
    for i in range(n_s - n_t + 1):
        for j in range(i + n_t-1,n_s):
            queue.append([i,j])
            
    min_window_size = n_s+1
    min_window = ""
    for q in queue:
        s_sub = S[q[0]:q[1]+1]
        if len(filter(lambda x: x in s_sub, list(T))) == len(T):
            if len(s_sub) < min_window_size:
                min_window_size = len(s_sub)
                min_window = s_sub
    return min_window_size, min_window

S = "ADOBECODEBANC"
T = "ABC"
miniWindow(S,T)
