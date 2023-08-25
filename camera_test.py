import cv2
import numpy as np
cap = cv2.VideoCapture(2)
cap2 = cv2.VideoCapture(1)
# cap2 = cv2.VideoCapture(2)

def auto_tint_correction(image):
    # Split the image into individual color channels
    b, g, r = cv2.split(image)

    # Compute the average color of the image
    avg_b = np.mean(b)
    avg_g = np.mean(g)
    avg_r = np.mean(r)

    # Compute the average intensity across the three channels
    avg_intensity = (avg_b + avg_g + avg_r) / 3.02

    # Estimate the target color for tint correction (gray world assumption)
    target_color = (avg_intensity, avg_intensity, avg_intensity)

    # Compute the scaling factors to adjust each channel towards the target color
    scale_b = target_color[0] / avg_b
    scale_g = target_color[1] / avg_g
    scale_r = target_color[2] / avg_r

    # Apply the scaling factors to correct the color balance
    b_corrected = np.clip(b * scale_b, 0, 255).astype(np.uint8)
    g_corrected = np.clip(g * scale_g, 0, 255).astype(np.uint8)
    r_corrected = np.clip(r * scale_r, 0, 255).astype(np.uint8)

    # Merge the color channels back to obtain the corrected image
    corrected_image = cv2.merge((b_corrected, g_corrected, r_corrected))

    return corrected_image

while cap.isOpened():
    ret, frame = cap.read()
    ret2,frame2 = cap2.read()
    ret3, frame3 = cap.read()


    # cv2.imshow('My Com cam', frame)
    cv2.imshow('came',frame)
    
    cv2.imshow('Webcam 2', frame2)
    cv2.imshow('auto tint ', auto_tint_correction(frame))
    cv2.imshow('Webcam 3', frame3)
    if cv2.waitKey(1) == ord('q'):
        break
    
cv2.waitKey(0)
cap.release()
cv2.destroyAllWindows()     