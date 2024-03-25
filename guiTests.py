import sys

import os

import time

import tkinter as tk

from PIL import ImageTk, Image

import _thread, threading

from flask import Flask, render_template, request

import controller

import client

# def __init__(self):
#     self.debug_text = "bitterly biting boggart bits"

class guiTests:
    
    def __init__(self):
        if os.environ.get('DISPLAY','') == '':
            print('no display found. Using :0.0')
            os.environ.__setitem__('DISPLAY', ':0.0')

        self.eye_position_vert = 0.27 # subtract from this one
        self.left_eye_position_horiz = 0.175 # add to this one
        self.right_eye_position_horiz = 0.675 # add to this one
        self.is_moving = False
        self.is_talking = False
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
    
# if os.environ.get('DISPLAY','') == '':
#     print('no display found. Using :0.0')
#     os.environ.__setitem__('DISPLAY', ':0.0')

# eye_position_vert = 0.27 # subtract from this one
# left_eye_position_horiz = 0.175 # add to this one
# right_eye_position_horiz = 0.675 # add to this one
# is_moving = False
# is_talking = False
# face_image = Image.open("Robot_Face.png")
# left_eye_image = Image.open("Robot_Eye.png")
# right_eye_image = Image.open("Robot_Eye.png")
# talking_left_image = Image.open("Robot_Talking_Symbol.png")
# talking_right_image = Image.open("Robot_Talking_Symbol.png")
# moving_left_image = Image.open("Robot_Moving_Symbol.png")
# moving_right_image = Image.open("Robot_Moving_Symbol.png")
# text_background_image = Image.open("Robot_Text_Background.png")
# testing_text = "bitterly biting boggart bits"
# window = tk.Tk()
# window.after(1500, lambda: window.attributes('-fullscreen', True))
# width = window.winfo_screenwidth()
# height = window.winfo_screenheight()
# window.geometry("%dx%d" % (width, height))
# face_image = face_image.resize((round(0.99*width), round(0.99*height)))

# background = ImageTk.PhotoImage(face_image)
# background_label = tk.Label(image=background, borderwidth=0)
# background_label.image = background
# background_label.place(x=0, y=0)

# left_eye_image = left_eye_image.resize((round(0.10*width), round(0.25*height)))
# left_eye = ImageTk.PhotoImage(left_eye_image)
# left_eye_label = tk.Label(image=left_eye, borderwidth=0)
# left_eye_label.image = left_eye
# left_eye_label.place(x=round(0.175*width), y=round(0.27*height))

# right_eye_image = right_eye_image.resize((round(0.10*width), round(0.25*height)))
# right_eye = ImageTk.PhotoImage(right_eye_image)
# right_eye_label = tk.Label(image=right_eye, borderwidth=0)
# right_eye_label.image = right_eye
# right_eye_label.place(x=round(0.70*width), y=round(0.27*height))

# talking_left_image = talking_left_image.resize((round(0.10*width), round(0.25*height)))
# talking_left = ImageTk.PhotoImage(talking_left_image)
# talking_left_label = tk.Label(image=talking_left, borderwidth=0)
# talking_left_label.image = talking_left
# talking_left_label.place(x=round(1.5*width), y=round(1.5*height))

# talking_right_image = talking_right_image.resize((round(0.10*width), round(0.25*height)))
# talking_right = ImageTk.PhotoImage(talking_right_image)
# talking_right_label = tk.Label(image=talking_right, borderwidth=0)
# talking_right_label.image = talking_right
# talking_right_label.place(x=round(1.5*width), y=round(1.5*height))

# moving_left_image = moving_left_image.resize((round(0.10*width), round(0.25*height)))
# moving_left = ImageTk.PhotoImage(moving_left_image)
# moving_left_label = tk.Label(image=moving_left, borderwidth=0)
# moving_left_label.image = moving_left
# moving_left_label.place(x=round(1.5*width), y=round(1.5*height))

# moving_right_image = moving_right_image.resize((round(0.10*width), round(0.25*height)))
# moving_right = ImageTk.PhotoImage(moving_right_image)
# moving_right_label = tk.Label(image=moving_right, borderwidth=0)
# moving_right_label.image = moving_right
# moving_right_label.place(x=round(1.5*width), y=round(1.5*height))

# text_background = ImageTk.PhotoImage(text_background_image)
# #text_background_label = tk.Label(window, text=text, image=text_background, borderwidth=0, compound='center')
# text_background_label = tk.Label(window, text=testing_text, font=('Arial', 28), borderwidth=0)
# text_background_label.image = text_background
# text_background_label.pack()
# text_background_label.place(x=round(0.10*width), y=round(0.855*height))

    def windowUpdate(self):
        is_talking = True
        #global testing_text
        #global window
        input_text = self.testing_text + " b"
        self.testing_text = input_text
        #self.text_background = ImageTk.PhotoImage(self.text_background_image)
        #self.text_background_label = tk.Label(self.window, text=self.text, image=self.text_background, borderwidth=0, compound='center')
        self.text_background_label = tk.Label(self.window, text=input_text, font=('Arial', 22), borderwidth=0)
        self.text_background_label.image = self.text_background
        #text_background_label.pack()
        self.text_background_label.place(x=round(0.10*self.width), y=round(0.855*self.height))
        self.window.after(330, self.windowUpdate)
        
    def secondMethod(self):
        counter = 1
        while(counter < 120):
            print(counter)
            counter = counter + 1
            time.sleep(.07)
    
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
        controller.find(data)
        #personality.find(data)
        return data

      app.run(host="0.0.0.0")
        
inst = guiTests()

# try:
#     _thread.start_new_thread(inst.mainThread,())
# except:
#    print ("Error: unable to start thread")
# try:
#     _thread.start_new_thread(inst.secondMethod,())
# except:
#     print ("Error: unable to start thread")
try:
    t3 = threading.Thread(target= inst.flaskTest, args= ())
    t3.start()
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