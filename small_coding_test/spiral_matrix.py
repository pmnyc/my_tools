"""
Spiral Matrix I

Given a matrix of m x n elements (m rows, n columns), return all elements of the matrix in spiral order.
For example,
Given the following matrix:
[
 [ 1, 2, 3 ],
 [ 4, 5, 6 ],
 [ 7, 8, 9 ]
]
You should return [1,2,3,6,9,8,7,4,5].
"""


def nextMove(move):
    moves = ['right','down','left','up']
    move_index = moves.index(move)
    if move_index == 3:
        nextmove = moves[0]
    else:
        nextmove = moves[move_index+1]
    return nextmove

def nextIndex(idx, nextmove):
    # idx=[0,1]
    if nextmove == 'right':
        return [idx[0],idx[1]+1]
    elif nextmove == 'down':
        return [idx[0]+1,idx[1]]
    elif nextmove == 'left':
        return [idx[0],idx[1]-1]
    elif nextmove == 'up':
        return [idx[0]-1,idx[1]]


def createSpiral(matrix):
    nrow = len(matrix)
    ncol = len(matrix[0])
    
    for i in range(nrow):
        for j in range(ncol):
            if i ==0 and j==0:
                to_visit =[[i,j]]
            else:
                to_visit += [[i,j]]
    
    queue = [[0,0]]
    count_elements = nrow * ncol
    for i in range(1,count_elements):
        if i == 1:
            prev = [0,0]
            to_visit.remove(prev)
            nextmove = 'right'
            curr = nextIndex(prev, nextmove)
            queue += [curr]
        else:
            prev = curr[:]
            curr = nextIndex(prev, nextmove)
            if curr not in to_visit:
                nextmove = nextMove(nextmove)
                curr = nextIndex(prev, nextmove)
            to_visit.remove(curr)
            queue += [curr]
    
    spiral = map(lambda i: matrix[i[0]][i[1]], queue)
    return spiral


matrix = [
 [ 1, 2, 3, 4],
 [ 5, 6, 7, 8],
 [ 9, 10, 11, 12 ]
]

createSpiral(matrix)