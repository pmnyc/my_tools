# -*- coding: utf-8 -*-
#!/usr/bin/env python

"""
@author: Man Peng

This progrma utilizs the selenium package
    to simulate the clicks to get through the
    webpages that use Windows ASP.NET technology

Softwares needed to be installed
In Linux:
$ sudo apt-get install libxss1 libappindicator1 libindicator7
$ sudo apt-get install xvfb
$ pip install pyvirtualdisplay selenium

town_order: specifies which town in the list of towns to process
startpage=1: specifies which page to start in that town's webpage
        default value is 1. If somehow network failed and one
        wants restart process from that page on, one can set that
        page number here. For example, there are 322 pages, but the
        program stops at page 123, set this startpage parameter to be
        123 so that it will continue with the rest of pages
save_html=True: specifies whether we save html cache or not
save_snapshot=True: specifies whether we take snapshot of the webpage
browser="Firefox": specifies which browswer to use, it is either FireFox
        or PhantomJS

Sample Usage:
>>> obj = processTown(town_order=1)
>>> obj.runTown()
>>> obj.turnToPage(319)
"""


from selenium import webdriver
import os, sys
import time

# load local files
from utils import load_settings
from utils import decorators
from app import parser_call


def dummyrun():
    """ This is just a dummy function in a quirky fashion """
    import random
    abcpfadspafmsdlfas = random.random()
    del abcpfadspafmsdlfas

def getSystem():
    system = sys.platform
    if 'win' in system.lower():
        system='Windows'
    elif 'linux' in system.lower():
        system='Linux'
    else:
        system='Linux'
    return system

if getSystem() == 'Linux':
    """
    The following pakcage and display is for running this program
        in Linux platform in command line interface
    """
    from pyvirtualdisplay import Display


class processTown(object):
    """
    This function is for running the web-crawling for the town specified
    by the parameter town_order (e.g. 1 means the first town in the table)
    listed by the website for the state.

    save_cache default value is None or False, unless it's specified as True
    It specifies whether we save the webapge snapshot info or not

    The default browser used here is Firefox. The other browser can be used
        is
        browser = "PhantomJS"
    """
    def __init__(self, town_order,
                startpage=1,
                save_html=True,
                save_snapshot=True,
                browser="Firefox"):
        self.town_order = town_order
        self.browser = browser
        self.save_html = save_html
        self.save_snapshot = save_snapshot
        self.parameters = load_settings.loadParameters()
        self.cache_folder_name = 'cache'
        self.page = 1
        # this specifies the current page it is running
        self.startpage = startpage

    def WriteUnicodeFile(self, outfile, content):
        f = open(outfile, 'w')
        f.write(content.encode('utf8'))
        f.close()

    def xvfbDisplay(self):
        if getSystem() == 'Linux':
            """ This is for running Linux Command Line interface 
                in a headless way
            """
            self.display = Display(visible=0, size=(800, 600))
            # this -noreset is mainly for the purpose of handling memory leak of xvfb package
                # by changin the source code
            x = self.display.cmd[:]
            #extra_cmd = "-ac +extension GLX +render -noreset"
            extra_cmd = "-noreset"
            x = x[:-1] + extra_cmd.split(" ") + x[-1:]
            self.display.cmd = x[:]
            self.display.start()
        else:
            pass

    def startInitPage(self):
        """
        This program starts the first webpage for further clicks
        """
        parameters = self.parameters
        site = parameters['web_link_start']
        town_counter_start0=1

        # town_counter specifies which town to process. If it is negative,
            # this means no limit, it will loop through the towns in the
            # table
        town_counter = self.town_order + 0
        
        # Click through the webpages to download the parcel webpages
        #self.xvfbDisplay()  # this option can turn on the xvfb virtualdisplay, which is not necessary
                            # when using PhantomJS
        if self.browser.lower() == 'firefox' and getSystem() == 'Windows':
            driver = webdriver.Firefox()
        elif self.browser.lower() == 'firefox' and getSystem() == 'Linux':
            self.xvfbDisplay()
            driver = webdriver.Firefox()
        elif self.browser.lower() == 'phantomjs' and getSystem() == 'Windows':
            driver = webdriver.PhantomJS(executable_path = self.parameters["PhantomJS_Windows_Exec"])
        elif self.browser.lower() == 'phantomjs' and getSystem() == 'Linux':
            driver = webdriver.PhantomJS(service_args=['--ssl-protocol=any'])
        else:
            error_message = "Firefox browser needs to be installed first!"
            decorators.writeLog(error_message, logfile=parameters['error_log_file'])
            raise Exception(error_message)
        time.sleep(0.1)
        dummyrun()
        driver.get(site)
        
        try:
            time.sleep(0.1)
            dummyrun()
            driver.find_element_by_xpath("//*[@id='ctl01']/div/div/div/div/div/div/div/table/tbody/tr[%s]/td/a" \
                                    %str(town_counter_start0+town_counter)).click()
        except:
            time.sleep(1)
            dummyrun()
            driver.find_element_by_xpath("//*[@id='ctl01']/div/div/div/div/div/div/div/table/tbody/tr[%s]/td/a" \
                                    %str(town_counter_start0+town_counter)).click()
        try:
            time.sleep(0.1)
            dummyrun()
            driver.find_element_by_css_selector("#MainContent_btnEnterOnlineDatabase").click()
        except:
            time.sleep(1)
            dummyrun()
            driver.find_element_by_css_selector("#MainContent_btnEnterOnlineDatabase").click()
        try:
            time.sleep(0.1)
            dummyrun()
            driver.find_element_by_xpath("//*[@id='MainContent_ddlSearchSource']/option[text()='All']").click()
        except:
            time.sleep(1)
            dummyrun()
            driver.find_element_by_xpath("//*[@id='MainContent_ddlSearchSource']/option[text()='All']").click()
        try:
            time.sleep(0.1)
            dummyrun()
            driver.find_element_by_css_selector("#SearchAll > span.btn.btn-primary").click()
        except:
            time.sleep(1)
            dummyrun()
            driver.find_element_by_css_selector("#SearchAll > span.btn.btn-primary").click()
        return driver

    def turnToPage(self, page):
        """
        This is just for turning to the page, usually for checking what happened
            when something goes wrong. For example, if the program stops at
            page 300 (seen in the log file), one may use this program to check
            what happened at page 300
        """
        #cache_folder_name = self.cache_folder_name
        driver = self.startInitPage()
        self.driver = driver
        driver = self.driver
        parameters = self.parameters
        if 'search.aspx' not in driver.current_url.lower():
            msg = "Browser has not reached the main page for properties yet."
            decorators.writeLog(msg, logfile=parameters['error_log_file'])
            raise Exception(msg)
        numOfPages_perPage = parameters['numOfPages_perPage']
        page_loop_counter = 1
        last_page = -1
        while True:
            page_curr = page_loop_counter * numOfPages_perPage + 1
            if page >= (page_loop_counter-1) * numOfPages_perPage + 1 and page <= page_curr-1:
                page_run = page+0
            else:
                page_run = page_curr + 0
            page_xpath = '//*[@id="MainContent_grdSearchResults"]/tbody/tr/td/table/tbody/tr/td/ \
                                        a[contains(@href,"Page$%s\')")]' %str(page_run)
            if page != page_curr or last_page != page:
                time.sleep(0.1)
                try:
                    dummyrun()
                    driver.find_element_by_xpath(page_xpath).click()
                except:
                    time.sleep(0.5)
                    try:
                        dummyrun()
                        driver.find_element_by_xpath(page_xpath).click()
                    except:
                        time.sleep(1)
                        try:
                            dummyrun()
                            driver.find_element_by_xpath(page_xpath).click()
                        except:
                            time.sleep(10)
                            try:
                                dummyrun()
                                driver.find_element_by_xpath(page_xpath).click()
                            except:
                                dummyrun()
                                time.sleep(60)
                                driver.find_element_by_xpath(page_xpath).click()
                last_page = page_run + 0
                page_loop_counter += 1
            if page_curr >= page:
                break


    def continueFromPage(self, page):
        """
        This is dfferent from the turnToPage function above. This
            function starts with the current driver, and continue
            to the webpage specified by page.
        This function is mainly for continuing running the crawler
            if somehow the program stopped at a certain page number
            due to network issue.
        """
        #cache_folder_name = self.cache_folder_name
        driver = self.driver
        page_original = page + 0
        parameters = self.parameters
        if 'search.aspx' not in driver.current_url.lower():
            msg = "Browser has not reached the main page for properties yet."
            decorators.writeLog(msg, logfile=parameters['error_log_file'])
            raise Exception(msg)
        numOfPages_perPage = parameters['numOfPages_perPage']
        page_loop_counter = 1
        last_page = -1
        while True:
            if page == 1:
                break
            page_curr = page_loop_counter * numOfPages_perPage + 1
            if page >= (page_loop_counter-1) * numOfPages_perPage + 1 and page <= page_curr-1:
                page_run = page+0
            else:
                page_run = page_curr + 0
            page_xpath = '//*[@id="MainContent_grdSearchResults"]/tbody/tr/td/table/tbody/tr/td/ \
                                        a[contains(@href,"Page$%s\')")]' %str(page_run)
            if page != page_curr or last_page != page:
                time.sleep(0.1)
                try:
                    dummyrun()
                    driver.find_element_by_xpath(page_xpath).click()
                except:
                    time.sleep(0.5)
                    try:
                        dummyrun()
                        driver.find_element_by_xpath(page_xpath).click()
                    except:
                        time.sleep(1)
                        try:
                            dummyrun()
                            driver.find_element_by_xpath(page_xpath).click()
                        except:
                            time.sleep(10)
                            try:
                                dummyrun()
                                driver.find_element_by_xpath(page_xpath).click()
                            except:
                                dummyrun()
                                time.sleep(60)
                                driver.find_element_by_xpath(page_xpath).click()
                last_page = page_run + 0
                page_loop_counter += 1
            if page_curr >= page:
                break
        # update the final page number
        self.page = page_original + 0

    def runTown(self):
        """
        The main program for running the pages for each town
        """
        parameters = self.parameters
        cache_folder_name = self.cache_folder_name
        driver = self.startInitPage()
        self.driver = driver
        self.continueFromPage(page=self.startpage) # this specifies where to start, default is page=1
        #loop through the pages unitl it hits the last page
        driver = self.driver
        page = self.page + 0
        town_link = driver.current_url
        townname = town_link.split("/")[-2]
        town_name = townname[:-2]+", "+townname[-2:]
        while True:
            if page == 1 or self.page == self.startpage:
                #page_xpath = '//*[@id="MainContent_grdSearchResults"]/tbody/tr/td/table/tbody/tr/td/span'
                #try:
                #    time.sleep(0.1)
                #    driver.find_element_by_xpath(page_xpath).click()
                #except:
                pass
            else:
                page_xpath = '//*[@id="MainContent_grdSearchResults"]/tbody/tr/td/table/tbody/tr/td/ \
                                a[contains(@href,"Page$%s\')")]' %str(page)
                try:
                    time.sleep(0.1)
                    dummyrun()
                    driver.find_element_by_xpath(page_xpath).click()
                except:
                    time.sleep(1)
                    try:
                        dummyrun()
                        driver.find_element_by_xpath(page_xpath).click()
                    except:
                        time.sleep(10)
                        try:
                            dummyrun()
                            driver.find_element_by_xpath(page_xpath).click()
                        except:
                            time.sleep(30)
                            try:
                                dummyrun()
                                driver.find_element_by_xpath(page_xpath).click()
                            except:
                                time.sleep(300)
                                try:
                                    dummyrun()
                                    driver.find_element_by_xpath(page_xpath).click()
                                except:
                                    msg = "The last page for %s is %s, and it is done!" % (town_name,str(page-1))
                                    decorators.writeLog(msg, logfile=parameters['log_file'])
                                    print(msg)
                                    # all pages have been processed, now stop the loop
                                    break

            msg = "Loading page %s for %s" % (str(page), town_name)
            decorators.writeLog(msg, logfile=parameters['log_file'])
            print(msg)
            # the following gives the number of rows and columns for the table
                # listing all parcels for the webpage
            #table_ncol = len(driver.find_elements_by_xpath('//*[@id="MainContent_grdSearchResults"]/tbody/tr/th'))
            try:
                table_nrow = len(driver.find_elements_by_xpath('//*[@id="MainContent_grdSearchResults"] \
                            /tbody/tr[contains(@class,"RowStyle")]'))
            except:
                msg = "The page for %s is %s does not have parcels listed there!" % (town_name,str(page))
                decorators.writeLog(msg, logfile=parameters['error_log_file'])
                print(msg)
                break
            if table_nrow == 0:
                msg = "The page for %s is %s does not have parcels listed there!" % (town_name,str(page))
                decorators.writeLog(msg, logfile=parameters['error_log_file'])
                print(msg)
                break

            # loop through each parcel in the table on the current webpage
            for i in range(table_nrow):
                xpath_search = '//*[@id="MainContent_grdSearchResults"]/tbody/tr[contains(@class,"RowStyle")] \
                            /td/a[contains(@href,"Parcel.aspx?pid")]'
                # the following "recursion" is a little weird, but it keeps the code running in case the time issue
                try:
                    time.sleep(0.05)
                    dummyrun()
                    driver.find_elements_by_xpath(xpath_search)[i].click()
                except:
                    try:
                        time.sleep(0.1)
                        dummyrun()
                        driver.find_elements_by_xpath(xpath_search)[i].click()
                    except:
                        try:
                            time.sleep(0.5)
                            dummyrun()
                            driver.find_elements_by_xpath(xpath_search)[i].click()
                        except:
                            try:
                                time.sleep(1)
                                dummyrun()
                                driver.find_elements_by_xpath(xpath_search)[i].click()
                            except:
                                try:
                                    time.sleep(10)
                                    dummyrun()
                                    driver.find_elements_by_xpath(xpath_search)[i].click()
                                except:
                                    try:
                                        time.sleep(30)
                                        dummyrun()
                                        driver.find_elements_by_xpath(xpath_search)[i].click()
                                    except:
                                        try:
                                            time.sleep(180)
                                            dummyrun()
                                            driver.find_elements_by_xpath(xpath_search)[i].click()
                                        except Exception as e:
                                            msg = str(e)+", page "+str(page)+", the "+str(i)+"-th in the list"
                                            print(msg)
                                            decorators.writeLog(msg, logfile=parameters['error_log_file'])
                                            continue
                try:
                    town_link = driver.current_url
                    townname = town_link.split("/")[-2]
                    pid = town_link.split("/")[-1].split('=')[-1]
                    if self.save_snapshot: #save in the cache folder
                        if not (os.path.exists(cache_folder_name)):
                            os.makedirs(cache_folder_name)
                        driver.save_screenshot("%s/%s_pid%s.png" %(cache_folder_name, townname,str(pid)))

                    content = driver.page_source
                    if self.save_html: #save in the cache folder
                        if not (os.path.exists(cache_folder_name)):
                            os.makedirs(cache_folder_name)
                        self.WriteUnicodeFile("%s/%s_pid%s.html" %(cache_folder_name,townname,str(pid)), content)
                    """ Now add the parser for scraping content info """
                    parser_call.callParser(content)
                except Exception as e:
                    msg = str(e)+", page "+str(page)+", the "+str(i)+"-th in the list..."
                    print(msg)
                    decorators.writeLog(msg, logfile=parameters['error_log_file'])

                try:
                    time.sleep(0.1)
                    dummyrun()
                    driver.execute_script("window.history.go(-1)")
                except:
                    try:
                        time.sleep(10)
                        dummyrun()
                        driver.execute_script("window.history.go(-1)")
                    except Exception as e:
                        print(str(e))
                        decorators.writeLog(str(e), logfile=parameters['error_log_file'])
                        continue
            # near end of page turning of while statement
            page += 1
            self.page = page + 0 # update the current page, i.e. self.page
            ## This is for clearing all cache
            # driver.delete_all_cookies()
        # Quite browser
        driver.quit()


