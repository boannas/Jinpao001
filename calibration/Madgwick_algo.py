import pyrealsense2 as rs
import matplotlib.pyplot as plt
import numpy as np
from ahrs.filters import Madgwick

# RealSense pipeline configuration
pipeline = rs.pipeline()
config = rs.config()
config.enable_stream(rs.stream.gyro, rs.format.motion_xyz32f, 200)
config.enable_stream(rs.stream.accel, rs.format.motion_xyz32f, 63)

# Start pipeline
pipeline.start(config)

# Initialize Madgwick filter
madgwick_filter = Madgwick()

# Your existing code for setting up plots...

# Collect and plot data in real-time
try:
    i = 0
    while True:
        # Wait for frames
        frames = pipeline.wait_for_frames()
        gyro_frame = frames.first_or_default(rs.stream.gyro)
        accel_frame = frames.first_or_default(rs.stream.accel)

        if gyro_frame and accel_frame:
            # Get gyroscope and accelerometer data
            gyro_data = gyro_frame.as_motion_frame().get_motion_data()
            accel_data = accel_frame.as_motion_frame().get_motion_data()

            # Update Madgwick filter with gyroscope and accelerometer data
            Madgwick.updateIMU(madgwick_filter, [gyro_data.x, gyro_data.y, gyro_data.z],[accel_data.x, accel_data.y, accel_data.z])

            # Get roll, pitch, and yaw angles from Madgwick filter quaternion output
            roll, pitch, yaw = madgwick_filter.quaternion.to_euler(degrees=True)

            # Your existing code for updating plots...

except KeyboardInterrupt:
    pass

# Stop pipeline
pipeline.stop()
