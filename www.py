import cv2
import numpy as np

def detect_green_objects(image):
    hsv = cv2.cvtColor(image, cv2.COLOR_BGR2HSV)
    pixel_size_min = 60
    pixel_size_max = 100
    lower_orange = np.array([11, 50, 50])
    upper_orange = np.array([25, 255, 255])
    lower_red = np.array([0, 50, 50])
    upper_red = np.array([10, 255, 255])
    lower_blue = np.array([100, 50, 50])
    upper_blue = np.array([130, 255, 255])
    
    mask_orange = cv2.inRange(hsv, lower_orange, upper_orange)
    mask_red = cv2.inRange(hsv, lower_red, upper_red)
    mask_blue = cv2.inRange(hsv, lower_blue, upper_blue)
    
    contours_orange, _ = cv2.findContours(mask_orange, cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_SIMPLE)
    contours_red, _ = cv2.findContours(mask_red, cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_SIMPLE)
    contours_blue, _ = cv2.findContours(mask_blue, cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_SIMPLE)

    for contour in contours_orange:
        x, y, w, h = cv2.boundingRect(contour)
        if pixel_size_max > w > pixel_size_min and pixel_size_max > h > pixel_size_min: 
            cv2.rectangle(image, (x, y), (x+w, y+h), (0, 140, 255), 2)
    for contour in contours_red:
        x, y, w, h = cv2.boundingRect(contour)
        if pixel_size_max > w > pixel_size_min and pixel_size_max > h > pixel_size_min: 
            cv2.rectangle(image, (x, y), (x+w, y+h), (0, 0, 255), 2)
    for contour in contours_blue:
        x, y, w, h = cv2.boundingRect(contour)
        if pixel_size_max > w > pixel_size_min and pixel_size_max > h > pixel_size_min:  
            cv2.rectangle(image, (x, y), (x+w, y+h), (255, 0, 0), 2)
    return image

def show_webcam(mirror=False):
    cam = cv2.VideoCapture(0)
    
    while True:
        ret_val, img = cam.read()
        if mirror:
            img = cv2.flip(img, 1)
        
        green_img = detect_green_objects(img)
        
        cv2.imshow('My Webcam', green_img)
        if cv2.waitKey(1) == 27:
            break
    
    cam.release()
    cv2.destroyAllWindows()

show_webcam(mirror=False)