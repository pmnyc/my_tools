# -*- coding: utf-8 -*-
#!/usr/bin/env python

"""
@author: Man Peng

This function loads setting parameters in config folder

Sample Usage:
>>> from utils.load_settings import loadParameters
>>> info = loadParameters()
"""

import json, os
import numpy as np
import warnings

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

def loadParameters(mfile="config/parameters.json"):
    info = loadJson(os.path.join(os.getcwd(),mfile))
    ## create the file cities_done_with_property_link_extraction.txt if in queue
        ## if it does not exist. This part is a patch
    try:
        citiy_lists_done = info["cities_done_with_property_link_extraction"]
        if not(os.path.isfile(citiy_lists_done)):
            with open(citiy_lists_done,'a') as f:
                f.close()
    except:
        pass
    # Done with this patch #
    
    ## patch2: check the existstence of city_list.txt file ##
    city_list_file = info["city_list"]
    city_list = np.genfromtxt(city_list_file,dtype="unicode",delimiter="\n")

    try:
        city_list = list(city_list)
    except:
        city_list=[str(city_list)]

    city_list = filter(lambda x: len(x.strip())>0, city_list)
    if len(city_list) == 0:
        warnings.warn("File %s is empty!" %city_list_file)
    # Done with patch2 #
    
    return info
