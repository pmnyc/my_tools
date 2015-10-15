"""
Reverse a singly linked list.

click to show more hints.

Hint:
A linked list can be reversed either iteratively or recursively. Could you
implement both?
"""

# Definition for singly-linked list.
class ListNode(object):
    def __init__(self,x):
        self.val = x
        self.next = None

class Solution(object):
    def reverseList(self, head):
        if head is None:
            return None
        else:
            # res is the final solution of reversed linked list
            # to use the recursion, we may need to apply the function
                # to the next object in the linked list
            
            # head is head node n1 for 1-->2-->3-->4
            res = self.reverseList(head.next)
            # res is now head n4 for 4-->3-->2
            # loop through a linked list using "while linkedlist"
                # and redefine the next movement
            r = res
            if r is None:
                return head # this is for case when only 1 element in linked list
            while r and r.next is not None:
                r = r.next
            # this is only to move pointer r to the very last of res, which is at 2
            r.next = head
            r.next.next = None
            # this r construction builds the last bridge between 4-->3-->2 to 
                # 4-->3-->2-->1
            return res


n1 = ListNode(1)
n2 = ListNode(2)
n3 = ListNode(3)
n4 = ListNode(4)
n5 = ListNode(5)
n1.next = n2
n2.next = n3
n3.next = n4
n4.next = n5
s = Solution()
r1 = s.reverseList(n1)
print r1.val
print r1.next.val
print r1.next.next.val
