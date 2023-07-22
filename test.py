import numpy as np
import cv2

cap = cv2.VideoCapture(0)

while True:
    # Capture frame-by-frame
    ret, image = cap.read()

    hsv = cv2.cvtColor(image, cv2.COLOR_BGR2HSV)
    # define the list of boundaries
    boundaries = [
	([0,50,50], [10, 255, 255])
    ]

    # loop over the boundaries
    for (lower, upper) in boundaries:
        # create NumPy arrays from the boundaries
        lower = np.array(lower)
        upper = np.array(upper)

        # find the colors within the specified boundaries and apply
        # the mask
        mask = cv2.inRange(hsv, lower, upper)
        output = cv2.bitwise_and(image, image, mask=mask)

        imageOut = np.hstack([image, output])

    # Display the resulting frame
    cv2.imshow('RGB',imageOut)
    if cv2.waitKey(1) & 0xFF == ord('x'):
        break

# When everything done, release the capture
cap.release()
cv2.destroyAllWindows()