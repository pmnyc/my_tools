import cv2
import numpy as np
from scipy import ndimage as ndi
import matplotlib.pyplot as plt

from skimage.morphology import watershed, disk
from skimage.filters import rank
from skimage.util import img_as_ubyte
from PIL import Image, ImageDraw, ImageFont


def getSegmentedImage(imagefile, show_image_width_inches=10):
    img = cv2.imread(imagefile)
    gray = cv2.cvtColor(img,cv2.COLOR_BGR2GRAY)
    image = img_as_ubyte(gray)
    image_shape = map(lambda x: int(x), np.shape(image))
    fig_width = show_image_width_inches
    fig_height = fig_width / (image_shape[1]*1.0/image_shape[0])

    # denoise image
    denoised = rank.median(image, disk(2))

    # find continuous region (low gradient -
    # where less than 10 for this image) --> markers
    # disk(5) is used here to get a more smooth image
    markers = rank.gradient(denoised, disk(5)) < 10
    markers = ndi.label(markers)[0]

    # local gradient (disk(2) is used to keep edges thin)
    gradient = rank.gradient(denoised, disk(2))

    # process the watershed
    labels = watershed(gradient, markers)

    # display results
    fig, axes = plt.subplots(nrows=2,ncols=2, sharex=True, sharey=True,
                                 figsize=(fig_width*2, fig_height*2))
    ax0, ax1, ax2, ax3 = axes.flatten()

    ax0.imshow(image, cmap=plt.cm.gray, interpolation='nearest')
    ax0.set_title("Original")
    ax1.imshow(gradient, cmap=plt.cm.spectral, interpolation='nearest')
    ax1.set_title("Local Gradient")
    ax2.imshow(markers, cmap=plt.cm.spectral, interpolation='nearest')
    ax2.set_title("Markers")
    ax3.imshow(image, cmap=plt.cm.gray, interpolation='nearest')
    ax3.imshow(labels, cmap=plt.cm.spectral, interpolation='nearest', alpha=.7)
    ax3.set_title("Segmented")

    for ax in axes.flatten():
        ax.axis('off')

    fig.subplots_adjust(hspace=0.01, wspace=0.01, top=0.9, bottom=0,
                        left=0, right=1)
    plt.show()


def labelCenter(label, labels):
    # this function is to find the center of the lable from all labels
    i_queue =[]
    j_queue = []
    for i in range(len(labels)):
        for j in range(len(labels[0])):
            if labels[i][j] == label:
                i_queue.append(i)
                j_queue.append(j)
    i_center = int(np.mean(np.unique(i_queue)))
    j_center = int(np.mean(np.unique(j_queue)))
    return i_center, j_center

def roofSegmentation(imagefile, 
                    shape_area,
                    output_image_file,
                    show_image_width_inches =10,
                    has_earth=True,
                    mini_area_threshould = 5,
                    slope = 0,
                    disk_edge = 2,
                    disk_marker = 5,
                    gradient_threshold = 10):

    """
    # Sample Parameter Values and Meanings
    shape_area, # this is the area of polygon shape of this roof, obtained from shape file
    show_image_width_inches =10 # output image file width in inches
    has_earth=True # this means the image includes grounds which need to be cleaned later on
    mini_area_threshould = 5 # minimum area of roof plane to be considered
    slope = 0 # general slope of the roof planes
    disk_edge = 2 # the rest three parameters are for defining how to make clusters based on gradient change
    disk_marker = 5
    gradient_threshold = 9
    """

    img = cv2.imread(imagefile)
    gray = cv2.cvtColor(img,cv2.COLOR_BGR2GRAY)
    image = img_as_ubyte(gray)
    image_shape = map(lambda x: int(x), np.shape(image))
    fig_width = show_image_width_inches
    fig_height = fig_width / (image_shape[1]*1.0/image_shape[0])
    del fig_height # this parameter is deprecated

    # denoise image
    denoised = rank.median(image, disk(disk_edge))

    # find continuous region (low gradient -
    # where less than 10 for this image) --> markers
    # disk(5) is used here to get a more smooth image
    markers = rank.gradient(denoised, disk(disk_marker)) < gradient_threshold
    markers = ndi.label(markers)[0]

    # local gradient (disk(2) is used to keep edges thin)
    gradient = rank.gradient(denoised, disk(disk_edge))

    # process the watershed
    labels = watershed(gradient, markers)

    if has_earth:
        grounds = labels[0][0], labels[image_shape[0]-1][image_shape[1]-1], labels[0][image_shape[1]-1], labels[image_shape[0]-1][0]
        label_set, counts = np.unique(filter(lambda x: x not in grounds, labels.flatten()), return_counts=True)
    else:
        label_set, counts = np.unique(labels.flatten(), return_counts=True)

    pixel_size = (shape_area + 0.0)/sum(counts)
    area_dic = {}
    for i in range(len(label_set)):
        label = label_set[i]
        cnt = counts[i]
        area = cnt * pixel_size / np.cos(np.pi * slope /180.0)
        if area >= mini_area_threshould:
            area_dic[label] = cnt * pixel_size

    # create plots
    fig, ax = plt.subplots()
    image_height = show_image_width_inches/((image_shape[1]+0.0)/(image_shape[0]+0.0))
    fig.set_size_inches(show_image_width_inches,image_height)
    ax.imshow(image, cmap=plt.cm.gray, interpolation='nearest')
    ax.imshow(labels, cmap=plt.cm.spectral, interpolation='nearest', alpha=.7)
    ax.set_title("Segmented")
    ax.axis('off')
    area_sum = 0
    for label in area_dic.keys():
        center = labelCenter(label, labels)
        ax.text(center[1], center[0], str(int(np.ceil(area_dic[label]))), style='italic', fontsize=13,
            bbox={'facecolor':'white', 'alpha':0.5, 'pad':10})
        area_sum += area_dic[label]
    fig.savefig(output_image_file)
    del fig
    print("Total Area is %s" %str(area_sum))


######## Solution #########

getSegmentedImage(imagefile="5 Nichols St_resize - Copy.jpg")

roofSegmentation(imagefile="5 Nichols St_resize - Copy.jpg", shape_area=311, output_image_file='_temp.png', slope = 0,
                    disk_edge = 2, disk_marker = 5, gradient_threshold = 10)

