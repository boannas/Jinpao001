import my_Function as ff
import pyrealsense2 as rs
import cv2
import numpy as np
# Configure depth and color streams
pipeline = rs.pipeline()
config = rs.config()
config.enable_stream(rs.stream.depth, 1280, 720, rs.format.z16, 30)                
config.enable_stream(rs.stream.color, 1280, 720, rs.format.bgr8, 30)
# Start streaming
pipeline.start(config)
tick_count = cv2.getTickCount()
frame_count = 0
try:
    while True:
        # Wait for a coherent pair of frames: depth and color
        frames = pipeline.wait_for_frames()
        # Align the RGB and Depth frames
        align = rs.align(rs.stream.depth)
        aligned_frames = align.process(frames)
        
        # Extract the aligned RGB and Depth frames from the aligned frames
        depth_frame = aligned_frames.get_depth_frame()
        color_frame = aligned_frames.get_color_frame()
        
        frame_count += 1
        
        if frame_count >= 20:  # Update FPS every 30 frames
            tick_count_new = cv2.getTickCount()
            time_spent = (tick_count_new - tick_count) / cv2.getTickFrequency()
            fps = frame_count / time_spent
            print("FPS: {:.2f}".format(fps),end='\r')
            frame_count = 0
            tick_count = cv2.getTickCount()
            
        if not depth_frame or not color_frame:
            continue
        
        # Convert images to numpy arrays
        depth_image = np.asanyarray(depth_frame.get_data())
        color_image = np.asanyarray(color_frame.get_data())
        hsv = cv2.cvtColor(color_image,cv2.COLOR_BGR2HSV)

        # Create HSV range as numpy array
        lower_green = np.array([65, 60, 40]) 
        upper_green = np.array([75, 255, 255])
        
        lower_red = np.array([0, 80, 55])
        upper_red = np.array([10, 255, 255])
        
        lower_blue = np.array([100, 70, 75])
        upper_blue = np.array([130, 255, 255])
    
        # create a mask for red color
        mask_red = cv2.medianBlur(cv2.inRange(hsv, lower_red, upper_red),5)
        # create a mask for green color
        mask_green = cv2.medianBlur(cv2.inRange(hsv, lower_green, upper_green),5)
        # create a mask for blue color
        mask_blue = cv2.medianBlur(cv2.inRange(hsv, lower_blue, upper_blue),5)
    
        # find contours in the red mask
        contours_red, _ = cv2.findContours(cv2.medianBlur((mask_red),5), cv2.RETR_TREE, cv2.CHAIN_APPROX_SIMPLE)
        # find contours in the green mask
        contours_green, _ = cv2.findContours(cv2.medianBlur((mask_green),7), cv2.RETR_TREE, cv2.CHAIN_APPROX_SIMPLE)
        # find contours in the blue mask
        contours_blue, _ = cv2.findContours(cv2.medianBlur((mask_blue),5), cv2.RETR_TREE, cv2.CHAIN_APPROX_SIMPLE)
    
        # Apply colormap on depth image (image must be converted to 8-bit per pixel first)
        depth_colormap = cv2.applyColorMap(cv2.convertScaleAbs(depth_image, alpha=0.03), cv2.COLORMAP_JET)

        # Resolution of each frame
        color_res = ff.find_res(color_image)
        depth_res = ff.find_res(depth_colormap)
        
        # Show detected color with RGB 
        cv2.imshow("contour_gree",mask_green)
        cv2.imshow("contour_blue",mask_blue)
        cv2.imshow("contour_red",cv2.medianBlur((mask_red),9))
        
        cv2.circle(color_image,(color_res[0]//2,color_res[1]//2),2,(0,0,255),5)         # Create a Origin circle
        for cnt in contours_red:
            contour_area = cv2.contourArea(cnt)
            if contour_area > 2000:
                x, y, w, h = cv2.boundingRect(cnt)
                cv2.rectangle(color_image, (x, y), (x + w, y + h), (0, 0, 255), 2)
                cv2.circle(color_image,(x+int(w)//2 ,y+int(h)//2 ),2,(255,255,255),3)  
                cv2.circle(depth_colormap,(x+int(w)//2 ,y+int(h)//2 ),2,(255,255,255),3)  
                if (w/h < 1.5) & (h/w < 1.5):
                    pos = ff.find_pos(color_image,w,x+int(w)//2 ,y+int(h)//2)
                    cv2.putText(color_image, "Box", (x, y+10), cv2.FONT_HERSHEY_SIMPLEX, 0.5, (255,255,255), 2)
                    # cv2.putText(color_image, "w: " + str(w) + " mm", (x, y+30), cv2.FONT_HERSHEY_SIMPLEX, 0.5, (255,255,255), 1)  
                    cv2.line(color_image,(x+int(w)//2 -80,y+int(h)//2),(x+int(w)//2+80 ,y+int(h)//2),(255,255,255),2)
                    cv2.line(color_image,(x+int(w)//2,y+int(h)//2-80),(x+int(w)//2 ,y+int(h)//2+80),(255,255,255),2)
                    depth_value = depth_image[y+int(h)//2,x+int(w)//2  ]
                    d = ff.find_Distance(w)
                    # cv2.putText(color_image, "d_RGB: " + str(d) + " mm", (x, y+15), cv2.FONT_HERSHEY_SIMPLEX, 0.5, (255,255,255), 1) 
                    cv2.putText(color_image, "d_Sensor: " + str(depth_value) + " mm", (x, y+30), cv2.FONT_HERSHEY_SIMPLEX, 0.5, (255,255,255), 1) 
                    cv2.putText(color_image, "x: " + str(round(pos[0],2)) + " mm ", (x, y+45), cv2.FONT_HERSHEY_SIMPLEX, 0.5, (255, 255, 255), 1)
                    cv2.putText(color_image, "y: " + str(round(pos[1],2)) + " mm ", (x, y+70), cv2.FONT_HERSHEY_SIMPLEX, 0.5, (255, 255, 255), 1)
                else :
                    # cv2.putText(color_image, "Color Strip", (x, y+10), cv2.FONT_HERSHEY_SIMPLEX,0.5, (255,255,255), 2) 
                    pass
            

        # loop through the green contours and draw a rectangle around them
        for cnt in contours_green:
            contour_area = cv2.contourArea(cnt)
            if contour_area > 2000:
                x, y, w, h = cv2.boundingRect(cnt)
                cv2.rectangle(color_image, (x, y), (x + w, y + h), (0, 255, 0), 2)
                cv2.circle(color_image,(x+int(w)//2 ,y+int(h)//2 ),2,(255,255,255),3)  
                cv2.circle(depth_colormap,(x+int(w)//2 ,y+int(h)//2 ),2,(255,255,255),3)  
                if (w/h < 1.5) & (h/w < 1.5):
                    pos = ff.find_pos(color_image,w,x+int(w)//2 ,y+int(h)//2)
                    cv2.putText(color_image, "Box", (x, y+10), cv2.FONT_HERSHEY_SIMPLEX, 0.5, (255,255,255), 2)
                    # cv2.putText(color_image, "d: " + str(w) + " mm", (x, y+30), cv2.FONT_HERSHEY_SIMPLEX, 0.5, (255,255,255), 1)  
                    depth_value = depth_image[y+int(h)//2,x+int(w)//2  ]
                    d = ff.find_Distance(w)
                    # cv2.putText(color_image, "d_RGB: " + str(d) + " mm", (x, y+15), cv2.FONT_HERSHEY_SIMPLEX, 0.5, (255,255,255), 1)
                    # cv2.putText(color_image, "w: " + str(w) + " mm", (x, y+75), cv2.FONT_HERSHEY_SIMPLEX, 0.5, (255,255,255), 1) 
                    cv2.line(color_image,(x+int(w)//2 -80,y+int(h)//2),(x+int(w)//2+80 ,y+int(h)//2),(255,255,255),2)
                    cv2.line(color_image,(x+int(w)//2,y+int(h)//2-80),(x+int(w)//2 ,y+int(h)//2+80),(255,255,255),2)
                    cv2.putText(color_image, "d_Sensor: " + str(depth_value) + " mm", (x, y+30), cv2.FONT_HERSHEY_SIMPLEX, 0.5, (255,255,255), 1) 
                    cv2.putText(color_image, "x: " + str(round(pos[0],2)) + " mm ", (x, y+45), cv2.FONT_HERSHEY_SIMPLEX, 0.5, (255, 255, 255), 1)
                    cv2.putText(color_image, "y: " + str(round(pos[1],2)) + " mm ", (x, y+70), cv2.FONT_HERSHEY_SIMPLEX, 0.5, (255, 255, 255), 1)
                else :
                    # cv2.putText(color_image, "Color Strip", (x, y+10), cv2.FONT_HERSHEY_SIMPLEX,0.5, (255,255,255), 2) 
                    pass
        # loop through the blue contours and draw a rectangle around them
        for cnt in contours_blue:
            contour_area = cv2.contourArea(cnt)
            if contour_area > 2000:
                x, y, w, h = cv2.boundingRect(cnt)
                cv2.rectangle(color_image, (x, y), (x + w, y + h), (255, 0, 0), 2)
                # cv2.polylines(color_image,[cnt],True,(255,255,255),3)
                cv2.circle(color_image,(x+int(w)//2 ,y+int(h)//2 ),2,(255,255,255),3)  
                cv2.circle(depth_colormap,(x+int(w)//2 ,y+int(h)//2 ),2,(255,255,255),3)  
                if (w/h < 1.5) & (h/w < 1.5):
                    pos = ff.find_pos(color_image,w,x+int(w)//2 ,y+int(h)//2)
                    cv2.putText(color_image, "Box", (x, y+10), cv2.FONT_HERSHEY_SIMPLEX, 0.5, (255,255,255), 2)
                    # cv2.putText(color_image, "d: " + str(w) + " mm", (x, y+30), cv2.FONT_HERSHEY_SIMPLEX, 0.5, (255,255,255), 1)  
                    depth_value = depth_image[y+int(h)//2,x+int(w)//2  ]
                    d = ff.find_Distance(w)
                    # cv2.putText(color_image, "W: " + str(w) + " mm", (x, y+15), cv2.FONT_HERSHEY_SIMPLEX, 0.5, (255,255,255), 1)
                    cv2.line(color_image,(x+int(w)//2 -80,y+int(h)//2),(x+int(w)//2+80 ,y+int(h)//2),(255,255,255),2)
                    cv2.line(color_image,(x+int(w)//2,y+int(h)//2-80),(x+int(w)//2 ,y+int(h)//2+80),(255,255,255),2)
                    cv2.putText(color_image, "d_Sensor: " + str(depth_value) + " mm", (x, y+30), cv2.FONT_HERSHEY_SIMPLEX, 0.5, (255,255,255), 1) 
                    cv2.putText(color_image, "x: " + str(round(pos[0],2)) + " mm ", (x, y+45), cv2.FONT_HERSHEY_SIMPLEX, 0.5, (255, 255, 255), 1)
                    cv2.putText(color_image, "y: " + str(round(pos[1],2)) + " mm ", (x, y+70), cv2.FONT_HERSHEY_SIMPLEX, 0.5, (255, 255, 255), 1)
                else :
                    # cv2.putText(color_image, "Color Strip", (x, y+10), cv2.FONT_HERSHEY_SIMPLEX,0.5, (255,255,255), 2) 
                    pass
            # Create center in depth screen to reference        
            cv2.circle(depth_colormap,(depth_res[0]//2, depth_res[1]//2),2,(255,255,255),3) 
    
        # Rendering Screen of color and depth sensor of realsense
        cv2.imshow('RealSense', color_image)
        cv2.imshow('Depth', depth_colormap)
        cv2.waitKey(1)

finally:
    # Stop streaming
    pipeline.stop()
    cv2.destroyAllWindows()