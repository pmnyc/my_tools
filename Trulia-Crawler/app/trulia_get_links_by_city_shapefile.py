"""
@author: Man Peng; Liming Zhou

This program is to extract the addresses by city through
    the coordinate meshed grids

Sample Usage:
>>> city = "worcester, ma"
>>> shapefile = os.path.join(os.getcwd(),"app/geomesh/gridpoly.shp")
>>> getAddressbyCity(city, shapefile)

, where shapefile is the shape file for Worcester, MA
"""

import pprint
try:
    import fiona
except:
    print("package fiona is not installed...")
    pass
import requests
import time
import numpy as np
import os
from fnmatch import fnmatch
from utils import merge2json

## Get current time stamp ##
def timeStamp():
    """returns a formatted current time/date"""
    #sample: 'Tue 18 Aug 2015 11:13:41 AM'
    #str(time.strftime("%a %d %b %Y %I:%M:%S %p"))
    return str(time.strftime("%Y-%m-%d"))

def proessCityName(city, space_substitute="_"):
    """ This funciton is to standardize the name of city and state
    For example, it will return "Los Angeles,CA" if city is given as
        "  los    angeles, ca "
    """
    
    def makeFirstLetterUpper(x):
        if x.find(' ') >=0:
            raise Exception('Name '+x+' should not have blank space!')
        x2 = x.lower()
        return x2[:1].upper() + x2[1:]
    
    space_count = city.count(" ")
    for i in range(space_count):
        city = city.strip().replace("  "," ").replace(" ,",",").replace(", ",",")
    town = city
    state = town[(town.index(",")+1):]
    town = town.replace(","+state,","+state.upper())
    city_ = town[:(town.index(","))]
    city_words = city_.split(' ')
    city_words= map(makeFirstLetterUpper,city_words)
    city_new = space_substitute.join(city_words)
    town= town.replace(city_,city_new)
    
    pprint.pprint("Processing the city/town: %s ... " %town.replace(",",", "))
    return town

def createFolder(folder):
    """ Create the folder if it does not exist"""
    if not(os.path.isdir(folder)):
        os.mkdir(folder)

def getAddressbyCity(city, shapefile, download_dir="app/data"):
    """ This program is to
        1) Get the meshed coordinate boxes through the shape file for a city
        2) Extract the webpage link addresses for each property within each box

    Sample Input:
        city='Worcester,MA'
        shapefile='app/geomesh/worcesterma.shp'

    download_dir specifies which folder to save resulting links for webpages
    """
    download_dir = os.path.join(os.getcwd(),download_dir)
    createFolder(download_dir)
    coord_box=[]
    with fiona.open(shapefile) as src:
        #add range to index src
        # print first 50 addresses
        counter = 0
        for tt in src:
            tmp=tt['properties']
            coord_box.append(str(tmp['Y_MIN'])+','+str(tmp['Y_MAX'])+','+str(tmp['X_MIN'])+','+str(tmp['X_MAX']))
            if counter < 50:
                pprint.pprint("Some coordinate boxes are " + str(coord_box))
                counter += 1
            else:
                pass

    # proxies = {
    #     "http": "http://nmpc\myuser:temppwd((@192.168.85.13:8080",
    #     "https": "http://nmpc\myuser:temppwd((@192.168.85.13:8080",
    #     }

    city = proessCityName(city)
    link_pattern = proessCityName(city, space_substitute=",")
    link_pattern_list = link_pattern.lower().split(",")[-2:]
    link_pattern = "*-" + "-".join(link_pattern_list) + "-*"
    linked=[]
    counter = 0
    for box in coord_box:
        adr='http://www.trulia.com/for_sale/"'+city+'/18_zm/'+box+'_xy/map_v'  
        r = requests.get(adr) # or add proxies=proxies if proxy is needed
        try:
            ind0=r.text.index('results:')
            txtp=r.text[ind0:]
            ind1=txtp.index('};')
            tp= txtp[:ind1].replace('results:','')+'}'
            tps=filter(lambda x: x.startswith('"pdpURL":'),tp.split(','))
            for tpsu in tps:
                link_ = tpsu.replace('"pdpURL":','').replace('"','').replace('\\','')
                if fnmatch(link_,link_pattern):
                    linked.append(link_)
                    if counter < 50:
                        # print the first 50 results
                        pprint.pprint("Some property webpage links are "+linked[-1])
                        counter += 1
                    else:
                        pass
                else:
                    continue
        except:
           pass
        #rx=requests.get('http://www.trulia.com/'+tps[0].replace('"pdpURL":','').replace('"','').replace('\\',''),proxies=proxies)
    link_header = "http://www.trulia.com"
    linked = list(set(np.array(linked))) #remove duplicate addresses
    links = map(lambda x: link_header+x, linked)
    links_dict = {"city":proessCityName(city, space_substitute=" ")}
    links_dict['update_date']= timeStamp()
    links_dict['links']= links

    outfile_name = proessCityName(city, space_substitute="_")
    outfile_name = outfile_name.lower().replace(",","_")
    merge2json.loaddict2jsonfile(links_dict,os.path.join(download_dir,outfile_name+'.json'))
