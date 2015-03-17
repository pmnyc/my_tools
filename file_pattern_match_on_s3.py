# -*- coding: utf-8 -*-
"""
@author: pm

This Program searches for the pattern of files in the s3 bucket and
    returns the files that match the pattern and also the id
    associated with the file

search_file_path_pattern
    is the path for searching files with wildcard included
"""

import json
import boto

class filePatternMatch(object):
    def __init__(self, search_file_path_pattern, s3_key_info="s3_key.json", wildcard="*"):
        self.search_file_path_pattern = search_file_path_pattern
        self.s3_key_info = s3_key_info
        self.wildcard = wildcard
    
    def getStructID(self,x,search_file_path_pattern,wildcard):
        # This function gives id masked by wildcard by matching x with search_file_path_pattern, in this example
            # the result should be 100000
        ## Sample Input
        # x = "mybucket/result/100000/test/results.json" #this defines the actual file name
        # search_file_path_pattern = "mybucket/result/*/test/results.json" #this is the pattern of file for matching
        ##
        search_short = search_file_path_pattern[:search_file_path_pattern.find(wildcard)]
        search_short_list = search_short.split("/")
        search_short_list = [i for i in search_short_list if i != '']
        x_split = x.split("/")
        x_split = [i for i in x_split if i != '']
        id = x_split[len(search_short_list)]
        return id

    def matchPatternInd(self,x,search_file_path_pattern,wildcard):
        # This function gives boolean result if string x matches the pattern given by search_file_path_pattern using wildcard
        ## Sample Input
        # x = "mybucket/result/100000/test/results.json" #this defines the actual file name
        # search_file_path_pattern = "mybucket/result/*/test/results.json" #this is the pattern of file for matching
        ##
        if search_file_path_pattern.count(wildcard) == 0:
            return (x == search_file_path_pattern)
        else:
            for i in range(search_file_path_pattern.count(wildcard)):
                search_file_path_pattern = search_file_path_pattern.replace("*","").replace("//","/")
            splits = search_file_path_pattern.split("/")
            splits = [i for i in splits if i != '']
            x_splits = x.split("/")
            match_list = []
            for i in range(len(splits)):
                match_list.append(splits[i] in x_splits)
            if len(match_list) == 0 or sum(match_list) < len(splits):
                return False
            elif sum(match_list) == len(splits):
                return True
            else:
                return False

    def loadJson(self,filename):
        # Sample input
        # filename = 's3_key.json'
        json_data=open(filename,'r')
        data = json.load(json_data)
        #pprint(data)
        json_data.close()
        return data

    def addSlash(self,loc):
        if not loc.endswith("/"):
            loc = loc + "/"
        return loc

    def createListofFilesOnS3(self):
        search_file_path_pattern = self.search_file_path_pattern
        s3_key_info = self.s3_key_info
        # s3_bucket can be referred easily from string search_file_path_pattern
        s3_bucket = search_file_path_pattern.split("/")[0]
        if not s3_bucket.lower().startswith("s3://"):
            s3_bucket = "s3://" + s3_bucket
        json_config = self.loadJson(s3_key_info)
        AWS_ACCESS_KEY_ID = json_config["AWS_ACCESS_KEY_ID"]
        AWS_SECRET_ACCESS_KEY = json_config["AWS_SECRET_ACCESS_KEY"]
        AWS_DEFAULT_REGION = json_config["AWS_DEFAULT_REGION"]
        conn = boto.connect_s3(
            aws_access_key_id = AWS_ACCESS_KEY_ID,
            aws_secret_access_key = AWS_SECRET_ACCESS_KEY, #is_secure=False # uncomment if you are not using ssl
            )
        s3_bucket = self.addSlash(s3_bucket)
        bucket = conn.get_bucket(s3_bucket.replace("s3://","").split("/")[0])
        buck = bucket.list()
        bucket_name = s3_bucket.replace("s3://","").replace("/","")
        files = [(bucket_name + "/" + key.name) for key in buck]
        if len(files) == 0:
            filelist = None
        else:
            filelist = []
            id = []
            for i in range(len(files)):
                if self.matchPatternInd(files[i], search_file_path_pattern, self.wildcard):
                    filelist.append("s3://" + files[i])
                    id_ = self.getStructID(files[i], search_file_path_pattern, self.wildcard)
                    id.append(id_)
                    
        self.filelist = filelist
        self.id = id

if __name__ == '__main__':
    def main(search_file_path_pattern, s3_key_info="s3_key.json", wildcard="*"):
        # sample input
        # search_file_path_pattern = "mybucket/result/*/test/results.json"
            # where search_file_path_pattern defines the pattern for searching certain files in s3 bucket
        myobj = filePatternMatch(search_file_path_pattern, s3_key_info, wildcard)
        myobj.createListofFilesOnS3()
        # what we cared about are myobj.filelist & myobj.id
        return myobj