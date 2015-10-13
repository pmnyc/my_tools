"""
Longest Consecutive Sequence

Given an unsorted array of integers, find the length of the longest consecutive elements sequence.

For example,
Given [100, 4, 200, 1, 3, 2],

The longest consecutive elements sequence is [1, 2, 3, 4]. Return its length: 4.
Your algorithm should run in O(n) complexity.

Lessons:
1) Write on paper for design first!!!!
2) Define the initial res on the function argument, and when it is called recursively
    inside the function, set res to be blank in that part
3) candidates and cand are usually mutually exclusive

4) Dictionary.has_key(key) is to check whether the key exists in the dictionary or not
"""


"""
class Solution(object):
   def findLongestConSeq(seq)
"""

def findLongestConSeq(candidates, cand, res):
    # res = [] list of lists
    # cand = []
    # candidates = seq
    for c in candidates:
        if [c] not in res:
            res.append([c])
    if sorted(cand) not in res and len(cand) >= 1:
        res.append(sorted(cand))
        
    seq_length = len(candidates)
    if seq_length == 0:
        res = res
    elif seq_length == 1:
        num = candidates[0]
        queue = cand[:]
        if (num + 1 in queue) or (num - 1 in queue) or len(queue) == 0:
            queue += candidates
            if sorted(queue) not in res:
                res.append(sorted(queue))
    else:
        for i, num in enumerate(candidates):
            queue = cand[:]
            if (num+1 in queue) or (num-1 in queue) or len(queue) == 0:
                queue += [num]
            candidates_new = candidates[:i] + candidates[i+1:]
            res_seq = findLongestConSeq(candidates_new, queue, [])
            for r in res_seq:
                if sorted(r) not in res:
                    res.append(sorted(r))
            else:
                continue
    return res

def getLongest(seq):
    res = findLongestConSeq(seq, [],[])
    max_value = 0
    max_queue = []
    for r in res:
        if len(r) > max_value:
            max_value = len(r)
            max_queue = r
    return max_value, max_queue

seq = [100, 4, 200, 1, 3, 2]
getLongest(seq)


#### Solutins #2
def longestConsecutive(num):
    dic = {}
    maxlen = 1
    for n in num:
        dic[n] = 1
    for n in num:
        if dic.has_key(n):
            tmp = n + 1
            l = 1
            while dic.has_key(tmp):
                l+=1
                del dic[tmp]
                tmp+=1
            tmp = n - 1
            while dic.has_key(tmp):
                l+=1
                del dic[tmp]
                tmp-=1
            maxlen = max(l, maxlen)
        else:
            continue
    return maxlen

## Solution #3

def longestConsecutive(num):
    dic = {}
    for n in num:
        dic[n] = [n]
    for n in num:
        if dic.has_key(n):
            tmp = n + 1
            while dic.has_key(tmp):
                if [tmp] not in dic[n]:
                    dic[n] += [tmp]
                del dic[tmp]
                tmp+=1
                
            tmp = n - 1
            while dic.has_key(tmp):
                if [tmp] not in dic[n]:
                    dic[n] += [tmp]
                del dic[tmp]
                tmp-=1
        else:
            continue
    return dic

seq = [100, 4, 200, 1, 3, 2]
longestConsecutive(seq)
