# import the necessary packages
import numpy as np
import cv2
import matplotlib.pyplot as plt

# load the image, convert it to grayscale, and blur it
image = cv2.imread("image_find_books.jpg")
gray = cv2.cvtColor(image, cv2.COLOR_BGR2GRAY)
gray = cv2.GaussianBlur(gray, (3, 3), 0)
#cv2.imshow("Gray", gray)


# detect edges in the image
edged = cv2.Canny(gray, 10, 250)
#cv2.imshow("Edged", edged)


# construct and apply a closing kernel to 'close' gaps between 'white'
# pixels
kernel = cv2.getStructuringElement(cv2.MORPH_RECT, (7, 7))
closed = cv2.morphologyEx(edged, cv2.MORPH_CLOSE, kernel)
#cv2.imshow("Closed", closed)
fig, ax = plt.subplots()
ax.imshow(closed)

# find contours (i.e. the 'outlines') in the image and initialize the
# total number of books found
_, cnts, _ = cv2.findContours(closed.copy(), cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_SIMPLE)
total = 0

# loop over the contours
for c in cnts:
	# approximate the contour
	peri = cv2.arcLength(c, True)
	approx = cv2.approxPolyDP(c, 0.02 * peri, True)

	# if the approximated contour has four points, then assume that the
	# contour is a book -- a book is a rectangle and thus has four vertices
	if len(approx) == 4:
		cv2.drawContours(image, [approx], -1, (0, 255, 0), 4)
		total += 1

# display the output
print "I found {0} books in that image".format(total)
fig, ax = plt.subplots()
ax.imshow(image)
