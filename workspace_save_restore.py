"""
This program is to save and restore current workspace
    information when using Python IDE
"""

import shelve, os
import numpy as np

#####################
# To Save Workspace:
#####################
def saveWorkspace(f):
    try:
        os.remove(f)
    except:
        pass
    my_shelf = shelve.open(f,flag='n') # n means new file
    dirs = dir()
    dirs = np.setdiff1d(globals().keys(),dirs)
    for key in dirs:
        try:
            my_shelf[key] = globals()[key]
        except TypeError:
            # __builtins__, my_shelf, and imported modules can not be shelved.
            print('ERROR shelving: {0}'.format(key))
    my_shelf.close()

#####################
# To restore:
#####################
def restoreWorkspace(f):
    my_shelf = shelve.open(f,flag='r')
    for key in my_shelf:
        try:
            globals()[key]=my_shelf[key]
        except Exception as e:
            print e
    my_shelf.close()

if __name__ == '__main__':
    saveWorkspace('shelve.out')
    restoreWorkspace('shelve.out')
