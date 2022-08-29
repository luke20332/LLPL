# This program is to preprocess the data set
# testing out how to process the information

# so from the data set, one by one we extract an image, then do some preprocessing:
# 1 = Convert image to binary
# 2 = Find the bounding box, just the license plate
# 3 = convert image to an np array, with label stored also
# 4 = store images in a folder
#  

import cv2 as cv
import numpy as np
import os
import time
import pytesseract

# where we installed pytesseract
pytesseract.pytesseract.tesseract_cmd = r'C:\Users\lukem\AppData\Local\Tesseract-OCR\tesseract.exe'


DIR = r"C:\Users\lukem\Documents\projects\LLPL\sampleimages"

img = cv.imread("sampleimages/6.jpg")  # small doesnt work
img = cv.cvtColor(img, cv.COLOR_BGR2GRAY)
#cv.imshow("original", img)

#print(img.shape[0], img.shape[1])

# set a max image resolution that images can be, otherwise they are resized.

# redone
# resize image such that the greater out of height and width is 720, adjust other param accordingly so that ratio is preserved


def rescaledImg(img):
  # check which is bigger out of width and height
  if img.shape[0] >= img.shape[1]:
    scale = (720 / img.shape[0]) # ensure / not //, caused an error 
  else:
    scale = (720 / img.shape[1])
    
  width = int(img.shape[1] * scale) # find the scale to adjust w,h st the larger of the 2 is 720 pixels
  height = int(img.shape[0] * scale)
  dimensions = (width, height)

  return cv.resize(img, dimensions, interpolation = cv.INTER_AREA) # return the resized image

img = rescaledImg(img)



#cv.imshow("resized",img)

#adaptive_thresh = cv.adaptiveThreshold(img, 255,cv.ADAPTIVE_THRESH_GAUSSIAN_C, cv.THRESH_BINARY, 23,11)
threshold, img = cv.threshold(img, 100, 255, cv.THRESH_BINARY)


#decide between adaptive and simple thresholding. May just use simple right now, as it returns the image where the license plates are in bold; adaptive returns ones where the edges are outlined - may not be as helpful for the computer vision.
# also otsu's binarisation, but ignored for now.


cv.imshow("Thresholded", img)

# attempting to make a slideshow

dir_size = 6

#for i in range (0,dir_size):
  #path = os.path.join(DIR, i)
"""
for image in os.listdir(DIR):
    img_path = os.path.join(DIR, image)
    print (img_path)
    img_array = cv.imread(img_path)
"""
 
    #img = cv.cvtColor(img_array, cv.COLOR_BGR2GRAY)
    #img = rescaledImg(img)
    #threshold, img = cv.threshold(img, 100, 255, cv.THRESH_BINARY)
    #cv.imshow("image",img)
    #time.sleep(3)
   


# Getting the boundary box
# need to specify the structure shape and kernel size, which either increases or decreases the area of the bounding box
# ie small ones (10,10) will just detect the individual characters

kernel = cv.getStructuringElement(cv.MORPH_RECT, (20,20))

# then dilate the thresholded image

#img = cv.dilate(img, kernel, iterations=1)

#cv.imshow("dilated", img)
# Finding the contours
# contours are the edges or boundaries of an object in an image
# line or curve joining points
# findContours will return the contours and hierarchy
# Contours are an np array, coords of a boundary point in the object. Preprocessing was done so that contour detection is easier
#hierarchy can be ignored for now

contours, hierarchy = cv.findContours(img, cv.RETR_EXTERNAL, cv.CHAIN_APPROX_NONE)

print(contours)

img2 = img.copy()

# create an empty text file to write to
file = open("Interpreted text", "w+")
file.write("")
file.close()

# then we loop through the contours list, passing it to pytesseract to identify any characters or blocks of text in the image. this is then written to the file.

for i in contours:
  x, y, w, h = cv.boundingRect(i)

  #overlay a rectangle
  rect = cv.rectangle(img2, (x,y),(x+w, y+h), (0,0,255), 2)

  cropped = img2[y:y+h, x:x+w]

  cv.imshow("cropped",cropped)

  file = open ("Interpreted text", "a")

  text = pytesseract.image_to_string(cropped)
  #text = "hello"

  file.write(text)
  file.write("\n")

  file.close 

cv.waitKey(0)