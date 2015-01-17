# -*- coding: utf-8 -*-
"""
This is to comibne all csv files of same format into one single csv file
@author: pm
sample usage:
    $ python combine_all_csv.py 'combinedCSV/combinedcsv.csv' --hasheader=true/false
where, 'combinedCSV/combinedcsv.csv' gives the directory of the output csv file that combines
    all csv files in the present work directory.
    --hasheader=true specifies all csv files in present work directory have header/variable information
    if --hasheader option is NOT specified, then the default option is --hasheader=true
"""

import os, pandas as pd
import sys
pwd = os.getcwd()
csvfolder = ""

if __name__ == "__main__":
    if len(sys.argv) < 2:
        print "Sample useage: $ python combine_all_csv.py 'combinedCSV/combinedcsv.csv' --hasheader=true/false"
        print "You can skip the --hasheader option, the default setting is --hasheader=True"
        exit(1)
    else:
        try:
            hasheader = sys.argv[2]
        except IndexError:
            hasheader = "--hasheader=true"
        combinded_csv_name = sys.argv[1]
        combinded_csv_name = combinded_csv_name.replace("'",'').replace('"','')

        csvfolder = os.path.join(pwd,csvfolder)
        os.chdir(csvfolder)
        ### Inside the csv folder
        def ensure_dir(f):
            d = os.path.dirname(f)
            if not os.path.exists(d) and d != '':
                os.makedirs(d)

        ensure_dir(combinded_csv_name) #this makes sure the specified folder is created if not existed

        if os.path.isfile(combinded_csv_name):
            os.remove(combinded_csv_name)

        def getfileextension(x):
            fileName, fileExtension = os.path.splitext(x)
            return fileExtension[1:].lower()

        dir_list = os.listdir(csvfolder)
        csv_list = [f for f in dir_list if getfileextension(f) == 'csv']
        if len(csv_list) == 0:
            print "No csv files in the folder " + csvfolder
            os.chdir(pwd)
            exit(1)
        else:
            header_ind = ("true" in hasheader.lower())
            if header_ind:
                headerline = 0
            else:
                headerline = None
            numofcsvfiles = len(csv_list)
            pandadata = pd.read_csv(csv_list[0],header=headerline)
            i = 1
            while i <= numofcsvfiles-1:
                pdi = pd.read_csv(csv_list[i],header=headerline)
                pandadata = pandadata.append(pdi)
                i += 1
            pandadata.to_csv(combinded_csv_name,index=None)
            del pandadata

        ### Get back to current work directory
        os.chdir(pwd)
