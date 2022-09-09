import cv2 as cv
import numpy as np
import os
import time
import pytesseract

# where we installed pytesseract
pytesseract.pytesseract.tesseract_cmd = r'C:\Users\lukem\AppData\Local\Tesseract-OCR\tesseract.exe'


img = cv.imread("sampleimages/1.jpg")  # small doesnt work

#convert to greyscale
gray = cv.cvtColor(img, cv.COLOR_BGR2GRAY)

#blur image to remove noise

blur = cv.GaussianBlur(gray, (0,0), sigmaX = 33, sigmaY = 33)

#divide the np arrays on a per element basis

divide = cv.divide(gray, blur, scale = 255)

# Find the otsu threshold

thresh = cv.threshold(divide, 0, 255, cv.THRESH_BINARY+cv.THRESH_OTSU)[1]

#cv.imshow("thresh", thresh)

# Some morphological operations
# Morphological operations are actions that can be performed on a binary image. One is called 'opening', and consists of erosion then dilation. Useful in removing noise

# erosion
# Simply put, erosion removes small pixels. It erodes the boundaries of the foreground object.
# The kernel slides over the original image, as per convolution, and a pixel will be 1 if every pixel under the kernel (3,3) is also 1. This removes small pixels.
# Thickness of foreground object decreases, and removes small white noises, and detatches 2 connected objects.

# Dilation
# The opposite of erosion, the kernel will make an element 1 if at least one of the elements underneath it is 1. Increases the white region in the image.

kernel = cv.getStructuringElement(cv.MORPH_RECT, (3,3))

morph = cv.morphologyEx(thresh, cv.MORPH_CLOSE, kernel)

cv.imshow("morbed", morph)

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



contours, hierarchy = cv.findContours(morph, cv.RETR_EXTERNAL, cv.CHAIN_APPROX_NONE)



# create an empty text file to write to
file = open("Interpreted text", "w+")
file.write("")
file.close()

# then we loop through the contours list, passing it to pytesseract to identify any characters or blocks of text in the image. this is then written to the file.


def findText():
  for i in contours:
    x, y, w, h = cv.boundingRect(i)

    #overlay a rectangle
    rect = cv.rectangle(morph, (x,y),(x+w, y+h), (0,0,255), 2)

    cropped = morph[y:y+h, x:x+w]

    cv.imshow("cropped",cropped)

    file = open ("Interpreted text", "a")

    text = pytesseract.image_to_string(cropped)
    #text = "hello"

    print(text)

    file.write(text)
    #file.write("\n")
    print("searching...")
    file.close 


#findText()

print(len(contours))

print("finished with search")
cv.waitKey(0)