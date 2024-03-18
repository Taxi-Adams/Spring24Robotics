import time

import tkinter as tk

import client

from PIL import ImageTk, Image

from tango import Tango

#bot = Tango()
eye_position_vert = 0.27 # subtract from this one
left_eye_position_horiz = 0.175 # add to this one
right_eye_position_horiz = 0.675 # add to this one
is_moving = False
is_talking = False
face_image = Image.open("Robot_Face.png")
left_eye_image = Image.open("Robot_Eye.png")
right_eye_image = Image.open("Robot_Eye.png")
talking_left_image = Image.open("Robot_Talking_Symbol.png")
talking_right_image = Image.open("Robot_Talking_Symbol.png")
moving_left_image = Image.open("Robot_Moving_Symbol.png")
moving_right_image = Image.open("Robot_Moving_Symbol.png")
text_background_image = Image.open("Robot_Text_Background.png")
text = "bitterly biting boggart bits"
window = tk.Tk()
width = window.winfo_screenwidth()
height = window.winfo_screenheight()
window.geometry("%dx%d" % (width, height))
face_image = face_image.resize((round(0.99*width), round(0.99*height)), Image.ANTIALIAS)

background = ImageTk.PhotoImage(face_image)
background_label = tk.Label(image=background, borderwidth=0)
background_label.image = background
background_label.place(x=0, y=0)

left_eye = ImageTk.PhotoImage(left_eye_image)
left_eye_label = tk.Label(image=left_eye, borderwidth=0)
left_eye_label.image = left_eye
left_eye_label.place(x=round(0.175*width), y=round(0.27*height))

right_eye = ImageTk.PhotoImage(right_eye_image)
right_eye_label = tk.Label(image=right_eye, borderwidth=0)
right_eye_label.image = right_eye
right_eye_label.place(x=round(0.675*width), y=round(0.27*height))

talking_left = ImageTk.PhotoImage(talking_left_image)
talking_left_label = tk.Label(image=talking_left, borderwidth=0)
talking_left_label.image = talking_left
talking_left_label.place(x=round(1.5*width), y=round(1.5*height))

talking_right = ImageTk.PhotoImage(talking_right_image)
talking_right_label = tk.Label(image=talking_right, borderwidth=0)
talking_right_label.image = talking_right
talking_right_label.place(x=round(1.5*width), y=round(1.5*height))

moving_left = ImageTk.PhotoImage(moving_left_image)
moving_left_label = tk.Label(image=moving_left, borderwidth=0)
moving_left_label.image = moving_left
moving_left_label.place(x=round(1.5*width), y=round(1.5*height))

moving_right = ImageTk.PhotoImage(moving_right_image)
moving_right_label = tk.Label(image=moving_right, borderwidth=0)
moving_right_label.image = moving_right
moving_right_label.place(x=round(1.5*width), y=round(1.5*height))

text_background = ImageTk.PhotoImage(text_background_image)
#text_background_label = tk.Label(window, text=text, image=text_background, borderwidth=0, compound='center')
text_background_label = tk.Label(window, text=text, font=('Arial', 28), borderwidth=0)
text_background_label.image = text_background
text_background_label.pack()
text_background_label.place(x=round(0.10*width), y=round(0.855*height))

def find(data: str) -> None:
    try:
        servoVal = int(data['value']) * 40 + 4000
        manipVal = int(data['value'])
        
        # get values and insert here? will it work? Copy over in the morning
        
    except: print(data)
    match data['servo']:
        case ['WHEELFORWARDBACKWARD', 'WHEELTURN']: 
        # Foward/ Backward
            if int(data['value'][1]) == 0:
                is_moving = False
                eye_position_vert = 0.27 # subtract from this one
                #bot.stop_wheels_fb()
                #print(int(data['value'][1]))
            # Backwards
            elif int(data['value'][1]) > 0:
                is_moving = True
                eye_position_vert = eye_position_vert - int(data['value'][1]) * eye_position_vert / 10000
                #servoVal = int(data['value'][1]) * (18.75) + 5900
                #print(int(servoVal))
            # Forwards
            elif int(data['value'][1]) < 0:
                is_moving = True
                eye_position_vert = eye_position_vert + int(data['value'][1]) * eye_position_vert / 10000
                #servoVal = 5900 - int(data['value'][1]) * (-17)
                #print(servoVal)

            #Left/ Right
            if int(data['value'][0]) == 0:
                is_moving = False
                left_eye_position_horiz = 0.175 # add to this one
                right_eye_position_horiz = 0.675 # add to this one
                #bot.stop_wheels_fb()
                #print(int(data['value'][0]))
            # Right
            elif int(data['value'][0]) > 0:
                is_moving = True
                eye_position_vert = left_eye_position_horiz + int(data['value'][0]) * left_eye_position_horiz / 10000
                eye_position_vert = right_eye_position_horiz + int(data['value'][0]) * right_eye_position_horiz / 10000
                #servoVal = int(data['value'][0]) * (18.75) + 5900
                #print(int(servoVal)) 
            # Left
            elif int(data['value'][0]) < 0:
                is_moving = True
                eye_position_vert = left_eye_position_horiz - int(data['value'][0]) * left_eye_position_horiz / 10000
                eye_position_vert = right_eye_position_horiz - int(data['value'][0]) * right_eye_position_horiz / 10000
                #servoVal = 5900 - int(data['value'][0]) * (-17)
                #print(servoVal)

        case "WAISTTURN": print(servoVal)
        case "HEADUPDOWN": print(servoVal)
        case "HEADTURN": print(servoVal)
        
def windowUpdate(text: str):
    is_talking = True
    test_text = text + " b"
    #self.text_background = ImageTk.PhotoImage(self.text_background_image)
    #self.text_background_label = tk.Label(self.window, text=self.text, image=self.text_background, borderwidth=0, compound='center')
    text_background_label = tk.Label(window, text=text, font=('Arial', 28), borderwidth=0)
    text_background_label.image = text_background
    text_background_label.pack()
    text_background_label.place(x=round(0.10*width), y=round(0.855*height))
    window.after(500, windowUpdate)
    # need a way to know if talking/what the tts text is
    if(is_moving and not is_talking):
        # eyes are arrows, others off screen
        left_eye_label.place(x=round(1.5*width), y=round(1.5*height))
        right_eye_label.place(x=round(1.5*width), y=round(1.5*height))
        talking_left_label.place(x=round(1.5*width), y=round(1.5*height))
        talking_right_label.place(x=round(1.5*width), y=round(1.5*height))
        moving_left_label.place(x=round(left_eye_position_horiz*width), y=round(eye_position_vert*height))
        moving_right_label.place(x=round(right_eye_position_horiz*width), y=round(eye_position_vert*height))
    elif(is_moving and is_talking):
        # eyes are still arrows, others off screen
        left_eye_label.place(x=round(1.5*width), y=round(1.5*height))
        right_eye_label.place(x=round(1.5*width), y=round(1.5*height))
        talking_left_label.place(x=round(1.5*width), y=round(1.5*height))
        talking_right_label.place(x=round(1.5*width), y=round(1.5*height))
        moving_left_label.place(x=round(left_eye_position_horiz*width), y=round(eye_position_vert*height))
        moving_right_label.place(x=round(right_eye_position_horiz*width), y=round(eye_position_vert*height))
    elif(not is_moving and is_talking):
        # eyes are speech bubbles, others off screen
        left_eye_label.place(x=round(1.5*width), y=round(1.5*height))
        right_eye_label.place(x=round(1.5*width), y=round(1.5*height))
        talking_left_label.place(x=round(left_eye_position_horiz*width), y=round(eye_position_vert*height))
        talking_right_label.place(x=round(right_eye_position_horiz*width), y=round(eye_position_vert*height))
        moving_left_label.place(x=round(1.5*width), y=round(1.5*height))
        moving_right_label.place(x=round(1.5*width), y=round(1.5*height))
    elif(not is_moving and not is_talking):
        # display normal eyes
        left_eye_label.place(x=round(left_eye_position_horiz*width), y=round(eye_position_vert*height))
        right_eye_label.place(x=round(right_eye_position_horiz*width), y=round(eye_position_vert*height))
        talking_left_label.place(x=round(1.5*width), y=round(1.5*height))
        talking_right_label.place(x=round(1.5*width), y=round(1.5*height))
        moving_left_label.place(x=round(1.5*width), y=round(1.5*height))
        moving_right_label.place(x=round(1.5*width), y=round(1.5*height))

def main(current_text: str) -> None:
    #bot = Tango()
    #bot.stop_wheels_fb()
    #bot.stop_wheels_lr()
    print(1)
    # Should always be true
    while(eye_position_vert < 100000000):
        windowUpdate(client.current_text) # pulls current_text variable from client instance
        time.sleep(.03)
        
if __name__ == "__main__":
    main()
