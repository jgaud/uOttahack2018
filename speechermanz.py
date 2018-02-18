import speech_recognition as sr
import cv2
import requests
import os
import smtplib
from email.mime.image import MIMEImage
from email.mime.multipart import MIMEMultipart
from email.mime.text import MIMEText
from talk import Talker

capture1 = cv2.VideoCapture(0) 

def capture_and_send(capture):
    s,image = capture.read()
    cv2.imwrite('capture.jpg', image)
    with open('capture.jpg', 'rb') as file:
        img_data = file.read()
    # Create a "related" message container that will hold the HTML 
    # message and the image. These are "related" (not "alternative")
    # because they are different, unique parts of the HTML message,
    # not alternative (html vs. plain text) views of the same content.
    msg = MIMEMultipart()
    msg['Subject'] = 'Front door capture.'
    msg['From'] = 'mailingtinging@gmail.com'
    msg['To'] = 'karimhurani@gmail.com'

    # Create the body with HTML. Note that the image, since it is inline, is 
    # referenced with the URL cid:myimage... you should take care to make
    # "myimage" unique
    text = MIMEText('<p><img src="cid:myimage"/></p>', _subtype='html')
    msg.attach(text)

    # Now create the MIME container for the image
    img = MIMEImage(img_data, name=os.path.basename('capture.jpg'))
    img.add_header('Content-Id', '<myimage>')  # angle brackets are important
    img.add_header("Content-Disposition", "inline", filename="myimage") # David Hess recommended this edit
    msg.attach(img)

    s = smtplib.SMTP('smtp.gmail.com:587')
    s.ehlo()
    s.starttls()
    s.ehlo()
    s.login('mailingtinging@gmail.com', 'testingffs')
    s.sendmail(msg['From'], msg['To'], msg.as_string())
    s.quit()
    capture.release()

def capture_img(capture):
    s,image = capture.read()
    cv2.imwrite('capture2.jpg', image)
    return 'capture2.jpg'

def isBox(file):
    with open(file, 'rb') as f:
        img = f.read()

    API_KEY = '0a2d040e7a574c17898314c2a8896ddf'
    BASE_URL = 'http://eastus2.api.cognitive.microsoft.com/vision/v1.0/'
    ANALYZE_URL = BASE_URL + "analyze"
    headers  = {
    'Content-Type': 'application/octet-stream','Ocp-Apim-Subscription-Key': API_KEY }
    params   = {'visualFeatures': 'Description'}
    response = requests.post(ANALYZE_URL, headers=headers, params=params, data=img)
    analysis = response.json()
    tags = analysis['description']['tags']
    print(tags)
    if 'box' in tags or 'suitcase' in tags or 'luggage' in tags:
        return True
    return False


# Record Audio
r = sr.Recognizer()
talker = Talker()
with sr.Microphone() as source:
    while 1<69:
        try:
            audio = r.listen(source)
            word_input = r.recognize_google(audio)
            print(word_input)
            if 'capture' in word_input.lower():
                print('yeet')
                capture_and_send(capture1)
            elif 'package at my front door' in word_input.lower() or 'package on my front door' in word_input.lower():
                print('wee')
                if isBox(capture_img(capture1)):
                    talker.talk('Yes, there is a package')
                else:
                    talker.talk('No, there is no package')
        except sr.UnknownValueError:
            continue

