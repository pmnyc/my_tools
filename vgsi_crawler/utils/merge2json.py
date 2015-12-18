#!/usr/bin/env python
# -*- coding: utf-8 -*-
"""
@author: Man Peng

This program is to merge two jsons of the same format into one json file

Sample Usage:
>>> merge2json('myjson1.json', 'myjson2.json', 'myoutput.json')
"""

import json

def loadJson(filename):
    json_data=open(filename,'r')
    data = json.load(json_data)
    json_data.close()
    return data

def loaddict2jsonfile(dic, tojson_filename):
    """
    This function loads a dic into tojson_filename file
    loaddict2jsonfile(my_dictionary, 'myjson.json')
    """
    with open(tojson_filename, mode='w') as feedsjson:
      json.dump(dic, feedsjson, indent=4)

def merge2json(json_file1, json_file2, outputfile):
    f1 = loadJson(json_file1)
    f2 = loadJson(json_file2)
    for k in f2.keys():
        if k in f1.keys():
            continue
        else:
            f1[k] = f2[k]
    loaddict2jsonfile(f1,outputfile)

def merge2dict(dict1, dict2, outputfile):
    f1 = dict1
    f2 = dict2
    for k in f2.keys():
        if k in f1.keys():
            continue
        else:
            f1[k] = f2[k]
    loaddict2jsonfile(f1,outputfile)
