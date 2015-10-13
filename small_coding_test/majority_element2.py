"""
Given an integer array of size n, find all elements that appear more than ⌊
n/3 ⌋ times. The algorithm should run in linear time and in O(1) space.
"""


def findMajority(a):
    dic = {}
    queue=[]
    for x in a:
        if dic.has_key(x):
            dic[x] += 1
        else:
            dic[x] = 1
        if dic[x] > len(a)/3 and x not in queue:
            queue.append(x)
    return queue
        
