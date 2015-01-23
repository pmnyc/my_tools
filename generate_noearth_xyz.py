"""
@author: pm

Sample Usage:
$ python generate_noearth_xyz.py <xyz_data.txt> <myoutput.txt> <scan_radius=10> <low_point_cutff=1.8>

a)  all units must be meters
    scan_radius and low_point_cutff are two optional options
b)  xyz_data is the input xyz data (point cloud data, no header), \
    and outputfile is the .txt name for noearth data
c)  parameter low_point_cutff is the cut-off distance for removing points if the points are \
    above the lowest point within radius by this much
d)  scan_radius is the radius it uses to scan the data to determine the lowest group point
"""

import pandas as pd, numpy as np
from numpy import genfromtxt
import copy, random, string
from sklearn.cluster import MiniBatchKMeans
import matplotlib.pyplot as plt

def noearth(xyz_data, outputfile, scan_radius, low_point_cutff, plotcluster=False):
    xyz = genfromtxt(xyz_data, delimiter=',')
    #xyz.head()
    def addIndex(x):
        return np.hstack((x,np.reshape(xrange(len(x)),(len(x),1))))
    #randomselect = random.sample(range(len(xyz)),min(len(xyz),500000))
    xyz_new = copy.copy(xyz)
    xyz_noearth = xyz_new[0]
    counter = 0
    
    x_coor = xyz_new[:, 0]
    y_coor = xyz_new[:, 1]
    min_x_coor = np.min(x_coor)
    min_y_coor = np.min(y_coor)
    max_x_coor = np.max(x_coor)
    max_y_coor = np.max(y_coor)
    x_grids = np.ceil((max_x_coor - min_x_coor)/(scan_radius * 2.0))
    y_grids = np.ceil((max_y_coor - min_y_coor)/(scan_radius * 2.0))    

    #while len(xyz_new) >= 1:
    for i in range(int(x_grids)):
        for j in range(int(y_grids)):
            x_lowend = min_x_coor + 2*i * scan_radius
            x_uppend = min_x_coor + 2*(i+1) * scan_radius
            y_lowend = min_y_coor + 2*j * scan_radius
            y_uppend = min_y_coor + 2*(j+1) * scan_radius
            idx_considered1 = (x_coor >= 0.5*(x_uppend+x_lowend) - 0.5) & ((x_coor <= 0.5*(x_uppend+x_lowend) + 0.5)) \
                                & (y_coor >= y_lowend) & (y_coor <= y_uppend)
            idx_considered2 = (y_coor >= 0.5*(y_uppend+y_lowend) - 0.5) & ((y_coor <= 0.5*(y_uppend+y_lowend) + 0.5)) \
                                & (x_coor >= x_lowend) & (x_coor <= x_uppend)
            idx_considered = (x_coor >= x_lowend) & (x_coor <= x_uppend) & (y_coor >= y_lowend) & (y_coor <= y_uppend)
            newdata = xyz_new[idx_considered]
            newdata2 = xyz_new[idx_considered1 | idx_considered2]
            if len(newdata) == 0:
                counter += 1
                continue
            else:
                lowercenter = np.min(newdata2[:, 2]) #get lowest point through a cross
                
                if plotcluster:
                    #applies k-means to cluster
                    elev = newdata[:, 2]
                    elev = elev.reshape(elev.shape[0],1)
                    n_clusters = 2
                    mbk = MiniBatchKMeans(init='k-means++', n_clusters=n_clusters)
                    mbk.fit(elev)
                    mbk_means_labels = mbk.labels_
                    mbk_means_cluster_centers = mbk.cluster_centers_
                    mbk_means_labels_unique = np.unique(mbk_means_labels)
                    lowercenter = np.min(mbk_means_cluster_centers)
                    #Plot k-means results
                    fig = plt.figure(figsize=(8, 3))
                    fig.subplots_adjust(left=0.02, right=0.98, bottom=0.05, top=0.9)
                    colors = ['#4EACC5', '#FF9C34']
                    ax = fig.add_subplot(1, 1, 1)
                    #add_subplot(1, 3, 2) means row 1, total 3 plots, current location is 2
                    for k, col in zip(range(n_clusters), colors):
                        my_members = mbk_means_labels == k
                        cluster_center = mbk_means_cluster_centers[k]
                        ax.plot(elev[my_members, 0], 'w',
                                markerfacecolor=col, marker='.')
                        ax.plot(mbk_means_cluster_centers[0], 'o', markerfacecolor=col,
                                markeredgecolor='k', markersize=6)
                    ax.set_title('MiniBatchKMeans')
                    ax.set_xticks(())
                    #plt.text(-3.5, 1.8, 'train time: %.2fs\ninertia: %f' %(t_mini_batch, mbk.inertia_))

                xyz_noearth = np.vstack((xyz_noearth,newdata[newdata[:, 2] >= low_point_cutff + lowercenter]))
                counter += 1

    df = pd.DataFrame(xyz_noearth)
    test_file = open(outputfile,'w')
    df.to_csv(test_file,index=None, header=False)
    test_file.close()
    del test_file

def id_generator(size=8, chars=string.ascii_uppercase + string.ascii_lowercase + string.digits):
    return ''.join(random.choice(chars) for _ in range(size))

if __name__ == '__main__':
    import sys
    if len(sys.argv) < 3:
        print "Sample Usage: python generate_noearth_xyz.py <xyz_data.txt> <myoutput.txt> \n <scan_radius=10> <low_point_cutff=1.8>"
        exit(1)
    elif sum([1 for m in sys.argv if 'scan_radius' in m.lower()]) >=1:
        scan_radius = [m.lower() for m in sys.argv if 'scan_radius' in m.lower()][0].replace("scan_radius","").replace("=","").replace(" ","")
        scan_radius = float(scan_radius)
    elif sum([1 for m in sys.argv if 'low_point_cutff' in m.lower()]) >=1:
        low_point_cutff = [m.lower() for m in sys.argv if 'low_point_cutff' in m.lower()][0].replace("low_point_cutff","").replace("=","").replace(" ","")
        low_point_cutff = float(low_point_cutff)
    else:
        scan_radius = None
        low_point_cutff = None
    
    if scan_radius == None:
        scan_radius = 20
    if low_point_cutff == None:
        low_point_cutff = 1.8
        
    tempoutfile1 = id_generator() + ".txt"
    noearth(sys.argv[1], sys.argv[2], scan_radius, low_point_cutff)