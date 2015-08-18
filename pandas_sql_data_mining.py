# -*- coding: utf-8 -*-
"""
@author: pm

This program is to introduce pandas dataframe manipulation, pandas interaction with sql server
"""

import pyodbc
import copy
import os, fnmatch
import pandas as pd, numpy as np
import pandas.io.sql as psql
from sqlalchemy import create_engine

engine = create_engine('mssql+pyodbc://myserver/mydb')
#engine = create_engine('mssql+pyodbc://server/database')
#engine = create_engine('mssql+pyodbc://user:password@server/database')
connStr = (
    r'Driver={SQL Server};' +
    r'Server=myserver;' +
    r'Database=ElectricLoadForecast;' +
    r'Trusted_Connection=Yes;'
    #UID=myusername;PWD=password'
    )
conn = pyodbc.connect(connStr)

sqlcmd = 'SELECT top 10 * FROM dbo.table'
sqldf = psql.read_sql(sqlcmd, conn) # or replace conn with engine
conn.close()

engine.has_table("mytable",schema="dbo") #to check existence of table 'mytable'

inputfile = "my.csv"
inputdf = pd.read_csv(inputfile,header=0)
inputdf['OPR_DATE'] = pd.to_datetime(inputdf['OPR_DATE'])
inputdf.to_sql("zzzzz", engine, schema="dbo",index=False)

######### Some Pandas Data Frame Manipulation, Selection ############
def pdindx_intercept(*argv):
    #import numpy as np
    #argv is a list of lists
    # for example, *argv can be 
        #a=[True,True]
        #b=[False,True]
    if len(argv) < 1:
        raise Exception("Need at least one argument")
    numargs = len(argv)
    if numargs == 1:
        return argv[0]
    elif len(argv[0]) == 0:
        return []
    else:
        for i in range(numargs):
            if i == 0:
                out = np.array(argv[i])
            else:
                out = out & np.array(argv[i])
        return out.tolist()

def pdindx_setdiff(a,b):
    #import numpy as np
    # for example 
    #a=[True,True]
    #b=[False,True]
    if len(a) == 0 or len(b) == 0:
        return []
    else:
        return (np.array(a) & (~(np.array(b)))).tolist()

def pdindx_union(*argv):
    #import numpy as np
    #argv is a list of lists
    # for example, *argv can be 
        #a=[True,True]
        #b=[False,True]

    if len(argv) < 1:
        raise Exception("Need at least one argument")
    numargs = len(argv)
    if numargs == 1:
        return argv[0]
    elif len(argv[0]) == 0:
        return []
    else:
        for i in range(numargs):
            if i == 0:
                out = np.array(argv[i])
            else:
                out = out | np.array(argv[i])
        return out.tolist()

def deleteFiles(pattern, path=None): # This is to delete all files of the same pattern
    #sample pattern = "*.pyc"
    #sample usage: deleteFiles(pattern="*.pyc")  # This is to delete all files with extension .pyc
    if path==None:
        cwd = os.getcwd()
    else:
        cwd = path
    filelist = os.listdir(cwd)
    pattn = pattern.lower()
    files = filter(lambda x: fnmatch.fnmatch(x.lower(),pattn), filelist)
    if len(files) >=1 :
        for i in range(len(files)):
            os.remove(files[i])
    print "Files deleted are \n" + (" " * 6) + ", ".join(files)


###  Data Manipulation  ###

idx_cd_case1 = ([int(x) in [102,292] for x in df['var1']])
idx_cd_case2 = ([int(x) in [710, 911] for x in df['var1']])

tmp = df.loc[idx_cd_case1,:]
df.loc[idx_cd_case1,['var2']] = tmp['var22'] + tmp['var23']
df.loc[idx_cd_case1,['var2']] = tmp['var22'] + tmp['var23']
index_max = df['var1'].argmax() # This is to find index with highest var1 value
tmp = df.loc[idx_cd_case1,:]
df.loc[df['keyvar'] < 0,['flag']] = 1
df['bill'] = df.loc[:,['a','b']].sum(axis = 1)
df.loc[~(df['control'].notnull()),['var3']]=0
df.loc[pdindx_intercept(idx_cd_case1,idx_cd_case2),['var4']] = 3.1415 * df['var2'][pdindx_intercept(idx_cd_case1,idx_cd_case2)]

df1 = copy.copy(df)
df2 = copy.copy(df)
df3 = pd.concat([df1, df2], axis=1) # This is to combine two data frames with same index by putting two columns
                                    # side by side
