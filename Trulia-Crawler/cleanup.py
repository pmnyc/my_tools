#!/usr/bin/env python
# -*- coding: utf-8 -*-
"""
@author: Man Peng

This program is to clean up all unnecessary files created by running the program

Sample Usage:
>>> python cleanup.py
"""

import os
import shutil
from fnmatch import fnmatch

curr_wdr = os.getcwd()

def deleteFiles(extension, folder):
    # Sample Input
    # extension = ".pyc"
    # folder = "utils"
    if os.path.isdir(os.path.join(curr_wdr,folder)):
        os.chdir(os.path.join(curr_wdr,folder))
        map(lambda x: os.remove(x), filter(lambda t: os.path.splitext(t)[1]==extension, os.listdir(".")))
        os.chdir(curr_wdr)

def deleteFolder(folder):
    # Sample Input
    # folder = "downloads"
    if os.path.isdir(os.path.join(os.getcwd(),folder)):
        shutil.rmtree(os.path.join(os.getcwd(),folder))

## clean all files in some folder ##
deleteFolder("downloads")


###########################################################
## clean .pyc files in the current main directory folder ## 
deleteFiles(".pyc", "")

## clean .pyc files in utils folder ##
deleteFiles(".pyc", "utils")

## clean .pyc files in crawler folder ##
deleteFiles(".pyc", "trulia_crawler")
deleteFiles(".pyc", "trulia_crawler/spiders")

## clean .pyc files in test folder ##
folder = "test"
folders = map(lambda t: folder+"/"+t, filter(lambda x: not(fnmatch(x,"*.*")),os.listdir(folder)))
deleteFiles(".pyc", folder)
for f in folders:
    deleteFiles(".pyc", f)

## clean .pyc files in app folder ##
deleteFiles(".pyc", "app")

## clean .pyc files in queue folder ##
deleteFiles(".pyc", "queue")

## clean .pyc files in output_bucket folder ##
deleteFiles(".pyc", "output_bucket")

## clean .pyc files in special_tasks folder ##
deleteFiles(".pyc", "special_tasks")

