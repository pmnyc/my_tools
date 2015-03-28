# -*- coding: utf-8 -*-
"""
@author: pm
"""

import file_pattern_match_on_s3
import json, boto, os, fnmatch
from boto.s3.connection import S3Connection
from boto.s3.connection import OrdinaryCallingFormat
import nrel_result_and_incent

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

if __name__ in ["__main__", "nrel_result_and_incent_f2"]:
    def main(struct_id, NREL_results_path_pattern, use_s3key_ind = True,s3_key_info="s3_key.json"):
        ### Sample Input
        # struct_id = 14
        # NREL_results_path_pattern = "mybucket/result/*/ee/*results.json"
        ###

        fileobj = file_pattern_match_on_s3.main(search_file_path_pattern = NREL_results_path_pattern, use_s3key_ind=use_s3key_ind)
        jsonfilelist = fileobj.filelist
        jsonfilelist = fnmatch.filter(jsonfilelist, patternsearch(NREL_results_path_pattern,struct_id))
        files_idx = [i for i,x in enumerate(fileobj.filelist) if x in jsonfilelist]
        #filenamelist = fileobj.filename
        filenamelist = map(lambda i: fileobj.filename[i], files_idx)

        for i in range(len(jsonfilelist)):
            downloadS3File(jsonfilelist[i], filenamelist[i], use_s3key_ind, s3_key_info)
            NREL_struct_id = filenamelist[i].split('_')[0]
            NREL_scenario = filenamelist[i].split('_')[1]  
            if i == 0:
                results_df = nrel_result_and_incent.main(NRELresultJson=filenamelist[i])
                results_df['struct_id'] = int(NREL_struct_id)
                results_df['scenario'] = NREL_scenario
            else:
                df = nrel_result_and_incent.main(NRELresultJson=filenamelist[i])
                df['struct_id'] = int(NREL_struct_id)
                df['scenario'] = NREL_scenario
                results_df = results_df.append(df,ignore_index=True)
            os.remove(filenamelist[i])
        # dfname = str(struct_id) + ".csv"
        try:
            del df
        except:
            pass
        
        # results_df.to_csv(dfname,index=False)
        return results_df
