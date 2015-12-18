# -*- coding: utf-8 -*-
#!/usr/bin/env python

"""
@author: Man Peng

This is the main execution program for running the Python programs

Sample Usage:

$ python main.py --town 1 --startpage 1 --save_html --save_snapshot

, where --town value must be provided
if --startpage is not provided, then default value is 1.
if --save_html is not provided, then default is no save of html file of webpage
if --save_snapshot is not provided, then default is no save of snapshot of webpage
"""

import os, sys

# load local files
from utils import loginpage_webbrowser
from utils import load_settings


def getPlatform():
    x = sys.platform
    x = x.lower()
    if x.startswith('win'):
        return 'Windows'
    elif x.startswith('linux'):
        return 'Linux'
    else:
        return ''

def findOptions(option, argvs):
    """ This function specifies the option in the command line
        and it will look for the value for this option
        The option starts with -- or -, but there must be a value
        following this option as the value of this option
    """
    # argvs = sys.argv
    # option = '--town'
    idx = [i for i,x in enumerate(argvs) if x.lower() == option.lower()]
    if idx == []:
        return None
    elif idx[0] == len(argvs) -1:
        raise Exception("The value for the option %s is missing!" %option)
    elif argvs[idx[0]+1].startswith("-"):
        raise Exception("The value for the option %s is missing!" %option)
    else:
        return argvs[idx[0]+1]


if __name__ == '__main__':
    parameters = load_settings.loadParameters()
    browser = parameters['browser']

    town_order = findOptions('--town', sys.argv)
    if town_order == None:
        error_msg = "Forgot to put the number for the town after --town! \n \
                    For example, in RI webpage, Charlestown is \n \
                    the first town in the table, then the value for the --town \n \
                    is 1"
        raise Exception()
    town_order = int(town_order)
    startpage = findOptions('--startpage', sys.argv)
    if startpage == None:
        startpage = 1
    else:
        startpage = int(startpage)

    idx = [i for i,x in enumerate(sys.argv) if x.lower() == '--save_html']
    if idx == []:
        save_html = False
    else:
        save_html = True
    idx = [i for i,x in enumerate(sys.argv) if x.lower() == '--save_snapshot']
    if idx == []:
        save_snapshot = False
    else:
        save_snapshot = True


    townObj = loginpage_webbrowser.processTown(town_order=town_order, 
                                browser = browser,
                                startpage=startpage,
                                save_html=save_html,
                                save_snapshot=save_snapshot)
    townObj.runTown()

