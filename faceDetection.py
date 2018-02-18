import cognitive_face as CF
import requests
from io import BytesIO
from PIL import Image, ImageDraw

def getRectangle(faceDictionary):
    rect = faceDictionary['faceRectangle']
    left = rect['left']
    top = rect['top']
    bottom = left + rect['height']
    right = top + rect['width']
    return ((left, top), (bottom, right))

KEY="99501daf83fc4c5f8e86ba5d20cdcb58"
CF.Key.set(KEY)

face_api_url = "https://eastus2.api.cognitive.microsoft.com/face/v1.0/"
CF.BaseUrl.set(face_api_url)

def faceDetect(img):
    faces = CF.face.detect(img)

    image = Image.open(img)

    draw = ImageDraw.Draw(image)
    for face in faces:
        draw.rectangle(getRectangle(face), outline='red')
    image.show()
    image.save(img)
