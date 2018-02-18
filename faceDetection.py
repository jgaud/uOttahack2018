import cognitive_face as CF
import requests
import os
import json
from io import BytesIO
from PIL import Image, ImageDraw

KEY="99501daf83fc4c5f8e86ba5d20cdcb58"
CF.Key.set(KEY)

face_api_url = "https://eastus2.api.cognitive.microsoft.com/face/v1.0/"
CF.BaseUrl.set(face_api_url)

serviceurldetect = 'https://eastus2.api.cognitive.microsoft.com/face/v1.0/detect'
serviceurlidentify = 'https://eastus2.api.cognitive.microsoft.com/face/v1.0/identify'
facelist = list()

def analyze_picture(img):

    serviceurlanalyze = 'https://eastus2.api.cognitive.microsoft.com/face/v1.0/analyze' 
 
    data = open(img, 'rb')

    reqs = requests.post(serviceurlanalyze, data, headers = {'Content-Type':'application/octet-stream', 'Ocp-Apim-Subscription-Key': KEY}, params = { 'visualFeatures' : 'Description, Tags, Faces, Categories, Color'})
    jinfoanalyze = reqs.json()
    try:
        categories = jinfoanalyze['categories']
        tags = jinfoanalyze['description']['tags']
        caption = jinfoanalyze['description']['captions'][0]['text']
        captionconfidence = jinfoanalyze['description']['captions'][0]['confidence']
        faces = jinfoanalyze['faces']
    
        print('Inferred Caption: ', caption, '      Confidence: ', captionconfidence)

        for cat in categories:
            print ("Category: ", cat['name'], "    Score:", cat['score'])

        for tag in tags:
            print (tag) 
    except:
        print ("Could not discern image")

def getRectangle(faceDictionary):
    rect = faceDictionary['faceRectangle']
    left = rect['left']
    top = rect['top']
    bottom = left + rect['height']
    right = top + rect['width']
    return ((left, top), (bottom, right))

requiredFaceAttributes = "gender,age,glasses"

def faceDetect(img_path):
    
    fname = "picture.jpg"
    data = open(fname, 'rb')

    image = Image.open(fname)

    analyze_picture(fname)

    facelist.clear()


    req = requests.post(serviceurldetect, data , headers = {'Content-Type':'application/octet-stream','Ocp-Apim-Subscription-Key': KEY}, params = {'returnFaceId': 'True', 'returnFaceLandmarks':'False', 'returnFaceAttributes':'emotion,gender,smile,age,facialhair,glasses'})
    jinfo = req.json()

    nbrfacesdetected = 0

    tempData = []
    
    for item in jinfo:
        nbrfacesdetected = nbrfacesdetected + 1
        faceid = item['faceId']
        facelist.append(faceid)

        smile = item['faceAttributes']['smile']
        tempData.append(smile)
        gender = item['faceAttributes']['gender']
        tempData.append(gender)
        age = item['faceAttributes']['age']
        tempData.append(age)
        glasses = item['faceAttributes']['glasses']
        tempData.append(glasses)
        emotion = item['faceAttributes']['emotion']
        v=list(emotion.values())
        k=list(emotion.keys())
        maxemotion = k[v.index(max(v))]
        emotionvalue = emotion[maxemotion]



        facialhair = item['faceAttributes']['facialHair']
        tempData.append(facialhair)

        print ("Gender: ", gender, "    Age: ", age, "    Smile: ", smile, "    Emotion: ", maxemotion, "    Glasses: ", glasses, "Facial hair", facialhair)

    print ("Number of faces detected: ", nbrfacesdetected)


    return tempData
