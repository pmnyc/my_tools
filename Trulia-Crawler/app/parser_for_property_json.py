# -*- coding: utf-8 -*-
#!/usr/bin/env python

"""
@author: Man Peng

This program is mainly for transforming the unstructured property 
    data in json format into the structured data.

Sample Usage:
>>> mfile = "worcester_ma_0001.json"
>>> obj = property_parser(property_json_file=mfile)
    Next function returns the square footage info obj.sqft_
>>> obj.getSqft() 

"""

import os
import json
import re
import warnings

def loadJson(filename):
    json_data=open(filename,'r')
    data = json.load(json_data)
    json_data.close()
    return data

def getFulldirAddress(x):
    """ In case if the file is not a full address, append main directory
    information to it"""
    x_first10 = x[:10]
    if x_first10.find(":\\") >=0 or x_first10.startswith("/") or x_first10.find(":/") >=0:
        return x
    else:
        return os.path.join(os.getcwd(),x)

class property_parser(object):
    """ This is the class for parsing the json information
        scraped from the web-crawler on a trulia.com property
        webpage.

        You may either provide the single json file for the
            property or the property's inform in a single
            dict value (e.g. {"city":"Worceser", "property_county_record":["a","b"]})

        For Example:
            >>> obj = property_parser(property_json_file='mydata/myproperty.json')
            or
            >>> obj = property_parser(property_info = {'a':1,'b':2})
    """
    def __init__(self, property_json_file=None, property_info=None):
        #super(ClassName, self).__init__() #there is no class inheritance 
        # for example, 
        if (property_info == None and property_json_file == None) or \
            (property_info != None and property_json_file != None):
            raise IOError("Either property_json_file or property_info (a \
                    dictionary) must be provided. You can't miss both of those \
                    two arguments and have both arguments. It has to be ONLY \
                    ONE of them provided...")
        else:
            pass

        ### Load the whole property information
        if property_info == None:
            # here, use the class method to call the property info loading function below
            self.property_info_ = property_parser.propertyinfo(property_json_file)
        else:
            self.property_info_ = property_info

        ### Load Lists for property county records, basic info and property features record
        self.property_features_record_ = self.loadKeyValues('property_features_record')
        self.property_county_record_ = self.loadKeyValues('property_county_record')
        self.property_basic_info_ = self.loadKeyValues('property_basic_info')
        self.zipcode_ = self.loadKeyValues('zipcode')
        self.streetAddress_ = self.loadKeyValues('streetAddress')
        self.city_ = self.loadKeyValues('city')
        self.state_ = self.loadKeyValues('state')
        self.listing_type_ = self.loadKeyValues('listing_type')
        self.features_last_updated_ = self.loadKeyValues('features_last_updated')
        self.property_dscription_ = self.loadKeyValues('property_dscription')
        self.county_last_updated_ = self.loadKeyValues('county_last_updated')
        self.http_address_ = self.loadKeyValues('http_address')
        self.full_address_ = self.streetAddress_+", "+self.city_+", "+self.state_+", "+ \
                    self.zipcode_

    def loadKeyValues(self, key):
        ### Load Lists for property county records, basic info and property features record
        try:
            x = self.property_info_[key]
        except KeyError:
            print("%s does not exist in the property information ..." %key)
            x = None
        return x

    @staticmethod
    def getFulldirAddress(x):
        """ In case if the file is not a full address, append main directory
        information to it"""
        x_first10 = x[:10]
        if x_first10.find(":\\") >=0 or x_first10.startswith("/") or x_first10.find(":/") >=0:
            return x
        else:
            return os.path.join(os.getcwd(),x)

    @classmethod
    def propertyinfo(cls, mfile):
        """
        mfile is the raw json file scraped from trulia.com webpage
        
        The returned result property_info is the dict for the raw json
            file scraped from the webpage
        """
        property_info = loadJson(getFulldirAddress(mfile))
        return property_info

    ######################################################################
    ### The following is the list of parsers for scraping each component of
        # property information from the trulia.com property webpages
    def getSqft(self):
        def matchsqft(x):
            try:
                x2 = re.match(r'\d+ sqft', x.replace(",",""))
                x3 = x2.group(0)
                x4 = int(x3.lower().replace("sqft",""))
                return x4
            except:
                return None

        try:
            sqft1 = filter(lambda x: x != None, map(matchsqft, self.property_basic_info_))[0]
        except:
            sqft1 = None
        try:
            sqft2 = filter(lambda x: x != None, map(matchsqft, self.property_county_record_))[0]
        except:
            sqft2 = None
        try:
            sqft3 = filter(lambda x: x != None, map(matchsqft, self.property_features_record_))[0]
        except:
            sqft3 = None

        if sqft1 >0:
            self.sqft_ = sqft1
        elif sqft2 >0:
            self.sqft_ = sqft2
        elif sqft3 >0:
            self.sqft_ = sqft3
        else:
            self.sqft_ = None
            warnings.warn("Square Footage Information is missing...")

