import cv2 as cv
#import numpy as np

import pytesseract

# where we installed pytesseract
pytesseract.pytesseract.tesseract_cmd = r'C:\Users\lukem\AppData\Local\Tesseract-OCR\tesseract.exe'

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


img = cv.imread("sampleimages/1.jpg")  # Load in our image

#img = imutils.resize(img, width=300)

img = rescaledImg(img)

#cv.imshow("resize", img)

#convert to greyscale
gray = cv.cvtColor(img, cv.COLOR_BGR2GRAY) 

# Remove excess noise from the image
# params are source image, diameter of pixel neighbourhood to apply smoothing to, 
# filter sigma in the color space - further colors are included in the mix, more equal across image
# filter sigma in the coordinate space,

gray = cv.bilateralFilter(gray, 11, 17, 17)

#cv.imshow("smoothed image", gray)

# Canny edge detection to find the edges in the image
# 2 params are the thresholds.

edge = cv.Canny(gray, 30, 200)

#cv.imshow("canny", edge)

# Find the contours on the sillohette image.
# first param is the contours matrix
# mode is RETR_LIST = give us all contours
# 3rd param is the approximation method for contours - dont give all of them



contours, new = cv.findContours(edge.copy(), cv.RETR_LIST, cv.CHAIN_APPROX_SIMPLE)

img1 = img.copy() # get the original image, dont want to affect the original

cv.drawContours(img1, contours, -1, (0,0,255), 2,)
#cv.imshow("contours", img1)

# Sort the identified contours
#   sort the list of all contours and find the 30 biggest, based on area.

contours = sorted(contours, key = cv.contourArea, reverse=True)[:30]
screenContour = None # the number plate contour, unassigned yet
img2 = img.copy() 
cv.drawContours(img2, contours, -1,(0,0,255), 3) # overlay the 30 largest on the image
#cv.imshow("Top 30 contours", img2)


# Finding the license plate region
# The general idea behind this part is for every contour, 


i = 7
for c in contours:
  perimeter = cv.arcLength(c, True) # find perimeter of the plate, 
  approx = cv.approxPolyDP(c, 0.018*perimeter, True) #approximate the curve of the polygon we have found, finds the number of edges on the contour
  if len(approx) == 4: # the contours with 4 sides
    screenContour = approx # 

  # crop out the rectangular part that we believe to be the license plate

  x, y, w, h = cv.boundingRect(c) # the coords needed to plot out the rectangle over the plate
  newImg = img[y:y+h, x:x+w]
  cv.imwrite('./'+str(i)+'.png', newImg) #storing the image of the cropped license plate
  i+=1
  break

#Draw the contours on the original image
# ensure that we have highlighted the license plate
# draws the found contours that define the license plate (screenContour) and overlay it on the original image

cv.drawContours(img, [screenContour], -1, (0,0,255), 2) 
cv.imshow("license plate", img)

# Extracting the text on the license plate

lpPath = './7.png'
croppedLp = cv.imread(lpPath)
cv.imshow("cropped license plate", croppedLp)
plateText = pytesseract.image_to_string(lpPath)
print("plate number is")
print(plateText)



cv.waitKey(0)