# -*- coding: utf-8 -*-
#!/usr/bin/env python
"""
@author: Man Peng

This program is to extract the boundaries of a city using Google Maps API

The Google Maps Geocoding API has the following limits in place:
    Standard Usage limits
    Users of the standard API:
        2,500 free requests per day
        10 requests per second

By default, the parameter_file specified below is the json file storing some
    private key info and manifest info. Here, the default
        parameter_file = "config/parameters.json"

Sample Usage:
>>> city = " worcester,    ma "
>>> loadGoogleMapsAPI(city)
, it returns the xmin, xmax, ymin, ymax of boundary box (lat long coordinates)
>>> mesh_grids = createMeshGrids(city)
"""

import json
import os
import urllib
from time import sleep
from utils.processcityname import proessCityName
from utils import get_coordinate_intervals


def loadJson(filename):
    json_data=open(filename,'r')
    data = json.load(json_data)
    json_data.close()
    return data

def loadgoogleapikey(paremeter_file):
    loc = os.path.join(os.getcwd(),paremeter_file)
    setting = loadJson(loc)
    return setting["google_api_key"]

def loadGoogleMapsAPI(city, parameter_file = "config/parameters.json"):
    """ First specify the parameter file storing the Google Maps Geocoding
        API key, which is config/parameters.json
    """
    api_key = loadgoogleapikey(parameter_file)
    googlemap_link = "https://maps.googleapis.com/maps/api/geocode/json?address={city}&key={apikey}"
    _city = proessCityName(city, space_substitute="+")
    _city = _city.replace(",",",+")
    url = googlemap_link.format(city=_city,apikey=api_key)
    url_ = urllib.urlopen(url)
    out = json.load(url_)
    url_.close()
    error_message = "Google Maps API did not return a result for %s" %proessCityName(city,space_substitute=" ")
    if out['status'] != "OK":
        raise Exception(error_message)
    else:
        pass
    out_2 = out['results']
    out_3 = out_2[0]
    locality_type = out_3['types']
    """
    # It is little dangerous to close this opiton for checking locality, but just make sure input city name is good enough
        # I closed it because I wasn't sure if there are other possible locality types I didn't account for.
    
    if "locality" not in locality_type and "administrative_area_level_3" not in locality_type and "sublocality" not in locality_type:
        raise Exception(error_message)
        # because if "administrative_area_level_1" is returned
            # in the types, that means it is on the state level
            # locality means the result is at least on city/town
            # level
    """
    bounds = out_3['geometry']['bounds']
    ne = bounds['northeast']['lat'], bounds['northeast']['lng']
    sw = bounds['southwest']['lat'], bounds['southwest']['lng']
    box = {'xmin':sw[0], 'xmax':ne[0], 'ymin':sw[1], 'ymax':ne[1]}
    return box

def getMeshGridSize(file_="config/parameters.json"):
    setting = loadJson(os.path.join(os.getcwd(),file_))
    lat_interval_length = setting["latitude_mesh_grid_size"]
    long_interval_length = setting["longitude_mesh_grid_size"]
    return (lat_interval_length, long_interval_length)

def createMeshGrids(city):
    """
    This function creates the mesh grids for the putting Trulia map link 
        address at zoom 18 level.
    Sample input:
        city = " worcester, ma"
    """
    x_y_interval_lengths = getMeshGridSize()
    lat_interval_length = x_y_interval_lengths[0]
    long_interval_length = x_y_interval_lengths[1]
    city_boundary = loadGoogleMapsAPI(city)
    # This is set the delay of running following codes by 0.1 second
        # This is useful for not trigging other servers to think
        # this program is attacking them
    sleep(0.1)
    cityname = proessCityName(city, space_substitute=" ")
    if type(city_boundary) is not dict:
        raise Exception("Google Map API call failed for %s. \
            The reasons could be either city name %s is spelled wrong, \
            or the Google Maps API calls reached daily limit..." \
            %(cityname, cityname))
    x_range = (city_boundary['xmin'],city_boundary['xmax'])
    lat_intervals = get_coordinate_intervals.getIntervals(x_range,lat_interval_length)
                # the buffer_size = 0.2 means the overlap accounts for 20% of the interval
    y_range = (city_boundary['ymin'],city_boundary['ymax'])
    long_intervals = get_coordinate_intervals.getIntervals(y_range,long_interval_length)
                # the buffer_size = 0.2 means the overlap accounts for 20% of the interval
    mesh_grids = get_coordinate_intervals.createXminXmaxYminYmax(lat_intervals, long_intervals)
    return mesh_grids
