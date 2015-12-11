# -*- coding: utf-8 -*-
"""
@author: Man Peng
"""
# Define here the models for your scraped items
#
# See documentation in:
# http://doc.scrapy.org/en/latest/topics/items.html

from scrapy import Item, Field


class housePageItem(Item):
    # define the fields for your item here like:
    streetAddress = Field()
    county_last_updated = Field(serializer=str)
    features_last_updated = Field(serializer=str)
    city = Field()
    state = Field()
    zipcode = Field()
    property_basic_info = Field()
    property_dscription = Field()
    property_county_record = Field()
    property_features_record = Field()
    listing_type = Field()
    start_url = Field()

class PicItem(Item):
    # Field() is basically to create a dictionary like values to assign
    image_urls = Field()
    images = Field()
    title = Field()
    url = Field()
    last_updated = Field(serializer=str)
