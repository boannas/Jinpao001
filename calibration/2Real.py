import pyrealsense2 as rs
import numpy as np
import cv2

# Configure depth and color streams
pipeline_1 = rs.pipeline()
pipeline_2 = rs.pipeline()
config_1 = rs.config()
config_2 = rs.config()

# Get device serial numbers
ctx = rs.context()
if len(ctx.devices) > 0:
    device_1 = ctx.devices[0]
    device_2 = ctx.devices[1]
    serial_1 = device_1.get_info(rs.camera_info.serial_number)
    serial_2 = device_2.get_info(rs.camera_info.serial_number)
    config_1.enable_device(serial_1)
    config_2.enable_device(serial_2)
else:
    print("No RealSense device is connected")
    exit(0)

config_1.enable_stream(rs.stream.depth, 640, 480, rs.format.z16, 30)
config_1.enable_stream(rs.stream.color, 640, 480, rs.format.bgr8, 30)
config_2.enable_stream(rs.stream.depth, 640, 480, rs.format.z16, 30)
config_2.enable_stream(rs.stream.color, 640, 480, rs.format.bgr8, 30)

# Start streaming from both cameras
pipeline_1.start(config_1)
pipeline_2.start(config_2)

try:
    while True:
        # Wait for a coherent pair of frames: depth and color
        frames_1 = pipeline_1.wait_for_frames()
        frames_2 = pipeline_2.wait_for_frames()
        depth_frame_1 = frames_1.get_depth_frame()
        color_frame_1 = frames_1.get_color_frame()
        depth_frame_2 = frames_2.get_depth_frame()
        color_frame_2 = frames_2.get_color_frame()
        
        # Convert images to numpy arrays
        depth_image_1 = np.asanyarray(depth_frame_1.get_data())
        color_image_1 = np.asanyarray(color_frame_1.get_data())
        depth_image_2 = np.asanyarray(depth_frame_2.get_data())
        color_image_2 = np.asanyarray(color_frame_2.get_data())

        # Apply colormap on depth image
        depth_colormap_1 = cv2.applyColorMap(cv2.convertScaleAbs(depth_image_1, alpha=0.03), cv2.COLORMAP_JET)
        depth_colormap_2 = cv2.applyColorMap(cv2.convertScaleAbs(depth_image_2, alpha=0.03), cv2.COLORMAP_JET)
        
        # Display images
        cv2.imshow('RealSense 1 - Depth', depth_colormap_1)
        cv2.imshow('RealSense 1 - Color', color_image_1)
        cv2.imshow('RealSense 2 - Depth', depth_colormap_2)
        cv2.imshow('RealSense 2 - Color', color_image_2)
        
        # Press 'q' to quit the program
        if cv2.waitKey(1) & 0xFF == ord('q'):
            break

finally:
    # Stop streaming
    pipeline_1.stop()
    pipeline_2.stop()
    cv2.destroyAllWindows()
