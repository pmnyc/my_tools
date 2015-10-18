"""
Triangle:

Given a triangle, find the minimum path sum from top to bottom. Each step you may move to adjacent numbers on the row below.
For example, given the following triangle
[
     [2],
    [3,4],
   [6,5,7],
  [4,1,8,3]
]
The minimum path sum from top to bottom is 11 (i.e., 2 + 3 + 5 + 1 = 11).
"""


triangle = [
     [2],
    [3,4],
   [6,5,7],
  [4,1,8,3]
]



def minimumTotal(triangle, cand, res=[]):
    # minitotal = minum sum
    # res = [[[0,0],[1,0]]] the numbers, of [[[]]]
    # cand = [[0,0],[1,0]], from top to bottom
    if len(cand) == len(triangle):
        return
    elif len(cand) == len(triangle) -1:
        prev = cand[-1]
        if triangle[prev[0]+1][prev[1]] < triangle[prev[0]+1][prev[1]+1]:
            res_ = cand + [[prev[0]+1,prev[1]]]
            if res_ not in res:
                res.append(res_)
            #minitotal = sum(map(lambda idx: triangle[idx[0]][idx[1]], res_))
        else:
            res_ = cand + [[prev[0]+1,prev[1]+1]]
            if res_ not in res:
                res.append(res_)
            #minitotal = sum(map(lambda idx: triangle[idx[0]][idx[1]], res_))
    else:
        if len(cand) ==0:
            prev=[-1,0]
        else:
            prev = cand[-1]
        for j, num in enumerate(triangle[len(cand)]):
            if j not in range(prev[1],prev[1]+2):
                continue
            else:
                cand_new = cand + [[prev[0]+1,j]]
                res_seq = minimumTotal(triangle, cand_new, res)
                for r in res_seq:
                    if r not in res:
                        res.append(r)
    return res


paths = minimumTotal(triangle, cand=[], res=[])
minitotal = sum(map(lambda i: max(triangle[i]),range(len(triangle))))
for p in paths:
    total = sum(map(lambda idx: triangle[idx[0]][idx[1]], p))
    if total < minitotal:
        minitotal = total
        minipath = map(lambda i: triangle[i[0]][i[1]], p)
