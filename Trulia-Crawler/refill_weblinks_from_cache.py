# -*- coding: utf-8 -*-
#!/usr/bin/env python

"""
@author: Man Peng

This program fills in the missing webpage links from the all_links_cached.csv
    file. This is done after the progrma for generating the webpage link files.

Sample Usage:
$ python refill_weblinks_from_cache.py
"""


from numpy import genfromtxt
import numpy as np
import os
import re
from utils.load_settings import loadParameters
from utils.processcityname import proessCityName
from fnmatch import fnmatch
from utils.load_settings import loadJson
from utils.load_settings import loaddict2jsonfile


def getFulldirAddress(x):
    """ In case if the file is not a full address, append main directory
    information to it"""
    x_first10 = x[:10]
    if x_first10.find(":\\") >=0 or x_first10.startswith("/") or x_first10.find(":/") >=0:
        return x
    else:
        return os.path.join(os.getcwd(),x)

def reverse_link_keyname_2_city(name):
    """
    This function is to reverse the link key names in the property links file
        back to the starndarized city name
    sample input
        name = 'worcester_ma_2015-10-02'
        -- expected return from this function is Worcester,MA
    """
    match_ = re.findall(r'_20\d+\-\d+\-\d+', name)[0]
    city = name.replace(match_,"")
    city_words = city.split("_")
    city_1 = city_words[:-1]
    state = city_words[-1]
    city = " ".join(city_1)+","+state
    city = proessCityName(city, space_substitute=" ")
    return city

def reverse_link_keyname_2_date(name):
    """
    This function is to reverse the link key names in the property links file
        back to the date when it was processed
    sample input
        name = 'worcester_ma_2015-10-02'
        -- expected return from this function is 2015-10-02
    """
    match_ = re.findall(r'_20\d+\-\d+\-\d+', name)[0]
    date = match_ = re.findall(r'20\d+\-\d+\-\d+', match_)[0]
    return date

def reverse_link_file_name_2_city(name):
    """
    This function is to reverse the link file for properties
        back to the starndarized city name
    sample input
        name = 'worcester_ma.json'
        -- expected return from this function is Worcester,MA
    """
    cityname = os.path.splitext(name)[0]
    city_words = cityname.split('_')
    city_1 = city_words[:-1]
    state = city_words[-1]
    city = " ".join(city_1)+","+state
    city = proessCityName(city, space_substitute=" ")
    return city

def addLinksfromCached2LinksFile(city, links_file, all_links_cached):
    """
    This function is to fill the missing links in the all_links_cahched.csv
        file into the links_file.
    
    Sample Inputs    
    
    city="Worcester,MA"
    links_file = 'worcester_ma.json'
    all_links_cached = 'queue/all_links_cached.csv'
    """
    param = loadParameters()
    links_array = genfromtxt(getFulldirAddress(all_links_cached), delimiter='\n', dtype="unicode")
    try:
        links_array = list(links_array)
    except:
        links_array = [str(links_array)]
    
    links_array = np.unique(np.array(links_array))
    links_array = filter(lambda t: fnmatch(t, "*"+ city.replace(",","-").replace(" ","-").replace("_","-") +"*"), 
                         links_array)
    
    link_file_info = loadJson(getFulldirAddress(param['property_webpage_link_storeage_folder']+"/"+links_file))
    last_key = max(link_file_info.keys())
    link_file_info_ = link_file_info[last_key]
    
    links_new = np.setdiff1d(links_array, link_file_info_)
    link_file_info[last_key] = list( map(lambda x: str(x), np.hstack((link_file_info_, links_new))) )
    
    loaddict2jsonfile(link_file_info, getFulldirAddress(param['property_webpage_link_storeage_folder']+"/"+links_file))

def refillMissingLinksfromCache():
    """
    This function scans the webpage link files 
    """
    param = loadParameters()
    links_data_folder = getFulldirAddress(param['property_webpage_link_storeage_folder'])
    links_files = os.listdir(links_data_folder)
    links_files = filter(lambda x: x.endswith(".json") and x.find("20")<0, links_files)

    all_links_cached = param['all_links_cached']

    for links_file in links_files:
        city = reverse_link_file_name_2_city(links_file)
        addLinksfromCached2LinksFile(city, links_file, all_links_cached)

if __name__ == "__main__":
    #import sys
    refillMissingLinksfromCache()

