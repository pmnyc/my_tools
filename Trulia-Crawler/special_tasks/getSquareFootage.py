# -*- coding: utf-8 -*-
#!/usr/bin/env python

"""
@author: Man Peng

This program is for extracting the square footage information
    for the properties whose json files are in the folder
    given in the command line.

This program needs to be run under the same directory as this Python program is in

$ python getSquareFootage.py property_file_folder myoutput.csv

, where property_file_folder is where the individual property files
    are stored, and myoutput.csv is the name of the output csv file.
"""

import os
import pandas as pd
import fnmatch
#from app.parser_for_property_json import property_parser

def null2Blank(x):
    if x == None:
        return ""
    else:
        return x

def loadFiles2DataFrame(files, json_folder):
    if len(files) == 0 or type(files) is not list:
        raise IOError("No json file is in the specified foder")
    else:
        df = pd.DataFrame(columns=('streetAddress', 'city', 'state', 'sqft'))
        numColumns = len(df.columns)
        for i in range(len(files)):
            file_ = files[i]
            file_ = os.path.join(json_folder, file_)
            property_obj = property_parser(property_json_file=file_)
            property_obj.getSqft()
            x = [property_obj.streetAddress_,
                      property_obj.city_, 
                      property_obj.state_,
                      property_obj.sqft_
            ]
            if numColumns != len(x):
                raise Exception("DataFrame and the Record inserted here \
                    do NOT have same dimention.")
            df.loc[i] = x
    return df

def getParentDirectory(directory):
    """ This is the fucntion that returns the parent directory for a given directory """
    return os.path.abspath(os.path.join(directory, os.pardir))

if __name__ == "__main__":
    import sys

    json_folder = sys.argv[1]
    out_csv = filter(lambda x: x.lower().find(".csv")>0, sys.argv)[0]

    curr_workdir = os.getcwd()
    main_dir = getParentDirectory(curr_workdir)

    files = os.listdir(json_folder)
    files = filter(lambda x: fnmatch.fnmatch(x.lower(),"*.json"), files)

    os.chdir(main_dir)
    # This is for adding parent directory for loading the pacakges from the
        # parent directory
    sys.path.append(main_dir)
    from app.parser_for_property_json import property_parser
    dataframe_ = loadFiles2DataFrame(files, os.path.join(curr_workdir,json_folder))
    os.chdir(curr_workdir)
    #print(out_csv)
    #print(dataframe_.head())
    dataframe_.to_csv(out_csv, index=False)

