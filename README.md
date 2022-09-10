# LLPL
Luke's License Plate Lookup

An attempt at a rudimentary ALPR (Automatic License Plate Lookup) system using Python and OpenCV to detect and interpret a car's license plate from an image.

As this project develops, I may experiment in including web-scraping to cross-reference found license plates and their entry on ratemydriver.com 


How it works

This program first takes in an image of a car and begins preprocessing the image to convert it into a version suitable for Tesseract.

The preprocessing includes:
  - Converting the image to greyscale
  - Rescaling the image such that the maximum height/width is 720 pixels. 
    -This is for the user, and is optional
  - Thresholding the image to a binary image. 
    - This is done to highlight just the text, reducing noise that may be picked up by the text interpreter.

The first version of this uses simple thresholding, but this is not very effective, in a later method I will attempt OTSU thresholding.

Then, we genereate a kernel / bounding box for the license plate.
Here, we specify a shape and size of the kernel, which influences the size of the bounding box. This is what is overlayed on the image to read the text.

Contours within the image are found. We pass in the image, and the openCV method 'findContours' will return a numpy array of all locations of a 'contour'.

Finally, using tesseract, we draw a box over each set of contours and find the license plate number.




Update - Version 0.4

After attempting to read license plates with tesseract, it appears as through tesseract does not have a very good success rate for the configuration that I had been using, possibly a problem on my behalf.

Therefore, I decided to use easyocr, another python package that reads text using machine learning. This was aided with a tutorial, and license plates were able to be recognised a lot more often.
As a result I will be going along with this package.

