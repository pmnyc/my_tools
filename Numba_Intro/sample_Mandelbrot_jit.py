"""
There are still some issues with calling @vectorize or @guvectorize inside  
    them. Do not double call them. But it can double call @jit
"""

import numpy as np
import pylab

from numba import jit, int64, vectorize, float64, guvectorize, complex128

@jit
def mandel(x, y, max_iters):
    """
    Given the real and imaginary parts of a complex number,
    determine if it is a candidate for membership in the Mandelbrot
    set given a fixed number of iterations.
    """
    c = complex(x,y)
    z = 0j
    for i in range(max_iters):
        z = z*z + c
        if z.real * z.real + z.imag * z.imag >= 4:
            return 255 * i // max_iters

    return 255

@jit
def create_fractal(min_x, max_x, min_y, max_y, image, iters):
    height = image.shape[0]
    width = image.shape[1]

    pixel_size_x = (max_x - min_x) / width
    pixel_size_y = (max_y - min_y) / height
    for x in range(width):
        real = min_x + x * pixel_size_x
        for y in range(height):
            imag = min_y + y * pixel_size_y
            color = mandel(real, imag, iters)
            image[y, x] = color

    return image


import datetime
starttime = datetime.datetime.now()

image = np.zeros((7000, 14000), dtype=np.uint8)
create_fractal(-2.0, 1.0, -1.0, 1.0, image, 20)
pylab.imshow(image)
pylab.gray()
pylab.show()

endtime = datetime.datetime.now()
print "It takes %s to run" %(endtime-starttime)

##################################################

@guvectorize(["void(float64[:], float64[:], float64[:], float64[:], int64[:,:], int64[:], int64[:,:])"],'(),(),(),(),(m,n),()->(m,n)')
def create_fractal2(min_x, max_x, min_y, max_y, image, iters,
                    res):    
    min_x = min_x[0]
    max_x = max_x[0]
    min_y = min_y[0]
    max_y = max_y[0]
    iters = iters[0]
    res = image[:,:]
    height = res.shape[0]
    width = res.shape[1]

    pixel_size_x = (max_x - min_x) / width
    pixel_size_y = (max_y - min_y) / height
    for x in range(width):
        real = min_x + x * pixel_size_x
        for y in range(height):
            imag = min_y + y * pixel_size_y
            #color = mandel(real, imag, iters)
            c = np.complex(real,imag)
            #z = 0j
            z = np.complex(0,0)
            color = 255
            for i in range(iters):
                z = z*z + c
                if z.real * z.real + z.imag * z.imag >= 4:
                    color = 255 * i // iters
            ## end of mandel function
            res[y, x] = color


import datetime
image = np.zeros((7000, 14000), dtype=np.int64)
starttime = datetime.datetime.now()
create_fractal2(-2.0, 1.0, -1.0, 1.0, image, 100)
pylab.imshow(image)
pylab.gray()
pylab.show()

endtime = datetime.datetime.now()
print "It takes %s to run" %(endtime-starttime)
# It took 45 seconds to run through

# It took 0:10:56.091615 to run without any JIT
