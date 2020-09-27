#Kamondy Tivadar - 2020
#Computer vision course - Szechenyi Istvan University of Gyor
#Coin recognition application

#import libaries
import cv2
import numpy as np

#loading in the image
img = cv2.imread("coins.jpg");

# blurring and convert image to grey scale
gray = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)
blurred = cv2.GaussianBlur(img, (17, 17), 0)

# showing the blurred and grey scaled image
cv2.imshow("grey scale", gray)
cv2.imshow("blurred", blurred)
cv2.waitKey(0)

# applying canny edge detection
outline = cv2.Canny(blurred, 30, 150)

# show canny edge det
cv2.imshow("Edges", outline)
cv2.waitKey(0)

# finding the contours
(cnts, _) = cv2.findContours(outline, cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_SIMPLE)

# drawing contours
cv2.drawContours(img, cnts, -1, (0, 255, 0), 2) #-1 will draw all of them
cv2.imshow("Result", img)
cv2.waitKey(0)

# Print how many coins are there
print("There are %i coins" % len(cnts))



"""
##Here just a quick OpenCV test
size = np.size(img)
skel = np.zeros(img.shape,np.uint8)

ret,img = cv2.threshold(img,127,255,0)
element = cv2.getStructuringElement(cv2.MORPH_CROSS,(3,3))
done = False

while( not done):
    eroded = cv2.erode(img,element)
    temp = cv2.dilate(eroded,element)
    temp = cv2.subtract(img,temp)
    skel = cv2.bitwise_or(skel,temp)
    img = eroded.copy()

    zeros = size - cv2.countNonZero(img)
    if zeros==size:
        done = True

cv2.imshow("skel",skel)
cv2.waitKey(0)
cv2.destroyAllWindows()
"""

