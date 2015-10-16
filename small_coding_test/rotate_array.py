"""
Rotate an array of n elements to the right by k steps.

For example, with n = 7 and k = 3, the array [1,2,3,4,5,6,7] is rotated to
[5,6,7,1,2,3,4].

Note:
Try to come up as many solutions as you can, there are at least 3 different
ways to solve this problem.
"""


def reverselastk(a, k):
    index = range(len(a))
    k = len(a) - k-1
    index_rev = index[k+1:] + index[:k+1]
    res = map(lambda i: a[i], index_rev)
    return res

a =  ['a','c','4','3','ea']
k = 3
reverselastk(a,k)
