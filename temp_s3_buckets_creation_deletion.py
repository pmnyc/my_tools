"""
@author: pm

Sample usage:
import temp_s3_buckets_bystructid
temp_s3_buckets_bystructid.copys3Files2temp(myid, search_pattern, s3_key_info)
temp_s3_buckets_bystructid.deleteTempBucket(myid, s3_key_info)
"""

import boto, json
import platform
import subprocess

def loadJson(filename):
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

def createBucket(bucketname, s3_key_info="s3_key.json"):
    json_config = loadJson(s3_key_info)
    AWS_ACCESS_KEY_ID = json_config["AWS_ACCESS_KEY_ID"]
    AWS_SECRET_ACCESS_KEY = json_config["AWS_SECRET_ACCESS_KEY"]
    conn = boto.connect_s3(
            aws_access_key_id = AWS_ACCESS_KEY_ID,
            aws_secret_access_key = AWS_SECRET_ACCESS_KEY) #is_secure=False # uncomment if you are not using ssl
    conn.create_bucket(bucketname)
    del conn

def deleteBucket0(bucketname, s3_key_info="s3_key.json"):
    #bucket has to be empty
    json_config = loadJson(s3_key_info)
    AWS_ACCESS_KEY_ID = json_config["AWS_ACCESS_KEY_ID"]
    AWS_SECRET_ACCESS_KEY = json_config["AWS_SECRET_ACCESS_KEY"]
    conn = boto.connect_s3(
            aws_access_key_id = AWS_ACCESS_KEY_ID,
            aws_secret_access_key = AWS_SECRET_ACCESS_KEY) #is_secure=False # uncomment if you are not using ssl
    try:
        conn.delete_bucket(bucketname)
    except:
        pass
    del conn

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

def awsCLCopycmd(from_search_pattern, myid, to_bucket, includefile_pattern_override=None):
    # sample input
    # from_search_pattern = "mybucket/result/*/ee/*results.json"
    # myid = 15437
    # to_bucket = 'zzzzzz.15437'
    # includefile_pattern_override = '/ee/*results.json'
    x = from_search_pattern.replace("s3://","").replace("S3://","")
    from_bucket = (x + "/").split("/")[0]
    x2 = x[:x.find("*")].split("/")[:-1]
    x_from = "s3://" + "/".join(x2) + "/" + str(myid) + "/"
    x_to = x_from.replace(from_bucket, to_bucket)
    cmd = 'aws s3 cp ' + x_from + ' ' + x_to + ' --exclude "*" '
    if includefile_pattern_override == None:
        includeformat = '--include "' + x.split('/')[-1] + '" --recursive'
    else:
        includeformat = '--include "' + includefile_pattern_override + '" --recursive'
    cmd += includeformat
    return cmd

def copyS3Files(s3_key_info, from_search_pattern, myid, to_bucket, includefile_pattern_override=None):
    cmd = awsEnvironcmd(s3_key_info=s3_key_info) + awsCLCopycmd(from_search_pattern=from_search_pattern, myid=myid, to_bucket=to_bucket,includefile_pattern_override=includefile_pattern_override)
    x = subprocess.call(cmd, shell=True)
    if x == 0:
        print "Successfully copied all needed files to temporary bucket " + to_bucket

def deleteBucket(bucketname, s3_key_info):
    cmd = awsEnvironcmd(s3_key_info=s3_key_info) + "aws s3 rm s3://" + bucketname + "/ --recursive"
    x = subprocess.call(cmd, shell=True)
    if x != 0:
        print "Bucket " + bucketname + " does not exist. No need to worry. :-)"
    del x
    deleteBucket0(bucketname, s3_key_info=s3_key_info)

if __name__ in ['__main__', 'temp_s3_buckets_bystructid']:
    def copys3Files2temp(myid, search_pattern, s3_key_info, temp_bucket_suffix = "zzzzzz.", includefile_pattern_override=None):
        ############ Sample Input #############
        # myid = 15437
        # temp_bucket_suffix = "zzzzzz."
        # search_pattern = "mybucket/result/*/ee/*results.json"
        # s3_key_info="s3_key.json"
        ###################################
        fhash = lambda x: int('9' * len(str(x))) + x
        temp_bucketname = temp_bucket_suffix + str(fhash(myid))
        try:
            createBucket(temp_bucketname, s3_key_info=s3_key_info)
            copyS3Files(s3_key_info, from_search_pattern=search_pattern, myid=myid, to_bucket=temp_bucketname, includefile_pattern_override=includefile_pattern_override)
        except:
            pass
    
    def deleteTempBucket(myid, s3_key_info, temp_bucket_suffix = "zzzzzz."):
        ############ Sample Input #############
        # myid = 15437
        # temp_bucket_suffix = "zzzzzz."
        # s3_key_info="s3_key.json"
        ###################################
        fhash = lambda x: int('9' * len(str(x))) + x
        temp_bucketname = temp_bucket_suffix + str(fhash(myid))
        try:
            deleteBucket(temp_bucketname, s3_key_info)
        except:
            pass
