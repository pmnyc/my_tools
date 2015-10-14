"""
N-Queens II

Follow up for N-Queens problem.
Now, instead outputting board configurations, return the total number of distinct solutions.

The idea is that none of them should be on the same row or col

hence, we go row by row

Lessons:
1) Creating 0 array using    [[0]*n]*n is very different from [[0 for i in range(n)] for j in range(n)]
    It is DANGEOURS to use [[0]*n]*n since it will replace other values even if you want to replace one value

"""

def isValid(grid, row, col):
    # row, col are numbers
    # this is for checking whether adding a [row, col] entry 1 is valid for current grid   
    curr_row = grid[row]
    curr_col = map(lambda i: grid[i][col],range(len(grid)))
    res = True
    if sum(curr_row)>0 or sum(curr_col) >0:
        res = False
    else:
        left_rows = range(len(grid))
        left_rows = left_rows[:row]+left_rows[row+1:]
        left_cols = range(len(grid))
        left_cols = left_cols[:col]+left_cols[col+1:]
        for i in left_rows:
            j = row+col-i
            if j in left_cols:
                if grid[i][j] == 1:
                    res = False
                    break
            j = col - row + i
            if j in left_cols:
                if grid[i][j] == 1:
                    res = False
                    break
    return res

def solve(grid_raw, cand, res=[]):
    #res = [[[0,1],[2,2]..]] etc, the index of solutions, of [[[]]]
        # res is the collection of solutions
    # cand is the added rows, cols, part of final solution like [[0,1],[2,2]], of [[]]
    n = len(grid_raw)
    #grid = [[0] * n] * n # replace list of lists is TRICKY, do not generate empty using [0,0] * n
    grid = [[0 for i in range(n)] for j in range(n)]
    for i in cand:
        grid[i[0]][i[1]] =1
    if len(cand) == n:
        res = res
    elif len(cand) == n-1:
        row = n-1
        for col in range(n):
            if isValid(grid, row, col):
                cand_new = cand + [[row, col]]
                res.append(cand_new)
                break
    else:
        start_row = len(cand)
        for col in range(n):
            if isValid(grid, start_row, col):
                cand_new = cand + [[start_row,col]]
                res_seq = solve(grid_raw, cand_new, res)
                for r in res_seq:
                    if r not in res:
                        res.append(r)
    return res
   
n = 4
grid = [[0] * n] * n
solve(grid, cand=[], res=[])
