# -*- coding: utf-8 -*-
"""
@author: Man Peng

This program is to export the link info we extracted from the geomesh
    and export it to the all_links_cached.csv file

Sample Usage:
>>> from utils.export_link2allcachedfile import exportLink2cache
>>> exportLink2cache('http://www.trula.com/***')
"""


from utils.load_settings import loadParameters
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

def exportLink2cache(link):
    """ This function exports the link info we extracted and store it in the 
    all_links_cached file for future reference"""
    param = loadParameters()
    links_cached_file = param["all_links_cached"]
    createFile(links_cached_file)
    writeText2File(link, getFulldirAddress(links_cached_file))

