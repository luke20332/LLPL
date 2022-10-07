# Luke's License Plate Lookup

An attempt at a rudimentary ALPR (Automatic License Plate Lookup) system using Python and OpenCV to detect and interpret a car's license plate from an image.
Once a License plate has been detected, it is cross referenced to rate-driver.co.uk, an forum for people to discuss (complain) about other drivers. Information about this car is given to the user, such as what the general public thinks of this driver.


How it works

This program first takes in an image of a car and begins preprocessing the image to convert it into a version suitable for computer vision packages.

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

~~Finally, using tesseract, we draw a box over each set of contours and find the license plate number.~~


Update - Version 0.4

After attempting to read license plates with tesseract, it appears as through tesseract does not have a very good success rate for the configuration that I had been using, possibly a problem on my behalf.

Therefore, I decided to use Easyocr, another python package that reads text using machine learning. This was aided with a tutorial, and license plates were able to be recognised a lot more often, given that the image is sufficiently clear.

![image](https://user-images.githubusercontent.com/78817201/189749208-c53aaae1-dc26-48e6-8c68-2f86d7e15062.png)


Looking up the plate:

Once a plate has been detected, the Requests library is used to find the plate's entry on rate-driver.co.uk
From there, BeautifulSoup returns the comments found on that entry, as well as the author's display name.

![examplecomments](https://user-images.githubusercontent.com/78817201/189750866-254e994c-eac4-4de4-9c51-0bfd381ca64f.JPG)


Sentiment Analysis.

Within the project, I am using the natural language processing library VaderSentiment to determine the general sentiment of the comments on the plate's entry. This coupled with comment rankings can provide the user with a good idea of the behaviour of this driver.
(This is albiet rather skewed due to the biased nature of the website's comments. It is very rare, if at all that a user will comment upon a user's driving praising their abilities).


![image](https://user-images.githubusercontent.com/78817201/194561136-39a224c5-4942-49da-ad3f-c11a7b226feb.png)

