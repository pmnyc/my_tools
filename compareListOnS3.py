# -*- coding: utf-8 -*-
"""
@author: man peng

This program is to get the list of IDs processed and
    the IDs in full list folder so that we can get
    the list of IDs that still need processing

This program does not work in Windows, has to be in Linux/Unix
    envrionment

This program assumes one has installed s4cmd tool
    if not, use $ sudo pip install s4cmd
    to install

Sample usage:
import compareListOnS3
list = compareListOnS3.main(done_file_pattern = "s3://mybucket/myfolder/files*.csv", \
                        full_list_pattern = "s3://mybucket/result/")
"""

import numpy as np
import subprocess, os

def getID(x, id_pattern):
    #sample input
    # x = '2015-04-20 19:48    6124 s3://mybucket/myfolder/files_46568.csv\n'
    # id_pattern defines where to extract ID info based on wildcard
    f = x.split(" ")[-1]
    f = f.replace("\n","")
    id_pattern_pt1 = id_pattern.split("*")[0]
    id_pattern_pt2 = id_pattern.split("*")[1]
    start_pos = f.find(id_pattern_pt1)
    end_pos = f.find(id_pattern_pt2,start_pos + len(id_pattern_pt1),len(f))
    if end_pos < 0:
        return ""
    else:
        f = f[start_pos:end_pos]
        f = f.replace(id_pattern_pt1,"")
        return f

def parsefile(file, id_pattern):
    f = open(file, 'r')
    files = f.readlines()
    ids_list = map(lambda t: getID(x=t, id_pattern=id_pattern),files)
    ids_list = filter(lambda x: x != None and x != '' and x.find(".") < 0, ids_list)
    return ids_list

def guessS4cmd(_):
    # sometimes s4cmd.py works, sometimes s4cmd works, depends on
        # how the program was installed
    a = 1
    b = 1
    try:
        a = subprocess.call(["s4cmd.py","ls"],stdout=subprocess.PIPE,stderr=subprocess.PIPE)
        b = subprocess.call(["s4cmd","ls"],stdout=subprocess.PIPE,stderr=subprocess.PIPE)
    except:
        pass
    if a == 0:
        return "s4cmd.py"
    elif b == 0:
        return "s4cmd"
    else:
        raise Exception("s4cmd program is not installed, need to $ pip install s4cmd")

if __name__ in ['__main__', 'compareListOnS3']:
    def main(done_file_pattern, full_list_pattern):
        # sample input
        # done_file_pattern = "s3://mybucket/myfolder/files*.csv"
            #this is the pattern of the files for IDs
        # full_list_pattern = "s3://mybucket/result/"
            #this is the pattern of folders containing IDs

        file_done = "is_files_done.csv"
        file_fulllist = "is_folder_ids.csv"

        cmd_done = 'echo "$(' + guessS4cmd(0) + ' ls ' + done_file_pattern + ')" > ' + file_done
        cmd_fullist = 'echo "$(' + guessS4cmd(0) + ' ls ' + full_list_pattern + ')" > ' + file_fulllist

        x = subprocess.call(cmd_done, shell=True)
        if x != 0:
            raise Exception(file_done + " file is not created by s4cmd")
        else:
            pass
        x = subprocess.call(cmd_fullist, shell=True)
        if x != 0:
            raise Exception(file_fulllist + " file is not created by s4cmd")
        else:
            pass

        ids_list_done = parsefile(file=file_done, id_pattern="files_*.csv")
        ids_list = parsefile(file=file_fulllist, id_pattern="result/*/")
        ids_torun = np.setdiff1d(ids_list, ids_list_done).tolist()

        try:
            os.remove(file_done)
        except:
            pass
        try:
            os.remove(file_fulllist)
        except:
            pass
        
        return ids_torun
