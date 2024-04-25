import threading
import tts
import time
import random

def readScript():
    voice = tts.Speech()
    script = voice.set_script('project10script.txt')
    while True:
        try:
            voice.tts_script()
        except:
            return

def checkAndMove(thread: threading.Thread):
    arr = [random.randint(1,100)] * 50 # Replace this with a queue holding the movements
    while True:
        if thread.is_alive():
            motion = arr.pop()
            print(motion)
            time.sleep(5)   # This can be removed as well when movements are added
        else:
            exit()

def main():
    t1 = threading.Thread(target=readScript)
    t1.start()

    t2 = threading.Thread(target=checkAndMove, args=(t1, ))
    t2.start()

main()
