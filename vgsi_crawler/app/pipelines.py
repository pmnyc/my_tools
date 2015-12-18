# -*- coding: utf-8 -*-
"""
@author: Man Peng
"""
# Define your item pipelines here
#
# Don't forget to add your pipeline to the ITEM_PIPELINES setting
# See: http://doc.scrapy.org/en/latest/topics/item-pipeline.html


class MyCrawlerPipeline(object):
    def process_item(self, item, mybase):
        return item
