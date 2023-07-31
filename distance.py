import math
def calculate_focal_length(sensor_width_mm, image_width_pixels, pixel_width_um, fov_degrees):
    fov_radians = math.radians(fov_degrees)
    focal_length_mm = (sensor_width_mm * image_width_pixels) / (2 * pixel_width_um * math.tan(fov_radians / 2))
    return focal_length_mm

# Given specifications
sensor_width_mm = 3.6
image_width_pixels = 1920
pixel_width_um = 1
fov_degrees = 75.7

focal_length_mm = calculate_focal_length(sensor_width_mm, image_width_pixels, pixel_width_um, fov_degrees)
print("Focal Length of the webcam:", focal_length_mm, "mm")