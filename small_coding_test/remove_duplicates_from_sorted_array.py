"""
Remove Duplicates from Sorted List

Given a sorted linked list, delete all elements with duplicates
For example,
Given 1->1->2, return 2.
Given 1->1->2->3->3, return 2.

"""

def removeDuplicates(a):
    n = len(a)
    if n <=1:
        pass
    else:
        i = 0
        back_step = 0
        while i < n-1:
            ii = i - back_step
            if ii >= 0:
                if a[ii] == a[ii+1]:
                    del a[ii:ii+2]
                    back_step += 2
                    i += 2
                else:
                    i += 1
    return a

a = [1,1,2,3,3]
