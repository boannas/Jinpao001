import cv2
import mediapipe as mp
import numpy as np

mp_drawing = mp.solutions.drawing_utils
mp_pose = mp.solutions.pose
cap = cv2.VideoCapture(0)

# Set up screen config
cap.set(cv2.CAP_PROP_FRAME_WIDTH, 960)
cap.set(cv2.CAP_PROP_FRAME_HEIGHT, 720)

# Curl counter variables
counter = 0 
R_counter = 0
stage = None
tick_count = cv2.getTickCount()
frame_count = 0
st,st2,st3 = None,None,None
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
            mp_lm = mp_pose.PoseLandmark
            # Get coordinates
            #Left Arm Angle
            L_shoulder = [landmarks[mp_lm.LEFT_SHOULDER.value].x,landmarks[mp_lm.LEFT_SHOULDER.value].y]
            L_elbow = [landmarks[mp_lm.LEFT_ELBOW.value].x,landmarks[mp_lm.LEFT_ELBOW.value].y]
            L_wrist = [landmarks[mp_lm.LEFT_WRIST.value].x,landmarks[mp_lm.LEFT_WRIST.value].y]
            L_hip = [landmarks[mp_lm.LEFT_HIP.value].x,landmarks[mp_lm.LEFT_HIP.value].y]
            
            #Right Arm angle
            R_shoulder = [landmarks[mp_lm.RIGHT_SHOULDER.value].x,landmarks[mp_lm.RIGHT_SHOULDER.value].y]
            R_elbow = [landmarks[mp_lm.RIGHT_ELBOW.value].x,landmarks[mp_lm.RIGHT_ELBOW.value].y]
            R_wrist = [landmarks[mp_lm.RIGHT_WRIST.value].x,landmarks[mp_lm.RIGHT_WRIST.value].y]
            R_hip = [landmarks[mp_lm.RIGHT_HIP.value].x,landmarks[mp_lm.RIGHT_HIP.value].y]
            
            
            # Calculate angle
            angle_L_arm = calculate_angle(L_shoulder, L_elbow, L_wrist)
            angle_L_body = calculate_angle(L_elbow,L_shoulder,L_hip)
            angle_R_arm = calculate_angle(R_shoulder,R_elbow,R_wrist)
            angle_R_body = calculate_angle(R_elbow,R_shoulder,R_hip)
            
            
            # Visualize angle
            cv2.putText(image, str(angle_L_body), 
                           tuple(np.multiply(L_shoulder, [640, 480]).astype(int)), 
                           cv2.FONT_HERSHEY_SIMPLEX, 0.5, (255, 255, 255), 2, cv2.LINE_AA
                                )
            cv2.putText(image, str(angle_R_body), 
                           tuple(np.multiply(R_shoulder, [640, 480]).astype(int)), 
                           cv2.FONT_HERSHEY_SIMPLEX, 0.5, (255, 255, 255), 2, cv2.LINE_AA
                                )
  
            # Curl counter logic
            dif_shoulder = (L_shoulder[0] - R_shoulder[0]) *100
            if abs(dif_shoulder) < 3:
                st3 = "Neutral"
            elif dif_shoulder > 0 :
                st3 = "L Rising"
            else :
                st3 = "R Rising"
                
            if angle_L_body > 30:
                st = "Left Error"
            else :
                st = None
            if angle_R_body > 30:
                st2 = "Right Error"
            else :
                st2 = None
                
                
            if angle_L_arm > 160:
                stage = "down"
            if angle_L_arm < 30 and stage =='down':
                stage="up"
                counter +=1
                       
            if angle_R_arm > 160:
                R_stage = "R_down"
            if angle_R_arm < 30 and R_stage =='R_down':
                R_stage="R_up"
                R_counter +=1
            
                
            
            
            # Calculate bounding box around pose landmarks
                     
        except:
            pass


        mp_drawing.draw_landmarks(image, results.pose_landmarks, mp_pose.POSE_CONNECTIONS,
                                        mp_drawing.DrawingSpec(color=(255,0,0), thickness=2, circle_radius=2), 
                                        mp_drawing.DrawingSpec(color=(255,216,0), thickness=2, circle_radius=2)
                                        )

        # Setup status box
        cv2.rectangle(image, (0,0), (360,600), (245,117,16), -1)
        
        # Rep data
        cv2.putText(image, 'L_REPS', (15,20), 
                    cv2.FONT_HERSHEY_SIMPLEX, 0.5, (0,0,0), 1, cv2.LINE_AA)
        cv2.putText(image, str(counter), 
                    (10,70), 
                    cv2.FONT_HERSHEY_SIMPLEX, 2, (255,255,255), 2, cv2.LINE_AA)
        
        cv2.putText(image, 'R_REPS', (15,90), 
                    cv2.FONT_HERSHEY_SIMPLEX, 0.5, (0,0,0), 1, cv2.LINE_AA)
        cv2.putText(image, str(R_counter), 
                    (10,140), 
                    cv2.FONT_HERSHEY_SIMPLEX, 2, (255,255,255), 2, cv2.LINE_AA)
        
        
        cv2.putText(image, str(st), 
                    (10,210), 
                    cv2.FONT_HERSHEY_SIMPLEX, 2, (255,255,255), 2, cv2.LINE_AA)
        cv2.putText(image, str(st2), 
                    (10,280), 
                    cv2.FONT_HERSHEY_SIMPLEX, 2, (255,255,255), 2, cv2.LINE_AA)
        cv2.putText(image, str(st3), 
                    (10,350), 
                    cv2.FONT_HERSHEY_SIMPLEX, 2, (255,255,255), 2, cv2.LINE_AA)
        # image = cv2.rotate(image,cv2.ROTATE_90_COUNTERCLOCKWISE)
        cv2.imshow('Mediapipe Feed', image)
        if cv2.waitKey(10) & 0xFF == ord('q'):
            break

    cap.release()
    cv2.destroyAllWindows()