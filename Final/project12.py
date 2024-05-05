import serial
import tts
import math
import time
import random
import engine
from tango import Tango
import RPi.GPIO as GPIO

GPIO.setmode(GPIO.BCM)

TRIG_PIN = 23
ECHO_PIN = 24

def get_serial() -> None:
    serial_port = '/dev/ttyUSB0'
    #serial_port = '/dev/ttyACM1'
    baud_rate = 115200

    ser = serial.Serial(serial_port, baud_rate)
    ser.readline()
    response = ser.readline()
    list_response = response.decode().split(',')
    print("Made it before list response loop")
    while list_response[0] != '$KT7':
        print("In loop before the ser.readline() line")
        response = ser.readline()
        #print("In loop after the ser.readline() line")
        list_response = response.decode().split(',')
        if(list_response[0] == '$KT7'):
            print("list_response length: ")
            print(len(list_response))
            if(len(list_response) != 4):
                continue
            elif(len(list_response) == 4):
                #print(list_response[0])
                print(list_response[1])
                print(list_response[2])
                print(list_response[3])
                print(list_response[4])
            if(list_response[1] == 'null' or list_response[2] == 'null' or list_response[3] == 'null' or list_response[4] == 'null'):
                continue
        #print("At the end of the loop")
        #print("")
    print("Should have now left the get serial loop!!!")
    return([float(list_response[1]), float(list_response[2]),
             float(list_response[3]), float(list_response[4])])

def _objectDetectionTestrand():
    x = random.randint(1, 1000)
    print(x)
    return x

def get_distance():
    GPIO.output(TRIG_PIN, False)
    time.sleep(0.1)

    GPIO.output(TRIG_PIN, True)
    time.sleep(0.00001)
    GPIO.output(TRIG_PIN, False)

    timeout = time.time()
    while GPIO.input(ECHO_PIN) == 0:
        if (time.time() - timeout) > 3:
            print("Timeout occurred while waiting for echo signal")
            return None
    pulse_start = time.time()

    timeout = time.time()
    while GPIO.input(ECHO_PIN) == 1:
        if (time.time() - timeout) > 3:
            print("Timeout occurred while receiving echo signal")
            return None
    pulse_end = time.time()

    pulse_duration = pulse_end - pulse_start

    distance = pulse_duration * 17150
    distance = round(distance, 2)

    return distance

def find_quadrant(coords: list) -> None:
    min_coord = min(coords)
    quadrant = coords.index(min_coord)
    tts.Speech().tts_input(str(quadrant)) # change to say project 12 stuff
    return quadrant


# returns an angle in degrees
def calc_angle(bottomLeft, bottomRight):
    # define constant base to be the sensor's reading of 2 to 1 distance (approx)
    base = 3.0
    print("calc angle bottomLeft: " + str(bottomLeft))
    print(", calc angle bottomRight: " + str(bottomRight))
    # phi is the angle from base to left wall
    phi = math.acos(((bottomLeft * bottomLeft + 9.0 - bottomRight * bottomRight) / (2 * base * bottomLeft))) * 180 / math.pi
    return phi

# returns a 2D vector
def calc_position(hypotenuse, phi):
    xDist = hypotenuse * math.cos(phi* math.pi / 180.0)
    yDist = hypotenuse * math.sin(phi * math.pi / 180.0)
    position = [xDist, yDist]
    return position
    
# returns an angle in degrees
def calc_turn_angle(firstPt, secondPt):
    facingX = firstPt[0] - secondPt[0]
    facingY = firstPt[1] - secondPt[1]
    normFactor = math.sqrt(facingX * facingX + facingY * facingY)
    if(normFactor == 0):
        print("The ****ing wheel isn't working again. Expect an error.")
    # normalized vector of which way the robot is facing
    dirFacing = [facingX / normFactor, facingY / normFactor]
    # using the unit circle to calculate the angle needed to turn to face exactly 'West'
    # the angle is the angle turned from west ccw, so turning cw that much should give exactly west
    angle = math.atan2(dirFacing[1], dirFacing[0]) * 180.0 / math.pi
    if(angle < 0):
        angle = 360.0 + angle
    return angle

def main():
    # initialize bot
    bot = Tango()
    coords = get_serial()
    #print("Reached point after getting serial")
    d1 = coords[0]
    d2 = coords[1]
    d3 = coords[2]
    d4 = coords[3]
    # find the current quadrant and report it vocally
    currentQuadrant = find_quadrant(coords)
    
    
    
    isNorth = False
    isSouth = False
    min_coord = min(coords)
    quadrant = coords.index(min_coord)
    if(quadrant == 1 or quadrant == 2):
        isSouth = True
        isNorth = False
    elif(quadrant == 0 or quadrant == 3):
        isSouth = False
        isNorth = True
    positionAngle = calc_angle(d3, d2)
    [x, y] = calc_position(d3, positionAngle)
    
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
    print("Made it past greeting the person")

    # Goes to the script/ AI, and gets the correct quadrant
    bot2 = engine.Dialog_Engine()
    targetQuadrant = bot2.main()
    print("Got a quadrant response/input!!!!!")
    
    # move backwards slowly
    time.sleep(2.0)
    bot.move_fb(5900)
    bot.move_fb(7000)
    time.sleep(1.3)
    bot.stop_wheels_fb()
    # get new distances and position
    coords2 = get_serial()
    d1Next = coords2[0]
    d2Next = coords2[1]
    d3Next = coords2[2]
    d4Next = coords2[3]
    phi = calc_angle(d3Next, d2Next)
    [x2, y2] = calc_position(d3Next, phi)
    firstPoint = [x, y]
    secondPoint = [x2, y2]
    # print("first point:" + str(x) + ", " + str(y))
    # print ("second point: " + str(x2) + ", " + str(y2))
    # calculate the current angle ccw from 90 degrees
    turnAngle = calc_turn_angle(firstPoint, secondPoint)
    print("I need to turn " + str(turnAngle) + " degrees")
    
    # project 12 code from here on
    # get the target quadrant from the user and set the targetQuadrant variable equal to it
    #targetQuadrant = 2
    if(currentQuadrant == 0):
        if(targetQuadrant == 0):
            # do nothing
            waiting = True
        elif(targetQuadrant == 1):
            # turn to face East
            turnAngle += 90
            fraction = turnAngle / 360.0
            bot.turn_lr(5900)
            bot.turn_lr(4500)
            time.sleep(fraction * 2.4)
            bot.stop_wheels_lr()
            bot.move_fb(4900)
            time.sleep(1.7) # replace with better measured time
            bot.stop_wheels_fb()
            temporaryCoords = get_serial()
            tempQuadrant = find_quadrant(temporaryCoords)
            currentQuadrant = 1
            if(tempQuadrant == 0):
                bot.move_fb(4900)
                time.sleep(0.45) # replace with better measured time
                bot.stop_wheels_fb()
        elif(targetQuadrant == 2):
            # turn to face East
            turnAngle += 90
            fraction = turnAngle / 360.0
            bot.turn_lr(5900)
            bot.turn_lr(4500)
            time.sleep(fraction * 2.4)
            bot.stop_wheels_lr()
            bot.move_fb(4900)
            time.sleep(1.7) # replace with better measured time
            bot.stop_wheels_fb()
            temporaryCoords = get_serial()
            tempQuadrant = find_quadrant(temporaryCoords)
            if(tempQuadrant == 0):
                bot.move_fb(4900)
                time.sleep(0.45) # replace with better measured time
                bot.stop_wheels_fb()
            # turn another 90 and move to the next quadrant
            turnAngle = 90.0
            fraction = turnAngle / 360.0
            bot.turn_lr(5900)
            bot.turn_lr(4500)
            time.sleep(fraction * 2.4)
            bot.stop_wheels_lr()
            bot.move_fb(4900)
            time.sleep(1.7) # replace with better measured time
            bot.stop_wheels_fb()
            temporaryCoords = get_serial()
            tempQuadrant = find_quadrant(temporaryCoords)
            currentQuadrant = 2
            if(tempQuadrant == 1):
                bot.move_fb(4900)
                time.sleep(0.45) # replace with better measured time
                bot.stop_wheels_fb()
        elif(targetQuadrant == 3):
            turnAngle += 180.0
            fraction = turnAngle / 360.0
            bot.turn_lr(5900)
            bot.turn_lr(4500)
            time.sleep(fraction * 2.4)
            bot.stop_wheels_lr()
            bot.move_fb(4900)
            time.sleep(1.7) # replace with better measured time
            bot.stop_wheels_fb()
            temporaryCoords = get_serial()
            tempQuadrant = find_quadrant(temporaryCoords)
            currentQuadrant = 3
            if(tempQuadrant == 0):
                bot.move_fb(4900)
                time.sleep(0.45) # replace with better measured time
                bot.stop_wheels_fb()
    elif(currentQuadrant == 1):
        if(targetQuadrant == 0):
            # turn to face East
            turnAngle += 270.0
            fraction = turnAngle / 360.0
            bot.turn_lr(5900)
            bot.turn_lr(4500)
            time.sleep(fraction * 2.4)
            bot.stop_wheels_lr()
            bot.move_fb(4900)
            time.sleep(1.7) # replace with better measured time
            bot.stop_wheels_fb()
            temporaryCoords = get_serial()
            tempQuadrant = find_quadrant(temporaryCoords)
            currentQuadrant = 0
            if(tempQuadrant == 1):
                bot.move_fb(4900)
                time.sleep(0.45) # replace with better measured time
                bot.stop_wheels_fb()
        elif(targetQuadrant == 1):
            waiting = True
        elif(targetQuadrant == 2):
            turnAngle += 180.0
            fraction = turnAngle / 360.0
            bot.turn_lr(5900)
            bot.turn_lr(4500)
            time.sleep(fraction * 2.4)
            bot.stop_wheels_lr()
            bot.move_fb(4900)
            time.sleep(1.7) # replace with better measured time
            bot.stop_wheels_fb()
            temporaryCoords = get_serial()
            tempQuadrant = find_quadrant(temporaryCoords)
            currentQuadrant = 2
            if(tempQuadrant == 1):
                bot.move_fb(4900)
                time.sleep(0.45) # replace with better measured time
                bot.stop_wheels_fb()
        elif(targetQuadrant == 3):
            turnAngle += 180.0
            fraction = turnAngle / 360.0
            bot.turn_lr(5900)
            bot.turn_lr(4500)
            time.sleep(fraction * 2.4)
            bot.stop_wheels_lr()
            bot.move_fb(4900)
            time.sleep(1.7) # replace with better measured time
            bot.stop_wheels_fb()
            temporaryCoords = get_serial()
            tempQuadrant = find_quadrant(temporaryCoords)
            if(tempQuadrant == 1):
                bot.move_fb(4900)
                time.sleep(0.45) # replace with better measured time
                bot.stop_wheels_fb()
            # turn another 90 and move to the next quadrant
            turnAngle = 90.0
            fraction = turnAngle / 360.0
            bot.turn_lr(5900)
            bot.turn_lr(4500)
            time.sleep(fraction * 2.4)
            bot.stop_wheels_lr()
            bot.move_fb(4900)
            time.sleep(1.7) # replace with better measured time
            bot.stop_wheels_fb()
            temporaryCoords = get_serial()
            tempQuadrant = find_quadrant(temporaryCoords)
            currentQuadrant = 3
            if(tempQuadrant == 2):
                bot.move_fb(4900)
                time.sleep(0.45) # replace with better measured time
                bot.stop_wheels_fb()
    elif(currentQuadrant == 2):
        if(targetQuadrant == 0):
            fraction = turnAngle / 360.0
            bot.turn_lr(5900)
            bot.turn_lr(4500)
            time.sleep(fraction * 2.4)
            bot.stop_wheels_lr()
            bot.move_fb(4900)
            time.sleep(1.7) # replace with better measured time
            bot.stop_wheels_fb()
            temporaryCoords = get_serial()
            tempQuadrant = find_quadrant(temporaryCoords)
            if(tempQuadrant == 2):
                bot.move_fb(4900)
                time.sleep(0.45) # replace with better measured time
                bot.stop_wheels_fb()
            turnAngle = 270.0
            fraction = turnAngle / 360.0
            bot.turn_lr(5900)
            bot.turn_lr(4500)
            time.sleep(fraction * 2.4)
            bot.stop_wheels_lr()
            bot.move_fb(4900)
            time.sleep(1.7) # replace with better measured time
            bot.stop_wheels_fb()
            temporaryCoords = get_serial()
            tempQuadrant = find_quadrant(temporaryCoords)
            currentQuadrant = 0
            if(tempQuadrant == 1):
                bot.move_fb(4900)
                time.sleep(0.45) # replace with better measured time
                bot.stop_wheels_fb()
        elif(targetQuadrant == 1):
            fraction = turnAngle / 360.0
            bot.turn_lr(5900)
            bot.turn_lr(4500)
            time.sleep(fraction * 2.4)
            bot.stop_wheels_lr()
            bot.move_fb(4900)
            time.sleep(1.7) # replace with better measured time
            bot.stop_wheels_fb()
            temporaryCoords = get_serial()
            tempQuadrant = find_quadrant(temporaryCoords)
            currentQuadrant = 1
            if(tempQuadrant == 2):
                bot.move_fb(4900)
                time.sleep(0.45) # replace with better measured time
                bot.stop_wheels_fb()
        elif(targetQuadrant == 2):
            waiting = True
        elif(targetQuadrant == 3):
            turnAngle += 270.0 # -90 could cause issues, may need to be +270
            fraction = turnAngle / 360.0
            bot.turn_lr(5900)
            bot.turn_lr(4500)
            time.sleep(fraction * 2.4)
            bot.stop_wheels_lr()
            bot.move_fb(4900)
            time.sleep(1.7) # replace with better measured time
            bot.stop_wheels_fb()
            temporaryCoords = get_serial()
            tempQuadrant = find_quadrant(temporaryCoords)
            currentQuadrant = 3
            if(tempQuadrant == 2):
                bot.move_fb(4900)
                time.sleep(0.45) # replace with better measured time
                bot.stop_wheels_fb()
    elif(currentQuadrant == 3):
        if(targetQuadrant == 0):
            fraction = turnAngle / 360.0
            bot.turn_lr(5900)
            bot.turn_lr(4500)
            time.sleep(fraction * 2.4)
            bot.stop_wheels_lr()
            bot.move_fb(4900)
            time.sleep(1.7) # replace with better measured time
            bot.stop_wheels_fb()
            temporaryCoords = get_serial()
            tempQuadrant = find_quadrant(temporaryCoords)
            currentQuadrant = 0
            if(tempQuadrant == 3):
                bot.move_fb(4900)
                time.sleep(0.45) # replace with better measured time
                bot.stop_wheels_fb()
        elif(targetQuadrant == 1):
            fraction = turnAngle / 360.0
            bot.turn_lr(5900)
            bot.turn_lr(4500)
            time.sleep(fraction * 2.4)
            bot.stop_wheels_lr()
            bot.move_fb(4900)
            time.sleep(1.7) # replace with better measured time
            bot.stop_wheels_fb()
            temporaryCoords = get_serial()
            tempQuadrant = find_quadrant(temporaryCoords)
            if(tempQuadrant == 3):
                bot.move_fb(4900)
                time.sleep(0.45) # replace with better measured time
                bot.stop_wheels_fb()
            turnAngle = 90.0
            fraction = turnAngle / 360.0
            bot.turn_lr(5900)
            bot.turn_lr(4500)
            time.sleep(fraction * 2.4)
            bot.stop_wheels_lr()
            bot.move_fb(4900)
            time.sleep(1.7) # replace with better measured time
            bot.stop_wheels_fb()
            temporaryCoords = get_serial()
            tempQuadrant = find_quadrant(temporaryCoords)
            currentQuadrant = 1
            if(tempQuadrant == 1):
                bot.move_fb(4900)
                time.sleep(0.45) # replace with better measured time
                bot.stop_wheels_fb()
        elif(targetQuadrant == 2):
            turnAngle += 90.0
            fraction = turnAngle / 360.0
            bot.turn_lr(5900)
            bot.turn_lr(4500)
            time.sleep(fraction * 2.4)
            bot.stop_wheels_lr()
            bot.move_fb(4900)
            time.sleep(1.7) # replace with better measured time
            bot.stop_wheels_fb()
            temporaryCoords = get_serial()
            tempQuadrant = find_quadrant(temporaryCoords)
            currentQuadrant = 2
            if(tempQuadrant == 3):
                bot.move_fb(4900)
                time.sleep(0.45) # replace with better measured time
                bot.stop_wheels_fb()
        elif(targetQuadrant == 3):
            waiting = True
            
    #Once in the correct quadrant, announce charge and leave
    speech.tts_input("I need to charge")

    coords = get_serial()
    d1 = coords[0]
    d2 = coords[1]
    d3 = coords[2]
    d4 = coords[3]
    currentQuadrant = find_quadrant(coords)
    positionAngle = calc_angle(d3, d2)
    [x, y] = calc_position(d3, positionAngle)
    time.sleep(1.35)
    bot.move_fb(5900)
    bot.move_fb(7000)
    time.sleep(1.18)
    bot.stop_wheels_fb()
    # get new distances and position
    coords2 = get_serial()
    d1Next = coords2[0]
    d2Next = coords2[1]
    d3Next = coords2[2]
    d4Next = coords2[3]
    phi = calc_angle(d3Next, d2Next)
    [x2, y2] = calc_position(d3Next, phi)
    firstPoint = [x, y]
    secondPoint = [x2, y2]
    # print("first point:" + str(x) + ", " + str(y))
    # print ("second point: " + str(x2) + ", " + str(y2))
    # calculate the current angle ccw from 90 degrees
    turnAngle = calc_turn_angle(firstPoint, secondPoint)
    print("I need to turn " + str(turnAngle) + " degrees")
    
    #MOTION to charging station (A1)
    targetQuadrant = 1
    if(currentQuadrant == 0):
        if(targetQuadrant == 1):
            # turn to face East
            turnAngle += 90
            fraction = turnAngle / 360.0
            bot.turn_lr(5900)
            bot.turn_lr(4500)
            time.sleep(fraction * 2.4)
            bot.stop_wheels_lr()
            bot.move_fb(4900)
            time.sleep(1.7) # replace with better measured time
            bot.stop_wheels_fb()
            temporaryCoords = get_serial()
            tempQuadrant = find_quadrant(temporaryCoords)
            currentQuadrant = 1
            if(tempQuadrant == 0):
                bot.move_fb(4900)
                time.sleep(0.45) # replace with better measured time
                bot.stop_wheels_fb()
    elif(currentQuadrant == 1):
        if(targetQuadrant == 1):
            waiting = True
    elif(currentQuadrant == 2):
        if(targetQuadrant == 1):
            fraction = turnAngle / 360.0
            bot.turn_lr(5900)
            bot.turn_lr(4500)
            time.sleep(fraction * 2.4)
            bot.stop_wheels_lr()
            bot.move_fb(4900)
            time.sleep(1.7) # replace with better measured time
            bot.stop_wheels_fb()
            temporaryCoords = get_serial()
            tempQuadrant = find_quadrant(temporaryCoords)
            currentQuadrant = 1
            if(tempQuadrant == 2):
                bot.move_fb(4900)
                time.sleep(0.45) # replace with better measured time
                bot.stop_wheels_fb()
    elif(currentQuadrant == 3):
        if(targetQuadrant == 1):
            fraction = turnAngle / 360.0
            bot.turn_lr(5900)
            bot.turn_lr(4500)
            time.sleep(fraction * 2.4)
            bot.stop_wheels_lr()
            bot.move_fb(4900)
            time.sleep(1.7) # replace with better measured time
            bot.stop_wheels_fb()
            temporaryCoords = get_serial()
            tempQuadrant = find_quadrant(temporaryCoords)
            if(tempQuadrant == 3):
                bot.move_fb(4900)
                time.sleep(0.45) # replace with better measured time
                bot.stop_wheels_fb()
            turnAngle = 90.0
            fraction = turnAngle / 360.0
            bot.turn_lr(5900)
            bot.turn_lr(4500)
            time.sleep(fraction * 2.4)
            bot.stop_wheels_lr()
            bot.move_fb(4900)
            time.sleep(1.7) # replace with better measured time
            bot.stop_wheels_fb()
            temporaryCoords = get_serial()
            tempQuadrant = find_quadrant(temporaryCoords)
            currentQuadrant = 1
            if(tempQuadrant == 0):
                bot.move_fb(4900)
                time.sleep(0.45) # replace with better measured time
                bot.stop_wheels_fb()
    # Annouces charging activated (End of script)
    speech.tts_input("Charging Activated")

        

if __name__ == "__main__":
   main()        
    
    
    
    
