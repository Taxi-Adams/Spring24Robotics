import sys
import os
import time
import serial
import tts
import math
import random
import engine
import tkinter as tk
from PIL import ImageTk, Image
import _thread, threading
from flask import Flask, render_template, request
import controller
import client
import server
from tango import Tango
import pyttsx3
import RPi.GPIO as GPIO

GPIO.setmode(GPIO.BCM)

TRIG_PIN = 23
ECHO_PIN = 24

# def __init__(self):
#     self.debug_text = "bitterly biting boggart bits"

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

class guiTests:
    
    def __init__(self):
        if os.environ.get('DISPLAY','') == '':
            print('no display found. Using :0.0')
            os.environ.__setitem__('DISPLAY', ':0.0')

        self.eye_position_vert = 0.27 # subtract from this one
        self.left_eye_position_horiz = 0.175 # add to this one
        self.right_eye_position_horiz = 0.70 # add to this one
        self.left_eye_rotation_degree = 0
        self.right_eye_rotation_degree = 0
        self.is_moving = False
        self.is_talking = False
        self.is_moving_forward = False
        self.is_moving_backward = False
        self.is_moving_right = False
        self.is_moving_left = False
        self.face_image = Image.open("Robot_Face.png")
        self.left_eye_image = Image.open("Robot_Eye.png")
        self.right_eye_image = Image.open("Robot_Eye.png")
        self.talking_left_image = Image.open("Robot_Talking_Symbol.png")
        self.talking_right_image = Image.open("Robot_Talking_Symbol.png")
        self.moving_left_image = Image.open("Robot_Moving_Symbol.png")
        self.moving_right_image = Image.open("Robot_Moving_Symbol.png")
        self.text_background_image = Image.open("Robot_Text_Background.png")
        #self.testing_text = "bitterly biting boggart bits"
        self.testing_text = "                                                                                 "
        self.window = tk.Tk()
        self.window.after(1500, lambda: self.window.attributes('-fullscreen', True))
        self.width = self.window.winfo_screenwidth()
        self.height = self.window.winfo_screenheight()
        self.window.geometry("%dx%d" % (self.width, self.height))
        self.face_image = self.face_image.resize((round(0.99*self.width), round(0.99*self.height)))
        
        #self.window2 = tk.Tk()

        self.background = ImageTk.PhotoImage(self.face_image)
        self.background_label = tk.Label(image=self.background, borderwidth=0)
        self.background_label.image = self.background
        self.background_label.place(x=0, y=0)

        self.left_eye_image = self.left_eye_image.resize((round(0.10*self.width), round(0.25*self.height)))
        self.left_eye = ImageTk.PhotoImage(self.left_eye_image)
        self.left_eye_label = tk.Label(image=self.left_eye, borderwidth=0)
        self.left_eye_label.image = self.left_eye
        self.left_eye_label.place(x=round(0.175*self.width), y=round(0.27*self.height))

        self.right_eye_image = self.right_eye_image.resize((round(0.10*self.width), round(0.25*self.height)))
        self.right_eye = ImageTk.PhotoImage(self.right_eye_image)
        self.right_eye_label = tk.Label(image=self.right_eye, borderwidth=0)
        self.right_eye_label.image = self.right_eye
        self.right_eye_label.place(x=round(0.70*self.width), y=round(0.27*self.height))

        self.talking_left_image = self.talking_left_image.resize((round(0.10*self.width), round(0.25*self.height)))
        self.talking_left = ImageTk.PhotoImage(self.talking_left_image)
        self.talking_left_label = tk.Label(image=self.talking_left, borderwidth=0)
        self.talking_left_label.image = self.talking_left
        self.talking_left_label.place(x=round(1.5*self.width), y=round(1.5*self.height))

        self.talking_right_image = self.talking_right_image.resize((round(0.10*self.width), round(0.25*self.height)))
        self.talking_right = ImageTk.PhotoImage(self.talking_right_image)
        self.talking_right_label = tk.Label(image=self.talking_right, borderwidth=0)
        self.talking_right_label.image = self.talking_right
        self.talking_right_label.place(x=round(1.5*self.width), y=round(1.5*self.height))

        self.moving_left_image = self.moving_left_image.resize((round(0.10*self.width), round(0.25*self.height)))
        self.moving_left = ImageTk.PhotoImage(self.moving_left_image)
        self.moving_left_label = tk.Label(image=self.moving_left, borderwidth=0)
        self.moving_left_label.image = self.moving_left
        self.moving_left_label.place(x=round(1.5*self.width), y=round(1.5*self.height))

        self.moving_right_image = self.moving_right_image.resize((round(0.10*self.width), round(0.25*self.height)))
        self.moving_right = ImageTk.PhotoImage(self.moving_right_image)
        self.moving_right_label = tk.Label(image=self.moving_right, borderwidth=0)
        self.moving_right_label.image = self.moving_right
        self.moving_right_label.place(x=round(1.5*self.width), y=round(1.5*self.height))

        self.text_background = ImageTk.PhotoImage(self.text_background_image)
        #text_background_label = tk.Label(window, text=text, image=text_background, borderwidth=0, compound='center')
        self.text_background_label = tk.Label(self.window, text=self.testing_text, font=('Arial', 22), borderwidth=0)
        self.text_background_label.image = self.text_background
        #self.text_background_label.pack()
        self.text_background_label.place(x=round(0.10*self.width), y=round(0.855*self.height))
        
        self.bot= Tango()
        
        # variables for use in changing eye image
        self.isMoving = False
        self.isTalking= False
        self.upDown = 5900
        self.leftRight = 5900

    def windowUpdate(self):
        #is_talking = True
        #global testing_text
        #global window
        self.isTalking = True
        #input_text = self.testing_text + " b"
        input_text = self.testing_text
        #self.testing_text = input_text
        #self.text_background = ImageTk.PhotoImage(self.text_background_image)
        #self.text_background_label = tk.Label(self.window, text=self.text, image=self.text_background, borderwidth=0, compound='center')
        self.text_background_label = tk.Label(self.window, text=input_text, font=('Arial', 22), borderwidth=0)
        self.text_background_label.image = self.text_background
        #text_background_label.pack()
        self.text_background_label.place(x=round(0.09*self.width), y=round(0.850*self.height))
        if(self.isMoving and not self.isTalking):
            self.left_eye_label.place(x=round(self.left_eye_position_horiz*self.width), y=round(self.eye_position_vert*self.height))
            self.right_eye_label.place(x=round(self.right_eye_position_horiz*self.width), y=round(self.eye_position_vert*self.height))
        elif(self.isMoving and self.isTalking):
            self.left_eye_label.place(x=round(self.left_eye_position_horiz*self.width), y=round(self.eye_position_vert*self.height))
            self.right_eye_label.place(x=round(self.right_eye_position_horiz*self.width), y=round(self.eye_position_vert*self.height))
        elif(not self.isMoving and self.isTalking):
            self.left_eye_label.place(x=round(self.left_eye_position_horiz*self.width), y=round(self.eye_position_vert*self.height))
            self.right_eye_label.place(x=round(self.right_eye_position_horiz*self.width), y=round(self.eye_position_vert*self.height))
        elif(not self.isMoving and not self.isTalking):
            self.left_eye_label.place(x=round(self.left_eye_position_horiz*self.width), y=round(self.eye_position_vert*self.height))
            self.right_eye_label.place(x=round(self.right_eye_position_horiz*self.width), y=round(self.eye_position_vert*self.height))
        self.window.after(330, self.windowUpdate)
        
    def secondMethod(self):
        counter = 1
        while(counter < 120):
            print(counter)
            counter = counter + 1
            time.sleep(.07)
    
    def mainThread(self):
        #self.windowUpdate("Hello World")
        self.windowUpdate()
        time.sleep(.015)
        self.window.mainloop()
        
    def otherMainThread(self):
        self.window2.mainloop()
        
    def nonGuiMainThread(self):
        # initialize bot
        bot = Tango()
        coords = get_serial()
        # default eye position vertical and horizontal
        self.eye_position_vert = 0.27
        self.left_eye_position_horiz = 0.175
        self.right_eye_position_horiz = 0.70
        #print("Reached point after getting serial")
        d1 = coords[0]
        d2 = coords[1]
        d3 = coords[2]
        d4 = coords[3]
        # find the current quadrant and report it vocally
        currentQuadrant = find_quadrant(coords)
        positionAngle = calc_angle(d3, d2)
        [x, y] = calc_position(d3, positionAngle)
        
        # Sets up Text-to-speech
        self.isTalking = True
        speech = tts.Speech()
        greetings = ['Hello!', 'Hi there!', 'Whats up!', 'Howdy!']

        # Waits until someone approaches
        while True:
            dist = _objectDetectionTestrand() #objectDetection.get_distance()
            if dist <= 42:
                break
        
        # Once someone approaches, greet them
        speech.tts_input((random.choice(greetings), "How can I assist?"))
        print("Made it past greeting the person")

        # Goes to the script/ AI, and gets the correct quadrant
        bot2 = engine.Dialog_Engine()
        targetQuadrant = bot2.main()
        print("Got a quadrant response/input!!!!!")
        self.isTalking = False
        
        # move backwards slowly
        self.isMoving = True
        self.eye_position_vert = 0.37
        time.sleep(2.0)
        bot.move_fb(5900)
        bot.move_fb(7000)
        time.sleep(1.3)
        bot.stop_wheels_fb()
        self.isMoving = False
        self.eye_position_vert = 0.27
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
                self.isMoving = True
                # turning right
                self.left_eye_position_horiz = 0.255
                self.right_eye_position_horiz = 0.755
                bot.turn_lr(5900)
                bot.turn_lr(4500)
                time.sleep(fraction * 2.4)
                bot.stop_wheels_lr()
                # default centered eye positions
                self.left_eye_position_horiz = 0.175
                self.right_eye_position_horiz = 0.70
                self.isMoving = False
                self.isMoving = True
                self.eye_position_vert = 0.17
                bot.move_fb(4900)
                time.sleep(1.7) # replace with better measured time
                bot.stop_wheels_fb()
                self.isMoving = False
                self.eye_position_vert = 0.27
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
                self.isMoving = True
                self.left_eye_position_horiz = 0.255
                self.right_eye_position_horiz = 0.755
                bot.turn_lr(5900)
                bot.turn_lr(4500)
                time.sleep(fraction * 2.4)
                bot.stop_wheels_lr()
                self.left_eye_position_horiz = 0.175
                self.right_eye_position_horiz = 0.70
                self.isMoving = False
                self.isMoving = True
                self.eye_position_vert = 0.17
                bot.move_fb(4900)
                time.sleep(1.7) # replace with better measured time
                bot.stop_wheels_fb()
                self.isMoving = False
                self.eye_position_vert = 0.27
                temporaryCoords = get_serial()
                tempQuadrant = find_quadrant(temporaryCoords)
                if(tempQuadrant == 0):
                    bot.move_fb(4900)
                    time.sleep(0.45) # replace with better measured time
                    bot.stop_wheels_fb()
                # turn another 90 and move to the next quadrant
                turnAngle = 90.0
                fraction = turnAngle / 360.0
                self.isMoving = True
                self.left_eye_position_horiz = 0.255
                self.right_eye_position_horiz = 0.755
                bot.turn_lr(5900)
                bot.turn_lr(4500)
                time.sleep(fraction * 2.4)
                bot.stop_wheels_lr()
                self.left_eye_position_horiz = 0.175
                self.right_eye_position_horiz = 0.70
                self.isMoving = False
                self.isMoving = True
                self.eye_position_vert = 0.17
                bot.move_fb(4900)
                time.sleep(1.7) # replace with better measured time
                bot.stop_wheels_fb()
                self.isMoving = False
                self.eye_position_vert = 0.27
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
                self.isMoving = True
                self.left_eye_position_horiz = 0.255
                self.right_eye_position_horiz = 0.755
                bot.turn_lr(5900)
                bot.turn_lr(4500)
                time.sleep(fraction * 2.4)
                bot.stop_wheels_lr()
                self.left_eye_position_horiz = 0.175
                self.right_eye_position_horiz = 0.70
                self.isMoving = False
                self.isMoving = True
                self.eye_position_vert = 0.17
                bot.move_fb(4900)
                time.sleep(1.7) # replace with better measured time
                bot.stop_wheels_fb()
                self.isMoving = False
                self.eye_position_vert = 0.27
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
                self.isMoving = True
                self.left_eye_position_horiz = 0.255
                self.right_eye_position_horiz = 0.755
                bot.turn_lr(5900)
                bot.turn_lr(4500)
                time.sleep(fraction * 2.4)
                bot.stop_wheels_lr()
                self.left_eye_position_horiz = 0.175
                self.right_eye_position_horiz = 0.70
                self.isMoving = False
                self.isMoving = True
                self.eye_position_vert = 0.17
                bot.move_fb(4900)
                time.sleep(1.7) # replace with better measured time
                bot.stop_wheels_fb()
                self.isMoving = False
                self.eye_position_vert = 0.27
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
                self.isMoving = True
                self.left_eye_position_horiz = 0.255
                self.right_eye_position_horiz = 0.755
                bot.turn_lr(5900)
                bot.turn_lr(4500)
                time.sleep(fraction * 2.4)
                bot.stop_wheels_lr()
                self.left_eye_position_horiz = 0.175
                self.right_eye_position_horiz = 0.70
                self.isMoving = False
                self.isMoving = True
                self.eye_position_vert = 0.17
                bot.move_fb(4900)
                time.sleep(1.7) # replace with better measured time
                bot.stop_wheels_fb()
                self.isMoving = False
                self.eye_position_vert = 0.27
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
                self.isMoving = True
                self.left_eye_position_horiz = 0.255
                self.right_eye_position_horiz = 0.755
                bot.turn_lr(5900)
                bot.turn_lr(4500)
                time.sleep(fraction * 2.4)
                bot.stop_wheels_lr()
                self.left_eye_position_horiz = 0.175
                self.right_eye_position_horiz = 0.70
                self.isMoving = False
                self.isMoving = True
                self.eye_position_vert = 0.17
                bot.move_fb(4900)
                time.sleep(1.7) # replace with better measured time
                bot.stop_wheels_fb()
                self.isMoving = False
                self.eye_position_vert = 0.27
                temporaryCoords = get_serial()
                tempQuadrant = find_quadrant(temporaryCoords)
                if(tempQuadrant == 1):
                    bot.move_fb(4900)
                    time.sleep(0.45) # replace with better measured time
                    bot.stop_wheels_fb()
                # turn another 90 and move to the next quadrant
                turnAngle = 90.0
                fraction = turnAngle / 360.0
                self.isMoving = True
                self.left_eye_position_horiz = 0.255
                self.right_eye_position_horiz = 0.755
                bot.turn_lr(5900)
                bot.turn_lr(4500)
                time.sleep(fraction * 2.4)
                bot.stop_wheels_lr()
                self.left_eye_position_horiz = 0.175
                self.right_eye_position_horiz = 0.70
                self.isMoving = False
                self.isMoving = True
                self.eye_position_vert = 0.17
                bot.move_fb(4900)
                time.sleep(1.7) # replace with better measured time
                bot.stop_wheels_fb()
                self.isMoving = False
                self.eye_position_vert = 0.27
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
                self.isMoving = True
                self.left_eye_position_horiz = 0.255
                self.right_eye_position_horiz = 0.755
                bot.turn_lr(5900)
                bot.turn_lr(4500)
                time.sleep(fraction * 2.4)
                bot.stop_wheels_lr()
                self.left_eye_position_horiz = 0.175
                self.right_eye_position_horiz = 0.70
                self.isMoving = False
                self.isMoving = True
                self.eye_position_vert = 0.17
                bot.move_fb(4900)
                time.sleep(1.7) # replace with better measured time
                bot.stop_wheels_fb()
                self.isMoving = False
                self.eye_position_vert = 0.27
                temporaryCoords = get_serial()
                tempQuadrant = find_quadrant(temporaryCoords)
                if(tempQuadrant == 2):
                    bot.move_fb(4900)
                    time.sleep(0.45) # replace with better measured time
                    bot.stop_wheels_fb()
                turnAngle = 270.0
                fraction = turnAngle / 360.0
                self.isMoving = True
                self.left_eye_position_horiz = 0.255
                self.right_eye_position_horiz = 0.755
                bot.turn_lr(5900)
                bot.turn_lr(4500)
                time.sleep(fraction * 2.4)
                bot.stop_wheels_lr()
                self.left_eye_position_horiz = 0.175
                self.right_eye_position_horiz = 0.70
                self.isMoving = False
                self.isMoving = True
                self.eye_position_vert = 0.17
                bot.move_fb(4900)
                time.sleep(1.7) # replace with better measured time
                bot.stop_wheels_fb()
                self.isMoving = False
                self.eye_position_vert = 0.27
                temporaryCoords = get_serial()
                tempQuadrant = find_quadrant(temporaryCoords)
                currentQuadrant = 0
                if(tempQuadrant == 1):
                    bot.move_fb(4900)
                    time.sleep(0.45) # replace with better measured time
                    bot.stop_wheels_fb()
            elif(targetQuadrant == 1):
                fraction = turnAngle / 360.0
                self.isMoving = True
                self.left_eye_position_horiz = 0.255
                self.right_eye_position_horiz = 0.755
                bot.turn_lr(5900)
                bot.turn_lr(4500)
                time.sleep(fraction * 2.4)
                bot.stop_wheels_lr()
                self.left_eye_position_horiz = 0.175
                self.right_eye_position_horiz = 0.70
                self.isMoving = False
                self.isMoving = True
                self.eye_position_vert = 0.17
                bot.move_fb(4900)
                time.sleep(1.7) # replace with better measured time
                bot.stop_wheels_fb()
                self.isMoving = False
                self.eye_position_vert = 0.27
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
                self.isMoving = True
                self.left_eye_position_horiz = 0.255
                self.right_eye_position_horiz = 0.755
                bot.turn_lr(5900)
                bot.turn_lr(4500)
                time.sleep(fraction * 2.4)
                bot.stop_wheels_lr()
                self.left_eye_position_horiz = 0.175
                self.right_eye_position_horiz = 0.70
                self.isMoving = False
                self.isMoving = True
                self.eye_position_vert = 0.17
                bot.move_fb(4900)
                time.sleep(1.7) # replace with better measured time
                bot.stop_wheels_fb()
                self.isMoving = False
                self.eye_position_vert = 0.27
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
                self.isMoving = True
                self.left_eye_position_horiz = 0.255
                self.right_eye_position_horiz = 0.755
                bot.turn_lr(5900)
                bot.turn_lr(4500)
                time.sleep(fraction * 2.4)
                bot.stop_wheels_lr()
                self.left_eye_position_horiz = 0.175
                self.right_eye_position_horiz = 0.70
                self.isMoving = False
                self.isMoving = True
                self.eye_position_vert = 0.17
                bot.move_fb(4900)
                time.sleep(1.7) # replace with better measured time
                bot.stop_wheels_fb()
                self.isMoving = False
                self.eye_position_vert = 0.27
                temporaryCoords = get_serial()
                tempQuadrant = find_quadrant(temporaryCoords)
                currentQuadrant = 0
                if(tempQuadrant == 3):
                    bot.move_fb(4900)
                    time.sleep(0.45) # replace with better measured time
                    bot.stop_wheels_fb()
            elif(targetQuadrant == 1):
                fraction = turnAngle / 360.0
                self.isMoving = True
                self.left_eye_position_horiz = 0.255
                self.right_eye_position_horiz = 0.755
                bot.turn_lr(5900)
                bot.turn_lr(4500)
                time.sleep(fraction * 2.4)
                bot.stop_wheels_lr()
                self.left_eye_position_horiz = 0.175
                self.right_eye_position_horiz = 0.70
                self.isMoving = False
                self.isMoving = True
                self.eye_position_vert = 0.17
                bot.move_fb(4900)
                time.sleep(1.7) # replace with better measured time
                bot.stop_wheels_fb()
                self.isMoving = False
                self.eye_position_vert = 0.27
                temporaryCoords = get_serial()
                tempQuadrant = find_quadrant(temporaryCoords)
                if(tempQuadrant == 3):
                    bot.move_fb(4900)
                    time.sleep(0.45) # replace with better measured time
                    bot.stop_wheels_fb()
                turnAngle = 90.0
                fraction = turnAngle / 360.0
                self.isMoving = True
                self.left_eye_position_horiz = 0.255
                self.right_eye_position_horiz = 0.755
                bot.turn_lr(5900)
                bot.turn_lr(4500)
                time.sleep(fraction * 2.4)
                bot.stop_wheels_lr()
                self.left_eye_position_horiz = 0.175
                self.right_eye_position_horiz = 0.70
                self.isMoving = False
                self.isMoving = True
                self.eye_position_vert = 0.17
                bot.move_fb(4900)
                time.sleep(1.7) # replace with better measured time
                bot.stop_wheels_fb()
                self.isMoving = False
                self.eye_position_vert = 0.27
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
                self.isMoving = True
                self.left_eye_position_horiz = 0.255
                self.right_eye_position_horiz = 0.755
                bot.turn_lr(5900)
                bot.turn_lr(4500)
                time.sleep(fraction * 2.4)
                bot.stop_wheels_lr()
                self.left_eye_position_horiz = 0.175
                self.right_eye_position_horiz = 0.70
                self.isMoving = False
                self.isMoving = True
                self.eye_position_vert = 0.17
                bot.move_fb(4900)
                time.sleep(1.7) # replace with better measured time
                bot.stop_wheels_fb()
                self.isMoving = False
                self.eye_position_vert = 0.27
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
        self.isTalking = True
        speech.tts_input("I need to charge")
        self.isTalking = False

        coords = get_serial()
        d1 = coords[0]
        d2 = coords[1]
        d3 = coords[2]
        d4 = coords[3]
        currentQuadrant = find_quadrant(coords)
        positionAngle = calc_angle(d3, d2)
        [x, y] = calc_position(d3, positionAngle)
        self.isMoving = True
        self.eye_position_vert = 0.37
        time.sleep(1.35)
        bot.move_fb(5900)
        bot.move_fb(7000)
        time.sleep(1.18)
        bot.stop_wheels_fb()
        self.isMoving = False
        self.eye_position_vert = 0.27
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
                self.isMoving = True
                self.left_eye_position_horiz = 0.255
                self.right_eye_position_horiz = 0.755
                bot.turn_lr(5900)
                bot.turn_lr(4500)
                time.sleep(fraction * 2.4)
                bot.stop_wheels_lr()
                self.left_eye_position_horiz = 0.175
                self.right_eye_position_horiz = 0.70
                self.isMoving = False
                self.isMoving = True
                self.eye_position_vert = 0.17
                bot.move_fb(4900)
                time.sleep(1.7) # replace with better measured time
                bot.stop_wheels_fb()
                self.isMoving = False
                self.eye_position_vert = 0.27
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
                self.isMoving = True
                self.left_eye_position_horiz = 0.255
                self.right_eye_position_horiz = 0.755
                bot.turn_lr(5900)
                bot.turn_lr(4500)
                time.sleep(fraction * 2.4)
                bot.stop_wheels_lr()
                self.left_eye_position_horiz = 0.175
                self.right_eye_position_horiz = 0.70
                self.isMoving = False
                self.isMoving = True
                self.eye_position_vert = 0.17
                bot.move_fb(4900)
                time.sleep(1.7) # replace with better measured time
                bot.stop_wheels_fb()
                self.isMoving = False
                self.eye_position_vert = 0.27
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
                self.isMoving = True
                self.left_eye_position_horiz = 0.255
                self.right_eye_position_horiz = 0.755
                bot.turn_lr(5900)
                bot.turn_lr(4500)
                time.sleep(fraction * 2.4)
                bot.stop_wheels_lr()
                self.left_eye_position_horiz = 0.175
                self.right_eye_position_horiz = 0.70
                self.isMoving = False
                self.isMoving = True
                self.eye_position_vert = 0.17
                bot.move_fb(4900)
                time.sleep(1.7) # replace with better measured time
                bot.stop_wheels_fb()
                self.isMoving = False
                self.eye_position_vert = 0.27
                temporaryCoords = get_serial()
                tempQuadrant = find_quadrant(temporaryCoords)
                if(tempQuadrant == 3):
                    bot.move_fb(4900)
                    time.sleep(0.45) # replace with better measured time
                    bot.stop_wheels_fb()
                turnAngle = 90.0
                fraction = turnAngle / 360.0
                self.isMoving = True
                self.left_eye_position_horiz = 0.255
                self.right_eye_position_horiz = 0.755
                bot.turn_lr(5900)
                bot.turn_lr(4500)
                time.sleep(fraction * 2.4)
                bot.stop_wheels_lr()
                self.left_eye_position_horiz = 0.175
                self.right_eye_position_horiz = 0.70
                self.isMoving = False
                self.isMoving = True
                self.eye_position_vert = 0.17
                bot.move_fb(4900)
                time.sleep(1.7) # replace with better measured time
                bot.stop_wheels_fb()
                self.isMoving = False
                self.eye_position_vert = 0.27
                temporaryCoords = get_serial()
                tempQuadrant = find_quadrant(temporaryCoords)
                currentQuadrant = 1
                if(tempQuadrant == 0):
                    bot.move_fb(4900)
                    time.sleep(0.45) # replace with better measured time
                    bot.stop_wheels_fb()
        # Annouces charging activated (End of script)
        self.isTalking = True
        speech.tts_input("Charging Activated")
        self.isTalking = False
        
inst = guiTests()

# try:
#     _thread.start_new_thread(inst.mainThread,())
# except:
#    print ("Error: unable to start thread")
# try:
#     t2 = threading.Thread(target= inst.flaskTest, args= ())
#     t2.start()
# except:
#     print ("Error: unable to start thread")
try:
    t2 = threading.Thread(target= inst.nonGuiMainThread, args= ())
    t2.start()
except:
    print("Error: Unable to start thread")
    

#inst.otherMainThread()

inst.mainThread()

    # if __name__ == "__main__":
    #     main(self)