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
"""

import json
#from pprint import pprint
def loadJson(filename):
    json_data=open(filename,'r')
    data = json.load(json_data)
    #pprint(data)
    json_data.close()
    return data

