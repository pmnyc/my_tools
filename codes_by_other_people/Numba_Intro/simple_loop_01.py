# -*- coding: utf-8 -*-
"""
For basic arrays or list calculations and loops, numba.jit
    just-in-time complier is easy to add by just using it
    as a decorator. The speed boosted by it is significant
    when there are too many loops

"""

import datetime
import numba
import numpy as np


#@numba.jit
def sum2d(arr):
    M, N = arr.shape
    result = 0.0
    for i in range(M):
        for j in range(N):
            result += arr[i,j]
    return result


## test
dimension = 10000
arr = np.arange(dimension**2).reshape(dimension, dimension)

starttime = datetime.datetime.now()
y = sum2d(arr)
endtime = datetime.datetime.now()
print "It takes %s to run" %(endtime-starttime)
