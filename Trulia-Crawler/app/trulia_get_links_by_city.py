"""
@author: Man Peng

This program is to extract the addresses by city through
    the coordinate meshed grids.
It calls the Google Maps API (see app/googlemapsapi) to
    get the boudaries for each town, then meshed into
    grids for Trulia to use on zoom level (currently) 17
    in order to obtain the property link address on web for
    future parsing purpose.

Sample Usage:
>>> city = "worcester, ma"
>>> getAddressbyCity(city)

"""

import pprint
import requests
import time
import numpy as np
import os
from fnmatch import fnmatch
from app.googlemapsapi import createMeshGrids
from utils.rotate_user_agent import randomUserAgent
from utils.load_settings import loadParameters
from utils.transform_links_dict_tojson import easy_json
from utils.load_settings import loadJson
from utils.merge2json import merge2dict
from utils.export_link2allcachedfile import exportLink2cache
from utils.remove_duplicates_in_arraycsvfile import unqiueList

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
    #pprint.pprint("Processing the city/town: %s ... " %town.replace(",",", "))
    return town

def createFolder(folder):
    """ Create the folder if it does not exist"""
    if not(os.path.isdir(folder)):
        os.mkdir(folder)

def getAddressbyCity(city, download_dir=None):
    """ This program is to
        1) Get the coordinate boundaries through the GoogleMapsAPI for a city
        2) Extract the webpage link addresses for each property within each box

    Sample Input:
        city='Worcester,MA'
        download_dir="app/data"

    download_dir specifies which folder to save resulting links for webpages
    """
    city = proessCityName(str(city), space_substitute=" ")
    param = loadParameters()
    if download_dir is None:
        download_dir = param["property_webpage_link_storeage_folder"]
    download_dir = os.path.join(os.getcwd(),download_dir)
    createFolder(download_dir)
    mesh_grids = createMeshGrids(city)

    # proxies = {
    #     "http": "http://nmpc\myuser:temppwd((@192.168.85.13:8080",
    #     "https": "http://nmpc\myuser:temppwd((@192.168.85.13:8080",
    #     }
    
    link_pattern = proessCityName(city, space_substitute=",")
    link_pattern_list = link_pattern.lower().split(",")
    link_pattern = "*-" + "-".join(link_pattern_list) + "-*"
    linked=[]
    counter = 0

    # get the map zoom level
    zoom_level = param["map_zoom_level"]
    # set download delay
    download_delay = param["download_delay_for_extracting_links"]

    cnt = 1
    for box in mesh_grids:
        # Show status of mesh grid search process
        print("Downloading the %s of %s mesh grids in the city of %s ..." %(str(cnt), str(len(mesh_grids)), city))
        cnt += 1
        
        # user_agent is for preventing being banned by website
        user_agent = randomUserAgent()
        box_ = ",".join(map(lambda x: str(x),box))
        adr='http://www.trulia.com/for_sale/'+city+'/'+zoom_level+'_zm/'+box_+'_xy/map_v'  
        r = requests.get(adr, headers={'User-Agent':user_agent}) # or add proxies=proxies if proxy is needed
        text_ = r.text
        text_ = text_ + "" # dummy step
        if len(text_) < 200:
            raise Exception("Downloading Map webpage failed for user agent %s" %user_agent)
        try:
            time.sleep(download_delay)  # This makes 1 second delay to make sure not to push too
                    # too hard to get info from the Trulia server
            ind0=text_.index('results:')
            txtp=text_[ind0:]
            ind1=txtp.index('};')
            tp= txtp[:ind1].replace('results:','')+'}'
            tps=filter(lambda x: x.startswith('"pdpURL":'),tp.split(','))
            ## get webpage links from the request
            def getLinks(tpsu):
                link_ = tpsu.replace('"pdpURL":','').replace('"','').replace('\\','')
                link_ = str(link_)
                # print("Processing %s ..." %link_)
                exportLink2cache("http://www.trulia.com"+link_)
                if fnmatch(link_.lower(),link_pattern.lower()):
                    linked.append(link_)
                    if counter < 1:
                        # print the first 1 results
                        pprint.pprint("Some property webpage links are "+linked[-1])
                        counter += 1
                    else:
                        pass
                else:
                    pass
            map(getLinks, tps)
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
    outfile_name = os.path.join(download_dir,outfile_name+'.json')
    # merge2json.loaddict2jsonfile(links_dict,outfile_name)
    # If the file already exisits, then insert newly added info to it
    if os.path.isfile(outfile_name):
        link_dict_old = loadJson(outfile_name)
        easy_json(links_dict, outfile_name)
        link_dict_new = loadJson(outfile_name)
        merge2dict(link_dict_new, link_dict_old, outfile_name)
    else:
        easy_json(links_dict, outfile_name)
    
    # Remove duplicates in the all_links_cached.csv files
    unqiueList(param["all_links_cached"])

