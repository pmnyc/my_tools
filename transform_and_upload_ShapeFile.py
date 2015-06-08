# -*- coding: utf-8 -*-
"""
@author: pm
"""
import os, re, sys
from osgeo import ogr, osr

class esriprj2standards(object):
    """
    Sample Usage:
    x = esriprj2standards('/tmp/myshape.shp')
    x.transformProj(26986, '/tmp/mynewshape.shp')
    """
    def __init__(self, infile):
        #infile is the path for the shape file (ending with .shp)
        self.infile = infile
        
        self.shapeproj_path = re.sub('.shp', '.prj', infile)
        prj_file = open(self.shapeproj_path, 'r')
        prj_txt = prj_file.read()
        self.srs = osr.SpatialReference()
        self.srs.ImportFromESRI([prj_txt])
        #print 'Shape prj is: %s' % prj_txt
        #print 'WKT is: %s' % srs.ExportToWkt()
        #print 'Proj4 is: %s' % srs.ExportToProj4()
        #print srs.AutoIdentifyEPSG()
        #print 'EPSG is: %s' % srs.GetAuthorityCode(None)
        driver = ogr.GetDriverByName('ESRI Shapefile')
        shape = driver.Open(self.infile)
        self.layer= shape.GetLayer()
        crs = self.layer.GetSpatialRef()
        self.proj4 = crs.ExportToProj4()
        self.wkt = crs.ExportToWkt()
        self.geom_type = self.layer.GetGeomType()
        self.geom_type_name = ogr.GeometryTypeToName(self.geom_type)
    
    def transformProj(self, destEPSG, outfile):
        #destEPSG is the desired EPSG for transformed shapefile, for example, for whole MA, we use 26986
        #get path and filename seperately 
        (outfilepath, outfilename) = os.path.split(outfile)
        #get file name without extension            
        (outfileshortname, extension) = os.path.splitext(outfilename)   #get file name without extension 
 
        # Spatial Reference of the output file
        outSpatialRef = osr.SpatialReference()
        outSpatialRef.ImportFromEPSG(destEPSG)
  
        # create Coordinate Transformation 
        coordTransform = osr.CoordinateTransformation(self.srs, outSpatialRef)

        # Open the input shapefile and get the layer 
        driver = ogr.GetDriverByName('ESRI Shapefile')
        indataset = driver.Open(self.infile, 0)
        if indataset is None:
            print 'No file to open'
            sys.exit(1)
        inlayer = indataset.GetLayer()
 
        # Create the output shapefile but check first if file exists, delete the files
        if os.path.exists(outfile):
            driver.DeleteDataSource(outfile)
 
        outdataset = driver.CreateDataSource(outfile)
 
        if outfile is None:
            print 'You forgot to put the output shape file name!'
            sys.exit(1)
        outlayer = outdataset.CreateLayer(outfileshortname, geom_type=self.geom_type)
        feature = inlayer.GetFeature(0)
        featureitems = feature.items()
        featurekeys = featureitems.keys()
        numOfFeaturekeys = len(featurekeys)
        fieldDefn = [None] * numOfFeaturekeys
        for i in range(numOfFeaturekeys):
            fieldDefn[i] = feature.GetFieldDefnRef(featurekeys[i])
            outlayer.CreateField(fieldDefn[i])

        # get the FeatureDefn for the output shapefile 
        featureDefn = outlayer.GetLayerDefn()
        #Loop through input features and write to output file 
        infeature = inlayer.GetNextFeature()
        while infeature:
            #get the input geometry 
            geometry = infeature.GetGeometryRef()
            #reproject the geometry, each one has to be projected separately
            geometry.Transform(coordTransform)
            #create a new output feature 
            outfeature = ogr.Feature(featureDefn)
            #set the geometry and attribute 
            outfeature.SetGeometry(geometry)
            for i in range(numOfFeaturekeys):
                outfeature.SetField(featurekeys[i], infeature.GetField(featurekeys[i]))
            #add the feature to the output shapefile 
            outlayer.CreateFeature(outfeature)
            #destroy the features and get the next input features 
            outfeature.Destroy
            infeature.Destroy
            infeature = inlayer.GetNextFeature()
        #close the shapefiles 
        indataset.Destroy()
        outdataset.Destroy()
        #create the prj projection file 
        outSpatialRef.MorphToESRI()
        if outfilepath == '':
            file = open(outfileshortname + '.prj', 'w')
        else:
            file = open(outfile.replace('.shp','.prj'), 'w')
        file.write(outSpatialRef.ExportToWkt())
        file.close()


class loadShape2psql(object):
    """
    Sample Usage:
    x = loadShape2psql('data.myshaptable', '')
    x.uploadMultipleShape()
    """
    def __init__(self,  outputDBTable, all_shapefile_folder,
                 shp2postgres_exe_loc = 'C:/PostgreSQL/9.3/bin', targetSRID = 926986,
                 host = 'myhost', user = 'postgres', database = 'mydb'):
 
                 #outputDBTable, such as, data.myshape, is the database table for storing shape files
                 #all_shapefile_folder is the folder location for all shape files to be uploaded
                 
                 #shp2postgres_exe_loc is the location of shp2postgres.exe
                 #targetSRID is the SRID for the shape file to be uploaded
                 #host is the host of PostGreSQL server
                 #user is the user name
                 #database is what database to be uploaded to
        self.shp2postgres_exe_loc = shp2postgres_exe_loc
        self.targetSRID = targetSRID
        self.host = host
        self.user = user
        self.database = database
        
        self.outputDBTable = outputDBTable
        self.all_shapefile_folder = all_shapefile_folder
    
    def createNewFolder(self, new_directory):
        if not os.path.exists(new_directory):
            os.makedirs(new_directory)
        else:
            raise Exception('Folder already existed!!!')

    def deleteFolder(self, directory):
        if not os.path.exists(directory):
            pass
        else:
            os.rmdir(directory)

    def uploadOneShp(self, shpFile, add_mode):
        #shpFile is the location of the shape files to be uploaded
        #add_mode is either -c or -a for creating or appending new data table
        workdir = os.getcwd()
        os.chdir(self.shp2postgres_exe_loc)
        if add_mode == '-c':
            sys_cmd = 'shp2pgsql -s '+str(self.targetSRID)+' '+add_mode+' -g geom -I '
        else:
            sys_cmd = 'shp2pgsql -s '+str(self.targetSRID)+' '+add_mode+' -g geom '
        sys_cmd = sys_cmd + '"'+shpFile+'" '+self.outputDBTable+' '
        sys_cmd = sys_cmd + '| psql -d '+self.database+' -h '+self.host+' -U '+self.user+' '
        os.system(sys_cmd)
        os.chdir(workdir)
    
    def uploadMultipleShape(self):
        workdir = os.getcwd()
        files = os.listdir(self.all_shapefile_folder)
        shapefiles = []
        for ii in range(len(files)):
            if files[ii][-4:] != '.shp':
                continue
            else:
                shapefiles.append(files[ii])

        if len(shapefiles) == 0:
            raise Exception('No Shape to be uploaded')
        else:
            for jj in range(len(shapefiles)):
                shpFile = shapefiles[jj]
                if jj == 0:
                    add_mode = '-c' #define if we create new table or just insert records
                else:
                    add_mode = '-a' #append/insert new records
                curshapefile = os.path.join(self.all_shapefile_folder,shpFile)
                self.uploadOneShp(curshapefile, add_mode)
        os.chdir(workdir)

if __name__ == '__main__':
    import sys
    x = esriprj2standards('/tmp/myshape.shp')
    x.transformProj(26986, '/tmp/newshape.shp')
