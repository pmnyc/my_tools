"""
Define Numba Data Types

a 3-dimension array of the same underlying type:
>>> numba.float32[:,:,:]
array(float32, 3d, A, nonconst)

Define an advanced data type using Numpy's definition
struct_dtype = np.dtype([('row', np.float64), ('col', np.float64)])
numba.from_dtype(struct_dtype)

2.4.3. Built-in functions
The following built-in functions are supported:

abs()
bool
complex
enumerate()
float
int: only the one-argument form
len()
min(): only the multiple-argument form
max(): only the multiple-argument form
print(): only numbers and strings; no file or sep argument
range
round(): only the two-argument form
zip()
"""

