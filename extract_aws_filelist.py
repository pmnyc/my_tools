# -*- coding: utf-8 -*-
"""
This is to export an S3 folder's list of files to a .csv file. The list doesn't contain subfolder names, but contains all files inside the subfolders
@author: pengma

sample usage:
$ python extract_aws_filelist.py s3://mybucket/myfolder myoutput.csv
    where. myoutput.csv is the output csv file for listing all s3 file names

config.json file this program calls to pull the access key info is of the format
{
"AWS_ACCESS_KEY_ID":"MYKEY",
"AWS_SECRET_ACCESS_KEY":"mysecretkey",
"AWS_DEFAULT_REGION":"us-east-1"
}
"""

import boto, sys

def createListofFilesOnS3(s3_loc, outputtable,**kwargs):
    if kwargs is not None:
        for key, value in kwargs.iteritems():
            if key == "access_key":
                access_key = value
            if key == "secret_key":
                secret_key = value
    conn = boto.connect_s3(
        aws_access_key_id = access_key,
        aws_secret_access_key = secret_key, #is_secure=False # uncomment if you are not using ssl
        )
    if not s3_loc.endswith("/"):
        s3_loc = s3_loc + "/"
    bucket = conn.get_bucket(s3_loc.replace("s3://","").split("/")[0])
    def findfilename(x):
        y = str(x)
        y = y.split("/")
        return y[-1]
    s3_folder = s3_loc.replace("s3://","")
    if s3_folder.endswith("/"):
        s3_folder = s3_folder[:-1]
    if len(s3_folder.split("/")) == 1:
        rs = bucket.list()
    else:
        rs = bucket.list(s3_folder.replace(s3_loc.replace("s3://","").split("/")[0] + "/","") + "/")

    files = [findfilename(key.name) for key in rs if not key.name.endswith('/')]
    filescript = ""
    for f in files:
        filescript += (f + "\n")

    f = open(outputtable,"w")
    f.write(filescript)
    f.close
    del f
    
    return None

if __name__ in ["__main__","extract_aws_filelist"]:
    ### Initial Parameters
    source_lazfile_folder_ons3 = sys.argv[-1]
    #source_lazfile_folder_ons3 = 'ma.las.mockdata/folder1' #sample value
    import json
    
    def loadJson(filename):
        json_data=open(filename,'r')##change
        data = json.load(json_data)
        json_data.close()
        return data
    
    json_config = loadJson("config.json")
    AWS_ACCESS_KEY_ID = json_config["AWS_ACCESS_KEY_ID"]
    AWS_SECRET_ACCESS_KEY = json_config["AWS_SECRET_ACCESS_KEY"]
    AWS_DEFAULT_REGION = json_config["AWS_DEFAULT_REGION"]
    #####

    if len(sys.argv) == 3:
        createListofFilesOnS3(s3_loc=sys.argv[1], outputtable=sys.argv[2], access_key=AWS_ACCESS_KEY_ID,secret_key=AWS_SECRET_ACCESS_KEY)