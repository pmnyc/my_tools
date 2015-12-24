"""
A moving average function using @guvectorize.

The guvectorize (or vector for scalar) is so far the fastest
    , and it works better with numpy array types

When using jit (sometimes does not improve performance, even)
    try to use python native features, such as list, not using
    Numpy array, etc.
"""

import numpy as np

from numba import guvectorize, jit, autojit, int64, float64

@guvectorize(['void(float64[:], intp[:], float64[:])'], '(n),()->(n)')
def move_mean(a, window_arr, out):
    window_width = window_arr[0]
    asum = 0.0
    count = 0
    for i in range(window_width):
        asum += a[i]
        count += 1
        out[i] = asum / count
    for i in range(window_width, len(a)):
        asum += a[i] - a[i - window_width]
        out[i] = asum / count

import datetime
arr = np.arange(20000000, dtype=np.float64)
starttime = datetime.datetime.now()

xx = move_mean(arr, 3)

endtime = datetime.datetime.now()
print "It takes %s to run" %(endtime-starttime)
# it ook 0.2 second to run through all calculations



# @jit('f8[:](f8[:],f8)') or use following

@jit
def move_mean(a, window_arr):
    window_width = window_arr
    asum = 0.0
    count = 0
    out = [None]*len(a)
    for i in range(window_width):
        asum += a[i]
        count += 1
        out[i] = asum / count
    for i in range(window_width, len(a)):
        asum += a[i] - a[i - window_width]
        out[i] = asum / count
    return out


import datetime
arr = list(np.arange(20000000, dtype=np.float64))
starttime = datetime.datetime.now()

x = move_mean(arr, 3)

endtime = datetime.datetime.now()
print "It takes %s to run" %(endtime-starttime)
# It took 20 seconds to run through all calculations