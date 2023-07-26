import cv2
import numpy as np
 
# Below function will read video imgs
cap = cv2.VideoCapture(1)
known_length = 25
focal_length = 80
distance = 0 

def find_Distance(pixel_lenght) :
    distance = (known_length * focal_length) / pixel_lenght
    return distance//1
def find_focal_length(pixel_length):
    focal_length = (pixel_length * distance)/known_length
    # print(focal_length)

def auto_tint_correction(image):
    # Split the image into individual color channels
    b, g, r = cv2.split(image)

    # Compute the average color of the image
    avg_b = np.mean(b)
    avg_g = np.mean(g)
    avg_r = np.mean(r)

    # Compute the average intensity across the three channels
    avg_intensity = (avg_b + avg_g + avg_r) / 3.02

    # Estimate the target color for tint correction (gray world assumption)
    target_color = (avg_intensity, avg_intensity, avg_intensity)

    # Compute the scaling factors to adjust each channel towards the target color
    scale_b = target_color[0] / avg_b
    scale_g = target_color[1] / avg_g
    scale_r = target_color[2] / avg_r

    # Apply the scaling factors to correct the color balance
    b_corrected = np.clip(b * scale_b, 0, 255).astype(np.uint8)
    g_corrected = np.clip(g * scale_g, 0, 255).astype(np.uint8)
    r_corrected = np.clip(r * scale_r, 0, 255).astype(np.uint8)

    # Merge the color channels back to obtain the corrected image
    corrected_image = cv2.merge((b_corrected, g_corrected, r_corrected))

    return corrected_image

while True:
    read_ok, img = cap.read()
    img_bcp = img.copy()
  
    # img = cv2.resize(img, (640, 480))                   # 640*480 px
    # Make a copy to draw contour outline
    input_image_cpy = img.copy()
    hsv = cv2.cvtColor(img, cv2.COLOR_BGR2HSV)
 
    # define range of red color in HSV
    lower_red = np.array([0, 50, 50])
    upper_red = np.array([10, 255, 255])
     
    # define range of green color in HSV
    lower_green = np.array([25, 52, 72]) 
    upper_green = np.array([102, 255, 255])
     
    # define range of blue color in HSV
    lower_blue = np.array([100, 50, 50])
    upper_blue = np.array([130, 255, 255])
 
    # create a mask for red color
    mask_red = cv2.inRange(hsv, lower_red, upper_red)
    # create a mask for green color
    mask_green = cv2.inRange(hsv, lower_green, upper_green)
    # create a mask for blue color
    mask_blue = cv2.inRange(hsv, lower_blue, upper_blue)
 
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
            # cv2.circle(img,((x+2)/2,(y+h)/2),3,(255,0,0))
            # cv2.putText(img, 'Red', (x, y-10), cv2.FONT_HERSHEY_SIMPLEX, 0.9, (0, 0, 255), 2)
            # cv2.putText(img, "x: " + str(x) + " " + "y: "+ str(y) , (x+60, y-10), cv2.FONT_HERSHEY_SIMPLEX, 0.5, (0, 0, 255), 2)
            # cv2.putText(img, "w: " + str(w) + " " + "h: "+ str(h) , (x+60, y+15), cv2.FONT_HERSHEY_SIMPLEX, 0.5, (0, 0, 255), 2)
            cv2.circle(img,(x+int(w)//2 ,y+int(h)//2 ),2,(0,0,0),3)  
            # cv2.putText(img, str(find_Distance(w)), (x, y+30), cv2.FONT_HERSHEY_SIMPLEX, 0.9, (255,255,255), 2)                           #find distance of known object size
            if (w/h < 1.5):
               cv2.putText(img, "Box", (x, y+10), cv2.FONT_HERSHEY_SIMPLEX, 0.5, (255,255,255), 2)
            else :
                cv2.putText(img, "Color Strip", (x, y+10), cv2.FONT_HERSHEY_SIMPLEX,0.5, (255,255,255), 2)   
            
 
    # loop through the green contours and draw a rectangle around them
    for cnt in contours_green:
        contour_area = cv2.contourArea(cnt)
        if contour_area > 1000:
            x, y, w, h = cv2.boundingRect(cnt)
            cv2.rectangle(img, (x, y), (x + w, y + h), (0, 255, 0), 2)
            # cv2.putText(img, 'Green', (x, y-10), cv2.FONT_HERSHEY_SIMPLEX, 0.9, (0, 255, 0), 2)
            # cv2.putText(img, "x: " + str(x) + " " + "y: "+ str(y) , (x+90, y-10), cv2.FONT_HERSHEY_SIMPLEX, 0.5, (0, 255, 0), 2)
            # cv2.putText(img, "w: " + str(w) + " " + "h: "+ str(h) , (x+90, y+15), cv2.FONT_HERSHEY_SIMPLEX, 0.5, (0, 255, 0), 2)
            cv2.circle(img,(x+int(w)//2 ,y+int(h)//2 ),2,(0,0,0),3)  
            # cv2.putText(img, str(find_Distance(w)), (x, y+30), cv2.FONT_HERSHEY_SIMPLEX, 0.9, (255,255,255), 2) 
            if (w/h < 1.5):
               cv2.putText(img, "Box", (x, y+10), cv2.FONT_HERSHEY_SIMPLEX, 0.5, (255,255,255), 2)
            else :
                cv2.putText(img, "Color Strip", (x, y+10), cv2.FONT_HERSHEY_SIMPLEX,0.5, (255,255,255), 2)  
 
    # loop through the blue contours and draw a rectangle around them
    for cnt in contours_blue:
        contour_area = cv2.contourArea(cnt)
        if contour_area > 1000:
            x, y, w, h = cv2.boundingRect(cnt)
            cv2.rectangle(img, (x, y), (x + w, y + h), (255, 0, 0), 2)
            # cv2.putText(img, 'Blue', (x, y-10), cv2.FONT_HERSHEY_SIMPLEX, 0.9, (255, 0, 0), 2)
            # cv2.putText(img, "x: " + str(x) + " " + "y: "+ str(y) , (x+60, y-10), cv2.FONT_HERSHEY_SIMPLEX, 0.5, (255, 0, 0), 2)
            # cv2.putText(img, "w: " + str(w) + " " + "h: "+ str(h) , (x+60, y+15), cv2.FONT_HERSHEY_SIMPLEX, 0.5, (255, 0, 0), 2)
            cv2.circle(img,(x+int(w)//2 ,y+int(h)//2 ),2,(0,0,0),3)  
            # cv2.putText(img, str(find_Distance(w)), (x, y+30), cv2.FONT_HERSHEY_SIMPLEX, 0.9, (255,255,255), 2) 
            if (w/h < 1.5):
               cv2.putText(img, "Box", (x, y+10), cv2.FONT_HERSHEY_SIMPLEX, 0.5, (255,255,255), 2)
            else :
                cv2.putText(img, "Color Strip", (x, y+10), cv2.FONT_HERSHEY_SIMPLEX,0.5, (255,255,255), 2)  
  
  
  
  
  
    # find_focal_length(360)
    cv2.imshow('correction',auto_tint_correction(img))
    # cv2.imshow('Greeny',img)
    cv2.imshow('HSV color Output', img)
     
    # Close video window by pressing 'x'
    if cv2.waitKey(1) & 0xFF == ord('x'):
        break