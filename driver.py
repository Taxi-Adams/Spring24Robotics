import flaskBackend, tts, mainController
import _thread, threading

def main() -> None:
    ''' This will be the main controller for the whole robot. We will run each service (movement, talking, etc) on a different thread'''

