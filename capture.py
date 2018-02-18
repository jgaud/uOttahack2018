import cv2

from faceDetection import faceDetect

camera_port = 1
capture = cv2.VideoCapture(camera_port);
s,image = capture.read()
s = True
counter = 0

while s:
    s,image = capture.read()
    if counter%200 == 0 :
        cv2.imwrite('frame%d.jpg'%counter,image)
        faceDetect('frame%d.jpg'%counter)
    counter = counter + 1 
