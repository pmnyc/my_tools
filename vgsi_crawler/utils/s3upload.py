# -*- coding: utf-8 -*-
#!/usr/bin/env python

"""
@author: Man Peng

Sample Usage:

$ python s3upload.py

"""

import subprocess
import time
import os, sys

# load local files
from utils import load_settings
from utils import decorators

def getPlatform():
    x = sys.platform
    x = x.lower()
    if x.startswith('win'):
        return 'Windows'
    elif x.startswith('linux'):
        return 'Linux'
    else:
        return ''

def runBashScript(cmd, error_message):
    x = subprocess.call(cmd, shell=True)
    if x != 0:
        x = subprocess.call(cmd, shell=True)
        if x != 0:
            time.sleep(30)
            parameters = load_settings.loadParameters()
            decorators.writeLog(error_message, logfile=parameters['error_log_file'])
            raise Exception(error_message)

if __name__ == '__main__':
    
    platform = getPlatform()
    if platform != 'Linux':
        raise Exception("The system for running s3 upload program has to be Linux")

    parameters = load_settings.loadParameters()

    outputfolder = "./" + parameters['output_folder']
    if not(outputfolder.endswith("/")):
        outputfolder = outputfolder + "/"
    s3_outputfolder = parameters['S3_output_folder']

    output_update_cmd = 'aws s3 sync %s %s' %(outputfolder, s3_outputfolder)
    error_message = "file upload to S3  was not successful, try again..."

    ## upload output files to S3
    runBashScript(output_update_cmd, error_message)
    runBashScript(output_update_cmd, error_message)

    ## Find log files and upload them
    firstoutfile = os.listdir(parameters['output_folder'])[0]
    towninfo = "_".join(firstoutfile.split('_')[:2])
    logfile = parameters['log_file']
    errorlogfile = parameters['error_log_file']
    logfile_new = os.path.join(os.path.dirname(logfile), towninfo + "_"+os.path.basename(logfile))
    errorlogfile_new = os.path.join(os.path.dirname(errorlogfile), towninfo + "_"+os.path.basename(errorlogfile))
    try:
        os.rename(os.path.join(os.getcwd(),logfile), os.path.join(os.getcwd(),logfile_new))
    except:
        pass
    try:
        os.rename(os.path.join(os.getcwd(),errorlogfile), os.path.join(os.getcwd(),errorlogfile_new))
    except:
        pass
    
    log_update_cmd = 'aws s3 sync %s %s' %(os.path.dirname(logfile)+"/", parameters['S3_log_folder'])
    runBashScript(log_update_cmd, error_message)
    runBashScript(log_update_cmd, error_message)
    
    ## Find cached files and upload them
    cache_update_cmd = 'aws s3 sync %s %s' %('./cache/', parameters['S3_cache_folder'])
    try:
        runBashScript(cache_update_cmd, error_message)
        runBashScript(cache_update_cmd, error_message)
    except:
        print("The update of cached files to S3 failed...")    
