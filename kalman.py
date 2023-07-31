import numpy as np

def kalman_filter(initial_state, initial_covariance, measurement, process_noise, measurement_noise):
    # Prediction step
    predicted_state = initial_state
    predicted_covariance = initial_covariance + process_noise

    # Update step
    kalman_gain = predicted_covariance / (predicted_covariance + measurement_noise)
    updated_state = predicted_state + kalman_gain * (measurement - predicted_state)
    updated_covariance = (1 - kalman_gain) * predicted_covariance

    return updated_state, updated_covariance

# Example usage:
# Assume the object moves with a constant velocity and we have noisy position measurements.

# Initial state and covariance
initial_state = 0.0  # Initial position estimate
initial_covariance = 1.0  # Initial covariance estimate (uncertainty)

# Process noise (system noise)
process_noise = 0.01  # Adjust this value based on the system behavior

# Measurement noise (sensor noise)
measurement_noise = 0.1  # Adjust this value based on the sensor characteristics

# Simulated measurements
measurements = [1.1, 2.0, 3.0, 4.1, 5.0]

# Kalman filter loop
for measurement in measurements:
    initial_state, initial_covariance = kalman_filter(initial_state, initial_covariance, measurement, process_noise, measurement_noise)
    print("Updated State:", initial_state, "Updated Covariance:", initial_covariance)
