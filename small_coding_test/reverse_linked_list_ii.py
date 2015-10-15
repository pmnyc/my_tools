"""
Reverse Linked List II

Reverse a linked list from position m to n. Do it in-place and in one-pass.
For example:
Given 1->2->3->4->5->NULL, m = 2 and n = 4,
return 1->4->3->2->5->NULL.

Lessons:
1) findNode(r,n) function returns the first if n<0, but if n is out of range, then return None
"""

class ListNode:
    def __init__(self, x):
        self.val = x
        self.next = None


def linkedlinklength(head):
    # this is to return the length of the linked list given the head
    cnt = 1
    r = head
    while r and r.next is not None:
        r = r.next
        cnt += 1
    return cnt

def findNode(head, n):
    # this is for getting the n-th element in the linkedlist given the head
    if head is None:
        return None
    if n <= 1:
        return head
    elif n > linkedlinklength(head):
        return None
    else:
        cnt = 1
        r = head
        while r and cnt <n:
            if r.next is not None:
                r = r.next
                cnt += 1
            else:
                cnt += 1
        return r

class Solution(object):
    def reverseList(self, head, m, n):
        if head is None or m>n:
            return None
        elif m == n:
            return head
        elif m ==1 and n ==2:
            r = head
            node2 = findNode(r, 2)
            node3 = findNode(r, 3)
            r.next = node3
            node2.next = r
            return node2
        elif n-m == 1:
            r = head
            n_node = findNode(r, n)
            m_node = findNode(r, m)
            m_minus1_node = findNode(r, m-1)
            n_add1_node = findNode(r, n+1)
            n_node.next = m_node
            m_node.next = n_add1_node
            m_minus1_node.next = n_node
            return head
        else:
            res = self.reverseList(head, m+1, n)
            r = res
            if r is None:
                return head
            if m == 1:
                node2 = findNode(r,2)
                n_node = findNode(r,n)
                n_add1_node = findNode(r,n+1)
                n_node.next = r
                r.next = n_add1_node
                return node2
            else:
                m_minus1_node = findNode(r, m-1)
                m_node = findNode(r, m)
                m_add1_node = findNode(r, m+1)
                n_node = findNode(r, n)
                n_add1_node = findNode(r, n+1)
                m_minus1_node.next = m_add1_node
                n_node.next = m_node
                m_node.next = n_add1_node
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
r1 = s.reverseList(n1,1,4)
print r1.val
print r1.next.val
print r1.next.next.val
print r1.next.next.next.val
print r1.next.next.next.next.val

