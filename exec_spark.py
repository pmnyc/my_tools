"""
@author: pm

This program is to execute the spark on the program.

Sample Usage:
~/spark/bin/spark-submit \
    --master yarn-client \
    --num-executors 12 \
    --executor-cores 1 \
    ./exec_spark.py
    
Use --num-executors --executor-cores so that their product is total # of cores on slave nodes
    for larger instances in slave nodes, use 2+ as --executor-cores
    use --executor-memory 2G (or whatever size you want for each executor)

, where --executor-cores needs to be 1 for defining a core for each executor,
and --num-executors can be the total number of cores in the cluster. To use pyspark,
one needs to set yarn-client as master.

In the code, set 3 X # of cores in the slave nodes as # of slices/partitions.
--master local[#cores] is only to let it run on master node in standalone mode.

Launch EMR Spark Cluster
aws emr create-cluster \
    --no-auto-terminate \
    --name MySparkCluster \
    --tags "Name=MyInstanceName" \
    --ami-version 3.7.0 \
    --instance-type m3.xlarge \
    --instance-count 3 \
    --use-default-roles \
    --ec2-attributes KeyName=emrspark,SubnetId=subnet-aabbccdd \
    --applications Name=Hive \
    --bootstrap-actions Path=s3://support.elasticmapreduce/spark/install-spark Path=s3://mybucket/sparkconfig.sh

"""

import get_list_of_ids_ons3
import numpy as np
import os, fnmatch, sys
import socket, urllib, json
import exec_single

from pyspark import SparkConf, SparkContext
from operator import add

def FilesMatchPattern(pattern):
    files_ = os.listdir(os.getcwd())
    return filter(lambda x: fnmatch.fnmatch(x.lower(),pattern.lower()), files_)

def removeSlash(x):
    if x.endswith("/"):
        return x[:-1]
    else:
        return x

def runID(id, reslt_search_pattern , usage_search_pattern , customer_data, s3_output,
            s3_key_info, temp_bucket_suffix):
        count = 0
        try:
            exec_single.main(id=id, reslt_search_pattern = reslt_search_pattern,
                    usage_search_pattern = usage_search_pattern,
                    customer_data = customer_data, s3_output = s3_output,
                    s3_key_info = s3_key_info, temp_bucket_suffix = temp_bucket_suffix)
            count += 1
        except:
            print str(id) + ' has not returned a result'
            print "Unexpected error:", sys.exc_info()[0]
            #raise
        return count

if __name__ == '__main__':
    ####### Parameters #########
    ############################
    id_selected = None #this is to specify the list of IDs to run. Set None if we use complete list
    n_cores = 8 #specify number of cores in slave nodes
    path_pattern = "s3://mybuckets/result"
    s3_output = 's3://mybucket/myoutput' #output folder for all output files
    
    ###
    customer_data = "mycustomer.csv"
    s3_key_info = "s3_key.json"
    sparkprog_folder = os.getcwd() #defines the directory for programs to be run in spark
    
    ###
    reslt_search_pattern = removeSlash(path_pattern).replace("s3://","") + "/*/ee/*results.json"
    usage_search_pattern = removeSlash(path_pattern).replace("s3://","") + "/*/ee/*myusage.html"
    ############################
    ############################

    ids = get_list_of_ids_ons3.main(path_pattern=path_pattern, s3_key_info=s3_key_info)
    if id_selected != None:
        ids = np.intersect1d(ids,id_selected)

    ### Run Spark for cluster computing
    # masterip = socket.gethostbyname(socket.gethostname()) #this is private ip
    # masterip = json.loads(urllib.urlopen("http://ip.jsontest.com/").read())["ip"] #this is public ip
    # sparkmasterip = "spark://" + masterip + ":7077"
    conf = SparkConf().setAppName("pm_spark")
    #conf = conf.setMaster("local[12]")
    #conf.set("spark.akka.failure-detector.threshold", 900000000.0)
    #conf.set("spark.scheduler.revive.interval", 99999999999)
    #slave_memory = "4g" #set memory of slave node to be 4GB
    #conf.set("spark.executor.memory", slave_memory)
    conf.set("spark.scheduler.mode", "FAIR") #default is FIFO
    sc = SparkContext(conf=conf)

    files_to_add_pattern = ['*.py', '*.txt', '*.json', '*.csv']
    pyfiles_list = []
    for i in range(len(files_to_add_pattern)):
        pyfiles_list += FilesMatchPattern(files_to_add_pattern[i])

    for f in pyfiles_list:
        sc.addPyFile(os.path.join(sparkprog_folder,f))

    slices = 3 * n_cores
    slices = min(slices, len(ids))  #This is just set upper limit of the number of slices to total length of ids
    if slices > 0:
        distList = sc.parallelize(ids, slices)
    else:
        distList = sc.parallelize(ids)

    rdd = distList.map(lambda x: runID(id=int(x), reslt_search_pattern = reslt_search_pattern,
                    usage_search_pattern = usage_search_pattern,
                    customer_data = customer_data, s3_output = s3_output,
                    s3_key_info = s3_key_info, temp_bucket_suffix = "zzzzz9xzufdj"))
    rdd.cache()
    totalcount = rdd.reduce(add)
    sc.stop()
    print "Total of " + str(totalcount) + " IDs are processed"