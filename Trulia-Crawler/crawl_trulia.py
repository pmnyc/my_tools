# -*- coding: utf-8 -*-
#!/usr/bin/env python

"""
@author: Man Peng

This program calls spyder Trulia_by_url to scrape infomation for each link
    of property provided.

Sample Usage:
$ python crawl_trulia.py -c "Worcester, MA" -l False -n 150

Option -c specifies the city to run

Options -l and -n are optional.
Option -l is bolean specifying whether to run geomesh to get all http links for the 
    city or not. Default value is False, which needs one to run
    $ python generate_links_by_city.py *** before
Option -n specifies how many properties in the property http-links file (given the city)
    to run. Default value is large enough to run all links.
"""

import os, subprocess
import numpy as np
import shutil
import generate_links_by_city
from datetime import datetime
import re
from utils.load_settings import loadParameters
from utils.pickledata import createFolder
from utils.pickledata import createFile
from utils.transform_links_dict_tojson import random_md5like_hash
from utils.transform_links_dict_tojson import add_extra_info_to_json
from utils.processcityname import proessCityName


"""
The following function is deprecated

def writeLinks2processedQuequ(link, quequ_file):
    #This function creates the queque csv file if it does not exist
    #    Once the link http address is given, it will record the result to
    #    links_crawled_queue_file file
    #Sample Input:
    #link = "http://trulia.com/***"
    #quequ_file = links_crawled_queue_file
    with open(quequ_file,'a') as f:
        f.writelines('%s\n' %link)
        f.close()
"""

def writeText2File(loginfo, mfile):
    """
    This function writes the log message to the file
    """
    with open(mfile,'a') as f:
        f.writelines('%s\n' %loginfo)
        f.close()

def linksinqueque(links_crawled_queue_file):
    f = open(links_crawled_queue_file,'r')
    linksinqueque = f.readlines()
    linksinqueque = map(lambda x: x.replace(u'\n',''), linksinqueque)
    linksinqueque = filter(lambda x: len(x.strip()) >0, linksinqueque)
    f.close()
    return linksinqueque


def craw_city(city, extract_http_links = False, max_num_properties_to_process=10**8):
    ## This if-then will extract all http links for the properties of the city ##
    ## if extract_http_links is defined True ##
    ## Be aware that this will take quite a long time to run through a large city ##
    ## Usually this step was already run through command line before doing any web crawling ##

    # start timing the program
    start=datetime.now()

    if extract_http_links:
        generate_links_by_city.trulia_get_links_by_city.getAddressbyCity(city)
    else:
        pass
    ## End of getting links process ##

    ## Generation of list of all http links for the properties in the city
    all_links = generate_links_by_city.getListofHttpLinks(city)

    ## create the queue csv file if it does not exist ##
    param = loadParameters()
    links_crawled_queue_file = param["links_crawled_queue"]
    output_bucket = os.path.join(os.getcwd(),param["output_bucket"])
    createFile(links_crawled_queue_file)
    links_crawled_queue_file = os.path.join(os.getcwd(),links_crawled_queue_file)
    links_quequed = linksinqueque(links_crawled_queue_file)

    # create the log folder if it does not exist, and log.log and error.log files
    temp_folder = os.path.join(os.getcwd(), output_bucket)
    createFolder(os.path.join(os.getcwd(),"log"))
    createFolder(temp_folder)
    createFolder(output_bucket)
    createFile("log/error.log")
    createFile("log/log.log")
    error_log_file = os.path.join(os.getcwd(),"log/error.log")
    log_file = os.path.join(os.getcwd(),"log/log.log")

    # assign a city name formatted in the way, for example, worcester_ma
    city2 = proessCityName(city, space_substitute="_")
    city2 = city2.lower().replace(',','_').replace(' ','_')

    ## set a threshold for number of properties to process when testing
    ## if link was already processed in the queque, then move on
    num_to_process = min(max_num_properties_to_process, len(all_links))
    links_in_loop = all_links[:num_to_process]
    links_in_loop = np.setdiff1d(links_in_loop, links_quequed)

    for link in links_in_loop:
        temp_outjson = city2+"_"+random_md5like_hash(12)+".json"

        cmd = 'scrapy crawl Trulia_by_url --nolog -a start_url="%s"' %link
        cmd += " -o "+temp_outjson
        try:
            call_status = subprocess.check_call(cmd,shell=True)
            if call_status == 0:
                success_log = "Scraping %s was successful." %link
                writeText2File(success_log, log_file) #write success info to the log.log file
                writeText2File(link, links_crawled_queue_file) #write the link to the queue as successful ones
                add_extra_info_to_json(temp_outjson, link)
                shutil.move(temp_outjson,temp_folder)
            else:
                failure_log = "Failed to scrape %s" %link
                writeText2File(failure_log, error_log_file)
        except:
            continue

    ## clean the temp_folder that stores all crawled webpages for the city
    # shutil.rmtree(temp_folder)

    ### calculate the time it took to run the program
    length = str(datetime.now()-start)
    try:
        milsec = re.findall('.\d+',length)[-1]
    except:
        milsec = ""
    second = length.replace(milsec,"")
    ### calculation of timing is done ###

    ## add log ##
    loginfo = "It took %s to web-crawl %s property webpages in %s ..." %(second, str(len(links_in_loop)), city)
    writeText2File(loginfo, log_file)
    print(loginfo)
    # To get a rough idea about the speed of web-crawling, it took 0:07:48 to web-crawl 100 property webpages in Worcester,MA ...
        # In other words, it took about 4.68 seconds to parse one webpage since the over-head loading of scrapy settings


if __name__ == '__main__':
    import sys

    args = sys.argv
    args_lower = map(lambda t: t.lower(), args)

    if "-c" not in args_lower:
        raise StandardError("The option -c for the input city is missing... The city needs to be of format 'Boston, MA'")
    else:
        pass

    city = args[args_lower.index("-c")+1]

    # Set option for extract_http_links
    if "-l" in args_lower:
        extract_http_links_ = args[args_lower.index("-l")+1]
        if extract_http_links_.lower() == "true":
            extract_http_links_ = True
        elif extract_http_links_.lower() == "false":
            extract_http_links_ = False
        else:
            raise StandardError("The option after -l has to be bolean!")
    else:
        ## Set default extract_http_links value to be False if it is not provided in the command line
        extract_http_links_ = False

    # Set option for max_num_properties_to_process
    if "-n" in args_lower:
        max_num_properties_to_process_ = args[args_lower.index("-n")+1]
        try:
            max_num_properties_to_process_ = int(float(max_num_properties_to_process_))
        except:
            raise ValueError("The option after -n has to be an interger!")
    else:
        ## Set default max_num_properties_to_process_ value to be False if it is not provided in the command line
        max_num_properties_to_process_ = 10**8

    craw_city(city, extract_http_links = extract_http_links_, max_num_properties_to_process = max_num_properties_to_process_)
