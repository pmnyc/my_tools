#!/usr/bin/env python
# -*- coding: utf-8 -*-
"""
@author: pm

This program is for downloading files under an ftp path. It can also 
    go in inside the folders to download files

Sample Usage:
>>> ftp_path = 'ftp://coast.noaa.gov/pub/DigitalCoast/lidar1_z/geoid12a/data/1436/'
>>> parallelDownload(ftp_path)
    or
>>> myfolder = os.path.join(os.getcwd(),'folder1')
>>> parallelDownload(ftp_path, localDir=myfolder)
"""

import os, time
from ftplib import FTP
from multiprocessing import cpu_count

# from multiprocessing import pool
# from functools import partial
# from itertools import repeat
# import ftplib

class syncFTP(object):
    """ This is for syncing content from ftp to local directory"""
    def __init__(self, ftp_path, userName=None, passWord=None,
                    localDir=None, deleteRemoteFiles=False,
                    onlyDiff=True):
        self.ftp_path = addSlash(ftp_path)
        self.userName = userName
        self.passWord = passWord
        self.localDir = localDir
        self.deleteRemoteFiles = deleteRemoteFiles
        self.onlyDiff = onlyDiff
        self.ftp_connection_count = 0
        # if self.localDir does not exist, then create a folder
        if self.localDir == None:
            self.localDir = os.getcwd()
        if not(os.path.isdir(self.localDir)):
            os.mkdir(os.path.join(self.localDir))

    @staticmethod
    def timeStamp():
        """returns a formatted current time/date"""
        #sample: 'Tue 18 Aug 2015 11:13:41 AM'
        return str(time.strftime("%a %d %b %Y %I:%M:%S %p"))

    @staticmethod
    def parseRemotepath(ftp_path):
        path1 = ftp_path[ftp_path.find('//')+2:]
        serverName = path1.split('/')[0]
        remotePath = path1.replace(serverName+'/','')
        return {'serverName':serverName, 'remotePath':remotePath}

    def syncFTPsetting(self):
        """ This is to set the FTP download settings """
        self.serverName = self.parseRemotepath(self.ftp_path)['serverName']
        self.remotePath = self.parseRemotepath(self.ftp_path)['remotePath']
        try:
            ftp = FTP(self.serverName)
            self.ftp_connection_count += 1
        except:
            print "Couldn't find server"
        ftp.login(self.userName,self.passWord)
        ftp.cwd(self.remotePath)
        if self.localDir == None:
            self.localDir = os.getcwd()
        try:
            self.ftp = ftp
            print "Connecting..."
            ## This is to get the difference between two folders ##
            if self.onlyDiff:
                lFileSet = set(os.listdir(self.localDir))
                rFileSet = set(ftp.nlst())
                transferList = list(rFileSet - lFileSet)
            else:
                transferList = ftp.nlst()
            self.transferList = transferList
        except Exception, e:
            print("Unexpected Error, "+str(e))
            print "Connection Error at " + self.timeStamp()
        #ftp.close() # Close FTP connection

    def downloadFile(self, fl):
        """
        This is for downloading file given file name fl
        Connect to an FTP server and download files to a local directory
        """
        if self.ftp_connection_count == 0:
            self.syncFTPsetting()
        else:
            pass
        # create a full local filepath
        localFile = os.path.join(self.localDir,fl)
        #open a the local file
        fileObj = open(localFile, 'wb')
        # Download the file a chunk at a time using RETR
        try:
            self.ftp.retrbinary('RETR ' + fl, fileObj.write)
            # Close the file
            print("File "+fl + " was downloaded.")
        except:
            fileObj.close()
            os.remove(localFile)
            raise Exception(fl + " may be a folder")
        # Delete the remote file if requested
        if self.deleteRemoteFiles:
            self.ftp.delete(fl)
            print("File "+fl+" is downloaded and deleted")
        fileObj.close()

def addSlash(f):
    if not(f.endswith('/')):
        return f+'/'
    else:
        return f

def parallelDownload(ftp_path, userName=None, passWord=None,
                    localDir=None, deleteRemoteFiles=False,
                    onlyDiff=True):
    ftpobj = syncFTP(ftp_path=ftp_path, userName=userName, passWord=passWord,
                    localDir=localDir, deleteRemoteFiles=deleteRemoteFiles,
                    onlyDiff=onlyDiff)
    ftpobj.syncFTPsetting()
    ncores = cpu_count()
    print("This computer has "+str(ncores)+" cores.")
    filesMoved = 0
    print str(len(ftpobj.transferList)) + " files will be downloaded..."
    for f in ftpobj.transferList:
        try:
            ftpobj.downloadFile(f)
            filesMoved += 1
        except Exception, e:
            print(str(e))
            os.mkdir(os.path.join(ftpobj.localDir,f))
            newpath = os.path.join(ftpobj.localDir,f)
            # This uses a recursive method for downloading subfolders
            ftp_path2 = addSlash(os.path.join(ftp_path,f))
            parallelDownload(ftp_path2, userName=userName, passWord=passWord,
                    localDir=newpath, deleteRemoteFiles=deleteRemoteFiles,
                    onlyDiff=onlyDiff)
    print "There are " + str(filesMoved) + " files are downloaded on " + ftpobj.timeStamp()
    #pool = Pool(processes=ncores)
    #pool.map(par_down, ftpobj.transferList)
    #pool.close()
