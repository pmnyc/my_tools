"""
Merge Intervals

Given a collection of intervals, merge all overlapping intervals.

For example,

Given [1,3],[2,6],[8,10],[15,18],
return [1,6],[8,10],[15,18].

Lessons:
1) Sort intervals by their starting point and do the merges
2)  #sort list according to the start value    
        intervals.sort(key=lambda x:x.start)
"""


def areTwooverlap(a,b):
    # a = [1,3]
    # b = [2,6]
    #left_min = min(a[0],b[0])
    left_max = max(a[0],b[0])
    right_min = min(a[1],b[1])
    #right_max = max(a[1],b[1])
    if right_min >= left_max:
        return True
    else:
        return False

def overlap(a,b):
    # this returns a list of intervals
    if areTwooverlap(a,b):
        return [[min(a[0],b[0]), max(a[1],b[1])]]
    else:
        return [a,b]
    
class Solution(object):
    def merge(self, intervals):
        intervals.sort(key=lambda x: x[0])
        queue = [intervals[0]]
        n = len(intervals)
        for i in range(1,n):
            if len(queue) ==1:
                queue = overlap(queue[-1], intervals[i])
            else:
                queue = queue[:-1] + overlap(queue[-1], intervals[i])
        return queue


intervals = [[1,3],[2,6],[5,8],[8,10],[15,18]]
Solution().merge(intervals)

######## Solution #2

def areTwooverlap(a,b):
    # a = [1,3]
    # b = [2,6]
    #left_min = min(a[0],b[0])
    left_max = max(a[0],b[0])
    right_min = min(a[1],b[1])
    #right_max = max(a[1],b[1])
    if right_min >= left_max:
        return True
    else:
        return False

def overlap(a,b):
    # this returns a list of intervals
    if areTwooverlap(a,b):
        return [[min(a[0],b[0]), max(a[1],b[1])]]
    else:
        return [a,b]

def merge(candidates, cand=[], res=[]):
    # res is the list of lists(intervals)
    if len(candidates) == 0:
        res = res
    elif len(candidates) == 1:
        if len(cand) ==0:
            res = candidates
        else:
            res = cand[:-1] + overlap(cand[-1], candidates[0])
    else:
        if len(cand) == 0:
            cand_new = [candidates[0]]
            candidates_new = candidates[1:]
        else:
            cand_new = cand[:-1] + overlap(cand[-1], candidates[0])
            candidates_new = candidates[1:]
        res = merge(candidates_new, cand_new, [])
    return res

merge(intervals)