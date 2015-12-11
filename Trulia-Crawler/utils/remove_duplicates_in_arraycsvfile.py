# -*- coding: utf-8 -*-
"""
@author: Man Peng

This program removes the duplicates of webpage links in the all_links_cached.csv
    file.

Sample Usage:
>>> from utils.remove_duplicates_in_arraycsvfile import unqiueList
>>> csvfile = "queue/zzzzzzzzzz.csv"
>>> unqiueList(csvfile)
"""


from numpy import genfromtxt
import numpy as np
import os


def writeText2File(loginfo, mfile):
    """
    This function writes the log message to the file
    """
    with open(mfile,'a') as f:
        f.writelines('%s\n' %loginfo)
        f.close()

def createFolder(folder):
    """ Create the folder if it does not exist
    The folder name or directory after the main_work_directory is needed
    """
    folder_ = os.path.join(os.getcwd(),folder)
    if not(os.path.isdir(folder_)):
        os.mkdir(folder_)

def createFile(file):
    """ Create the file if it does not exist
    The file name or directory after the main_work_directory is needed
    """
    file_ = os.path.join(os.getcwd(),file)
    if not(os.path.isfile(file_)):
        with open(file_,"a") as f:
            f.close()

def getFulldirAddress(x):
    """ In case if the file is not a full address, append main directory
    information to it"""
    x_first10 = x[:10]
    if x_first10.find(":\\") >=0 or x_first10.startswith("/") or x_first10.find(":/") >=0:
        return x
    else:
        return os.path.join(os.getcwd(),x)

def unqiueList(csvfile):
    """ This function is to remove duplicates of csv file that stores all links """
    links_array = genfromtxt(getFulldirAddress(csvfile), delimiter='\n', dtype="unicode")
    links_array_2 = np.unique(links_array)
    np.savetxt(getFulldirAddress(csvfile), links_array_2,  fmt='%s')

