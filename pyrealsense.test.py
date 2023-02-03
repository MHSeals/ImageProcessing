from DepthSensor import DepthSensor
import numpy as np
import cv2 as cv

frames = []
with DepthSensor() as camera:

    # Convert images to numpy arrays
    frames = map(lambda frame:  (np.asanyarray(frame[0].get_data()), np.asanyarray(
        frame[1].get_data())), camera.get_frames())
    

# set the lower and upper bounds for the green hue
lower_green = np.array([50, 100, 50])
upper_green = np.array([70, 255, 255])

image = frames[0][0]
# create a mask for green color using inRange function
mask = cv.inRange(image, lower_green, upper_green)
# apply the mask to the image
result = cv.bitwise_and(image, image, mask=mask)

cv.imshow("mask", mask)
cv.imshow("original color", frames)