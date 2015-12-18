# -*- coding: utf-8 -*-
#!/usr/bin/env python

"""
@author: Man Peng

This program is for calling the main parser of the webpage.
It won't return any value, but will dump results onto local folder
specified in output_folder in settings.json

Sample Usage:
content here is content of hmtl file

>>> from app import parser_call
>>> parser_call.callParser(content)

"""

import os
import json
import datetime

# load local files
from app import parser
from utils import load_settings


def openHtmlfile(file_):
    f = open(file_, "r")
    content = f.read()
    return content

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

def callParser(content):
    ## The content is the content of the HTML
    parameters = load_settings.loadParameters()
    output_dict = {}
    house_obj = parser.Parser(content)
    
    physical_address = house_obj.getLocation()
    year_built = house_obj.getYearBuilt()
    pid = house_obj.getPID()
    town = house_obj.getTown()
    output_dict['physical_address'] = physical_address
    output_dict['year_built'] = year_built
    building_area = house_obj.getBuildingAreas() # here building_area is a dictionary
    building_attributes = house_obj.getBuildingAttributes() # also a dictionary
    output_dict.update(building_area)
    output_dict.update(building_attributes)
    
    filename = town.replace(" ","").replace(",","_") + "_pid" + pid
    current_yearmonth = str(datetime.datetime.now())[:7]
    dict_index = filename + "_" + current_yearmonth
    
    ## The following is to put parcel information under the key (index) for this parcel
    town_nostate = town.split(",")[0].strip()
    if filter(lambda x: town_nostate.lower() in x.lower(), output_dict.keys()) == []:
        output_dict = {dict_index: output_dict}
    
    output_folder = os.path.join(os.getcwd(), parameters["output_folder"])
    # This controls whether it write the json output to the output folder or not
        # if the output_folder specified in the settings is empty, then no output
    if parameters["output_folder"].strip() != "":
        if not(os.path.isdir(output_folder)):
            os.mkdir(output_folder)
        loaddict2jsonfile(output_dict, os.path.join(output_folder, filename+".json"))
