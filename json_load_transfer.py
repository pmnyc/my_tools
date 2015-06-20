# -*- coding: utf-8 -*-
"""
Load Simple JSON configuration
@author: pm

---------------------
Sample Usage:
import loadJson
json_config = loadJson.loadJson("config.json")
---------------------

To get output:
print json_config['maps'][0]['id'] #(because json_config['maps'] is list of two dictionaries)
print json_config['masks']['id']
print json_config['par3']

Example: JSON file is config.json
{
"maps":[{"id":"id1","value":"0"},{"id":"id2","value":"1"}],
"masks":{"id":"id_mask"},
"om_points":"value",
"par3": 1
}


Next program is to load one Json info into another Json file
    Remark: Both from and to json files already exist
---------------------
Sample Usage:
>>> import json_load_transfer
>>> json_load_transfer.transferJsonInfo(fromjson = 'myfrom.json', tojson = 'myto.json')

If this program is put in another folder, say, utilities, then put an emptpy __init__.py file in that folder
    and use
>>> from utilities import json_load_transfer
---------------------
"""

import json

__author__ = 'pm'

def loadJson(filename):
    json_data=open(filename,'r')
    data = json.load(json_data)
    json_data.close()
    return data

def transferJsonInfo(fromjson, tojson):
    def loadJson(filename):
        json_data=open(filename,'r')
        data = json.load(json_data)
        json_data.close()
        return data

    try:
        fromdata = loadJson(fromjson)
    except Exception as e:
        fromdata = {}
    try:
        feeds = loadJson(tojson)
    except Exception as e:
        feeds = {}

    with open(tojson, mode='w') as feedsjson:
        for keys, items in fromdata.items():
            feeds[keys] = items
        json.dump(feeds, feedsjson, indent=4)
