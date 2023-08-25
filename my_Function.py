import cv2
import numpy as np
import HSV_TEST as hs
def find_Distance(pixel_lenght) :
    distance = (hs.known_length * hs.focal_length) / pixel_lenght
    return round(distance,2)

def find_focal_length(pixel_length):
    focal_length = (pixel_length * hs.distance)/hs.known_length
    # print(focal_length)
    
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

def calibrate(img):
    # cameraMatrix = np.array([ [1.00638688e+03, 0.00000000e+00, 3.47294852e+02],
    # [0.00000000e+00, 1.00773340e+03 ,2.53520066e+02],
    # [0.00000000e+00, 0.00000000e+00, 1.00000000e+00]])
    
    # cameraMatrix = np.array ([[1360.88232201858,	0,	966.302514506494],
    # [0,	1361.03552700234,	561.125523108043],
    # [0,	0,	1]])
    # dist = np.array([-0.269712980162175,	-0.00106457561408199,0,	0])
    
    cameraMatrix = np.array ( [[1286.07392497320,	0,	969.446993471624],
    [0,	1274.58108622654,	569.611138353188],
    [0,	0,	1]])

    dist = np.array([-0.272879410600478	,0.0297633751356664,0,0])

    h,  w = img.shape[:2]
    newCameraMatrix, roi = cv2.getOptimalNewCameraMatrix(cameraMatrix, dist, (w,h), 1, (w,h))

    mapx, mapy = cv2.initUndistortRectifyMap(cameraMatrix, dist, None, newCameraMatrix, (w,h), 5)
    dst = cv2.remap(img, mapx, mapy, cv2.INTER_LINEAR)

    # crop the image
    x, y, w, h = roi
    dst = dst[y:y+h, x:x+w]
    return dst

def find_pos(image,width,x,y) :
    pixel_size_mm = hs.known_length / width
    horizontal_mm,verticle_mm = find_res(image)[0] * pixel_size_mm ,find_res(image)[1] * pixel_size_mm
    x_ori = horizontal_mm / 2                      # Distance from Center frame
    y_ori = verticle_mm / 2 
    
    x_mm = (x * pixel_size_mm)                      # Distance from 
    y_mm = (y * pixel_size_mm)
    
    x_fromOriginal = (x * pixel_size_mm) - x_ori
    y_fromOriginal = y_ori  -(y * pixel_size_mm)
    
    # print("x : ",horizontal_res)
    # print("y : ",verticle_res)
    # print("x1 : ",x_mm)
    # print("y1 : ",y_mm)
    # print("x2 : ",x_fromOriginal)
    # print("y2 : ",y_fromOriginal)
    
    return [x_fromOriginal,y_fromOriginal,x_ori,y_ori,horizontal_mm,verticle_mm]

def find_res(image) :
    # fetching the dimensions
    wid = image.shape[1]
    hgt = image.shape[0]
    return [wid,hgt]