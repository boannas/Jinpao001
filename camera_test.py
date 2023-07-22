import cv2

cap = cv2.VideoCapture(0)
cap2 = cv2.VideoCapture(1)

while cap.isOpened():
    ret, frame = cap.read()
    ret2,frame2 = cap2.read()


    cv2.imshow('My Com cam', frame)
    cv2.imshow('Webcam Logi', frame2)

    if cv2.waitKey(1) == ord('q'):
        break
    
cv2.waitKey(0)
cap.release()
cv2.destroyAllWindows()