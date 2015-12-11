# -*- coding: utf-8 -*-
#!/usr/bin/env python

"""
@author: Man Peng

This program is for extracting property status such as "For Sale", "Sold" and "Foreclosure"
    from the file that stores the webpage links.
    Status can be analyzed from the links.

The corresponding file storing webpage links must exist first, for example, in order to
    get the file  worcester_ma_property_status.json, the file  worcester_ma.json
    must exist first.

Sample Usage:
$ python create_property_status_from_weblinks.py -c "worcester,ma"
"""


import numpy as np
import os
from generate_links_by_city import getListofHttpLinks
from generate_links_by_city import getHttpLinksUpdateDate
from utils.processcityname import proessCityName
from utils.merge2json import loaddict2jsonfile
from utils.load_settings import loadParameters
from utils.load_settings import loadJson


def getAddressFromTruliaLink(link, city):
    """
    for example,
    link = "http://www.trulia.com/homes/Massachusetts/Worcester/sold/1787371-319-Lovell-St-Worcester-MA-01602"
    The function will return city name, street address, full addresss.
    """
    cityname = proessCityName(city, space_substitute=" ")
    address_inlist = link.split("/")[-1].split("-")[1:]
    city_state_inlist = cityname.replace(","," ").replace("  "," ").split(" ")
    street_inlist = address_inlist[:(len(address_inlist)-len(city_state_inlist)-1)]
    
    zipcode = address_inlist[-1]
    state = address_inlist[-2]
    city = cityname[:cityname.index(',')]
    street_address = " ".join(street_inlist)
    
    full_address = street_address + ", " + city + ", " + state + " " + zipcode
    out_ = {"full_address":full_address,
           "street_address":street_address,
           "city": city,
           "state": state,
           "zipcode": zipcode }
    return out_

def getPropertyStatus(link):
    """
    This is to get the property status based on the link address.
    Three types are "For Sale", "Sold" and "Foreclosure"
    """
    if "trulia.com/homes/" in link:
        return "Sold"
    elif "trulia.com/property/" in link:
        return "For Sale"
    elif "trulia.com/foreclosure/" in link:
        return "Foreclosure"
    else:
        return ""


def createpropertystatus(city):
    """
    This function is to dump the property status dict to the json file
        in the same folder as the file storing all webpage links
    """

    links = np.array(getListofHttpLinks(city))
    lastest_update_date = getHttpLinksUpdateDate(city)
    keyname = proessCityName(city, space_substitute="_").lower().replace(",","_") \
                + "_" + lastest_update_date
    city_properties = {keyname:[]}

    for link in links:
        output_dict = {}
        output_dict["webpage_link"] = link
        output_dict["property_status"] = getPropertyStatus(link)
        linkinfo = getAddressFromTruliaLink(link, city)
        for k in linkinfo.keys():
            output_dict[k] = linkinfo[k]
        city_properties[keyname] += [output_dict]

    param = loadParameters()
    property_status_storage_folder = param['property_webpage_link_storeage_folder']
    property_status_storage_folder = os.path.join(os.getcwd(),property_status_storage_folder)

    filename_ = proessCityName(city, space_substitute="_")
    filename_ = filename_.lower().replace(",","_") + "_property_status.json"
    filename_ = os.path.join(property_status_storage_folder, filename_)

    if os.path.isfile(filename_):
        property_file_info = loadJson(filename_)
    else:
        property_file_info = {}

    property_file_info[keyname] = city_properties[keyname]
    loaddict2jsonfile(property_file_info, filename_)

if __name__ == '__main__':
    import sys
    argvs = sys.argv
    argvs_lower = map(lambda t: t.lower(), argvs)
    if '-c' not in argvs_lower:
        raise StandardError("It needs option -c to specify the city you need to extract property status information!!")
    else:
        pass
    city = argvs[argvs_lower.index("-c")+1]
    city = str(city)
    createpropertystatus(city)

