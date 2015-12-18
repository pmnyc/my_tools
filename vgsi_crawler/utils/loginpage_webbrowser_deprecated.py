# -*- coding: utf-8 -*-
#!/usr/bin/env python

"""
@author: Man Peng

The following function is deprecated.

The following function is to append the successive PIDs 
for getting all possible properties in the town. Unfortunately
the website does not necessarily use the consecutive
pids in towns. There are big jumps occassionally.


This progrma utilizs the selenium package
    to simulate the clicks to get through the
    webpages that use Windows ASP.NET technology

town_order specifies which town in the list of towns to process

"""


from selenium import webdriver
import os, sys
import time

# load local files
from utils import load_settings
from utils import decorators


def runTown_ver0(town_order, save_cache=None):
    """
    This function is for running the web-crawling for the town specified
    by the parameter town_order (e.g. 1 means the first town in the table)
    listed by the website for the state.

    save_cache default value is None or False, unless it's specified as True
    It specifies whether we save the webapge snapshot info or not
    """
    parameters = load_settings.loadParameters()
    site = parameters['web_link_start']

    town_counter_start0=1
    if save_cache == None:
        save_cache = False
    elif save_cache == True or save_cache == False:
        pass
    else:
        raise Exception("save_cache parameter must be one of None, True or False")

    cache_folder_name = 'cache'
    if save_cache and not (os.path.exists(cache_folder_name)):
        os.makedirs(cache_folder_name)

    # town_counter specifies which town to process. If it is negative,
        # this means no limit, it will loop through the towns in the
        # table
    town_counter = town_order + 0
    # pids_limit specifies the limit of parcles to process at one time
        # during the code testing stage. It will be set to be super
        # large number to make sure all parcels to be processed
    pids_limit = parameters['pid_limits']

    # Click through the webpages to download the parcel webpages
    driver = webdriver.Firefox()
    driver.get(site)

    driver.find_element_by_xpath("//*[@id='ctl01']/div[3]/div/div/div[5]/div/div/div[2]/table/tbody/tr[%s]/td[1]/a" \
                                %str(town_counter_start0+town_counter)).click()
    driver.find_element_by_css_selector("#MainContent_btnEnterOnlineDatabase").click()
    driver.find_element_by_xpath("//*[@id='MainContent_ddlSearchSource']/option[text()='All']").click()
    driver.find_element_by_css_selector("#SearchAll > span.btn.btn-primary").click()

    town_link = driver.current_url
    townname = town_link.split("/")[-2]
    pid_link = town_link.replace("Search.aspx","").replace("search.aspx","")
    pid_link += "Parcel.aspx?pid="
    pid_curr = 1
    pid_counter = 0
    successive_bad_pids_threshold = parameters['successive_bad_pids_threshold']
    successive_bad_pids = 0
    while True:
        if pid_counter > pids_limit:
           break
        pid_link_curr = pid_link + str(pid_curr)
        driver.get(pid_link_curr)
        curr_url = driver.current_url
        found_error_bolean = ("error" in curr_url.lower() and "found" in curr_url.lower())
        if found_error_bolean and successive_bad_pids > successive_bad_pids_threshold:
            break
        pid_curr += 1
        pid_counter += 1
        # determine whether continue checking webpages or parse webpage
            # and then crawl it
        if found_error_bolean and successive_bad_pids <= successive_bad_pids_threshold:
            successive_bad_pids += 1
            continue
        else:
            successive_bad_pids = 0
            if save_cache: #save in the cache folder
                driver.save_screenshot("%s/%s_pid%s.png" %(cache_folder_name, townname,str(pid_curr-1)))
            #content = driver.page_source
            #if save_cache: #save in the cache folder
                #WriteUnicodeFile("%s/%s_pid%s.html" %(cache_folder_name,townname,str(pid_curr-1)), content)
    try:
        # close browser
        driver.close()
    except:
        pass


"""The following is a template for getting saratoga county webpages"""
# driver.get("http://saratoga.sdgnys.com/index.aspx")
# driver.find_element_by_id("btnPublicAccess").click()
# driver.find_element_by_id("chkAgree").click()
# driver.find_element_by_id("btnSubmit").click()
# driver.find_element_by_xpath("//select[@name='ddlMunic']/option[text()='Clifton Park']").click()
# driver.find_element_by_xpath("//input[@id='btnSearch']").click()
# print driver.current_url
# driver.close()
