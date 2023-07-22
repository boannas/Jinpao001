import cv2
import numpy as np
 
# Below function will read video img2s
cap2 = cv2.VideoCapture(0)
 
 

while True:
    read_ok2, img2 = cap2.read()
    img2_bcp = img2.copy()
  
    img2 = cv2.resize(img2, (640, 480))
    # Make a copy to draw contour outline
    input_image_cpy2 = img2.copy()
 
    hsv2 = cv2.cvtColor(img2, cv2.COLOR_BGR2HSV)
 
    # define range of red color in HSV
    lower_red2 = np.array([0, 50, 50])
    upper_red2 = np.array([10, 255, 255])
     
    # define range of green color in HSV
    lower_green2 = np.array([25, 52, 72])
    upper_green2 = np.array([102, 255, 255])
     
    # define range of blue color in HSV
    lower_blue2 = np.array([100, 50, 50])
    upper_blue2 = np.array([130, 255, 255])
 
    # create a mask for red color
    mask_red2 = cv2.inRange(hsv2, lower_red2, upper_red2)
    # create a mask for green color
    mask_green2 = cv2.inRange(hsv2, lower_green2, upper_green2)
    # create a mask for blue color
    mask_blue2 = cv2.inRange(hsv2, lower_blue2, upper_blue2)
 
    # find contours in the red mask
    contours_red2, _ = cv2.findContours(mask_red2, cv2.RETR_TREE, cv2.CHAIN_APPROX_SIMPLE)
    # find contours in the green mask
    contours_green2, _ = cv2.findContours(mask_green2, cv2.RETR_TREE, cv2.CHAIN_APPROX_SIMPLE)
    # find contours in the blue mask
    contours_blue2, _ = cv2.findContours(mask_blue2, cv2.RETR_TREE, cv2.CHAIN_APPROX_SIMPLE)
 
    # loop through the red contours and draw a rectangle around them
    for cnt in contours_red2:
        contour_area = cv2.contourArea(cnt)
        if contour_area > 1000:
            x, y, w, h = cv2.boundingRect(cnt)
            cv2.rectangle(img2, (x, y), (x + w, y + h), (0, 0, 255), 2)
            cv2.putText(img2, 'Red', (x, y-10), cv2.FONT_HERSHEY_SIMPLEX, 0.9, (0, 0, 255), 2)
 
    # loop through the green contours and draw a rectangle around them
    for cnt in contours_green2:
        contour_area = cv2.contourArea(cnt)
        if contour_area > 1000:
            x, y, w, h = cv2.boundingRect(cnt)
            cv2.rectangle(img2, (x, y), (x + w, y + h), (0, 255, 0), 2)
            cv2.putText(img2, 'Green', (x, y-10), cv2.FONT_HERSHEY_SIMPLEX, 0.9, (0, 255, 0), 2)
 
    # loop through the blue contours and draw a rectangle around them
    for cnt in contours_blue2:
        contour_area = cv2.contourArea(cnt)
        if contour_area > 1000:
            x, y, w, h = cv2.boundingRect(cnt)
            cv2.rectangle(img2, (x, y), (x + w, y + h), (255, 0, 0), 2)
            cv2.putText(img2, 'Blue', (x, y-10), cv2.FONT_HERSHEY_SIMPLEX, 0.9, (255, 0, 0), 2)
  
    cv2.imshow('SHV color Output', img2)
     
    # Close video window by pressing 'x'
    if cv2.waitKey(1) & 0xFF == ord('x'):
        break