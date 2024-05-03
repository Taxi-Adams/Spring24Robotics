#import objectDetection
import tts
import engine
import random
'''
1. Wait in A0 for human (UWB)
2. Wait for human input -> Check script
    - If not in script, ask GPT
3. Repeat 2 Until directions are asked for
4. Guide person to correct quadrant (Motion Multithread?) -> Try to get to middle
5. Say goodbye
5. Go to A0 -> Aim for middle
6. Announce "Charging needed"
7. Go to A1
8. Announce "Charging activated"
'''
def _objectDetectionTestrand():
    x = random.randint(1, 1000)
    print(x)
    return x

def main() -> None:
    # Sets up Text-to-speech
    speech = tts.Speech()
    greetings = ['Hello!', 'Hi there!', 'Whats up!', 'Howdy!']

    # Waits until someone approaches
    while True:
        dist = _objectDetectionTestrand() #objectDetection.get_distance()
        if dist <= 50:
            break
    
    # Once someone approaches, greet them
    speech.tts_input((random.choice(greetings), "How can I assist?"))

    # Goes to the script/ AI, and gets the correct quadrant
    bot = engine.Dialog_Engine()
    quadrant = bot.main()

    #TODO: ADD MOTION SCRIPT HERE

    #Once in the correct quadrant, announce charge and leave
    speech.tts_input("I need to charge")

    #TODO: MOTION to charging station (A1)

    # Annouces charging activated (End of script)
    speech.tts_input("Charging Activated")
    
if __name__ == "__main__":
    main()