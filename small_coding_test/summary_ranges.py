"""
Given a sorted integer array without duplicates, return the summary of its
ranges.

For example, given [0,1,2,4,5,7], return ["0->2","4->5","7"].
"""


def getIntervals(S):
    queue = []
    for i in range(len(S)):
        if len(queue)==0:
            start = 0
        else:
            start = queue[-1][1]+1
        if S[i] + 1 == S[min(i+1,len(S)-1)]:
            end = i+1
            continue
        else:
            end = i
        queue += [[start, end]]
    
    res = []
    for i in queue:
        if i[1] == i[0]:
            res += [str(S[i[0]])]
        else:
            res += [str(S[i[0]]) + "->" + str(S[i[1]])]
    return res

S = [0,1,2,4,5,7]
print getIntervals(S)
