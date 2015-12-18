# -*- coding: utf-8 -*-
#!/usr/bin/env python

"""
@ author: Man Peng

This program puts all json files in folder, say, 'json_folder', containing
    square footage, stories, vintage information into one file, say, 'outputfile.csv'

Sample Usage:

>>> loadSomePropertyInfo2csv("json_folder", 'outputfile.csv') #remove!!!!
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

def createCSVfile(csvfile, header):
    if not(os.path.isfile(csvfile)):
        f = open(csvfile, 'a')
        f.write(header+"\n")
        f.close()

def write2csv(csvfile, header, line):
    createCSVfile(csvfile, header)
    if os.path.isfile(csvfile):
        f = open(csvfile, 'a')
        f.write(line+"\n")
        f.close()


def loadSomePropertyInfo2csv(jsonfolder, csvfile):
    jsonfiles = os.listdir(os.path.join(os.getcwd(), jsonfolder))
    cache = {}
    for jfile in jsonfiles:
        jinfo = loadJson(os.path.join(os.path.join(os.getcwd(), jsonfolder, jfile)))
        latestkey = max(jinfo.keys())
        if latestkey in cache:
            continue
        else:
            cache[latestkey]=1
            csvinfo_dict = {}
            try:
                csvinfo_dict['year_built'] = jinfo[max(jinfo.keys())]['year_built']
            except KeyError:
                csvinfo_dict['year_built'] = ""
            try:
                csvinfo_dict['stories'] = jinfo[max(jinfo.keys())]['stories']
            except KeyError:
                csvinfo_dict['stories'] = ""
            try:
                csvinfo_dict['gross_area_sqft'] = jinfo[max(jinfo.keys())]['GrossArea']
            except KeyError:
                csvinfo_dict['gross_area_sqft'] = ""
            try:
                csvinfo_dict['living_area_sqrt'] = jinfo[max(jinfo.keys())]['LivingArea']
            except KeyError:
                csvinfo_dict['living_area_sqrt'] = ""
            try:
                csvinfo_dict['physical_address'] = jinfo[max(jinfo.keys())]['physical_address']
            except KeyError:
                csvinfo_dict['physical_address'] = ""
            header = csvinfo_dict.keys()
            line = map(lambda x: csvinfo_dict[x], header)
            header = map(lambda x: '"'+x+'"', header)
            # The following is to remove the , in case it's there since this is written
                # into a csv file (comman deliminated file)
            line = map(lambda x: '"'+x+'"', line)
            ",".join(line)
            write2csv(csvfile, ",".join(header), ",".join(line))

