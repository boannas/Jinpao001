# Import the required modules
import cv2
import numpy as np

# Define a function to detect moving points in a video
def detect_moving_points (video):
  # Create a background subtractor object
  bg_subtractor = cv2.createBackgroundSubtractorMOG2 ()

  # Loop over the frames of the video
  while True:
    # Read the next frame
    ret, frame = video.read ()

    # If the frame is None, break the loop
    if frame is None:
      break

    # Convert the frame to grayscale
    gray = cv2.cvtColor (frame, cv2.COLOR_BGR2GRAY)

    # Apply the background subtractor to get the foreground mask
    fg_mask = bg_subtractor.apply (gray)

    # Find the contours of the foreground mask
    contours, _ = cv2.findContours (fg_mask, cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_SIMPLE)

    # Loop over the contours
    for contour in contours:
      # Get the bounding rectangle of the contour
      x, y, w, h = cv2.boundingRect (contour)

      # Draw a red rectangle around the contour on the original frame
      cv2.rectangle (frame, (x, y), (x + w, y + h), (0, 0, 255), 2)

    # Show the original frame with the detected moving points
    cv2.imshow ('Frame', frame)

    # Wait for a key press or 30 ms
    key = cv2.waitKey (30)

    # If the key is 'q', break the loop
    if key == ord ('q'):
      break

  # Release the video object and destroy all windows
  video.release ()
  cv2.destroyAllWindows ()

# Create a video object from a file or a camera
video = cv2.VideoCapture (0)
# video = cv2.VideoCapture (0)

# Call the function to detect moving points in the video
detect_moving_points (video)
