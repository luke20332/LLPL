# 4th version of the license plate recogniser
# instead using easy ocr instead of pytesseract.
# pytesseract rarely worked, this works majority of the time 

import cv2 as cv
from matplotlib import pyplot as plt
import numpy as np
import imutils
import easyocr
import requests
from bs4 import BeautifulSoup
from textblob import TextBlob
from vaderSentiment.vaderSentiment import SentimentIntensityAnalyzer

#text = "empty"
#opencv reads in images as bgr, whereas plt reads as rgb, so the colours on the image are difference
# working examples:
# image4.jpg is H892 FKL
# inbetweeners 4

img = cv.imread('sampleimages/mrbean1edit.jpg')

def preProcess(img):

  print("--- Performing Preprocessing ---")

  adjustimg = cv.cvtColor(img, cv.COLOR_BGR2RGB)
  plt.imshow(adjustimg)
  #plt.show()

  gray = cv.cvtColor(img, cv.COLOR_BGR2GRAY)



  # bilaterial filter to blur the image, reducing noise
  bfilter = cv.bilateralFilter(gray, 11, 17, 17) 

  #canny edge detection to find the edges of the plate
  edged = cv.Canny(bfilter, 30, 200) 

  plt.imshow(cv.cvtColor(edged, cv.COLOR_BGR2RGB))
  #plt.show()

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
  #plt.show()

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

  global text # define global variable from inside a function
  text = result[0][-2]

  print("The License plate is {}".format(text))
  font = cv.FONT_HERSHEY_SIMPLEX
  res = cv.putText(img, text = text, org = (approx[0][0][0], approx[1][0][1]+60), fontFace=font, fontScale=1, color=(0,255,0), thickness=2, lineType=cv.LINE_AA)
  res = cv.rectangle(img, tuple(approx[0][0]), tuple(approx[2][0]), (0,255,0),3)
  plt.imshow(cv.cvtColor(res, cv.COLOR_BGR2RGB))

  plt.show()
  #return text

preProcess(img)


# Now that we have deciphered the license plate from the image, we can now plug that into rate-driver to get the reviews, however, we cannot have spaces in the url
# .replace will not change the original variable, need to assign the value of the function to a different variable
#text = "H982 FKL"
plateText = text.replace(" ", "")


# get the site's HTML code into python to interact with it


def getReviews(plate):

  #allcomments is a list of dictionaries for all comments on the forum. in form author:comment
  global allComments
  allComments = []

  global commentText # array of strings of all comments
  commentText = []

  headers = {'User-Agent':'Mozilla/5.0 (Windows NT 6.1; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/62.0.3202.89 Safari/537.36'}
  # headers is a map sent to the web server to we dont get blacklisted, some websites will identify the python web agent and auto block

  URL = "https://rate-driver.co.uk/{}".format(plate) #
  print(URL)
  #URL = "https://rate-driver.co.uk/H982FKL"
  page = requests.get(URL, headers = headers) # HTTP GET request the web page from the web server, keeping the header in, This is stored in a python object.
  print ("Accessing {} ...".format(URL))
  #print(page.text)

  # Use Beautiful Soup to parse HTML code more efficiently.

  soup = BeautifulSoup(page.content, "html.parser") # content, not text, to parse raw bytes.


  # this line with find the h3 tag that is named Comments, and return the next div. This is the first comment of the page.
  #results = soup.find(lambda tag: tag.name == "h3" and "Comments" in tag.text).find_next("div")

  #this line finds all divs where the class name is 'comment' indicating we have a comment. returns an iterable containing all the HTML for all the comments on this page.
  comments = soup.findAll("div", class_ = "comment")
  
  for comment in comments:

    author = comment.find("span", itemprop = "author")
    comText = comment.find("span", itemprop="text")
    commentText.append(comText.text.strip())

    #print(author.text) #.text strips the attributes
    #print("{} \n ".format(comText.text.strip()) )
    #print()
    
    comDict = {
      "author" : author.text.strip(),
      "comment" : comText.text.strip(),
       #rating
    }

    allComments.append(comDict)


  #print(allComments)

  commentText = ' '.join(commentText)
   
  # bit shoddy, but the above method convers the previous commentText (an array of strings) into a single string of every comment on the website.


  #print(commentText) 



  #print(results0.prettify()) # easier viewing 

getReviews(plateText)



def returnxComments():
  number = int(input("How many comments would you like to see? "))
  # do a check here if number > len(allComments)
  for x in range (number):
    print("Author: {}".format(allComments[x]["author"]))
    print("Comment: {}".format(allComments[x]["comment"]))
    print()

returnxComments()

print(" --- Performing sentiment analysis of comments --- ")

def sentiment():
  # convert commentsText into either a vadersentiment object or a textblob object. Could do a combo of both later on.


  analyzer = SentimentIntensityAnalyzer()

  vs = analyzer.polarity_scores(commentText)

  #print(vs)

  # ideally, we would like to use the given compound measure as our unidimensional measure of sentiment.
  # for the mr bean example, we have a compounded sentiment of -0.9723 = very negative.

  #fix this

  print(vs["compound"])

  global sentScore
  if vs['compound'] <= 0 and vs['compound'] > 0.5:
    sentScore = "negative"
  if vs['compound'] <= 0.5 and vs['compound'] > 0:
    sentScore = "positive"
  if vs['compound'] <= -0.5:
    sentScore = "strongly negative"
  else:
    sentScore = "negative"

  print ("After examining the comments for {}, we concluded that the overall user sentiment is {}".format(text,sentScore))


sentiment()