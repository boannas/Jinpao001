import pyrealsense2 as rs
import matplotlib.pyplot as plt
import numpy as np

# RealSense pipeline configuration
pipeline = rs.pipeline()
config = rs.config()
config.enable_stream(rs.stream.gyro, rs.format.motion_xyz32f, 200)
config.enable_stream(rs.stream.accel, rs.format.motion_xyz32f, 63)

# Start pipeline
pipeline.start(config)

# Set up plot
plt.ion()
fig, axs = plt.subplots(3, 1, figsize=(8, 12))

# Gyroscope plot
gyro_x, gyro_y, gyro_z = [], [], []
x_data = []
line_gyro_x, = axs[0].plot(x_data, gyro_x, label='Gyro X')
line_gyro_y, = axs[0].plot(x_data, gyro_y, label='Gyro Y')
line_gyro_z, = axs[0].plot(x_data, gyro_z, label='Gyro Z')
axs[0].legend()
axs[0].set_title('Gyroscope')

# Accelerometer plot
accel_x, accel_y, accel_z = [], [], []
line_accel_x, = axs[1].plot(x_data, accel_x, label='Accel X')
line_accel_y, = axs[1].plot(x_data, accel_y, label='Accel Y')
line_accel_z, = axs[1].plot(x_data, accel_z, label='Accel Z')
axs[1].legend()
axs[1].set_title('Accelerometer')

# Orientation plot
orientation_x, orientation_y, orientation_z = [], [], []
line_orientation_x, = axs[2].plot(x_data, orientation_x, label='Roll')
line_orientation_y, = axs[2].plot(x_data, orientation_y, label='Pitch')
line_orientation_z, = axs[2].plot(x_data, orientation_z, label='Yaw')
axs[2].legend()
axs[2].set_title('Orientation')

# Collect and plot data in real-time
try:
    i = 0
    while True:
        # Wait for frames
        frames = pipeline.wait_for_frames()
        gyro_frame = frames.first_or_default(rs.stream.gyro)
        accel_frame = frames.first_or_default(rs.stream.accel)

        if gyro_frame and accel_frame:
            # Get gyroscope data
            gyro_data = gyro_frame.as_motion_frame().get_motion_data()
            gyro_x.append(gyro_data.x)
            gyro_y.append(gyro_data.y)
            gyro_z.append(gyro_data.z)

            # Get accelerometer data
            accel_data = accel_frame.as_motion_frame().get_motion_data()
            accel_x.append(accel_data.x)
            accel_y.append(accel_data.y)
            accel_z.append(accel_data.z)

            # Calculate orientation (example: using pitch and roll)
            roll = np.arctan2(accel_data.y, np.sqrt(accel_data.x**2 + accel_data.z**2))
            pitch = np.arctan2(-accel_data.x, np.sqrt(accel_data.y**2 + accel_data.z**2))
            orientation_x.append(roll)
            orientation_y.append(pitch)
            # Note: Calculating yaw requires a magnetometer or other techniques

            x_data.append(i)
            i += 1

            # Update plot data
            for line, data in zip([line_gyro_x, line_gyro_y, line_gyro_z,
                                   line_accel_x, line_accel_y, line_accel_z,
                                   line_orientation_x, line_orientation_y],
                                  [gyro_x, gyro_y, gyro_z,
                                   accel_x, accel_y, accel_z,
                                   orientation_x, orientation_y]):
                line.set_xdata(x_data)
                line.set_ydata(data)

            # Update plot limits
            for ax in axs:
                ax.relim()
                ax.autoscale_view()

            # Redraw plot
            fig.canvas.draw()
            fig.canvas.flush_events()

except KeyboardInterrupt:
    print("Exiting...")

finally:
    # Stop pipeline
    pipeline.stop()
