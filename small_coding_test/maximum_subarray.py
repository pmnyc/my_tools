# -*- coding: utf-8 -*-
"""
Find the contiguous subarray within an array (containing at least one number)
which has the largest sum.

For example, given the array [−2,1,−3,4,−1,2,1,−5,4],
the contiguous subarray [4,−1,2,1] has the largest sum = 6.
"""


def choose2fromn(n):
    queue = []
    for i in range(n-1):
        for j in range(i+1,n):
            queue.append([i,j])
    return queue

def findMatrSubarray(a):
    nodeindx = choose2fromn(len(a))
    max_sum= (-1) * sum(map(lambda x: abs(x), a)) -1 
    max_str = []
    for ii in nodeindx:
        sub_str = a[ii[0]:ii[1]+1]
        if sum(sub_str) > max_sum:
            max_sum = sum(sub_str)
            max_str = sub_str
    return max_sum, max_str

a = [ -2, 1, -3, 4, -1, 2, 1, -5, 4]
findMatrSubarray(a)

# solution#2

def findAllseq(candidates, cand=[], res=[]):
    if len(candidates) ==0:
        res = res
    elif len(candidates) ==1:
        if len(cand) >= 1:
            if cand not in res:
                res.append(cand)
        if cand+candidates not in res:
            res.append(cand+candidates)
    else:
        if len(cand) >= 1:
            if cand not in res:
                res.append(cand)
        for i, num in enumerate(candidates):
            if i == 0:
                res_seq_1 = findAllseq(candidates[i+1:], cand+[candidates[0]])
                for r in res_seq_1:
                    if r not in res:
                        res.append(r)
            else:
                res_seq_2 = findAllseq(candidates[i+1:])
                for r in res_seq_2:
                    if r not in res:
                        res.append(r)
    return res

def findMaxSum(a):
    max_sum= (-1) * sum(map(lambda x: abs(x), a)) -1 
    max_str = []
    que = findAllseq(a)
    for r in que:
        if sum(r) > max_sum:
            max_sum = sum(r)
            max_str = r
    return max_sum, max_str

findMaxSum(a)