import cv2
import numpy as np
#from scipy import ndimage as ndi
import matplotlib.pyplot as plt

#from skimage.morphology import watershed, disk
#from skimage.filters import rank
from skimage.util import img_as_ubyte
#from PIL import Image, ImageDraw, ImageFont
#import matplotlib.image as mpimg

#import matplotlib.pyplot as plt
#from skimage.filters import threshold_otsu, threshold_adaptive
#import numpy as np
#import pylab

def weightedAvg(color, mask):
    # color = red, a 2D matrix
    # mask = shadow, a 2D matrix
    return np.multiply(color+0.0, mask+0.0).sum().sum() / (0.00+mask.sum().sum())

def rgb2gray(rgb):
    return np.dot(rgb[...,:3], [0.299, 0.587, 0.144])

def roughShadowRemoval(imagefile, shadow_gray_threshold=100):
    if type(imagefile) is str:
        image = cv2.imread(imagefile)
    else:
        image = imagefile[:] + 0
    gray = cv2.cvtColor(image,cv2.COLOR_BGR2GRAY)
    #gray = cv2.GaussianBlur(gray, (21, 21), 0)
    image_gray = img_as_ubyte(gray)
    shadow_mask = (image_gray < shadow_gray_threshold) * image_gray
    lite_mask = (image_gray >= shadow_gray_threshold) * image_gray

    #fig, ax = plt.subplots()
    #ax.imshow(shadow_mask)

    kernel = cv2.getStructuringElement(cv2.MORPH_ELLIPSE,(3,3))
    #kernel2 = cv2.getStructuringElement(cv2.MORPH_ELLIPSE,(5,5))
    shadow_core = cv2.erode(shadow_mask, kernel)
    lite_core = cv2.erode(lite_mask, kernel)
    #lite_mask_new = cv2.dilate(lite_mask, kernel)
    #shadow_mask_new = cv2.dilate(shadow_mask, kernel)
    fig, ax = plt.subplots()
    ax.imshow(shadow_core)
    #fig, ax = plt.subplots()
    #ax.imshow(lite_core)
       
    #averaging pixel intensities in the shadow/lit areas
    red = image[:,:,2]
    green = image[:,:,1]
    blue = image[:,:,0]

    shadowavg_red = weightedAvg(red, shadow_core)
    shadowavg_green = weightedAvg(green, shadow_core)
    shadowavg_blue = weightedAvg(blue, shadow_core)

    litavg_red = weightedAvg(red, lite_core)
    litavg_green = weightedAvg(green, lite_core)
    litavg_blue = weightedAvg(blue, lite_core)

    ratio_red = litavg_red / shadowavg_red
    ratio_blue = litavg_blue / shadowavg_blue
    ratio_green = litavg_green / shadowavg_green

    # recover the color in the shadow region
    image_new = image[:] + 0
    buffer_zone = ((lite_core>0) + (shadow_core>0)) * 1
    buffer_zone = (buffer_zone == 0) * 1
    image_new[:,:,2] = image_new[:,:,2] * (lite_mask>0)  + (shadow_mask>0) * ratio_red * image_new[:,:,2]
    image_new[:,:,1] = image_new[:,:,1] * (lite_mask>0)  + (shadow_mask>0) * ratio_green * image_new[:,:,1]
    image_new[:,:,0] = image_new[:,:,0] * (lite_mask>0)  + (shadow_mask>0) * ratio_blue * image_new[:,:,0]
    #dilated_image = cv2.dilate(image,kernel2)
    #image_mixed = image + dilated_image
    #image_new[:,:,2] = image_new[:,:,2] * (buffer_zone==0) + dilated_image[:,:,2] * (buffer_zone>0)
    #image_new[:,:,1] = image_new[:,:,1] * (buffer_zone==0) + dilated_image[:,:,1] * (buffer_zone>0)
    #image_new[:,:,0] = image_new[:,:,0] * (buffer_zone==0) + dilated_image[:,:,0] * (buffer_zone>0)
    return image_new

imagefile = "BpeRS.png"
img = roughShadowRemoval(imagefile, shadow_gray_threshold=100)
fig, ax = plt.subplots()
ax.imshow(img)

