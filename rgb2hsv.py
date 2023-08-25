import cv2 
import numpy as np
redBGR = np.uint8([[[4,3,128 ]]])
greenBGR = np.uint8([[[4,130,4 ]]])
blueBGR = np.uint8([[[169,9,9 ]]])
hsv_green = cv2.cvtColor(greenBGR,cv2.COLOR_BGR2HSV)
print ("green : " + str(hsv_green))
hsv_red = cv2.cvtColor(redBGR,cv2.COLOR_BGR2HSV)
print ("red : " + str(hsv_red))
hsv_blue = cv2.cvtColor(blueBGR,cv2.COLOR_BGR2HSV)
print ("blue : " + str(hsv_blue))