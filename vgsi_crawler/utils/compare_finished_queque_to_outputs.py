# -*- coding: utf-8 -*-
#!/usr/bin/env python

"""
@author: Man Peng

This program is to compare the links in the queue file (links_crawled_queue.csv)
    to the links in all files in the folder output_bucket to get the links
    that are actually not processed but somehow got in the finished queue.
    This will help us process these links later on.

Just run the file in the main directory, it will print out the files you need
    to pay attention to.
"""

import os
import numpy as np

# load local files
from utils.load_settings import loadParameters
from utils.load_settings import loadJson

param = loadParameters()
output_bucket = param["output_bucket"]
finished_queue_file = param["links_crawled_queue"]

## get the links in queque that are supposed to be done
f = open(finished_queue_file, 'r')
links_done = f.readlines()
links_in_queque = map(lambda x: x.replace(u"\n",""), links_done)
f.close()

## find the links for all files in the output folder/bucket
links_done = []
files = os.listdir(output_bucket)
for f in files:
    file_info = loadJson(output_bucket+"/"+f)
    link = str(file_info['http_address'])
    links_done.append(link)

links_diff = np.setdiff1d(links_in_queque, links_done)
links_diff = list(links_diff)

for link in links_diff:
    print("The links shown in finished queue but not in output bucket/folder are \n%s" %link)

