from twilio.rest import Client

class Texter:
    def __init__(self):
        self.client = Client("ACd1e7a00182441a2f66b754a9b24fdd94", "bf0ec4df7a34fdc6e1f002a136c6e988")
    def text(self, msg):
        self.client.messages.create(to="+16136181755", 
                           from_="+18193031761", 
                           body=msg)
        print("Text sent.")