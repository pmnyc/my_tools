#!/usr/bin/python

'''

v1

***
License:

Creative Commons Attribution Non-Commercial License V2.0

http://creativecommons.org/licenses/by-nc/2.0/ca/legalcode.en

***
Theory:
(The brackets contain the Python variable describing each)

This program attempts to classify raw LiDAR points into buildings and non-buildings.

It does this by assuming roof tops are mostly flat. 

To assess flatness, it loops through all the LiDAR points (testfile), selecting a number of points (min_size) surrounding each point in a cluster.

From there, it computes the Delaunay Triangulation of this cluster of points. Using this Delaunay Triangulation, the volume of the cluster is computed by summing the volume of each tetrahedron.

A histogram is display which shows the volumes of all these clusters. A single threshold is input by the user (threshold) below which the cluster is of a building, and above which, the cluster is not a building.

Most histograms have two peaks, the best threshold is somewhere in the "valley". The histogram settings may need to be tweaked

The classification is then updated by the threshold provided.

Since the ground is usually flat too, the final classification loops through all the points, removing the points which are too close to the ground based upon a second threshold (height_tolerance).

***
Requirements:

-Any Linux or Windows machine. This was built on Ubuntu 12.04 at the time, so it may need to have the libraries tweaked for your version

***
Installation:

On Ubuntu 14.04/Debian (untested):

- sudo apt-get install python-liblas python-scipy
This should install all the needed libraries!

Windows/Mac:

The libraries will remain the same, but you'll be on your own for the installation of libraries. If you have specific instructions which work, let me know!

***
Workstation requirements:

Beware, this script is RAM intensive. 2.5million points is about 1.75GB of RAM and can take more than an hour. Python of course isn't the most ideal language for this and there is plenty of tweaking to do!

I did try to port some of this code to Nvidia CUDA but never could get it as accurate as the original version. Any advice here would be greatly appreciated!

***
Data:

http://www.opentopography.org/ is a great source for free LiDAR. What's needed is "all returns", of an urban or semi-urban area. The best data sets also approximately gridded/evenly distributed. Usually you don't need to do any further modification of the data but if it's too clustered, you may run into issues with this algorithm.

***
Usage:

You need to pass in 3 parameters, and a 4th after some processing has already been completed. A 5th parameter is derived internally.

The three input in the command line in order are testfile, min_size, height_tolerance.

testfile = the name of the raw LiDAR file
min_size = the size of each cluster, 15-60 is a reasonable range
height_tolerance = the height that all roofs are assumed to be from the ground. Must match the units of the LiDAR file in the Z-direction. 2.5meters is a nice number, or 8.2 feet,

the heightfile is internally computed from the testfile. ie: testfile = "file.las" , heightfile = "fileHeight.las". You will need to precompute the heightfile using lastools (http://www.cs.unc.edu/~isenburg/lastools/)

In lastools, there's a couple steps:

1) Use lasground to classify all the points which are ground "lasground -i file.las -o classifiedground.las" or similar.
2) Use lasheight to modify the Z-coordinate of the LiDAR file to be the height of each point to the local ground surface "lasheight.exe -i classifiedground.las -o fileHeight.las -replace_z"

Place "fileHeight.las" in the same directory as "file.las" and you should be good to go!

the threshold is input by the user from the plot. See https://a.fsdn.com/con/app/proj/planarrooftopdetectioninlidar/screenshots/OttHist45.png for an example. The dashed line shows the ideal threshold that was determined using an exhaustive search.

Then run python Version1.1.py [testfile] [min_size] [height_tolerance]

***
Tweaking:

Most of the time, the accuracy is split between 3 variables, the min_size, height_tolerance and the threshold. The threshold scales on the min_size, so unless the min_size is on the extreme, most of the tweaking is done to the threshold. The height_tolerance is generally stable and can be assumed to be at least 1-storey high.

There is also a minor tweaking of the classification with a buffer to remove local points where the neighbours are mostly roof or ground. This is set to 20%/80% where if there's 80% which are roof tops, the point is reclassified as roof. Generally, this changes less than 1% of points and doesn't really need to be tweaked

***
Further information:

If you would like a copy of my thesis further describing this code and other modifications, send me a message through SourceForge!
'''

import math
import matplotlib.pyplot as plt
from liblas import *
import numpy as np
from scipy.spatial import cKDTree
from scipy import *
from scipy.spatial import Delaunay
import sys      
def number_of_clustered (point_list):
    count = 0   
    for point in point_list:
        if point.roof == True:
            count += 1
    return count
def volume (vertice_list,point_list):
    sum = 0
    for vertice in vertice_list:
        AB = point_list[vertice[1]]-point_list[vertice[0]]
        AC = point_list[vertice[2]]-point_list[vertice[0]]
        AD = point_list[vertice[3]]-point_list[vertice[0]]
        sum+=math.fabs(np.dot(AB,np.cross(AC,AD)))
    sum=sum/6
    return sum  
def percent_roofs(cluster_list, size):
    roofs = 0.0
    non_roofs = 0.0
    for point in cluster_list:
        if point.roof:
            roofs +=1
        else:
            non_roofs+=1
    return roofs/size
def build_del_points(point_num_list,point_list):
    del_point = np.array([0,0,0])
    for point in point_num_list:
        del_point = np.vstack((del_point,np.array([point_list[point].x, point_list[point].y, point_list[point].z]))) 
    del_point = np.delete(del_point,0,0)    
    return del_point
testfile = str(sys.argv[1])
heightfile = str(sys.argv[1]).replace(".las","Height.las")
min_size = int(sys.argv[2])
height_tolerance = float(sys.argv[3])
f = file.File(testfile, mode='r')
f2 = file.File(heightfile, mode='r')
h = f.header
print "\nUsing source file:",testfile
print "Using height file:",heightfile
print "Contains:",len(f)," points"
print "Minimum building size:",min_size
print "Height tolerance for determining ground:",height_tolerance
print " -Loading file into RAM"
points = [p for p in f]
heights = [p for p in f2]   
f.close()
f2.close()
del f,f2
for idx,point in enumerate(points):
    point.roof = False
    point.h = heights[idx].z
X = [i.x for i in points]
Y = [i.y for i in points]
print "  *File loaded into RAM"
print " -Making KDTree"
tree_part = cKDTree(zip(X,Y))
del X,Y,heights
print "  *Done making KDTree"
print " -Calculating volumes of points"
for point in points:
    sorts =  tuple((cKDTree.query(tree_part,(point.x, point.y),k=min_size))[1])
    dl = Delaunay(build_del_points(sorts, points))
    point.volume = volume(dl.vertices, dl.points)
volumes = [i.volume for i in points]

plt.hist(volumes, bins=1000, histtype="step")
plt.xlabel(str("Volume of "+str(min_size)+" point clusters"))
plt.ylabel("Frequency")
plt.show()

threshold = input(" ***Enter the desired threshold value: ")
outfile = file.File(testfile.replace(".las","") + "_" + str(threshold) + "_" + str(min_size) + "_" + str(height_tolerance) + ".las", mode='w', header=h)
print " *Done calculating volumes of points, threshold to be used is",threshold,"m^3"
for point in points:
    sorts =  tuple((cKDTree.query(tree_part,(point.x, point.y),k=min_size))[1])
    if point.volume <= threshold:
        for p in xrange(min_size):
            points[sorts[p]].roof = True
print "  *Done clustering"
print "    Number of clustered points so far:",number_of_clustered(points)
for point in points:
    if point.h <= height_tolerance:
        point.roof = False
print "Buffering point cloud to nearest neighbors"
for point in points:
    sorts =  tuple((cKDTree.query(tree_part,(point.x, point.y),k=min_size))[1])
    window_cluster = [points[sorts[i]] for i in xrange(min_size)]
    percent = percent_roofs(window_cluster,min_size)
    if  percent <= 0.2:
        point.roof = False
    elif percent >=0.8:
        point.roof = True
del window_cluster
print "Number of clustered points so far:",number_of_clustered(points)
for point in points:
    if point.roof:
        point.classification = 6
    else:
        point.classification = 1
    outfile.write(point)
outfile.close()
