# -*- coding: utf-8 -*-
#!/usr/bin/env python

"""
@author: Man Peng

This program moves the list of cities we finished running geomesh on to the 
    list of cities that are still waiting for being processed.

Sample Usage:
$ python organize_city_list.py
"""


from numpy import genfromtxt
import os, numpy as np
from fnmatch import fnmatch
from utils.load_settings import loadParameters
from utils.processcityname import proessCityName

def getFulldirAddress(x):
    """ In case if the file is not a full address, append main directory
    information to it"""
    x_first10 = x[:10]
    if x_first10.find(":\\") >=0 or x_first10.startswith("/") or x_first10.find(":/") >=0:
        return x
    else:
        return os.path.join(os.getcwd(),x)

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


def organizeCityList():
    """ This function moves the names of the cities geomesh processed to the list for processed one """
    param = loadParameters()
    city_list_file = param["city_list"]
    cities_done_file = param["cities_done_with_property_link_extraction"]
    city_list_file = os.path.join(os.getcwd(), city_list_file)
    cities_done_file = os.path.join(os.getcwd(), cities_done_file)

    city_list = genfromtxt(city_list_file, dtype="unicode", delimiter="\n")
    city_list = map(lambda x: proessCityName(x, space_substitute=" "), city_list)

    links_data_folder = getFulldirAddress(param['property_webpage_link_storeage_folder'])
    links_files = os.listdir(links_data_folder)
    links_files = filter(lambda x: x.endswith(".json") and x.find("20")<0, links_files)
    city_processed = map(reverse_link_file_name_2_city, links_files)
    city_still_not_processed = list(np.setdiff1d(city_list, city_processed))

    # write the city procssed and cities not processed to the files in queue
    np.savetxt(cities_done_file, city_processed,  fmt='%s')
    np.savetxt(city_list_file, city_still_not_processed,  fmt='%s')


if __name__ == '__main__':
    try:
        organizeCityList()
    except Exception as e:
        print(str(e))
        print("The moving of finished and unfinished city list failed!!")

