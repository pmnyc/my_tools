# -*- coding: utf-8 -*-
"""
@author: pm
"""

import file_pattern_match_on_s3
import json, boto, os, fnmatch, numpy as np
from boto.s3.connection import S3Connection
from boto.s3.connection import OrdinaryCallingFormat
import myparsing

class filePatternMatch(object):
    def __init__(self, mywork_id, search_file_path_pattern):
        if not(search_file_path_pattern.startswith('s3://')):
            self.search_file_path_pattern = 's3://' + search_file_path_pattern
        else:
            self.search_file_path_pattern = search_file_path_pattern
        self.mywork_id = mywork_id
        if str(self.mywork_id) not in self.search_file_path_pattern:
            raise Exception('mywork ID given is not part of search path. Re-check ID or Path')
        self.bucketname = self.search_file_path_pattern.replace('s3://','').split('/')[0]

    def getpath(self):
        searchpattern_short = self.search_file_path_pattern.replace('s3://','').replace(self.bucketname+'/','')
        prefix = searchpattern_short[:searchpattern_short.find("*")]
        conn = S3Connection(calling_format=OrdinaryCallingFormat())
        bucket = conn.get_bucket(self.bucketname)
        #rs = bucket.list()
        ## use delimiter / to find the folders only, use '' to find all files including folders
        rs =  bucket.list(prefix=prefix, delimiter='')
        files = [key.name for key in rs if fnmatch.fnmatch(key.name,searchpattern_short)]
        conn.close()
        self.prefix_bucket = prefix
        return np.array(files)

    def getScenarioID(self):
        files = self.getpath()
        ids = np.array(['a'])
        ids = np.delete(ids,0)
        for f in files:
            splits = f.split('/')
            sid = splits[splits.index('ee') + 1]
            ids = np.append(ids, sid)
        self.s3file_key_name = files
        self.scenarios = ids
        #return self
    
    def download(self, bucketname=None, s3file_key_name=None,
                    savefolder=None, filename=None):
        # s3file_key_name = np.array(['myfolder/mockdata/138948/ee/adsf-abfads-sdf/abcd.html'])
            # remark s3file_key_name is actually an array, even though there is only one element in there
        # bucketname = 'myfolder'
        # savefolder = 'file_folder'
        # filename = 'download.html'
        def quickextractScnarioid(x):
            splits = x.split('/')
            sid = splits[splits.index('ee') + 1]
            return sid

        self.getScenarioID()
        if bucketname == None:
            bucketname = self.bucketname
        if s3file_key_name == None:
            s3file_key_name = self.s3file_key_name
        elif type(s3file_key_name) is str:
            s3file_key_name = np.array([s3file_key_name])
        else:
            pass
        if savefolder == None:
            savefolder = os.getcwd()
        else:
            savefolder = os.path.join(os.getcwd(),savefolder)
        if filename == None:
            filename = ''
        if type(filename) is str:
            filename = [filename] * len(s3file_key_name)

        conn = S3Connection(calling_format=OrdinaryCallingFormat())
        bucket = conn.get_bucket(bucketname)
        rs =  bucket.list(prefix=self.prefix_bucket, delimiter='')
        i = 0
        filesdownloaded = []
        for key in rs:
            if key.name not in s3file_key_name:
                continue
            else:
                downloadfile_local = os.path.join(savefolder,quickextractScnarioid(key.name)+'_'+key.name.split('/')[-1])
                key.get_contents_to_filename(downloadfile_local)
                filesdownloaded.append(downloadfile_local)
                i += 1
        conn.close()
        self.filesdownloaded = filesdownloaded
        print("There are "+str(i)+' files downloaded for mywork_ID '+str(self.mywork_id)+"...")

    def cleanupDownloaded(self):
        try:
            print("Files downloaded to local drive for mywork_ID "+str(self.mywork_id)+" are about to be deleted...")
            for f in self.filesdownloaded:
                os.remove(f)
        except Exception, e:
            pass

def downloadS3File(s3filepath, s3filename, use_s3key_ind,s3_key_info):
    #sample input
    # s3filepath = 's3://mybucket/result/14/ee/6b1f0f9c-cc9a-4378-ada6-88691f0f1d9c/results.json'
    # s3filename = "14_6b1f0f9c-cc9a-4378-ada6-88691f0f1d9c_results.json"
    def loadJson(filename):
        # Sample input
        # filename = 's3_key.json'
        json_data=open(filename,'r')
        data = json.load(json_data)
        json_data.close()
        return data
    def gets3BucketName(x):
        x = x.replace("s3://","").replace("S3://","")
        return x.split("/")[0]
    def gets3Filekey(x):
        x = x.replace("s3://","").replace("S3://","")
        if x.endswith("/"):
            x = x[:-1]
        return x[(x.find("/")+1):]

    if use_s3key_ind == True:
        json_config = loadJson(s3_key_info)
        AWS_ACCESS_KEY_ID = json_config["AWS_ACCESS_KEY_ID"]
        AWS_SECRET_ACCESS_KEY = json_config["AWS_SECRET_ACCESS_KEY"]
        #AWS_DEFAULT_REGION = json_config["AWS_DEFAULT_REGION"]
        conn = boto.connect_s3(
            aws_access_key_id = AWS_ACCESS_KEY_ID,
            aws_secret_access_key = AWS_SECRET_ACCESS_KEY #is_secure=False # uncomment if you are not using ssl
            )
    else:
        conn = S3Connection(calling_format=OrdinaryCallingFormat())

    s3_bucket = gets3BucketName(s3filepath)
    bucket = conn.get_bucket(s3_bucket)
    key = bucket.get_key(gets3Filekey(s3filepath))
    key.get_contents_to_filename(s3filename)

def patternsearch(x, struct_id):
    #x = 'mybucket/result/*/ee/*results.json'
    return '*' + x[:x.find('*')] + str(struct_id) + '/*'

if __name__ in ["__main__", "myparsing_f2"]:
    def main(struct_id, mywork_results_path_pattern, use_s3key_ind = True,s3_key_info="s3_key.json"):
        ### Sample Input
        # struct_id = 14
        # mywork_results_path_pattern = "mybucket/result/*/ee/*results.json"
        ###

        fileobj = file_pattern_match_on_s3.main(search_file_path_pattern = mywork_results_path_pattern, use_s3key_ind=use_s3key_ind)
        jsonfilelist = fileobj.filelist
        jsonfilelist = fnmatch.filter(jsonfilelist, patternsearch(mywork_results_path_pattern,struct_id))
        files_idx = [i for i,x in enumerate(fileobj.filelist) if x in jsonfilelist]
        #filenamelist = fileobj.filename
        filenamelist = map(lambda i: fileobj.filename[i], files_idx)

        for i in range(len(jsonfilelist)):
            downloadS3File(jsonfilelist[i], filenamelist[i], use_s3key_ind, s3_key_info)
            my_struct_id = filenamelist[i].split('_')[0]
            mywork_scenario = filenamelist[i].split('_')[1]  
            if i == 0:
                results_df = myparsing.main(myworkresultJson=filenamelist[i])
                results_df['struct_id'] = int(my_struct_id)
                results_df['scenario'] = mywork_scenario
            else:
                df = myparsing.main(myworkresultJson=filenamelist[i])
                df['struct_id'] = int(my_struct_id)
                df['scenario'] = mywork_scenario
                results_df = results_df.append(df,ignore_index=True)
            os.remove(filenamelist[i])
        # dfname = str(struct_id) + ".csv"
        try:
            del df
        except:
            pass
        
        # results_df.to_csv(dfname,index=False)
        return results_df
