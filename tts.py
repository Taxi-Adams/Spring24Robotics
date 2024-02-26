import pyttsx3

class Speech:
    def __init__(self) -> None:
        self.engine = pyttsx3.init()
    
    def tts(self, toSay: str) -> None:
        self.engine.say(toSay)
        self.engine.runAndWait()
