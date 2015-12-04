# -*- coding: utf-8 -*-
#!/usr/bin/env python

"""
@author: pm

This program stores some of commonly used decorators
    for the rest of the porgram to use


## Test 1 ##
@memorize_simple
def multi(x,y):
    return x*y
multi(2,3)
multi(2,3)

## Test 1 ##
@memorize()
def multi(x,y):
    return x*y
multi(2,3)
multi(2,3)

## Test 3 ##
@logs("mylogs/mylog.txt")
def divi(x,y):
    return x/y
divi(1,0)
"""

import functools
import os, sys
import re
import logging
import datetime

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


class logs_base(object):
    """
    Logs the results and errors in log folder
    """
    def __init__(self, logfile):
        logfile = logfile.replace("\\",'/')
        self.logfile = logfile
    
    #@classmethod
    #@staticmethod
    def isFullDir(self, path):
        """
        This program is to tell whether a directory
            given is a full directory or partial one
        """
        try:
            temp_ = re.match(r'[a-zA-Z]:/',path).group(0)
            if len(temp_) >= 2:
                full_dir = True
        except:
            if path.startswith("/"):
                full_dir = True
            else:
                full_dir = False
        return full_dir

    def getFulldir(self, path):
        """
        This program assigns the full directory of the file/folder
            if the path is given.
        """
        fulldir_ind = self.isFullDir(path)
        if fulldir_ind:
            return path
        else:
            if path.startswith('./'):
                path = path[2:]
            return os.path.join(os.getcwd(),path)

    def createFile(self, path):
        """
        This program creates the folder and file if the given path does not
            have the folder or file ready in the local drive
        """
        full_path = self.getFulldir(path)
        full_path = full_path.replace("\\",'/')
        # file_, ext = os.path.splitext(full_path)
        # if ext == '':
        #     folder_ind = True
        # else:
        #     folder_ind = False
        filename = os.path.basename(full_path)
        folder = os.path.dirname(full_path)
        if not os.path.exists(folder):
            os.makedirs(folder)
        try:
            len(open(full_path, 'r').readlines())
        except (TypeError, IOError):
            # The filename wasn't valid for use with the filesystem.
            #logging.error(e)
            print("The log file %s does not exist, creating it now..." % filename)
            log = open(full_path, 'w')
            #log.write('%s\n' % e)
            log.close()

    def getCurrentTime(self):
        """
        This program is to get the current time into a string
        """
        time_ = str(datetime.datetime.now())
        time_ = time_.split(".")[:-1][-1]
        return time_

def logs(*argvs):
    """
    This is the decorator that writes the logs to the log file. If
    the log file does not exist, it will create it first
    """
    def logs_decorator(func):
        self = logs_base(*argvs) #self is just an object from logs_base
        @functools.wraps(func)
        def wrapper(*args):
            try:
                res = func(*args)
            except Exception as e:
                logging.error(e)
                self.createFile(self.logfile)
                full_path = self.getFulldir(self.logfile)
                full_path = full_path.replace("\\",'/')
                log = open(full_path, 'a')
                log.write('[%s]:  %s\n' %(self.getCurrentTime() ,e))
                log.close()
                res = None
            return res

        return wrapper
    return logs_decorator

