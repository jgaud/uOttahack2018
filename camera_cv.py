import cv2
import requests
import json
import time
import os
import smtplib
from email.mime.image import MIMEImage
from email.mime.multipart import MIMEMultipart
from email.mime.text import MIMEText
from texter import Texter

def isBox(frame):
    cv2.imwrite('tmp.jpg', frame)
    with open('tmp.jpg', 'rb') as file:
        img = file.read()

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

def send_email():
    with open('tmp.jpg', 'rb') as file:
        img_data = file.read()
    # Create a "related" message container that will hold the HTML 
    # message and the image. These are "related" (not "alternative")
    # because they are different, unique parts of the HTML message,
    # not alternative (html vs. plain text) views of the same content.
    msg = MIMEMultipart()
    msg['Subject'] = 'Package arrived.'
    msg['From'] = 'mailingtinging@gmail.com'
    msg['To'] = 'karimhurani@gmail.com'

    # Create the body with HTML. Note that the image, since it is inline, is 
    # referenced with the URL cid:myimage... you should take care to make
    # "myimage" unique
    text = MIMEText('<p><img src="cid:myimage"/></p>', _subtype='html')
    msg.attach(text)

    # Now create the MIME container for the image
    img = MIMEImage(img_data, name=os.path.basename('tmp.jpg'))
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

if __name__ == '__main__':
    texter = Texter()
    video_capture = cv2.VideoCapture(0)

    # p = Process(target=speecher.listen, group=None)
    # p.start()
    c = 0
    while True:
        # Capture frame-by-frame
        ret, frame = video_capture.read()
        frame = cv2.flip(frame, 1)
        if ret is True:
            gray = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)
        else:
            print('wee')
            continue

        if c % 250 == 0:    
            x = isBox(frame)
            print(x)
            if (x):
                send_email()
                texter.text('Your package is here.')
                print("Email sent.")
        # Display the resulting frame
        cv2.imshow('Video', frame)
        if cv2.waitKey(1) & 0xFF == ord('q'):
            break
        c+=1

    # When everything is done, release the capture
    video_capture.release()
    cv2.destroyAllWindows()
