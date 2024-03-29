import flaskBackend, client, personality
import _thread, threading

def main() -> None:
    ''' This will be the main controller for the whole robot. We will run each service (movement, talking, etc) on a different thread'''
    
    t1 = threading.Thread(target= flaskBackend.main, args= ())
    t2 = threading.Thread(target= client.main, args= ())
    t3 = threading.Thread(target= personality.main, args= ())

    t1.start()
    t2.start()
    t3.start()

main()
