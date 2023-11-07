import cv2
import mediapipe as mp
import numpy as np
import time
mp_drawing = mp.solutions.drawing_utils
mp_pose = mp.solutions.pose
video_path = r"C:\Users\napat\Downloads\Bad.mp4"
cap = cv2.VideoCapture(0)
# Curl counter variables
counter = 0 
R_counter = 0
stage = None
tick_count = cv2.getTickCount()
frame_count = 0
# We need to set resolutions. 
# so, convert them from float to integer. 
# frame_width = int(cap.get(3)) 
# frame_height = int(cap.get(4)) 
   
# size = (frame_width, frame_height) 
   
# Below VideoWriter object will create 
# a frame of above defined The output  
# is stored in 'filename.avi' file. 
# result = cv2.VideoWriter('Bad_case.avi',  
#                          cv2.VideoWriter_fourcc(*'MJPG'),10, size) 

def calculate_angle(a,b,c):
    a = np.array(a) # First
    b = np.array(b) # Mid
    c = np.array(c) # End
    
    radians = np.arctan2(c[1]-b[1], c[0]-b[0]) - np.arctan2(a[1]-b[1], a[0]-b[0])
    angle = np.abs(radians*180.0/np.pi)
    
    if angle >180.0:
        angle = 360-angle
        
    return angle 

## Setup mediapipe instance
with mp_pose.Pose(min_detection_confidence=0.5, min_tracking_confidence=0.5) as pose:
    while cap.isOpened():
        ret, frame = cap.read()
        frame_count += 1
        
        if frame_count >= 20:  # Update FPS every 30 frames
            tick_count_new = cv2.getTickCount()
            time_spent = (tick_count_new - tick_count) / cv2.getTickFrequency()
            fps = frame_count / time_spent
            print("FPS: {:.2f}".format(fps),end='\r')
            frame_count = 0
            tick_count = cv2.getTickCount()
        
        # Recolor image to RGB
        image = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)
        image.flags.writeable = False
      
        # Make detection
        results = pose.process(image)
    
        # Recolor back to BGR
        image.flags.writeable = True
        image = cv2.cvtColor(image, cv2.COLOR_RGB2BGR)
        
        # Extract landmarks
        try:
            landmarks = results.pose_landmarks.landmark
            
            # Get coordinates
            shoulder = [landmarks[mp_pose.PoseLandmark.LEFT_SHOULDER.value].x,landmarks[mp_pose.PoseLandmark.LEFT_SHOULDER.value].y]
            elbow = [landmarks[mp_pose.PoseLandmark.LEFT_ELBOW.value].x,landmarks[mp_pose.PoseLandmark.LEFT_ELBOW.value].y]
            wrist = [landmarks[mp_pose.PoseLandmark.LEFT_WRIST.value].x,landmarks[mp_pose.PoseLandmark.LEFT_WRIST.value].y]
            
            R_shoulder = [landmarks[mp_pose.PoseLandmark.RIGHT_SHOULDER.value].x,landmarks[mp_pose.PoseLandmark.RIGHT_SHOULDER.value].y]
            R_elbow = [landmarks[mp_pose.PoseLandmark.RIGHT_ELBOW.value].x,landmarks[mp_pose.PoseLandmark.RIGHT_ELBOW.value].y]
            R_wrist = [landmarks[mp_pose.PoseLandmark.RIGHT_WRIST.value].x,landmarks[mp_pose.PoseLandmark.RIGHT_WRIST.value].y]
            
            # Calculate angle
            angle = calculate_angle(shoulder, elbow, wrist)
            R_angle = calculate_angle(R_shoulder,R_elbow,R_wrist)
            
            # 

            # Visualize angle
            # cv2.putText(image, str(angle), 
            #                tuple(np.multiply(elbow, [640, 480]).astype(int)), 
            #                cv2.FONT_HERSHEY_SIMPLEX, 0.5, (255, 255, 255), 2, cv2.LINE_AA
            #                     )
            # cv2.putText(image, str(R_angle), 
            #                tuple(np.multiply(R_elbow, [640, 480]).astype(int)), 
            #                cv2.FONT_HERSHEY_SIMPLEX, 0.5, (255, 255, 255), 2, cv2.LINE_AA
            #                     )
  
            # Curl counter logic
            if angle > 160:
                stage = "down"
            if angle < 30 and stage =='down':
                stage="up"
                counter +=1
                       
            if R_angle > 160:
                R_stage = "R_down"
            if R_angle < 30 and R_stage =='R_down':
                R_stage="R_up"
                R_counter +=1
            # Calculate bounding box around pose landmarks
                     
        except:
            pass


        mp_drawing.draw_landmarks(image, results.pose_landmarks, mp_pose.POSE_CONNECTIONS,
                                        mp_drawing.DrawingSpec(color=(255,0,0), thickness=2, circle_radius=2), 
                                        mp_drawing.DrawingSpec(color=(255,216,0), thickness=2, circle_radius=2)
                                        )
        # result.write(image) 
        # Setup status box
        # cv2.rectangle(image, (0,0), (90,150), (245,117,16), -1)
        
        # # Rep data
        # cv2.putText(image, 'L_REPS', (15,20), 
        #             cv2.FONT_HERSHEY_SIMPLEX, 0.5, (0,0,0), 1, cv2.LINE_AA)
        # cv2.putText(image, str(counter), 
        #             (10,70), 
        #             cv2.FONT_HERSHEY_SIMPLEX, 2, (255,255,255), 2, cv2.LINE_AA)
        
        # cv2.putText(image, 'R_REPS', (15,90), 
        #             cv2.FONT_HERSHEY_SIMPLEX, 0.5, (0,0,0), 1, cv2.LINE_AA)
        # cv2.putText(image, str(R_counter), 
        #             (10,140), 
        #             cv2.FONT_HERSHEY_SIMPLEX, 2, (255,255,255), 2, cv2.LINE_AA)
        cv2.imshow('Mediapipe Feed', image)

        if cv2.waitKey(10) & 0xFF == ord('q'):
            break

    cap.release()
    cv2.destroyAllWindows()