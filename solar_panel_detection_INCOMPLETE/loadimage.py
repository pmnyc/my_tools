# -*- coding: utf-8 -*-
"""
This function is for loading the images into matrices

@author: 
"""

import os, sys, csv
import pandas as pd
import numpy as np
from scipy import misc
import matplotlib.pyplot as plt

def readCSVtoDict(myFilePath):
    with open(myFilePath, 'rb') as csvfile:
        res = []
        #sniff to find the format
        fileDialect = csv.Sniffer().sniff(csvfile.read(1024))
        csvfile.seek(0)
        #read the CSV file into a dictionary
        dictReader = csv.DictReader(csvfile, dialect=fileDialect)
        for row in dictReader:
            #do your processing here
            #print(row)
            res += [row]
    return res

def inputImage(image_dir, imagefiles, labels):
    # This function loads all image files from the list imagefiles and combine the labels 0,1 to the image pixel matrix
    counter = 0
    for imgfile in imagefiles:
        imgfile_name = os.path.splitext(imgfile)[0]
        try:
            image_matrix = misc.imread(os.path.join(image_dir, imgfile))
        except IOError as err:
            print("IOError: {0}, skip this file and continue...".format(err))
            continue
        # plt.imshow(image_matrix, cmap=plt.cm.gray) #show image
        assert image_matrix[:,:,0].shape == image_shape, "Image file %s shape is NOT %s" %(imgfile, str(image_shape))
        image_matrix = np.reshape(image_matrix,
                                   (image_matrix.shape[2], image_matrix.shape[0]*image_matrix.shape[1]))
        if np.int(labels.query('id == "'+imgfile_name+'"')['class']) == 0:
            y = np.array([0,1], dtype=np.int8)
        else:
            y = np.array([1,0], dtype=np.int8)  # y =[0,1] meaning does not have solar panel, y=[1,0] means it has solar panel
        train_X = [image_matrix, y] if counter==0 else np.vstack((train_X, [image_matrix, y]))
        counter += 1
    return train_X


###########  if __name__ == '__main__':

train_image_dir = "./data/train"
test_image_dir = "./data/test"
image_shape = (101, 101)
train_image_lables_dir = "./data/labels/train_solution.csv"
test_image_lables_dir = "./data/labels/test_solution.csv"

# labels must be of the format  id, class

"""
from glob import glob
filelist = glob('image*.tif') # use pattern to search for file names
"""
train_images = os.listdir(train_image_dir)
test_images = os.listdir(test_image_dir)
common_prefix_filenames = os.path.commonprefix(train_images + test_images)

train_labels = pd.read_csv(train_image_lables_dir)
test_labels = pd.read_csv(test_image_lables_dir)

train_labels['id'] = train_labels['id'].map(lambda x: common_prefix_filenames + str(int(x))) # add common prefix 'image' to the id to match image file names
test_labels['id'] = test_labels['id'].map(lambda x: common_prefix_filenames + str(int(x)))

traindata = inputImage(train_image_dir, train_images, train_labels)
testdata = inputImage(test_image_dir, test_images, test_labels)





