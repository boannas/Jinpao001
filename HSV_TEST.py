import cv2
import numpy as np
import my_Function as ff

# Below function will read video imgs
cap = cv2.VideoCapture(0)
known_length = 110
focal_length = 480
# distance = 0 
# list = [0]
# l2 = []


while True:
    read_ok, img = cap.read()
    img_bcp = img.copy()
    # img = cv2.resize(img,(960,720))
    # cv2.imshow("ggg",img)
    calibrated_img = ff.calibrate(img)
    
    # Make a copy to draw contour outline
    hsv = (ff.calibrate(cv2.cvtColor((img), cv2.COLOR_BGR2HSV)))
    
    # define range of red color in HSV
    # lower_red = np.array([0, 95, 100])
    # upper_red = np.array([10, 255, 255])
     
    # # define range of green color in HSV
    lower_green = np.array([50, 78, 80]) 
    upper_green = np.array([75, 255, 255])
     
    # # define range of blue color in HSV
    # lower_blue = np.array([100, 85, 85])
    # upper_blue = np.array([115, 255, 255])
    
    lower_red = np.array([0, 120, 120])
    upper_red = np.array([10, 255, 255])
     
    # # define range of green color in HSV
    # lower_green = np.array([50, 90, 90]) 
    # upper_green = np.array([80, 255, 255])
     
    # # define range of blue color in HSV
    lower_blue = np.array([100, 70, 50])
    upper_blue = np.array([130, 255, 255])
    
    # lower_green = np.array([40, 120, 120])
    # upper_green = np.array([90, 200, 200])
    # lower_red = np.array([0, 40, 40])
    # upper_red = np.array([25, 255, 255])
    # lower_blue = np.array([110, 50, 50])
    # upper_blue = np.array([120, 255, 255])
 
    # create a mask for red color
    mask_red = cv2.medianBlur(cv2.inRange(hsv, lower_red, upper_red),5)
    # create a mask for green color
    mask_green = cv2.medianBlur(cv2.inRange(hsv, lower_green, upper_green),5)
    # create a mask for blue color
    mask_blue = cv2.medianBlur(cv2.inRange(hsv, lower_blue, upper_blue),5)
 
    # find contours in the red mask
    contours_red, _ = cv2.findContours(mask_red, cv2.RETR_TREE, cv2.CHAIN_APPROX_SIMPLE)
    # find contours in the green mask
    contours_green, _ = cv2.findContours(mask_green, cv2.RETR_TREE, cv2.CHAIN_APPROX_SIMPLE)
    # find contours in the blue mask
    contours_blue, _ = cv2.findContours(mask_blue, cv2.RETR_TREE, cv2.CHAIN_APPROX_SIMPLE)
    
    # loop through the red contours and draw a rectangle around them
    cv2.imshow("contour_gree",mask_green)
    cv2.imshow("contour_blue",mask_blue)
    cv2.imshow("contour_red",mask_red)
    cv2.circle(calibrated_img,(ff.find_res(calibrated_img)[0]//2,ff.find_res(calibrated_img)[1]//2),2,(255,255,255),10)         # Create a Origin circle
    
    for cnt in contours_red:
        contour_area = cv2.contourArea(cnt)
        if contour_area > 2000:
            x, y, w, h = cv2.boundingRect(cnt)
            cv2.rectangle(calibrated_img, (x, y), (x + w, y + h), (0, 0, 255), 2)
            cv2.circle(calibrated_img,(x+int(w)//2 ,y+int(h)//2 ),2,(0,0,0),3)  
            if (w/h < 1.2) & (h/w < 1.2):
                d = ff.find_Distance(w)
                list.append(d)
                pos = ff.find_pos(calibrated_img,w,x+int(w)//2 ,y+int(h)//2)
                cv2.putText(calibrated_img, "Box", (x, y+10), cv2.FONT_HERSHEY_SIMPLEX, 0.5, (255,255,255), 2)
                cv2.putText(calibrated_img, "d: " + str(d) + " mm", (x, y+30), cv2.FONT_HERSHEY_SIMPLEX, 0.5, (255,255,255), 1)  
                cv2.putText(calibrated_img, "x: " + str(round(pos[0],2)) + " mm ", (x, y+45), cv2.FONT_HERSHEY_SIMPLEX, 0.5, (255, 255, 255), 1)
                cv2.putText(calibrated_img, "y: " + str(round(pos[1],2)) + " mm ", (x, y+60), cv2.FONT_HERSHEY_SIMPLEX, 0.5, (255, 255, 255), 1)
                # cv2.putText(calibrated_img, "Frame_X: " + str(round(pos[4],2)), (ff.find_res(calibrated_img)[0]-200, ff.find_res(calibrated_img)[1]-20), cv2.FONT_HERSHEY_SIMPLEX,0.5, (0,0,0), 2)
                # cv2.putText(calibrated_img, "Frame_Y: " + str(round(pos[5],2)), (ff.find_res(calibrated_img)[0]-200, ff.find_res(calibrated_img)[1]-5), cv2.FONT_HERSHEY_SIMPLEX,0.5, (0,0,0), 2)
            else :
                cv2.putText(img, "Color Strip", (x, y+10), cv2.FONT_HERSHEY_SIMPLEX,0.5, (255,255,255), 2)   
            
 
    # loop through the green contours and draw a rectangle around them
    for cnt in contours_green:
        contour_area = cv2.contourArea(cnt)
        if contour_area > 1000:
            x, y, w, h = cv2.boundingRect(cnt)
            cv2.rectangle(calibrated_img, (x, y), (x + w, y + h), (0, 255, 0), 2)
            cv2.circle(calibrated_img,(x+int(w)//2 ,y+int(h)//2 ),2,(0,0,0),3)  
            
            if (w/h < 1.2) & (h/w < 1.2):
               if (w/h < 1.2) & (h/w < 1.2):
                d = ff.find_Distance(w)
                list.append(d)
                pos = ff.find_pos(calibrated_img,w,x+int(w)//2 ,y+int(h)//2)
                cv2.putText(calibrated_img, "Box", (x, y+10), cv2.FONT_HERSHEY_SIMPLEX, 0.5, (255,255,255), 2)
                cv2.putText(calibrated_img, "d: " + str(d) + " mm", (x, y+30), cv2.FONT_HERSHEY_SIMPLEX, 0.5, (255,255,255), 1)  
                cv2.putText(calibrated_img, "x: " + str(round(pos[0],2)) + " mm ", (x, y+45), cv2.FONT_HERSHEY_SIMPLEX, 0.5, (255, 255, 255), 1)
                cv2.putText(calibrated_img, "y: " + str(round(pos[1],2)) + " mm ", (x, y+60), cv2.FONT_HERSHEY_SIMPLEX, 0.5, (255, 255, 255), 1)
                cv2.putText(calibrated_img, "Frame_X: " + str(round(pos[4],2)), (ff.find_res(calibrated_img)[0]-200, ff.find_res(calibrated_img)[1]-20), cv2.FONT_HERSHEY_SIMPLEX,0.5, (0,0,0), 2)
                cv2.putText(calibrated_img, "Frame_Y: " + str(round(pos[5],2)), (ff.find_res(calibrated_img)[0]-200, ff.find_res(calibrated_img)[1]-5), cv2.FONT_HERSHEY_SIMPLEX,0.5, (0,0,0), 2)
            else :
                cv2.putText(calibrated_img, "Color Strip", (x, y+10), cv2.FONT_HERSHEY_SIMPLEX,0.5, (255,255,255), 2)  
 
    # loop through the blue contours and draw a rectangle around them
    for cnt in contours_blue:
        contour_area = cv2.contourArea(cnt)
        if contour_area > 1000:
            x, y, w, h = cv2.boundingRect(cnt)
            cv2.rectangle(calibrated_img, (x, y), (x + w, y + h), (255, 0, 0), 2)
            cv2.circle(calibrated_img,(x+int(w)//2 ,y+int(h)//2 ),2,(0,0,0),3)  
            
            if (w/h < 1.2) & (h/w < 1.2):
               if (w/h < 1.2) & (h/w < 1.2):
                d = ff.find_Distance(w)
                list.append(d)
                pos = ff.find_pos(calibrated_img,w,x+int(w)//2 ,y+int(h)//2)
                cv2.putText(calibrated_img, "Box", (x, y+10), cv2.FONT_HERSHEY_SIMPLEX, 0.5, (255,255,255), 2)
                cv2.putText(calibrated_img, "d: " + str(d) + " mm", (x, y+30), cv2.FONT_HERSHEY_SIMPLEX, 0.5, (255,255,255), 1)  
                cv2.putText(calibrated_img, "x: " + str(round(pos[0],2)) + " mm ", (x, y+45), cv2.FONT_HERSHEY_SIMPLEX, 0.5, (255, 255, 255), 1)
                cv2.putText(calibrated_img, "y: " + str(round(pos[1],2)) + " mm ", (x, y+60), cv2.FONT_HERSHEY_SIMPLEX, 0.5, (255, 255, 255), 1)
                # cv2.putText(calibrated_img, "Frame_X: " + str(round(pos[4],2)), (ff.find_res(calibrated_img)[0]-200, ff.find_res(calibrated_img)[1]-20), cv2.FONT_HERSHEY_SIMPLEX,0.5, (0,0,0), 2)
                # cv2.putText(calibrated_img, "Frame_Y: " + str(round(pos[5],2)), (ff.find_res(calibrated_img)[0]-200, ff.find_res(calibrated_img)[1]-5), cv2.FONT_HERSHEY_SIMPLEX,0.5, (0,0,0), 2)
            else :
                cv2.putText(calibrated_img, "Color Strip", (x, y+10), cv2.FONT_HERSHEY_SIMPLEX,0.5, (255,255,255), 2)  
    if len(list) > 10 :
        list = []
    else :
        if len(list) == len(l2) :
            avg = 0
        else :
            avg = sum(list)/len(list)
    l2 = list.copy()
    # print("Before calibrate res : ", find_res(img))
    # print("After calibrate res : ", find_res(calibrated_img))
    # cv2.putText(calibrated_img, "Frame Size : " + ff.find_pos(calibrated_img,w,h,x+int(w)//2 ,y+int(h)//2)[4], (ff.find_res(calibrated_img)[0]-200, ff.find_res(calibrated_img)[1]-20), cv2.FONT_HERSHEY_SIMPLEX,0.5, (255,255,255), 2)
    
  
    cv2.putText(img, "Average Distance " + str(round(avg,2)), (420,340 ), cv2.FONT_HERSHEY_SIMPLEX,0.5, (255,255,255), 2)  
    cv2.imshow('Original photo',img)
    # calib = cv2.resize(calibrated_img,(ff.find_res(calibrated_img)[0]*10,ff.find_res(calibrated_img)[1]*10))
    # print("Reso : ",ff.find_res(calibrated_img))
    cv2.imshow('HSV color Output', calibrated_img)
    
    # cv2.imshow('Resize Output', calib)
    
     
    # Close video window by pressing 'x'
    if cv2.waitKey(1) & 0xFF == ord('x'):
        break