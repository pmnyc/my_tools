# -*- coding: utf-8 -*-
"""
@author: pm

This program is to get the list of all folders from the specified
    directory of the s3 folder
This code only works on Linux, Unix platform

Sample Usage:
import get_list_of_folders_ons3
folders = get_list_of_folders_ons3.main(path_pattern="s3://mybucket/result", s3_key_info="s3_key.json")
"""

import json
import os, platform
import subprocess
import string, random

def id_generator(size=12, chars=string.ascii_lowercase + string.digits):
    return ''.join(random.choice(chars) for _ in range(size))

def loadJson(filename):
    # Sample input
    # filename = 's3_key.json'
    json_data=open(filename,'r')
    data = json.load(json_data)
    #pprint(data)
    json_data.close()
    return data

def addSlash(x):
    if not(x.endswith("/")):
        x += "/"
    return x

def awsEnvironcmd(s3_key_info="s3_key.json"):
    if platform.system().lower() == "windows":
        cmd = ""
    else:
        json_config = loadJson(s3_key_info)
        AWS_ACCESS_KEY_ID = json_config["AWS_ACCESS_KEY_ID"]
        AWS_SECRET_ACCESS_KEY = json_config["AWS_SECRET_ACCESS_KEY"]
        AWS_DEFAULT_REGION = json_config["AWS_DEFAULT_REGION"]
        cmd = "export AWS_ACCESS_KEY_ID=" + AWS_ACCESS_KEY_ID + " ; "
        cmd += "export AWS_SECRET_ACCESS_KEY=" + AWS_SECRET_ACCESS_KEY + " ; "
        cmd += "export AWS_DEFAULT_REGION=" + AWS_DEFAULT_REGION + " ; "
    return cmd

def parseOutputTxtFile(txtfile):
    #sample input:
    #txtfile = 'cz7eda5eszbf.txt'
    text_file = open(txtfile, "r")
    lines = text_file.readlines()
    ids = []
    for line in lines:
        x = ""
        if line.replace('\n','').strip().endswith("/") and line.replace('\n','').strip().startswith("PRE "):
            x = line.replace('\n','').strip()
            x = x.replace("/","").replace("PRE","").replace(" ","")
            ids.append(x)
    return ids

def assignInteger(x):
    try:
        if int(float(x)) == float(x):
            return int(float(x))
    except:
        return None

if __name__ in ['__main__','get_list_of_ids_ons3']:
    def main(path_pattern, s3_key_info="s3_key.json"):
        # sample input
        # path_pattern = "s3://mybucket/result"

        if platform.system().lower() not in ['linux','unix']:
            raise Exception("The OS for get_list_of_ids_ons3.py program has to be Linux or Unix")

        tempoutfilename = id_generator() + ".txt"
        aws_ls_cmd = awsEnvironcmd(s3_key_info=s3_key_info) + 'aws s3 ls ' + addSlash(path_pattern)
        aws_ls_cmd = 'echo "$(' + aws_ls_cmd + ')" > ' + tempoutfilename

        x=subprocess.call(aws_ls_cmd, shell=True)
        if x != 0:
            raise Exception("The AWS command line to export list of folders, files to txt file failed")

        list_of_ids = parseOutputTxtFile(tempoutfilename)
        list_of_ids = filter(lambda t: assignInteger(t) != None, list_of_ids)

        try:
            os.remove(tempoutfilename)
        except:
            pass

        return list_of_ids