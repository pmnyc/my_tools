# -*- coding: utf-8 -*-
#!/usr/bin/env python

### Multiprocessing Templates ###
"""
import os
import multiprocessing as mp

def run(filename_def_param): 
    filename, def_param = filename_def_param # unpack arguments
    ... # call external program on `filename`

def safe_run(*args, **kwargs):
    #Call run(), catch exceptions.
    try: run(*args, **kwargs)
    except Exception as e:
        print("error: %s run(*%r, **%r)" % (e, args, kwargs))

def main():
    # populate files
    ws = r'D:\Data\Users\jbellino\Project\stJohnsDeepening\model\xsec_a'
    workdir = os.path.join(ws, r'fieldgen\reals')
    files = ((os.path.join(workdir, f), ws)
             for f in os.listdir(workdir) if f.endswith('.npy'))

    # start processes
    n_cores = multiprocessing.cpu_count()
    pool = mp.Pool() # use all available CPUs
    pool.map(safe_run, files)

if __name__=="__main__":
    mp.freeze_support() # optional if the program is not frozen
    main()


If there are many files then pool.map() could be replaced by for _ in pool.imap_unordered(safe_run, files): pass.
There is also mutiprocessing.dummy.Pool that provides the same interface as multiprocessing.Pool but uses threads instead of processes that might be more appropriate in this case.
You don't need to keep some CPUs free. Just use a command that starts your executables with a low priority (on Linux it is a nice program).
"""

### Sample 2
"""
import multiprocessing

def runSimulation(params):
    #This is the main processing function. It will contain whatever
    code should be run on multiple processors.

    param1, param2 = params
    # Example computation
    processedData = []
    for ctr in range(1000000):
    processedData.append(param1 * ctr - param2 ** 2)

    return processedData

if __name__ == '__main__':
    # Define the parameters to test
    param1 = range(100)
    param2 = range(2, 202, 2)

    # Zip the parameters because pool.map() takes only one iterable
    params = zip(param1, param2)

    pool = multiprocessing.Pool()
    results = pool.map(runSimulation, params)
"""

### Sample 3
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
"""