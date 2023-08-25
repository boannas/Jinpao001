import pyrealsense2 as rs
import numpy as np
import cv2

# Configure depth and color streams
pipeline = rs.pipeline()
config = rs.config()
config.enable_stream(rs.stream.color, 640, 480, rs.format.hsv8, 30)

# Start streaming
pipeline.start(config)

# Define the color range to detect (in this case, green)
lower_green = np.array([0, 100, 0])
upper_green = np.array([100, 255, 100])

try:
    while True:
        # Wait for a coherent color frame
        frames = pipeline.wait_for_frames()
        color_frame = frames.get_color_frame()

        if not color_frame:
            continue

        # Convert color image to numpy array
        color_image = np.asanyarray(color_frame.get_data())

        # Apply a color threshold to detect green objects
        mask = cv2.inRange(color_image, lower_green, upper_green)
        result = cv2.bitwise_and(color_image, color_image, mask=mask)

        # Show the resulting image
        cv2.imshow('RealSense', result)

        if cv2.waitKey(1) & 0xFF == ord('q'):
            break

finally:
    # Stop streaming
    pipeline.stop()
    cv2.destroyAllWindows()
