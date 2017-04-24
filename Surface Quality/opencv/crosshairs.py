import cv2

camera_port = 0
ramp_frames = 30

camera = cv2.VideoCapture(camera_port)

def get_image():
	retval, im = camera.read()
	return im

for i in range(ramp_frames):
 temp = get_image()
print("Taking image...")
# Take the actual image we want to keep
camera_capture = get_image()
file = "/home/pi/test_image.png"
# A nice feature of the imwrite method is that it will automatically choose the
# correct format based on the file extension you provide. Convenient!
cv2.imwrite(file, camera_capture)
 


nomeimg = "/home/pi/test_image.png"

img = cv2.imread(nomeimg)
gray = cv2.imread(img,0) #convert grayscale and binarize

element = cv2.getStructuringElement(cv2.MORPH_CROSS, (5,5))
graydilate = cv2.erode(gray, element) #imgbnbin

cv2.imshow('image',graydilate)
cv2.waitKey(0)


ret,thresh = cv2.threshold(graydilate,127,255,cv2.THRESH_BINARY_INV) #binarize

imgbnbin = thresh
cv2.imshow('image',graydilate)
cv2.waitKey()

imgbnbin, contours, heirarchy = cv2.findContours(imgbnbin,cv2.RETR_TREE,cv2.CHAIN_APPROX_SIMPLE)
print(len(contours))


# take only biggest contour basing on area
Areacontours = list()
calcarea = 0.0
unicocnt = 0.0
for i in range (0, len(contours)):
        area = cv2.contourArea(contours[i])
        #print("area")
        #print(area)
        if (area > 90):
                if (calcarea<area):
                        calcarea = area
                        unicocnt = contours[i]

#Roughness
perimeter = cv2.arcLength(unicocnt, True)
hull = cv2.convexHull(unicocnt)
hullperimeter = cv2.arcLength(hull,True)

print("perimeter")
print(perimeter)
print("hullperimeter")
print(hullperimeter)


roughness = perimeter/hullperimeter
print("roughness")
print(roughness)

# You'll want to release the camera, otherwise you won't be able to create a new
# capture object until your script exits
del(camera)
