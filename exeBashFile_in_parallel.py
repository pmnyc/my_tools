# -*- coding: utf-8 -*-
"""
This is to run simple bash file (on Linux) using Python's simple parallel computing
@author: pm

sample usage:
    $ python exeBashFile_in_parallel.py mybashfile.sh
where, the mybashfile.sh is the bash file one wants to distribute

For example, $ echo 'ls -l' > mybashfile.sh
    to create a temporary sample bash file to test this code
"""

import sys, os, subprocess
from multiprocessing import Pool, cpu_count

def runcommd(x):
    # process = subprocess.Popen(x, stdout=subprocess.PIPE, stderr=subprocess.PIPE,shell=True)
    # if process.poll() == 0:
        # print x
    # else:
        # print "FAILED " + x
    process = 1
    try:
        process = subprocess.check_call(x,shell=True)
    except:
        print "FAILED TO EXECUTE " + x
    if process == 0:
        pass
    else:
        print "FAILED TO EXECUTE " + x

if __name__ == "__main__":
    if len(sys.argv) != 2:
        print "Sample Usage is $ python exeBashFile_in_parallel.py <mybashfile.sh>"
        exit(1)
    else:
        bashfile = sys.argv[-1]
        ncores = cpu_count()
        file = open(bashfile,"r")
        cmd = file.readlines()
        cmd = [("/bin/sh -c '" + x.replace("; \n","").replace("; ","").strip() + "'") for x in cmd]
        file.close
        del file

        print "This machine has", ncores, "cores"
        pool = Pool(processes=ncores)
        pool.map(runcommd, cmd)
