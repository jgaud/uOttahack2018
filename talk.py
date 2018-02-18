import pyttsx

class Talker:
    def __init__(self):
        self.engine = pyttsx.init()
    def talk(self, phrase):
        self.engine.say(phrase)
        self.engine.runAndWait()