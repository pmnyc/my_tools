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

# load local files
from utils import decorators


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

def loadParameters(config="conf/settings.json"):
    "This function lodas the initial paramters in the conf folder"

    self = decorators.logs_base(config)
    full_path = self.getFulldir(self.logfile)
    config_ = full_path.replace("\\",'/')

    parameters = loadJson(config_)
    return parameters

