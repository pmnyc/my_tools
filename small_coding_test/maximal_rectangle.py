"""
Maximal Rectangle

Given a 2D binary matrix filled with 0's and 1's, find the largest rectangle containing all ones and return its area.
"""


import numpy as np

def isAlloneMatrix(matrix):
    if not matrix: #this means if "matrix" is not an actual matrix
        return (0, False)
    else:
        counter = 0
        for row in matrix:
            if counter==0:
                matrix_flat = row
            else:
                matrix_flat += row
            counter += 1
    if sum(matrix_flat) < len(matrix_flat):
        return (0, False)
    else:
        return (sum(matrix_flat), True)

def choose2fromn(n):
    queue= []
    for i in range(n-1):
        for j in range(i+1,n):
            queue.append([i,j])
    return queue

def getMaxMatrix(matrix):
    nrow, ncol = np.array(matrix).shape
    row_queue = choose2fromn(nrow)
    col_queue = choose2fromn(ncol)
    
    max_area = 0
    max_rowcol = []
    for row in row_queue:
        rows = matrix[row[0]:row[1]+1]
        for col in col_queue:
            sub_matrix = map(lambda x: x[col[0]:col[1]+1], rows)
            res = isAlloneMatrix(sub_matrix)
            if res[1] and res[0]>max_area:
                max_area = res[0]
                max_rowcol= [row, col]
    return max_area, max_rowcol


matrix = [[0,0,1,0,0],
    [0,1,1,1,0],
    [1,0,1,1,0],
    [0,1,1,1,1],
    [1,1,1,0,1],
    [0,1,1,1,1]]

getMaxMatrix(matrix)

### Solution #2
class Solution:
    # @param matrix, a list of lists of 1 length string
    # @return an integer
    def maximalRectangle(self, matrix):
        # Make a list of heights
        if not matrix:
            return 0
        n = len(matrix)
        if not matrix[0]:
            return 0
        m = len(matrix[0])
        hist = [[0 for j in range(m)] for i in range(n)]
        for i in range(n):
            for j in range(m):
                if i == 0:
                    hist[i][j] = int(matrix[i][j])
                else:
                    if matrix[i][j] == '1':
                        hist[i][j] = 1 + hist[i - 1][j]
        res = 0
        for row in hist:
            res = max(res, self.max_hist_rect(row))
        return res

    def max_hist_rect(self, heights):
        if not heights:
            return 0
        n = len(heights)
        max_area = heights[0]
        stack = []
        for i in range(n + 1):
            while stack and (i == n or heights[stack[-1]] > heights[i]):
                h = heights[stack.pop()]
                if stack:
                    w = i - stack[-1] - 1
                else:
                    w = i
                max_area = max(max_area, h * w)
            stack.append(i)
        return max_area

Solution().maximalRectangle(matrix)