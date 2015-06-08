# -*- coding: utf-8 -*-
"""
@author: pm
"""

import os, sys, shutil, osgeo.ogr as ogr, osgeo.osr as osr

def downloadtoShp(host, dbname, user, password, polygonname, dbtable = 'public.temp_view', port=5432, EPSG_touse=26986):
    """
    # Sample Inputs
    host = 'myhost.us-east-1.rds.amazonaws.com'
    dbname = "mydb"
    port = 5432
    user = 'myuser'
    password = 'mypwd'
    dbtable = 'public.temp_view_104967594'

    polygonname = "mypoly_0000000.shp"
    EPSG_touse = 26986
    """

    polygonname_noext = os.path.splitext(polygonname)[0]
    polygonname_noext = polygonname_noext.encode('utf-8')
    #output = polygonname
    output = polygonname_noext
    
    # Schema definition of SHP file
    out_driver = ogr.GetDriverByName('ESRI Shapefile')

    try:
        del out_ds
    except NameError:
        print 'No out_ds is available for deletion, please ignore this and continue'
    if os.path.exists(output):
        out_driver.DeleteDataSource(output)
    out_ds = out_driver.CreateDataSource(output)
    out_srs = osr.SpatialReference()
    out_srs.ImportFromEPSG(EPSG_touse)
    out_layer = out_ds.CreateLayer(polygonname_noext, out_srs, geom_type=ogr.wkbPolygon)

    PGcomd = "PG: host=" + host + " dbname=" + dbname + " user=" + user + " password=" + password

    conn=ogr.Open(PGcomd)
    #print conn
    if conn is None:
        print 'Could not open a database or GDAL is not correctly installed!'
        sys.exit(1)

    #layer = conn.GetLayerByName(dbtable)
    layer = conn.ExecuteSQL("select * from " + dbtable)

    numoffeats = layer.GetFeatureCount()
    feats = [None] * numoffeats
    feats = map(lambda i: layer.GetFeature(i), range(numoffeats))

    feat = feats[0]
    feat_keys = feat.keys()

    for i in range(len(feat_keys)):
        fieldDefn = feat.GetFieldDefnRef(feat_keys[i])
        out_layer.CreateField(fieldDefn)
    #del i
    outfeatureDef = out_layer.GetLayerDefn()

    for i in range(numoffeats):
        outfeature = ogr.Feature(outfeatureDef)
        feat = feats[i]
        outfeature.SetGeometry(feat.GetGeometryRef())
        for j in range(len(feat_keys)):
            outfeature.SetField(feat_keys[j],feat.GetField(feat_keys[j]))
        out_layer.CreateFeature(outfeature)
        outfeature.Destroy()
        feat.Destroy()

    conn.Destroy()
    out_ds.Destroy()

    spfiles = os.listdir(os.path.join(os.getcwd(),polygonname_noext))
    
    for i in range(len(spfiles)):
        shutil.move(os.path.join(os.getcwd(),polygonname_noext,spfiles[i]), os.getcwd())

    shutil.rmtree(polygonname_noext)

if __name__ in ['__main__','pggis2shp']:
    #use __name__ == '__main__' if running codes in the current file
    #use __name__ == 'pggis2shp' if calling this code in another python codes
    #import sys
    """sample usage
    python pggis2shp.py -host myhost -dbname mydb -user myuser -password mypwd -polygonname mypoly.shp -port 5432
    """
    argv = sys.argv #here, in the sys.argv, even numerical values are passed as strings
    i=1
    if len(argv) <= 3:
        raise Exception('Too few arguements')
    while i <= len(argv)-1:
        #print argv[i]
        if argv[i]=="-host":
            host=argv[i+1]
        elif argv[i]=="-dbname":
            dbname=argv[i+1]
        elif argv[i]=="-user":
            user=argv[i+1]
        elif argv[i]=="-password":
            password=argv[i+1]
        elif argv[i]=="-polygonname":
            polygonname=argv[i+1]
        elif argv[i]=="-dbtable":
            dbtable=argv[i+1]
        elif argv[i]=="-port":
            port=argv[i+1]
        elif argv[i]=="-EPSG_touse":
            EPSG_touse=argv[i+1]
        i += 1
    
    def addprime(x):
        #if isinstance(x, basestring):
        return "'" + str(x) + "'"

    args = addprime(host) + ", " + addprime(dbname) + ", " + addprime(user) + ", " + addprime(password) + ", " + addprime(polygonname)

    try:
        args = args + ", dbtable=" + addprime(dbtable)
    except NameError:
        args = args
    try:
        args = args + ", port=" + str(port)
    except NameError:
        args = args
    try:
        args = args + ", EPSG_touse=" + str(EPSG_touse)
    except NameError:
        args = args
    
    exec_cmd = "downloadtoShp(" + args + ")"
    exec(exec_cmd)
