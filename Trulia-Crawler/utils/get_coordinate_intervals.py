# -*- coding: utf-8 -*-
#!/usr/bin/env python

"""
@author: Man Peng

The program "getIntervals" is simply split the an interval into
    several equidistant intervals (except the last interval
    if there is not enough space left)
The program "createXminXmaxYminYmax" creates the mesh grid broundaries
    once the intervals for x-axis and y-axis are given.

The following parameters are used in the function getIntervals
internal_buffer_size = 0.2 means there is "20%" of any resulting interval overlap
        with the adjacent intervals.
        Hence, internal_buffer_size = 0 means the intervals are strictly next to each other
        with no overlap intervals.
external_buffer_size=0.5 means there is total "50%" expansion of the interval (x_min, x_max).

"""

import numpy as np
from utils.load_settings import loadParameters


def expandInterval(x_min, x_max, external_buffer_size):
    """ This function is to expand the interval given by x_min, x_max by the percentage
        given by external_buffer_size """
    buffer_size_oneside = (x_max - x_min) * external_buffer_size * 0.5
    x_min_2 = x_min - buffer_size_oneside
    x_max_2 = x_max + buffer_size_oneside
    return (x_min_2, x_max_2)


def getIntervals(x_range, grid_interval_length, internal_buffer_size=None, external_buffer_size=None):
    """
    Sample Input
       x_range = (1,10)
       grid_interval_length = 2
       internal_buffer_size=0
       external_buffer_size=0
    expected output is
    array([[  1.,   3.],
            [  3.,   5.],
            [  5.,   7.],
            [  7.,   9.],
            [  9.,  10.]]
    """
    param = loadParameters()
    if internal_buffer_size == None:
        internal_buffer_size = param["internal_buffer_size_for_geomesh"]
    if external_buffer_size == None:
        external_buffer_size = param["external_buffer_size_for_geomesh"]
    
    length = grid_interval_length + 0.00 # this is to prevent integer type division issue
    side_buffersize = internal_buffer_size * 0.25 * length
    x_min = np.min((x_range[0],x_range[1]))
    x_max = np.max((x_range[0],x_range[1]))
    
    # expand the interval by external_buffer_size, then redefine interval boundary
    x_interval_expanded = expandInterval(x_min, x_max, external_buffer_size)
    x_min = x_interval_expanded[0]
    x_max = x_interval_expanded[1]
    
    x_range = (x_min+0.00,x_max+0.00)
    nsteps = np.floor((x_range[1] - x_range[0])/length)
    x_range_rightend = x_range[0] + length * nsteps
    for i in range(int(nsteps)):
        if i == 0:
            intervals = np.array([x_range[0] - side_buffersize,x_range[0] + length+side_buffersize])
        else:
            intervals = np.vstack((intervals,[x_range[0] + i * length - side_buffersize 
                        , x_range[0] + (i+1) * length +side_buffersize]))
    if np.abs(x_range_rightend - x_range[1]) > 1e-8:
        intervals = np.vstack((intervals,[x_range_rightend - side_buffersize , x_range[1]+side_buffersize]))
    return intervals


def createXminXmaxYminYmax(x_intervals, y_intervals):
    """
    This function is combine all possible x_min, x_max, y_min, y_max
        based on x, y intervals to create the boundaries for all possible
        mesh grids
    Sampel Inputs:
        x_intervals = np.array([[  1.,   3.],
           [  3.,   5.],
           [  5.,   7.],
           [  7.,   9.],
           [  9.,  10.]])
        y_intervals = np.array([[  1.,   3.],
               [  3.,   5.],
               [  5.,   7.],
               [  7.,   9.],
               [  9.,  10.]])
    """
    counter = 0
    for i in range(len(x_intervals)):
        for j in range(len(y_intervals)):
            x_ = x_intervals[i]
            y_ = y_intervals[j]
            xy_ = np.hstack((x_,y_))
            if counter == 0:
                xy_stack = xy_
            else:
                xy_stack = np.vstack((xy_stack,xy_))
            counter += 1
    return xy_stack
