#!/usr/bin/env python

"""
@author: Man Peng

This program is for generating files for storing http addresses
    for propreties given the file listing the cities/towns to run

Sample Usage:
>>> python generate_links_by_city.py
"""

import os
import re
import numpy as np
from app import trulia_get_links_by_city
from utils.processcityname import proessCityName
from utils.load_settings import loadParameters
from utils.load_settings import loadJson


def process_citylist(myfile):
    """ get links for properties in the city if the list of cities is given in 
        myfile
    """
    # Sample Input
    # myfile = 'queue/city_list.txt'
    list_ = np.genfromtxt(os.path.join(os.getcwd(),myfile), delimiter='\n', dtype="unicode")
    
    try:
        list_ = list(list_)
    except:
        list_=[str(list_)]
    
    list_ = filter(lambda x: len(x.strip()) >0, list_)
    list_ = map(lambda x: proessCityName(x, space_substitute=" "), list_)
    list_ = map(lambda x: str(x), list_)

    ## run by each city, if one fails, move on to the next one
    for city in list_:
        try:
            trulia_get_links_by_city.getAddressbyCity(city)
        except Exception as e:
            print(str(e))
            continue


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


def getListofHttpLinks(city):
    """
    This function is for obtaining the list of all http links for the properties
        listed by Trulia in the city/town
    Sample input:
    city = "worcester, ma"
    """
    city_ = proessCityName(city, space_substitute="_")
    filename = city_.replace(",","_").replace(" ","_").lower()+".json"
    param = loadParameters()
    datafolder = param['property_webpage_link_storeage_folder']
    file_ = os.path.join(os.getcwd(),datafolder,filename)
    if not(os.path.isfile(file_)):
        raise IOError("File %s does not exist for %s !!" %(filename, city_))
    else:
        pass
    property_link_file = loadJson(file_)

    ## Get the latest update ##
    keys = property_link_file.keys()
    latest_key = max(keys)
    links_list = property_link_file[latest_key]
    return links_list

def getHttpLinksUpdateDate(city):
    """
    This function is for obtaining the latest update of the list of http links for the properties
        listed by Trulia in the city/town
    Sample input:
    city = "worcester, ma"
    """
    city_ = proessCityName(city, space_substitute="_")
    filename = city_.replace(",","_").replace(" ","_").lower()+".json"
    param = loadParameters()
    datafolder = param['property_webpage_link_storeage_folder']
    file_ = os.path.join(os.getcwd(),datafolder,filename)
    if not(os.path.isfile(file_)):
        raise IOError("File %s does not exist for %s !!" %(filename, city_))
    else:
        pass
    property_link_file = loadJson(file_)

    ## Get the latest update ##
    keys = property_link_file.keys()
    latest_key = max(keys)
    date = latest_key.replace(filename.replace(".json","")+"_","")
    return date

if __name__ == '__main__':
    param = loadParameters()
    file_ = param["city_list"]
    process_citylist(file_)

