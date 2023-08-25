import real as hs

def find_Distance(pixel_lenght) :
    distance = (hs.known_length * hs.focal_length) / pixel_lenght
    return round(distance,2)

def find_focal_length(pixel_length,distance):
    focal_length = (pixel_length * distance)/hs.known_length
    print("Focal length : ",focal_length)
    
def find_pixel_length(dis):
    pixel_length = hs.known_length*hs.focal_length/dis
    print(pixel_length)
    return pixel_length
#
def find_pos(image,width,x,y) :
    pixel_size_mm = hs.known_length / width
    horizontal_mm,verticle_mm = find_res(image)[0] * pixel_size_mm ,find_res(image)[1] * pixel_size_mm
    x_ori = horizontal_mm / 2                               # Origin of frame
    y_ori = verticle_mm / 2 
    
    x_mm = (x * pixel_size_mm)                              # Distance to mm
    y_mm = (y * pixel_size_mm)
    
    x_fromOriginal = (x * pixel_size_mm) - x_ori            # Reorigin to center of frame
    y_fromOriginal = y_ori  - (y * pixel_size_mm)
    
    return [x_fromOriginal,y_fromOriginal,x_ori,y_ori,horizontal_mm,verticle_mm]

def find_res(image) :
    height, width, channels = image.shape
    return [width,height]

#