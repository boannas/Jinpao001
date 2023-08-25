import pyrealsense2 as rs
import numpy as np
import time
import matplotlib.pyplot as plt

def calibrate_accel(pipeline, samples=100):
    ax_sum, ay_sum, az_sum = 0.0, 0.0, 0.0

    for _ in range(samples):
        frames = pipeline.wait_for_frames()
        accel_frame = frames.first_or_default(rs.stream.accel)
        if accel_frame:
            accel_data = accel_frame.as_motion_frame().get_motion_data()
            ax_sum += accel_data.x
            ay_sum += accel_data.y
            az_sum += accel_data.z

    ax_avg = ax_sum / samples
    ay_avg = ay_sum / samples
    az_avg = az_sum / samples

    initial_roll = np.arctan2(ay_avg, np.sqrt(ax_avg**2 + az_avg**2))
    initial_pitch = np.arctan2(-ax_avg, np.sqrt(ay_avg**2 + az_avg**2))

    return ax_avg, ay_avg, az_avg, initial_roll, initial_pitch

def complementary_filter(gyro_data, accel_data, dt, accel_calibration):
    global roll, pitch, yaw
    alpha = 0.98

    gx, gy, gz = gyro_data.x, gyro_data.y, gyro_data.z
    ax, ay, az = accel_data.x, accel_data.y, accel_data.z

    # Remove accelerometer bias
    ax -= accel_calibration[0]
    ay -= accel_calibration[1]
    az -= accel_calibration[2]

    # Integrate gyroscope data
    roll += gx * dt
    pitch += gy * dt
    yaw += gz * dt

    # Calculate accelerometer angles
    accel_roll = np.arctan2(ay, np.sqrt(ax**2 + az**2)) - accel_calibration[3]
    accel_pitch = np.arctan2(-ax, np.sqrt(ay**2 + az**2)) - accel_calibration[4]

    # Apply complementary filter
    roll = alpha * roll + (1 - alpha) * accel_roll
    pitch = alpha * pitch + (1 - alpha) * accel_pitch

    return roll, pitch, yaw

# Initialize variables
roll, pitch, yaw = 0.0, 0.0, 0.0

# Configure the pipeline
pipeline = rs.pipeline()
config = rs.config()
config.enable_stream(rs.stream.gyro)
config.enable_stream(rs.stream.accel)

# Start streaming
profile = pipeline.start(config)

# Calibrate accelerometer
accel_calibration = calibrate_accel(pipeline)

try:
    prev_time = time.time()

    while True:
        # Get gyroscope and accelerometer data
        frames = pipeline.wait_for_frames()
        gyro_frame = frames.first_or_default(rs.stream.gyro)
        accel_frame = frames.first_or_default(rs.stream.accel)

        if gyro_frame and accel_frame:
            gyro_data = gyro_frame.as_motion_frame().get_motion_data()
            accel_data = accel_frame.as_motion_frame().get_motion_data()

            # Calculate time delta
            curr_time = time.time()
            dt = curr_time - prev_time
            prev_time = curr_time

            # Apply complementary filter
            roll, pitch, yaw = complementary_filter(gyro_data, accel_data, dt, accel_calibration)

            # Print roll, pitch, yaw in degrees
            print("Roll: {:.2f}°, Pitch: {:.2f}°, Yaw: {:.2f}°".format(np.rad2deg(roll), np.rad2deg(pitch), np.rad2deg(yaw)))

finally:
    pipeline.stop()
