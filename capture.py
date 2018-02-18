import cv2

from faceDetection import faceDetect
from PIL import ImageTk, Image

camera_port = 0
capture = cv2.VideoCapture(camera_port);
s,image = capture.read()
s = True
counter = 0

def constantCapture():
    while s:
        s,image = capture.read()
        if counter%200 == 0 :
            cv2.imwrite('frame%d.jpg'%counter,image)
            faceDetect('frame%d.jpg'%counter)
        counter = counter + 1

def takeCapture():
    s,image = capture.read()
    path = "picture.jpg"
    cv2.imwrite(path, image)
    return path
