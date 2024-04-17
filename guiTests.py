import sys

import os

import time

import tkinter as tk

from PIL import ImageTk, Image

import _thread, threading

from flask import Flask, render_template, request

import controller

import client

from tango import Tango

import pyttsx3

# def __init__(self):
#     self.debug_text = "bitterly biting boggart bits"

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
        self.testing_text = "bitterly biting boggart bits"
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
        input_text = self.testing_text + " b"
        self.testing_text = input_text
        #self.text_background = ImageTk.PhotoImage(self.text_background_image)
        #self.text_background_label = tk.Label(self.window, text=self.text, image=self.text_background, borderwidth=0, compound='center')
        self.text_background_label = tk.Label(self.window, text=input_text, font=('Arial', 22), borderwidth=0)
        self.text_background_label.image = self.text_background
        #text_background_label.pack()
        self.text_background_label.place(x=round(0.10*self.width), y=round(0.855*self.height))
        
        # if(self.is_moving_forward and not self.is_moving_left and not self.is_moving_right):
        #     self.left_eye_rotation_degree = 0
        #     self.right_eye_rotation_degree = 0
        # elif(self.is_moving_backward and not self.is_moving_left and not self.is_moving_right):
        #     self.left_eye_rotation_degree = 180
        #     self.right_eye_rotation_degree = 180
        # elif(self.is_moving_left and not self.is_moving_backward and not self.is_moving_forward):
        #     self.left_eye_rotation_degree = 270
        #     self.right_eye_rotation_degree = 270
        # elif(self.is_moving_right and not self.is_moving_backward and not self.is_moving_forward):
        #     self.left_eye_rotation_degree = 90
        #     self.right_eye_rotation_degree = 90
        # elif(self.is_moving_forward and self.is_moving_left):
        #     self.left_eye_rotation_degree = 315
        #     self.right_eye_rotation_degree = 315
        # elif(self.is_moving_forward and self.is_moving_right):
        #     self.left_eye_rotation_degree = 45
        #     self.right_eye_rotation_degree = 45
        # elif(self.is_moving_backward and self.is_moving_left):
        #     self.left_eye_rotation_degree = 225
        #     self.right_eye_rotation_degree = 225
        # elif(self.is_moving_backward and self.is_moving_right):
        #     self.left_eye_rotation_degree = 135
        #     self.right_eye_rotation_degree = 135
        # else:
        #     self.left_eye_rotation_degree = 0
        #     self.right_eye_rotation_degree = 0
        
        
        # Delete eye images before next iteration to remove ghosting
        # self.left_eye_label.destroy()
        # self.right_eye_label.destroy()
        # self.talking_left_label.destroy()
        # self.talking_right_label.destroy()
        # self.moving_left_label.destroy()
        # self.moving_right_label.destroy()
        
        # self.window.after(330, self.windowUpdate)
        if(self.isMoving and not self.isTalking):
            # display moving arrow eyes
            # self.left_eye_image = self.left_eye_image.rotate(self.left_eye_rotation_degree)
            # self.left_eye = ImageTk.PhotoImage(self.left_eye_image)
            # self.left_eye_label = tk.Label(image=self.left_eye, borderwidth=0)
            # self.left_eye_label.image = self.left_eye
            # self.right_eye_image = self.right_eye_image.rotate(self.right_eye_rotation_degree)
            # self.right_eye = ImageTk.PhotoImage(self.right_eye_image)
            # self.right_eye_label = tk.Label(image=self.right_eye, borderwidth=0)
            # self.right_eye_label.image = self.right_eye
            self.left_eye_label.place(x=round(self.left_eye_position_horiz*self.width), y=round(self.eye_position_vert*self.height))
            self.right_eye_label.place(x=round(self.right_eye_position_horiz*self.width), y=round(self.eye_position_vert*self.height))
            # self.left_eye_label.place(x=round(1.5*self.width), y=round(1.5*self.height))
            # self.right_eye_label.place(x=round(1.5*self.width), y=round(1.5*self.height))
            # self.talking_left_image = self.talking_left_image.rotate(self.left_eye_rotation_degree)
            # self.talking_left = ImageTk.PhotoImage(self.talking_left_image)
            # self.talking_left_label = tk.Label(image=self.talking_left, borderwidth=0)
            # self.talking_left_label.image = self.talking_left
            # self.talking_right_image = self.talking_right_image.rotate(self.right_eye_rotation_degree)
            # self.talking_right = ImageTk.PhotoImage(self.talking_right_image)
            # self.talking_right_label = tk.Label(image=self.talking_right, borderwidth=0)
            # self.talking_right_label.image = self.talking_right
            # self.talking_left_label.place(x=round(1.5*self.width), y=round(1.5*self.height))
            # self.talking_right_label.place(x=round(1.5*self.width), y=round(1.5*self.height))
            # self.moving_left_image = self.moving_left_image.rotate(self.left_eye_rotation_degree)
            # self.moving_left = ImageTk.PhotoImage(self.moving_left_image)
            # self.moving_left_label = tk.Label(image=self.moving_left, borderwidth=0)
            # self.moving_left_label.image = self.moving_left
            # self.moving_right_image = self.moving_right_image.rotate(self.right_eye_rotation_degree)
            # self.moving_right = ImageTk.PhotoImage(self.moving_right_image)
            # self.moving_right_label = tk.Label(image=self.moving_right, borderwidth=0)
            # self.moving_right_label.image = self.moving_right
            # self.moving_left_label.place(x=round(self.left_eye_position_horiz*self.width), y=round(self.eye_position_vert*self.height))
            # self.moving_right_label.place(x=round(self.right_eye_position_horiz*self.width), y=round(self.eye_position_vert*self.height))
        elif(self.isMoving and self.isTalking):
            # more important to display arrow eyes, as talking is also indicated with subtitles on mouth
            # self.left_eye_image = self.left_eye_image.rotate(self.left_eye_rotation_degree)
            # self.left_eye = ImageTk.PhotoImage(self.left_eye_image)
            # self.left_eye_label = tk.Label(image=self.left_eye, borderwidth=0)
            # self.left_eye_label.image = self.left_eye
            # self.right_eye_image = self.right_eye_image.rotate(self.right_eye_rotation_degree)
            # self.right_eye = ImageTk.PhotoImage(self.right_eye_image)
            # self.right_eye_label = tk.Label(image=self.right_eye, borderwidth=0)
            # self.right_eye_label.image = self.right_eye
            self.left_eye_label.place(x=round(self.left_eye_position_horiz*self.width), y=round(self.eye_position_vert*self.height))
            self.right_eye_label.place(x=round(self.right_eye_position_horiz*self.width), y=round(self.eye_position_vert*self.height))
            # self.left_eye_label.place(x=round(1.5*self.width), y=round(1.5*self.height))
            # self.right_eye_label.place(x=round(1.5*self.width), y=round(1.5*self.height))
            # self.talking_left_image = self.talking_left_image.rotate(self.left_eye_rotation_degree)
            # self.talking_left = ImageTk.PhotoImage(self.talking_left_image)
            # self.talking_left_label = tk.Label(image=self.talking_left, borderwidth=0)
            # self.talking_left_label.image = self.talking_left
            # self.talking_right_image = self.talking_right_image.rotate(self.right_eye_rotation_degree)
            # self.talking_right = ImageTk.PhotoImage(self.talking_right_image)
            # self.talking_right_label = tk.Label(image=self.talking_right, borderwidth=0)
            # self.talking_right_label.image = self.talking_right
            # self.talking_left_label.place(x=round(1.5*self.width), y=round(1.5*self.height))
            # self.talking_right_label.place(x=round(1.5*self.width), y=round(1.5*self.height))
            # self.moving_left_image = self.moving_left_image.rotate(self.left_eye_rotation_degree)
            # self.moving_left = ImageTk.PhotoImage(self.moving_left_image)
            # self.moving_left_label = tk.Label(image=self.moving_left, borderwidth=0)
            # self.moving_left_label.image = self.moving_left
            # self.moving_right_image = self.moving_right_image.rotate(self.right_eye_rotation_degree)
            # self.moving_right = ImageTk.PhotoImage(self.moving_right_image)
            # self.moving_right_label = tk.Label(image=self.moving_right, borderwidth=0)
            # self.moving_right_label.image = self.moving_right
            # self.moving_left_label.place(x=round(self.left_eye_position_horiz*self.width), y=round(self.eye_position_vert*self.height))
            # self.moving_right_label.place(x=round(self.right_eye_position_horiz*self.width), y=round(self.eye_position_vert*self.height))
        elif(not self.isMoving and self.isTalking):
            # eyes are speech bubbles, others off screen
            # self.left_eye_image = self.left_eye_image.rotate(self.left_eye_rotation_degree)
            # self.left_eye = ImageTk.PhotoImage(self.left_eye_image)
            # self.left_eye_label = tk.Label(image=self.left_eye, borderwidth=0)
            # self.left_eye_label.image = self.left_eye
            # self.right_eye_image = self.right_eye_image.rotate(self.right_eye_rotation_degree)
            # self.right_eye = ImageTk.PhotoImage(self.right_eye_image)
            # self.right_eye_label = tk.Label(image=self.right_eye, borderwidth=0)
            # self.right_eye_label.image = self.right_eye
            self.left_eye_label.place(x=round(self.left_eye_position_horiz*self.width), y=round(self.eye_position_vert*self.height))
            self.right_eye_label.place(x=round(self.right_eye_position_horiz*self.width), y=round(self.eye_position_vert*self.height))
            # self.left_eye_label.place(x=round(1.5*self.width), y=round(1.5*self.height))
            # self.right_eye_label.place(x=round(1.5*self.width), y=round(1.5*self.height))
            # self.talking_left_image = self.talking_left_image.rotate(self.left_eye_rotation_degree)
            # self.talking_left = ImageTk.PhotoImage(self.talking_left_image)
            # self.talking_left_label = tk.Label(image=self.talking_left, borderwidth=0)
            # self.talking_left_label.image = self.talking_left
            # self.talking_right_image = self.talking_right_image.rotate(self.right_eye_rotation_degree)
            # self.talking_right = ImageTk.PhotoImage(self.talking_right_image)
            # self.talking_right_label = tk.Label(image=self.talking_right, borderwidth=0)
            # self.talking_right_label.image = self.talking_right
            # self.talking_left_label.place(x=round(self.left_eye_position_horiz*self.width), y=round(self.eye_position_vert*self.height))
            # self.talking_right_label.place(x=round(self.right_eye_position_horiz*self.width), y=round(self.eye_position_vert*self.height))
            # self.moving_left_image = self.moving_left_image.rotate(self.left_eye_rotation_degree)
            # self.moving_left = ImageTk.PhotoImage(self.moving_left_image)
            # self.moving_left_label = tk.Label(image=self.moving_left, borderwidth=0)
            # self.moving_left_label.image = self.moving_left
            # self.moving_right_image = self.moving_right_image.rotate(self.right_eye_rotation_degree)
            # self.moving_right = ImageTk.PhotoImage(self.moving_right_image)
            # self.moving_right_label = tk.Label(image=self.moving_right, borderwidth=0)
            # self.moving_right_label.image = self.moving_right
            # self.moving_left_label.place(x=round(1.5*self.width), y=round(1.5*self.height))
            # self.moving_right_label.place(x=round(1.5*self.width), y=round(1.5*self.height))
        elif(not self.isMoving and not self.isTalking):
            # display normal eyes
            # self.left_eye_image = self.left_eye_image.rotate(self.left_eye_rotation_degree)
            # self.left_eye = ImageTk.PhotoImage(self.left_eye_image)
            # self.left_eye_label = tk.Label(image=self.left_eye, borderwidth=0)
            # self.left_eye_label.image = self.left_eye
            # self.right_eye_image = self.right_eye_image.rotate(self.right_eye_rotation_degree)
            # self.right_eye = ImageTk.PhotoImage(self.right_eye_image)
            # self.right_eye_label = tk.Label(image=self.right_eye, borderwidth=0)
            # self.right_eye_label.image = self.right_eye
            self.left_eye_label.place(x=round(self.left_eye_position_horiz*self.width), y=round(self.eye_position_vert*self.height))
            self.right_eye_label.place(x=round(self.right_eye_position_horiz*self.width), y=round(self.eye_position_vert*self.height))
            # self.left_eye_label.place(x=round(self.left_eye_position_horiz*self.width), y=round(eye_position_vert*self.height))
            # self.right_eye_label.place(x=round(self.right_eye_position_horiz*self.width), y=round(eye_position_vert*self.height))
            # self.talking_left_image = self.talking_left_image.rotate(self.left_eye_rotation_degree)
            # self.talking_left = ImageTk.PhotoImage(self.talking_left_image)
            # self.talking_left_label = tk.Label(image=self.talking_left, borderwidth=0)
            # self.talking_left_label.image = self.talking_left
            # self.talking_right_image = self.talking_right_image.rotate(self.right_eye_rotation_degree)
            # self.talking_right = ImageTk.PhotoImage(self.talking_right_image)
            # self.talking_right_label = tk.Label(image=self.talking_right, borderwidth=0)
            # self.talking_right_label.image = self.talking_right
            # self.talking_left_label.place(x=round(1.5*self.width), y=round(1.5*self.height))
            # self.talking_right_label.place(x=round(1.5*self.width), y=round(1.5*self.height))
            # self.moving_left_image = self.moving_left_image.rotate(self.left_eye_rotation_degree)
            # self.moving_left = ImageTk.PhotoImage(self.moving_left_image)
            # self.moving_left_label = tk.Label(image=self.moving_left, borderwidth=0)
            # self.moving_left_label.image = self.moving_left
            # self.moving_right_image = self.moving_right_image.rotate(self.right_eye_rotation_degree)
            # self.moving_right = ImageTk.PhotoImage(self.moving_right_image)
            # self.moving_right_label = tk.Label(image=self.moving_right, borderwidth=0)
            # self.moving_right_label.image = self.moving_right
            # self.moving_left_label.place(x=round(1.5*self.width), y=round(1.5*self.height))
            # self.moving_right_label.place(x=round(1.5*self.width), y=round(1.5*self.height))
        self.window.after(330, self.windowUpdate)
            
        
    def newFind(self, data: dict) -> None:
        # controller's find method, imported here to test for calling from here and not controller itself.
        try:
            servoVal = int(data['value']) * 40 + 4000
        except: pass
        match data['servo']:
            case ['WHEELFORWARDBACKWARD', 'WHEELTURN']: 
                if int(data['value'][1]) == 0:
                    self.bot.stop_wheels_fb()
                    self.eye_position_vert = 0.27
                    #self.left_eye_rotation_degree = 0
                    #self.right_eye_rotation_degree = 0
                    self.is_moving_forward = False
                    self.is_moving_backward = False
                    self.isMoving = False
                # Backwards
                elif int(data['value'][1]) > 0:
                    servoVal = int(data['value'][1]) * (12) + 5900
                    self.bot.move_fb(servoVal)
                    if(servoVal < 5500 or servoVal > 6300):
                        self.eye_position_vert = 0.37
                        self.is_moving_backward = True
                        self.is_moving_forward = False
                    elif(servoVal >= 5500 and servoVal <= 6300):
                        # gives wiggle room for eyes to look straight left/right
                        self.eye_position_vert = 0.27
                        self.is_moving_forward = False
                        self.is_moving_backward = False
                    #self.left_eye_rotation_degree = 180
                    #self.right_eye_rotation_degree = 180
                    #self.eye_position_vert = self.eye_position_vert - int(data['value'][1]) * self.eye_position_vert / 1000
                    self.isMoving = True
                # Forwards
                elif int(data['value'][1]) < 0:
                    servoVal = 5900 - int(data['value'][1]) * (-17)
                    self.bot.move_fb(servoVal)
                    if(servoVal < 5500 or servoVal > 6300):
                        self.eye_position_vert = 0.17
                        self.is_moving_backward = False
                        self.is_moving_forward = True
                    elif(servoVal >= 5500 and servoVal <= 6300):
                        # gives wiggle room for eyes to look straight left/right
                        self.eye_position_vert = 0.27
                        self.is_moving_forward = False
                        self.is_moving_backward = False
                    #self.left_eye_rotation_degree = 0
                    #self.right_eye_rotation_degree = 0
                    #self.eye_position_vert = self.eye_position_vert + int(data['value'][1]) * self.eye_position_vert / 1000
                    self.isMoving = True

    	    #Left/ Right
                if int(data['value'][0]) == 0:
                    self.bot.stop_wheels_lr()
                    self.left_eye_position_horiz = 0.175 # add to this one
                    self.right_eye_position_horiz = 0.70 # add to this one
                    self.is_moving_right = False
                    self.is_moving_left = False
                    self.isMoving = False
                # Right
                elif int(data['value'][0]) > 0:
                    servoVal = 5900 - int(data['value'][0]) * (17)
                    self.bot.turn_lr(servoVal) 
                    if(servoVal < 5500 or servoVal > 6300):
                        self.left_eye_position_horiz = 0.255
                        self.right_eye_position_horiz = 0.755
                        self.is_moving_left = False
                        self.is_moving_right = True
                    elif(servoVal >= 5500 and servoVal <= 6300):
                        # gives wiggle room for eyes to look straight up/down
                        self.left_eye_position_horiz = 0.175
                        self.right_eye_position_horiz = 0.70
                        self.is_moving_right = False
                        self.is_moving_left = False
                    #self.left_eye_rotation_degree = 90
                    #self.right_eye_rotation_degree = 90
                    #self.left_eye_position_horiz = self.left_eye_position_horiz + int(data['value'][0]) * self.left_eye_position_horiz / 1000
                    #self.right_eye_position_horiz = self.right_eye_position_horiz + int(data['value'][0]) * self.right_eye_position_horiz / 1000
                    self.isMoving= True
                # Left
                elif int(data['value'][0]) < 0:
                    servoVal = 5900 + int(data['value'][0]) * (-18.75)
                    self.bot.turn_lr(int(servoVal))
                    if(servoVal < 5500 or servoVal > 6300):
                        self.left_eye_position_horiz = 0.105
                        self.right_eye_position_horiz = 0.625
                        self.is_moving_left = True
                        self.is_moving_right = False
                    elif(servoVal >= 5500 and servoVal <= 6300):
                        # gives wiggle room for eyes to look straight up/down
                        self.left_eye_position_horiz = 0.175
                        self.right_eye_position_horiz = 0.70
                        self.is_moving_right = False
                        self.is_moving_left = False
                    #self.left_eye_rotation_degree = 270
                    #self.right_eye_rotation_degree = 270
                    #self.left_eye_position_horiz = self.left_eye_position_horiz - int(data['value'][0]) * self.left_eye_position_horiz / 1000
                    #self.right_eye_position_horiz = self.right_eye_position_horiz - int(data['value'][0]) * self.right_eye_position_horiz / 1000
                    self.isMoving = True
            case "WAISTTURN": self.bot.turn_waist(servoVal)
            case "HEADUPDOWN": self.bot.head_up_down(servoVal)
            case "HEADTURN": self.bot.head_lr(servoVal)
        
    def secondMethod(self):
        counter = 1
        while(counter < 120):
            print(counter)
            counter = counter + 1
            time.sleep(.07)
    
    def ttsMethod(self):
        engine = pyttsx3.init()
        """ RATE"""
        rate = engine.getProperty('rate')   # getting details of current speaking rate
        print (rate)                        #printing current voice rate
        engine.setProperty('rate', 125)     # setting up new voice rate


        """VOLUME"""
        volume = engine.getProperty('volume')   #getting to know current volume level (min=0 and max=1)
        print (volume)                          #printing current volume level
        engine.setProperty('volume',1.0)    # setting up volume level  between 0 and 1
        
        """VOICE"""
        voices = engine.getProperty('voices')       #getting details of current voice
        engine.setProperty('voice', voices[12].id)  #changing index, changes voices. o for male, 12 for english? yes!
        #engine.setProperty('voice', voices[1].id)   #changing index, changes voices. 1 for female
        # for voice in engine.getProperty('voices'):
        #     print(voice)

        engine.say("Hello World!")
        engine.say('My current speaking rate is ' + str(rate))
        engine.say("Buddha bellowed bitterly biting boggart bits belatedly")
        engine.runAndWait()
        engine.stop()
        
        
    
    def mainThread(self):
        self.windowUpdate()
        time.sleep(.015)
        self.window.mainloop()
        
    def otherMainThread(self):
        self.window2.mainloop()
        
    def flaskTest(self):
      app = Flask(__name__, template_folder="templates")
      controller.main()
      #personality.main()
      @app.route("/")
      def hello():
          return render_template("webpage.html")

      @app.route("/process", methods = ["post"])
      def receive():
        data = request.get_json()
        print(data)
        # working:
        #controller.find(data)
        # also working now! can access data locally much easier:
        self.newFind(data)
        #personality.find(data)
        return data

      app.run(host="0.0.0.0")
        
inst = guiTests()

# try:
#     _thread.start_new_thread(inst.mainThread,())
# except:
#    print ("Error: unable to start thread")
try:
    t2 = threading.Thread(target= inst.flaskTest, args= ())
    t2.start()
except:
    print ("Error: unable to start thread")
try:
    #t3 = threading.Thread(target= client.main, args= ())
    t3 = threading.Thread(target= inst.ttsMethod, args= ())
    t3.start()
    print("Client thread should have started")
except:
    print ("Error: unable to start thread")
# try:
#     t0= threading.Thread(target= inst.otherMainThread, args= ())
#     t0.start()
# except:
#     print ("Error: unable to start thread")
# try:
#     t1 = threading.Thread(target= inst.mainThread, args= ())    
#     t1.start()
# except:
#     print ("Error: unable to start thread")
    

#inst.otherMainThread()

inst.mainThread()

    # if __name__ == "__main__":
    #     main(self)
