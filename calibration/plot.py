import pyrealsense2 as rs
import matplotlib.pyplot as plt
import numpy as np
import quaternion
from ahrs.filters import Madgwick

# RealSense pipeline configuration
pipeline = rs.pipeline()
config = rs.config()
config.enable_stream(rs.stream.gyro, rs.format.motion_xyz32f, 200)
config.enable_stream(rs.stream.accel, rs.format.motion_xyz32f, 63)

# Start pipeline
pipeline.start(config)

# Initialize Madgwick filter
madgwick = Madgwick()

# Process data and update orientation
def process_data(gyro_data, accel_data, dt):
    q = madgwick.updateIMU(gyro_data, accel_data, dt)
    euler_angles = quaternion.as_euler_angles(quaternion.quaternion(*q))
    return euler_angles

# Conversion functions
def accel_to_mps2(accel_data):
    G_TO_MPS2 = 9.80665
    return [x * G_TO_MPS2 for x in accel_data]

def gyro_to_radps(gyro_data):
    DPS_TO_RADPS = np.pi / 180.0
    return [x * DPS_TO_RADPS for x in gyro_data]

# Update the data processing loop
while True:
    try:
        # Read data from sensors
        frames = pipeline.wait_for_frames()
        gyro_frame = frames.first_or_default(rs.stream.gyro)
        accel_frame = frames.first_or_default(rs.stream.accel)
        gyro_data = gyro_frame.as_motion_frame().get_motion_data()
        accel_data = accel_frame.as_motion_frame().get_motion_data()

        # Convert data to appropriate units
        gyro_data_np = np.array([gyro_data.x, gyro_data.y, gyro_data.z])
        accel_data_np = np.array([accel_data.x, accel_data.y, accel_data.z])
        gyro_radps = gyro_to_radps(gyro_data_np)
        accel_mps2 = accel_to_mps2(accel_data_np)

        # Process data and update orientation
        roll, pitch, yaw = process_data(gyro_radps, accel_mps2, dt)

        # Rest of the plotting code...

    except KeyboardInterrupt:
        break

pipeline.stop()
