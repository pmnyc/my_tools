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

def getShadowMask(image):
    # Convert to HSV
    hsv1 = cv2.cvtColor(image, cv2.COLOR_BGR2HSV)
    # Renormalize Hue channel to 0-255
    hsv1[:,:,0] = ((255.0/179.0)*hsv1[:,:,0]).astype('uint8')
    # Convert to HSV again
    # Remember, channels are now RGB
    hsv2 = cv2.cvtColor(hsv1, cv2.COLOR_RGB2HSV)
    # Extract out the "red" channel
    #red = hsv2[:,:,0]
    # Perform Otsu thresholding and INVERT the image
    # Anything larger than threshold is white, anything greater is black
    _,out = cv2.threshold(hsv2[:,:,2], 0, 255, cv2.THRESH_BINARY_INV+cv2.THRESH_OTSU)
    #fig, ax = plt.subplots()
    #ax.imshow(out>0)
    return (out>0)

def getShadowMask2(image, shadow_gray_threshold=127, gray=None):
    if gray is None:
        gray = cv2.cvtColor(image, cv2.COLOR_RGB2GRAY)
    #gray = cv2.GaussianBlur(gray, (21, 21), 0)
    image_gray = gray
    return (image_gray < shadow_gray_threshold)

def reRenderShadow(image, focus_point_index, visited_pixel, 
                   pixel_radius=5, shadow_gray_threshold=100):
    gray = cv2.cvtColor(image,cv2.COLOR_RGB2GRAY)
    #gray = cv2.GaussianBlur(gray, (21, 21), 0)
    image_gray = gray
    shadow_ind = getShadowMask2(image, shadow_gray_threshold=shadow_gray_threshold, gray=gray)
    #shadow_ind = getShadowMask(image)
    shadow_mask = shadow_ind * image_gray
    lite_mask = ~shadow_ind * image_gray

    # for example, focus_point_index = [0,88] a point in a shadow
    nrows = shadow_mask.shape[0]
    ncols = shadow_mask.shape[1]
    row_up = max(0,focus_point_index[0] - pixel_radius)
    row_down = min(nrows-1,focus_point_index[0] + pixel_radius)
    col_left = max(0,focus_point_index[1] - pixel_radius)
    col_right = min(ncols-1,focus_point_index[1] + pixel_radius)
    
    row_indices = np.array(map(lambda x: [x] * (col_right-col_left+1), range(row_up, row_down+1)))
    row_indices = row_indices.flatten()
    col_indices = np.array(range(col_left, col_right+1) * (row_down-row_up+1))
    indices = (row_indices, col_indices)
    idx = map(lambda x: list(x), zip(row_indices, col_indices))
    visited_pixel += idx
    
    red_crop = image[:,:,2][indices[0],indices[1]] + 0.0
    green_crop = image[:,:,1][indices[0],indices[1]] + 0.0
    blue_crop = image[:,:,0][indices[0],indices[1]] + 0.0
    
    shadow_crop = shadow_mask[indices[0],indices[1]] +0.0
    lite_crop = lite_mask[indices[0],indices[1]] +0.0
    shadow_crop = (shadow_crop > 0) * 1.0
    lite_crop = (lite_crop > 0) * 1.0
    # zero mask is the just a cropped shadow mask focus around the small square around focus point
    zero_mask = shadow_mask * 0.0
    zero_mask[indices[0],indices[1]] = shadow_crop
    
    if sum(shadow_crop) == 0.0 or sum(lite_crop) == 0.0:
        res = image
    else:
        shadowavg_red = red_crop.dot(shadow_crop)/sum(shadow_crop)
        shadowavg_green = green_crop.dot(shadow_crop)/sum(shadow_crop)
        shadowavg_blue = blue_crop.dot(shadow_crop)/sum(shadow_crop)

        litavg_red = red_crop.dot(lite_crop)/sum(lite_crop)
        litavg_green = green_crop.dot(lite_crop)/sum(lite_crop)
        litavg_blue = blue_crop.dot(lite_crop)/sum(lite_crop)
    
        ratio_red = litavg_red / shadowavg_red
        ratio_blue = litavg_blue / shadowavg_blue
        ratio_green = litavg_green / shadowavg_green
        
        res = image[:] + 0
        res[:,:,2] = res[:,:,2] * (zero_mask<=0)  + (zero_mask>0) * (ratio_red * res[:,:,2])
        res[:,:,1] = res[:,:,1] * (zero_mask<=0)  + (zero_mask>0) * (ratio_green * res[:,:,1])
        res[:,:,0] = res[:,:,0] * (zero_mask<=0)  + (zero_mask>0) * (ratio_blue * res[:,:,0])
    
    return {"result": res.astype(dtype='uint8'), "visited":visited_pixel}


#image_raw = image[:]+0
image = image_raw[:] + 0
visited_pixel = []
fig, ax = plt.subplots()
ax.imshow(image)
shadow_ind = getShadowMask2(image, shadow_gray_threshold=110)
shadow_indices = np.where(shadow_ind == True)
for i in range(len(shadow_indices[0]))[:]:
    focus_point_index = [shadow_indices[0][i],shadow_indices[1][i]]
    if focus_point_index not in visited_pixel:
        r = reRenderShadow(image, focus_point_index, 
                               visited_pixel,
                               pixel_radius=15, shadow_gray_threshold=110)
        image = r["result"]
        visited_pixel = r["visited"]

fig, ax = plt.subplots()
ax.imshow(image)

    

imagefile = "BpeRS.png"
imagefile = "shadow-117ym8a.jpg"
image = cv2.imread(imagefile)
fig, ax = plt.subplots()
ax.imshow(image)