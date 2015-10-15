"""
Number of Islands

Given a 2d grid map of '1's (land) and '0's (water), count the number of islands. 
An island is surrounded by water and is formed by connecting adjacent lands horizontally or vertically. 
You may assume all four edges of the grid are all surrounded by water.

Example 1:

11110
11010
11000
00000
Answer: 1

Example 2:

11000
11000
00100
00011

Answer: 3
"""

# index = [[0,1],[1,1]] of [[]]

def neibors(x, nrow, ncol):
    # x=[0,1]
    rows = range(nrow)
    cols = range(ncol)
    res = []
    if x[1]-1 in cols:
        left_ = [x[0],x[1]-1]
        res += [left_]
    if x[1]+1 in cols:
        right_ = [x[0],x[1]+1]
        res += [right_]
    if x[0]-1 in rows:
        up_ = [x[0]-1, x[1]]
        res += [up_]
    if x[0]+1 in rows:
        down_ = [x[0]+1, x[1]]
        res += [down_]
    return res

def findIsland(x, islands, nrow, ncol):
    # x =[0,1]
    # islands = {'[0,0]':[[0,0]]}
    if len(islands.keys()) == 0:
        return None
    else:
        for k in islands.keys():
            if x in islands[k] or len(filter(lambda x: x in islands[k],neibors(x,nrow,ncol))) >0:
                return k

land_index = []
isolated_lands =[]
islands={}
nrow = len(g)
ncol = len(g[0])

for i in range(nrow):
    for j in range(ncol):
        if g[i][j] == '1':
            land_index += [[i,j]]
            nebors_ = neibors([i,j],nrow,ncol)
            counter = 0
            for nei in nebors_:
                if g[nei[0]][nei[1]] == '1':
                    counter += 1
            if counter == 0:
                isolated_lands += [[i,j]]



g = [
    list('11000'),
    list('11000'),
    list('00100'),
    list('00011')
]

