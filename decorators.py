# -*- coding: utf-8 -*-
#!/usr/bin/env python

"""
@author: pm

This program stores some of commonly used decorators
    for the rest of the porgram to use

"""

import functools

def suppress_erros(func):
    """Automatically silence any erros that occur within a function"""

    @functools.wraps(func)
    def wrapper(*args, **kwargs):
        try:
            return func(*args, **kwargs)
        except Exception:
            pass

    return wrapper

def memorize_simple(func):
    """
    Cache the resutls of the function in the memory so it does not 
    need to be called again if the same arguments are provided before.
    """
    verbose = False
    cache = {}
    @functools.wraps(func)
    def wrapper(*args):
        if args in cache:
            # remove it before using it in real application
            if verbose:
                print("This function %s has been called before on the same parameter values" %func.__name__)
            return cache[args]

        # remove it before using it in real application to avoid too many
            # annoying logging to appear on screen
        if verbose:
            print("Calling the function %s" %func.__name__)
        res = func(*args)

        # now save this newly run result in the memory (cache)
        cache[args] = res
        return res

    return wrapper


## next is to define the decorator with arguments in it
class memorize(object):
    """ This is another decorator of memorization using extra
        argument such as indicating whether to print the steps
        or not
    """
    def __init__(self, verbose=True):
        #super(memorize, self).__init__()
        self.verbose = verbose
        try:
            isinstance(self.cache, dict)
        except (AttributeError, NameError):
            self.cache = {}
    def __call__(self, func):
        """
        If there are decorator arguments, __call__() is only called
        once, as part of the decoration process! You can only give
        it a single argument, which is the function object.
        """
        @functools.wraps(func)
        def wrapper(*args):
            if args in self.cache:
                if self.verbose:
                    print("This function %s has been called before on the same parameter values" %func.__name__)
                return self.cache[args]
            if self.verbose:
                print("Calling the function %s" %func.__name__)
            res = func(*args)
            self.cache[args] = res
            return res

        return wrapper


##Test##
"""
@memorize_simple
def multi(x,y):
    return x*y
multi(2,3)
multi(2,3)

@memorize()
def multi(x,y):
    return x*y
multi(2,3)
multi(2,3)
"""