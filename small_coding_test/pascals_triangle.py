"""
Given numRows, generate the first numRows of Pascal's triangle.

For example, given numRows = 5,
Return

[
     [1],
    [1,1],
   [1,2,1],
  [1,3,3,1],
 [1,4,6,4,1]
]

Lessons:
1) For simple problem without DP (dynamic programming), we can use recursion
    direclty. When involving DP, better have the framework like
    function(candidates, cand, res=[])
"""

def pascalTriagle(n, memorization={}, res=[]):
    if n < 1:
        res = res #blank
    elif n ==1:
        res= [[1]]
        memorization[n] = res
    elif n ==2:
        res = [[1],[1,1]]
        memorization[n] = res
    else:
        curr_queue = [1]
        if memorization.has_key(n-1):
            prev = memorization[n-1]
        else:
            prev = pascalTriagle(n-1,memorization, res)
        for ii in range(len(prev[-1])-1):
            curr_queue += [prev[-1][ii] + prev[-1][ii+1]]
        curr_queue += [1]
        res = prev + [curr_queue]
        memorization[n] = res
    return res

n=4
pascalTriagle(5)
