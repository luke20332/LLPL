# 4th version of the license plate recogniser
# instead using easy ocr instead of pytesseract.
# pytesseract rarely worked, this works majority of the time 

import cv2 as cv
from matplotlib import pyplot as plt
import numpy as np
import imutils
import easyocr
import requests

#opencv reads in images as bgr, whereas plt reads as rgb, so the colours on the image are difference

img = cv.imread('sampleimages/image4.jpg')

def preProcess(img):
  adjustimg = cv.cvtColor(img, cv.COLOR_BGR2RGB)
  plt.imshow(adjustimg)
  plt.show()

  gray = cv.cvtColor(img, cv.COLOR_BGR2GRAY)



  # bilaterial filter to blur the image, reducing noise
  bfilter = cv.bilateralFilter(gray, 11, 17, 17) 

  #canny edge detection to find the edges of the plate
  edged = cv.Canny(bfilter, 30, 200) 

  plt.imshow(cv.cvtColor(edged, cv.COLOR_BGR2RGB))
  plt.show()

  # find contours and apply mask
  # we use findContours, passing in a copy of the edge image, and return a list of all contours in the imge, with retr_tree. - retrieval method
  # chain approx to give approximations for the contours, not the whole image.
  # the variable contours is a list of the contours, keypoints is the contours and their hierarchy.

  # then we extract the 10 largest contours based on area

  keypoints = cv.findContours(edged.copy(), cv.RETR_TREE, cv.CHAIN_APPROX_SIMPLE)
  contours = imutils.grab_contours(keypoints)
  contours = sorted(contours, key = cv.contourArea, reverse = True)[:10]

  # then using approxPolyDP, we find a contour with 4 sides, using douglass peucker algo.
  # first curve to use is the contour in the for loop
  # 2nd param is the approximation accuracy - distance from one curve to another so that distance is less than or equal to the specified precision
  location = None
  for contour in contours:
    approx = cv.approxPolyDP(contour, 10, True)
    if len(approx) == 4:
      location = approx #
      break

  #print(location)
  # the corners of the license plate, a list of 2 coordinates that outline the license plate.

  # masking the image, rest of image is black, while the area with the LP is colour.
  #new_image is an image where the area of the LP is one color, the rest is another
  # to do so, make a np zero mask, which is transparent. THis is bitwise anded with the mask
  mask = np.zeros(gray.shape, np.uint8)
  new_image = cv.drawContours(mask, [location], 0, (255,0,0), -1)

  new_image = cv.bitwise_and(img, img, mask=mask)

  plt.imshow(cv.cvtColor(new_image, cv.COLOR_BGR2RGB))
  plt.show()

  # then we create (x,y), a list of coordinates, where the mask is transparent (LP)
  # x1,y1 is the beginning of the rectangle
  #x2,y2 is the end of the rectangle
  (x,y) = np.where(mask == 255)
  (x1,y1) = (np.min(x), np.min(y))
  (x2,y2) = (np.max(x), np.max(y))
  cropped_image = gray[x1:x2+1, y1:y2+1]

  plt.imshow(cv.cvtColor(cropped_image, cv.COLOR_BGR2RGB))
  plt.show()

  # reader var is an object which performs easyocr operations on the image
  reader = easyocr.Reader(['en'])
  result = reader.readtext(cropped_image)
  #print (result)

  # the results of reader.readtext is a list, with the 4 coordinates of the text box, the text that was found, and the confidence level the system has in its result.


  text = result[0][-2]
  print("The License plate is {}".format(text))
  font = cv.FONT_HERSHEY_SIMPLEX
  res = cv.putText(img, text = text, org = (approx[0][0][0], approx[1][0][1]+60), fontFace=font, fontScale=1, color=(0,255,0), thickness=2, lineType=cv.LINE_AA)
  res = cv.rectangle(img, tuple(approx[0][0]), tuple(approx[2][0]), (0,255,0),3)
  plt.imshow(cv.cvtColor(res, cv.COLOR_BGR2RGB))

  plt.show()

#preProcess()


# Now that we have deciphered the license plate from the image, we can now plug that into rate-driver to get the reviews, however, we cannot have spaces in the url
# .replace will not change the original variable, need to assign the value of the function to a different variable
text = "H982 FKL"


text123 = text.replace(" ", "")
print(text123)

# get the site's HTML code into python to interact with it




def getReviews(plate):
  URL = "https://rate-driver.co.uk/{}".format(plate)
  page = requests.get(URL)
  print (URL)
  print(page.text)


getReviews(text123)

