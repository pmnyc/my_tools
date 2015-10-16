"""
Rotate Image

You are given an n x n 2D matrix representing an image.
Rotate the image by 90 degrees (clockwise).

The idea is to rotate each layer
"""


def direction(idx, n):
    # idx = [0,1]
    # n = 3
    if idx[0] == 0:
        return 'n'
    elif idx[0] == n-1:
        return 's'
    elif idx[1] == 0:
        return 'w'
    elif idx[1] == n-1:
        return 'e'

def getoutlayer(n):
    index = []
    for i in range(n):
        for j in range(n):
            if i in [0,n-1] or j in [0,n-1]:
                index.append([i,j])
    return index

def rotateLayer(n):
    # n = 3 # n is the dimension of matrix
    # index is the index of outside layer
    index = getoutlayer(n)
    index_rotate = []
    for idx in index:
        dir_ = direction(idx, n)
        if dir_ == 'n':
            offset = idx[1]
            idx_ = [offset ,n-1]
        elif dir_ == 'e':
            offset = idx[0]
            idx_ = [n-1, n-1-offset]
        elif dir_ == 's':
            offset = n-1-idx[1]
            idx_ = [0, n-1-offset]
        elif dir_ == 'w':
            offset = n-1-idx[0]
            idx_ = [0, offset]
        else:
            pass
        index_rotate += [idx_]
    return index_rotate

def rotateoutLayer(matrix):
    n = len(matrix)
    layers = range(1,n/2 +1)
    for layer in layers:
        index = []
        dim = n - (layer-1) *2
        offset = layer-1
        layer_count = 4 * (dim-1)
        idx_boundary = range(layer-1, n-layer+1)
        idx_min = min(idx_boundary)
        idx_max = max(idx_boundary)
        i = 1
        while i <= layer_count:
            if i == 1:
                index += [[offset,offset]]
            else:
                prev = index[-1]
                if prev == [idx_min,idx_min]:
                    curr = [idx_min, idx_min+1]
                elif prev == [idx_min, idx_max]:
                    curr = [idx_min+1, idx_max]
                elif prev == [idx_max, idx_max]:
                    curr = [idx_max, idx_max-1]
                elif prev == [idx_max, idx_min]:
                    curr = [idx_max-1, idx_min]
                elif prev[0] == idx_min:
                    curr = [idx_min, prev[1]+1]
                elif prev[1] == idx_max:
                    curr = [prev[0]+1, idx_max]
                elif prev[0] == idx_max:
                    curr = [idx_max, prev[1]-1]
                elif prev[1] == idx_min:
                    curr = [prev[0]-1,idx_min]
                else:
                    curr = None
                index += [curr]
            i += 1
        add_steps = dim-1
        order = range(layer_count)
        order_rotate = map(lambda x: x + add_steps, order)
        order_rotate = map(lambda x: x % (layer_count), order_rotate)
        index_rotate = map(lambda i: index[i], order_rotate)
        elements = map(lambda i: matrix[i[0]][i[1]], index)
        for i in order:
            matrix[index_rotate[i][0]][index_rotate[i][1]] = elements[i]
    
    return matrix


matrix = [[1,2,3,4],[5,6,7,8],[9,10,11,12],[13,14,15,16]]
print matrix
print rotateoutLayer(matrix)
