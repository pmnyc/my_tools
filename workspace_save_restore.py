"""
This program is to save and restore current workspace
    information when using Python IDE
"""

import shelve

#####################
# To Save Workspace:
#####################
def saveWorkspace(filename):
    my_shelf = shelve.open(filename,'n') # 'n' for new

    for key in dir():
        try:
            my_shelf[key] = globals()[key]
        except TypeError:
            #
            # __builtins__, my_shelf, and imported modules can not be shelved.
            #
            print('ERROR shelving: {0}'.format(key))
    my_shelf.close()

#####################
# To restore:
#####################
def restoreWorkspace(filename):
    my_shelf = shelve.open(filename)
    for key in my_shelf:
        globals()[key]=my_shelf[key]
    my_shelf.close()

if __name__ == '__main__':
    saveWorkspace('shelve.out')
    restoreWorkspace('shelve.out')
