# -*- coding: utf-8 -*-
#!/usr/bin/env python

"""
@author: Man Peng

This program loads the json info for the Trulia links in an easy way, i.e.
        each key stores all links info for one download, and the key is of the format
        'worcester_ma_2015-09-12', hence one may identify the town and update date
        from the key name

This program includes the random hash key generation for storing data, but it
    is not recommended to use to make program more complex in future.

linkinfo is the dict with keys [u'city', u'links', u'update_date']

Sample Usage:
>>> easy_json(linkinfo, 'output.json')
"""

import json
import random, string
from utils.load_settings import loadJson


def random_md5like_hash(length=24):
    # available_chars= string.hexdigits[:16] # this is only 0123456789abcdef
    available_chars= string.digits + string.ascii_lowercase # this is '0123456789abcdefghijklmnopqrstuvwxyz'
    return ''.join(map(lambda t: random.choice(available_chars), range(length)))


def loaddict2jsonfile(dic, tojson_filename):
    """
    This function loads a dic into tojson_filename file
    loaddict2jsonfile(my_dictionary, 'myjson.json')
    """
    with open(tojson_filename, mode='w') as feedsjson:
      json.dump(dic, feedsjson, indent=4)


def add_extra_info_to_json(jsonfile, http_address, field_to_add="http_address"):
    """
    This function is specifically JUST for adding the http link address to the 
        json file dumped out from the web-cralwer
    """
    jsoninfo = loadJson(jsonfile)

    if type(jsoninfo) is list:
        jsoninfo = jsoninfo[0]

    jsoninfo['http_address'] = http_address
    loaddict2jsonfile(jsoninfo, jsonfile)


def complex_json(linkinfo, tojson_filename):
    """
    This program loads the json info for the Trulia links to a more comprehensive
        and complex way by using hash keys
    linkinfo is the dict info by grabbing all links for the city through geomesh
    tojson_filename is the json file name for dumping all results to
    """
    linkinfo_2={}
    hash_key_value = random_md5like_hash()
    linkinfo_2['index_keys'] = ['city','update_date','hash_key']
    linkinfo_2['index_values'] = [linkinfo['city'],linkinfo['update_date'],hash_key_value]
    linkinfo_2[hash_key_value] = linkinfo['links']
    linkinfo_3={'Description':"Link data are referred by a 24-bit hash key. \
                    This hash key is unique up to the pair (city ,update_date)",
                'Hash_Key_Identifier': ['city','update_date'],
                "Data": linkinfo_2}
    loaddict2jsonfile(linkinfo_3, tojson_filename)


def easy_json(linkinfo, tojson_filename):
    """
    This program loads the json info for the Trulia links in an easy way, i.e.
        each key stores all links info for one download, and the key is of the format
        'worcester_ma_2015-09-12', hence one may identify the town and update date
        from the key name
    linkinfo is the dict info by grabbing all links for the city through geomesh
    tojson_filename is the json file name for dumping all results to
    """
    data_key = linkinfo['city'].lower().replace(',','_').replace(' ','_') + '_' +\
            linkinfo['update_date']
    linkinfo_2={}
    linkinfo_2[data_key] = linkinfo['links']
    loaddict2jsonfile(linkinfo_2, tojson_filename)
