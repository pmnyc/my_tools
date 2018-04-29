# -*- coding: utf-8 -*-
"""
Explicit @jit signatures can use a number of types. Here are some common ones:

void is the return type of functions returning nothing (which actually return 
    None when called from Python)

------------------
The following table contains the elementary numeric types currently defined by Numba and their aliases.

Type name(s)    Shorthand   Comments
boolean b1  represented as a byte
uint8, byte u1  8-bit unsigned byte
uint16  u2  16-bit unsigned integer
uint32  u4  32-bit unsigned integer
uint64  u8  64-bit unsigned integer
int8, char  i1  8-bit signed byte
int16   i2  16-bit signed integer
int32   i4  32-bit signed integer
int64   i8  64-bit signed integer
intc    –   C int-sized integer
uintc   –   C int-sized unsigned integer
intp    –   pointer-sized integer
uintp   –   pointer-sized unsigned integer
float32 f4  single-precision floating-point number
float64, double f8  double-precision floating-point number
complex64   c8  single-precision complex number
complex128  c16 double-precision complex number

array types can be specified by indexing any numeric type, 
    e.g. float32[:] for a one-dimension single-precision array 
    or int8[:,:] for a two-dimension array of 8-bit integers.

nogil = True can not hold Python’s global interpreter lock (GIL). Useful when 
    writing programs on multi-core system

------------------
numba.typeof(value)
Create a Numba type accurately describing the given value. None is returned if the value isn’t supported in nopython mode.

>>> numba.typeof(np.empty(3))
array(float64, 1d, C)
>>> numba.typeof((1, 2.0))
(int64, float64)
>>> numba.typeof([0])
reflected list(int64)

------------------
Instead of using typeof(), non-trivial scalars such as structured types can also be constructed programmatically.

numba.from_dtype(dtype)
Create a Numba type corresponding to the given Numpy dtype:

>>> struct_dtype = np.dtype([('row', np.float64), ('col', np.float64)])
>>> tp
Record([('row', '<f8'), ('col', '<f8')])
>>> tp[:, :]
unaligned array(Record([('row', '<f8'), ('col', '<f8')]), 2d, A)
"""

from numba import jit, int32

@jit(nogil=True)
def add1(x,y):
    return x+y

add1(100, 200)

add1.inspect_types() # This gives the types of inputs
    # as an inspection for some debugs

#########################

@jit(int32(int32, int32))
def add2(x,y):
    return x+y

add1(100, 200)
# The int32(...) specifies the return type
    # and the (int32, int32) specify the
    # types of input

#########################

from numba import vectorize, float64

@vectorize([float64(float64, float64),
            int32(int32, int32)])
def add4(x, y):
    return x + y
    
add4(4,6)
# the possible x,y and return values types are provided in the list []
    # but this only works on one element as an input

#########################
from numba import guvectorize, int64

@guvectorize(["void(int64[:], int64[:], int64[:])"], '(n),()->(n)')
def add5(x, y, res):
    for i in range(x.shape[0]):
        res[i] = x[i] + y[0]

add5([1,2,3,4,5], 6)
# The guvectorize deals with inputs having arrays.
    # where x is array of int64 values
    # , and y is a scalar, but still in the code
    # we use y[0] to represent the scalar
    # the (n),() -> (n) denotes that it is an array
        # of n elements and a scalar as input, to get
        # the result of array of n elements.
        # the empty () here denotes a scalar
# guvectorize will convert list to numpy array, hence we have
    # .shape associated with x.shape. The list has no shape feature. 

@guvectorize(["void(float64[:,:], float64[:,:], float64[:,:])"],
             "(m,n),(n,p)->(m,p)")
def f(a, b, result):
    """ This is a function for matrix m*n times n*p getting
        result matrix of m*p"""
    ...

#########################
import datetime
import numba


@numba.jit(nogil=True)
def add55(x, y):
    res = []
    for i in range(len(x)):
        res += [x[i] + y]
    return res

def add66(x, y):
    res = []
    for i in range(len(x)):
        res += [x[i] + y]
    return res


x = [0] * 100000000
y = 10

## test speeds
starttime = datetime.datetime.now()
r = add5(x, y)
endtime = datetime.datetime.now()
print "It takes %s to run" %(endtime-starttime)
# It took 6.5 seconds to use @guvectorize

starttime = datetime.datetime.now()
r = add55(x, y)
endtime = datetime.datetime.now()
print "It takes %s to run" %(endtime-starttime)
# It took 50 seconds to use @jit, 62 seconds to use @autojit

starttime = datetime.datetime.now()
r = add66(x, y)
endtime = datetime.datetime.now()
print "It takes %s to run" %(endtime-starttime)
# It took 40 seconds without using any jit

##################################################
##################################################
from numba import guvectorize, int64, float64
import numpy as np

@guvectorize(["void(float64[:,:], float64[:,:], float64[:], intp[:])"],
             "(m,n),(p,n)->(m),(m)", nopython=True)
def find_nearest_points(a, b, res, idx):
    """ This functions finds the data point in matrix 'b' that is closest to a given
        data point in matrix 'a'. This is useful, for example, given a sequence of GPS
        data points of matrix 'a', which points of interest in data points of matrix 'b'
        are closest to this sequence of GPS points.
        'a', 'b' can not have nan values
    Parameters
    ----------
    a : array-like list or numpy array
        The main data points for the match (similar to left join in SQL)
    b: array-like list or numpy array
        The reference data points for the match
    Returns:
    ----------
    res: array-like list or numpy array
        The smallest distance between a given data poin in matrix 'a' and data points in matrix 'b'
    idx: array-like list or numpy array
        The index of the data point in reference matrix 'b' that is closet to a given data point in
        matrix 'a'
    Examples:
    ----------
        >>> out = find_nearest_points(np.array([[1,2],[3,4]]),
                                      np.array([[4,2],[1,3],[7,3]]))
        out[0][1] is the cloest distance between [3,4] from 'a' and any point in 'b'
        out[1][1] is the index of point in 'b' having cloest distance between [3,4] from 'a' 
                    and any point in 'b'
    """
    # ensure the a,b are the matrix having same num of columns
    assert len(a[0]) == len(b[0])
    n_col = len(a[0])
    for i in range(len(a)):
        min_dis = 1.0 * 1e20
        min_idx = -1
        for j in range(len(b)):
            s = 0.0
            for col in range(n_col):
                s += (a[i][col] - b[j][col]) ** 2
            if s ** 0.5 < min_dis:
                min_dis = s ** 0.5
                min_idx = j + 0
        if min_idx <0:
            res[i] = np.nan
        else:
            res[i] = min_dis
        idx[i] = min_idx
    ...
    # End of find_nearest_points function
