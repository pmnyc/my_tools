"""
Given an array of size n, find the majority element. The majority element is
the element that appears more than ⌊ n/2 ⌋ times.

You may assume that the array is non-empty and the majority element always
exist in the array.
"""


def defmajorityElement(a):
    dic = {}
    for x in a:
        if dic.has_key(x):
            dic[x] += 1
        else:
            dic[x] = 1
        if dic[x] > len(a)/2:
            return x
            break #jump out of cycle

