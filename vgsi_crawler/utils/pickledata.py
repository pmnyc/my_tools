# -*- coding: utf-8 -*-
"""
This program pickle object data onto local drive and load picked(serialized)
    data into python 

@author: Man Peng

Sample Usage:
>>> import pickledata
>>> pickle_dir = pickledata._pickle_dir()
>>> dumpObj(newobj, 'mypickle.p')
>>> newobj2 = loadObj('mypickle.p')
"""

import pickle
import json
import os

def loadJson(filename):
    json_data=open(filename,'r')
    data = json.load(json_data)
    json_data.close()
    return data

def createFolder(folder):
    """ Create the folder if it does not exist"""
    if not(os.path.isdir(folder)):
        os.mkdir(folder)

def createFile(file_):
    """ Create the file if it does not exist"""
    file_ = os.path.join(os.getcwd(),file_)
    if not(os.path.isfile(file_)):
        open(file_, 'a').close()
    else:
        pass

# def _pickle_dir(setting_file="config/settings.json"):
    # settingjson = loadJson(os.path.join(os.getcwd(),setting_file))
    # pickledir = settingjson['pickled_dir']
    # pickledir = os.path.join(os.getcwd(),pickledir)
    # return pickledir

def _pickle_dir():
    pickledir = os.path.join(os.getcwd(),"downloads")
    return pickledir

def dumpObj(data, pickle_file):
    """ This function dumps the data/object into a serialized file """
    # sample input
    # pickle_file = "test.p"
    pickledir = _pickle_dir()
    createFolder(pickledir)
    pickle.dump(data, open(os.path.join(pickledir,pickle_file), "wb"))

def loadObj(pickle_file):
    """ This function load the pickle file into a python object """
    # pickle_file = "test.p"
    pickledir = _pickle_dir()
    ob = pickle.load(open(os.path.join(pickledir,pickle_file), "rb"))
    return ob
