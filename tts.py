import pyttsx3

class Speech():
    def __init__(self) -> None:
        self.engine = pyttsx3.init()
        self.script = []

    def set_script(self, filename: str) -> None:
        file = open(filename, "r")
        self.script = (file.read().split("\n"))
    
    def tts_input(self, toSay: str) -> None:
        self.engine.say(toSay)
        self.engine.runAndWait()

    def tts_script(self) -> None:
        self.engine.say(self.script[0])
        self.script.pop(0)
        self.engine.runAndWait()
        
        