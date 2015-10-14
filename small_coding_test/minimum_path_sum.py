"""
Given a m x n grid filled with non-negative numbers, find a path from top left
to bottom right which minimizes the sum of all numbers along its path.

Note: You can only move either down or right at any point in time.

Lessons:
1) When using recursion, try to make candidates and cand more specific, don't try
    to write general senarios since the movements of cand to candidates 
    won't be too random or general
"""


def right(x):
    # x = [1,2]
    return [x[0],x[1]+1]

def down(x):
    return [x[0]+1,x[1]]

def isBnexttoA(a,b):
    # a = [0,0]
    # b = [0,2]
    return (a[0]<=b[0] and a[1]<b[1]) or (a[0]<b[0] and a[1]<=b[1])

def findSteps(candidates, cand=[[0,0]], res =[]):
    # cand, res are both list of lists
    # cand is [[]]
    # candidates is [[]]
    # res is [[[ ]]]
    candidates = filter(lambda x: isBnexttoA(cand[-1],x), candidates)
    if len(candidates) == 0:
        res = res
    elif len(candidates) == 1:
        if right(cand[-1])==candidates[0] or down(cand[-1])==candidates[0]:
            if cand + candidates not in res:
                res.append(cand + candidates)
    else:
        # for right move
        if right(cand[-1]) in candidates:
            cand_new = cand + [right(cand[-1])]
            candidates_new = filter(lambda x: isBnexttoA(cand_new[-1],x), candidates)
            res_seq = findSteps(candidates=candidates_new, cand=cand_new, res=[])
            for r in res_seq:
                if r not in res:
                    res.append(r)
        # for down move
        if down(cand[-1]) in candidates:
            cand_new = cand + [down(cand[-1])]
            candidates_new = filter(lambda x: isBnexttoA(cand_new[-1],x), candidates)
            res_seq = findSteps(candidates=candidates_new, cand=cand_new, res=[])
            for r in res_seq:
                if r not in res:
                    res.append(r)
    return res
    
def getpathvalue(path, grid):
    #path = [[0, 0], [0, 1], [0, 2], [1, 2]]
    value =0
    for p in path:
        value += grid[p[0]][p[1]]
    return value

def getMaxValue(grid):
    nrow = len(grid)
    ncol = len(grid[0])
    #steps = nrow+ncol-2
    grid_index =[]
    for i in range(nrow):
        for j in range(ncol):
            grid_index.append([i,j])
    paths = findSteps(candidates=grid_index)
    max_value =0
    max_path=[]
    for path in paths:
        v = getpathvalue(path, grid)
        if v > max_value:
            max_value = v
            max_path = path
    return max_value, max_path

grid = [[3,4,1],[3,2,8]]
getMaxValue(grid)
