"""
Given an array and a value, remove all instances of that value in place and
return the new length.

The order of elements can be changed. It doesn't matter what you leave beyond
the new length.
"""

def removeElement(a, val):
    n = len(a)
    i = 0
    back_step = 0
    while i <= n-1:
        if a[i-back_step] == val:
            del a[i-back_step]
            back_step += 1
        i += 1
    return a

a = [ 1, 2, 3, 4, 5, 3, 6, 7]
removeElement(a, 1)
