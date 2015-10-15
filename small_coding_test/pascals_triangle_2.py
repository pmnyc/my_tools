"""
Given an index k, return the kth row of the Pascal's triangle.

For example, given k = 3,
Return [1,3,3,1].


[1,1,1,1,1],
[1,1,1,1,1],
[1,2,1,1,1],
[1,3,3,1,1],
[1,4,6,4,1],

Note:
Could you optimize your algorithm to use only O(k) extra space?
"""

def pascalLastrow(n):
    res = [[1 for i in range(n+1)] for j in range(n)]
    for i in range(n):
        if i > 0:
            prev = res[i-1]
            for j in range(1,i+1):
                res[i][j] = prev[j-1] + prev[j]
    return res[-1]


n = 4
pascalLastrow(n)