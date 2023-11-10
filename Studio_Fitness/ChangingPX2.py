import cv2

# Capture video from a camera
cap = cv2.VideoCapture(0)

# Read the first frame
ret, frame = cap.read()

# Convert the frame to grayscale
gray = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)

# Define a background subtractor object
fgbg = cv2.createBackgroundSubtractorMOG2()

while True:
    # Read a new frame
    ret, frame = cap.read()

    # Apply the background subtractor to get the foreground mask
    fgmask = fgbg.apply(frame)

    # Apply thresholding to remove noise
    thresh = cv2.threshold(fgmask, 127, 255, cv2.THRESH_BINARY)[1]

    # Find contours in the thresholded image
    contours, hierarchy = cv2.findContours(thresh, cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_SIMPLE)

    # Draw bounding boxes around the moving objects
    for contour in contours:
        (x, y, w, h) = cv2.boundingRect(contour)
        cv2.rectangle(frame, (x, y), (x + w, y + h), (0, 255, 0), 2)

    # Display the resulting frame
    cv2.imshow('frame', frame)

    # Exit if the user presses 'q'
    if cv2.waitKey(1) & 0xFF == ord('q'):
        break

# Release the capture and destroy all windows
cap.release()
cv2.destroyAllWindows()
