# -*- coding: utf-8 -*-
"""
Explicit @jit signatures can use a number of types. Here are some common ones:

void is the return type of functions returning nothing (which actually return 
    None when called from Python)
intp and uintp are pointer-sized integers (signed and unsigned, respectively)
intc and uintc are equivalent to C int and unsigned int integer types

int8, uint8, int16, uint16, int32, uint32, int64, uint64 are fixed-width integers 
    of the corresponding bit width (signed and unsigned)
float32 and float64 are single- and double-precision floating-point numbers, respectively
complex64 and complex128 are single- and double-precision complex numbers, respectively

array types can be specified by indexing any numeric type, 
    e.g. float32[:] for a one-dimension single-precision array 
    or int8[:,:] for a two-dimension array of 8-bit integers.

nogil = True can not hold Python’s global interpreter lock (GIL). Useful when 
    writing programs on multi-core system
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
