#!/usr/bin/env python
# -*- coding: utf-8 -*-
"""
@author: Man Peng

This program is to clean up all unnecessary files created by running the program

Sample Usage:

First copy this file to the main work directory, then run

>>> python cleanup.py
"""

import os
import shutil
from fnmatch import fnmatch

curr_wdr = os.getcwd()
readmefile = filter(lambda x: 'readme' in x.lower(), os.listdir('.'))
if len(readmefile) == 0:
    raise Exception('YOU ARE NOT IN ROOT WORK DIRECTORY!!!')


def deleteFiles(extension, folder):
    # Sample Input
    # extension = ".pyc"
    # folder = "utils"
    if os.path.isdir(os.path.join(curr_wdr,folder)):
        os.chdir(os.path.join(curr_wdr,folder))
        try:
            map(lambda x: os.remove(x), filter(lambda t: os.path.splitext(t)[1]==extension, os.listdir(".")))
        except:
            pass
        os.chdir(curr_wdr)

def deleteFolder(folder):
    # Sample Input
    # folder = "downloads"
    if os.path.isdir(os.path.join(os.getcwd(),folder)):
        try:
            shutil.rmtree(os.path.join(os.getcwd(),folder))
        except:
            pass

## clean all files in some folder ##
deleteFolder("log")
deleteFolder("cache")
deleteFolder("postprocess_output")


###########################################################
## clean .pyc files in the current main directory folder ## 
deleteFiles(".pyc", "")

# delete files staring with Xvfb_
try:
    map(lambda x: os.remove(x), filter(lambda t: t.lower().startswith('xvfb_'), os.listdir(".")))
except:
    pass
try:
    map(lambda x: os.remove(x), filter(lambda t: t.lower().startswith('ghostdriver'), os.listdir(".")))
except:
    pass
try:
    map(lambda x: os.remove(x), filter(lambda t: t.lower().startswith('nohup.out'), os.listdir(".")))
except:
    pass
    
## clean .pyc files in utils folder ##
deleteFiles(".pyc", "utils")

## clean .pyc files in app folder ##
deleteFiles(".pyc", "app")
deleteFiles(".pyc", "bin")
