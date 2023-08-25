import pyrealsense2 as rs
import numpy as np
import time
from matplotlib.animation import FuncAnimation
from itertools import count
import matplotlib.pyplot as plt

def gyro_data_to_euler(gyro_data, dt):
    global roll, pitch, yaw

    gx, gy, gz = gyro_data
    roll += gx * dt
    pitch += gy * dt
    yaw += gz * dt

    return roll, pitch, yaw

# Initialize variables
roll, pitch, yaw = 0.0, 0.0, 0.0

# Configure the pipeline
pipeline = rs.pipeline()
config = rs.config()
config.enable_stream(rs.stream.gyro)
# Start streaming
profile = pipeline.start(config)
start_time = time.time()

x=[]
y=[]
y2=[]
index = count()
def hahah(i):
    
    plt.plot(x,y)
    plt.plot(x,y2)
    plt.cla()



try:
    prev_time = time.time()
    
    while True:
        # Wait for a coherent pair of frames: depth and color
        frames = pipeline.wait_for_frames()
        ani = FuncAnimation(plt.gcf(),hahah)
        plt.show()   
        
        # Get gyro frame
        gyro_frame = frames.first_or_default(rs.stream.gyro)

        if gyro_frame:
            # Get gyroscope data
            gyro_data = gyro_frame.as_motion_frame().get_motion_data()

            # Calculate time delta
            current_time = time.time()
            elapsed_time = current_time - start_time
            # print(elapsed_time)
            dt = current_time - prev_time
            prev_time = current_time


            # Calculate roll, pitch, and yaw
            roll, pitch, yaw = gyro_data_to_euler([gyro_data.x, gyro_data.y, gyro_data.z], dt)
            # plt.plot(gyro_data.x,gyro_data.y,gyro_data.z)
            # plt.title('Sample Graph')
            # plt.show()
            c_r = -8.63/60 +0.28/60
            c_p = 1.73/60 -0.64/60
            c_y = -1.74/60 + 0.07/60
            print("Roll: {:.2f}, Pitch: {:.2f}, Yaw: {:.2f}".format(np.degrees(roll) - (c_r*elapsed_time),np.degrees(pitch) - (c_p*elapsed_time),np.degrees(yaw) - (c_y*elapsed_time)))
            # print("Roll",gyro_data.x)
            y.append(roll)
            y2.append(pitch)
            x.append(elapsed_time)
         
finally:
    # Stop streaming
    pipeline.stop()
    
    