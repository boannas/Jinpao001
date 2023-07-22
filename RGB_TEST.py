import cv2
import numpy as np
 
# Below function will read video imgs
cap = cv2.VideoCapture(1)
 
 

while True:
    read_ok, img = cap.read()
    img_bcp = img.copy()
  
    img = cv2.resize(img, (640, 480))
    # Make a copy to draw contour outline
    input_image_cpy = img.copy()
 
    rgb = cv2.cvtColor(img, cv2.COLOR_BGR2RGB)
 
    # define range of red color in rgb
    lower_red = np.array([200, 0, 0])
    upper_red = np.array([255, 190, 190])
     
    # define range of green color in rgb
    lower_green = np.array([0, 190, 0])
    upper_green = np.array([190, 255, 190])
     
    # define range of blue color in rgb
    lower_blue = np.array([0, 0, 190])
    upper_blue = np.array([190, 190, 255])
 
    # create a mask for red color
    mask_red = cv2.inRange(rgb, lower_red, upper_red)
    # create a mask for green colory
    mask_green = cv2.inRange(rgb, lower_green, upper_green)
    # create a mask for blue color
    mask_blue = cv2.inRange(rgb, lower_blue, upper_blue)
 
    # find contours in the red mask
    contours_red, _ = cv2.findContours(mask_red, cv2.RETR_TREE, cv2.CHAIN_APPROX_SIMPLE)
    # find contours in the green mask
    contours_green, _ = cv2.findContours(mask_green, cv2.RETR_TREE, cv2.CHAIN_APPROX_SIMPLE)
    # find contours in the blue mask
    contours_blue, _ = cv2.findContours(mask_blue, cv2.RETR_TREE, cv2.CHAIN_APPROX_SIMPLE)
 
    # loop through the red contours and draw a rectangle around them
    for cnt in contours_red:
        contour_area = cv2.contourArea(cnt)
        if contour_area > 1000:
            x, y, w, h = cv2.boundingRect(cnt)
            cv2.rectangle(img, (x, y), (x + w, y + h), (0, 0, 255), 2)
            cv2.putText(img, 'Red', (x, y-10), cv2.FONT_HERSHEY_SIMPLEX, 0.9, (0, 0, 255), 2)
 
    # loop through the green contours and draw a rectangle around them
    for cnt in contours_green:
        contour_area = cv2.contourArea(cnt)
        if contour_area > 1000:
            x, y, w, h = cv2.boundingRect(cnt)
            cv2.rectangle(img, (x, y), (x + w, y + h), (0, 255, 0), 2)
            cv2.putText(img, 'Green', (x, y-10), cv2.FONT_HERSHEY_SIMPLEX, 0.9, (0, 255, 0), 2)
 
    # loop through the blue contours and draw a rectangle around them
    for cnt in contours_blue:
        contour_area = cv2.contourArea(cnt)
        if contour_area > 1000:
            x, y, w, h = cv2.boundingRect(cnt)
            cv2.rectangle(img, (x, y), (x + w, y + h), (255, 0, 0), 2)
            cv2.putText(img, 'Blue', (x, y-10), cv2.FONT_HERSHEY_SIMPLEX, 0.9, (255, 0, 0), 2)
  
    cv2.imshow('RGB color Output', img)
     
    # Close video window by pressing 'x'
    if cv2.waitKey(1) & 0xFF == ord('x'):
        break