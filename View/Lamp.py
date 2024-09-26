import tkinter as tk
from PIL import Image, ImageTk
import os



class Lamp:
    def __init__(self, parent):

        # Current state
        self.currentState = "OFF"

        # Image directory (cross-platforms path)
        image_dir = os.path.join("Images")


        # Bulb OFF image + resizing
        bulbOFF_image = Image.open(os.path.join(image_dir, "OFF.png")) 
        bulbOFF_resized = bulbOFF_image.resize((300, 350))  
        self.bulbOFF = ImageTk.PhotoImage(bulbOFF_resized)  

        # Bulb ON image + resizing
        bulbON_image = Image.open(os.path.join(image_dir, "ON.png"))
        bulbON_resized = bulbON_image.resize((300, 350))  
        self.bulbON = ImageTk.PhotoImage(bulbON_resized)

        # OFF Switch image + resizing
        offPic_image = Image.open(os.path.join(image_dir, "SWITCHOFF.png"))
        offPic_resized = offPic_image.resize((120, 150))  
        self.offPic = ImageTk.PhotoImage(offPic_resized)
        
        # ON switch image + resizing
        onPic_image = Image.open(os.path.join(image_dir, "SWITCHON.png"))
        onPic_resized = onPic_image.resize((120, 150))  
        self.onPic = ImageTk.PhotoImage(onPic_resized)


        # Switch ON and OFF handler
        self.btnToggle = tk.Button(parent, image = self.offPic, bd = 0, bg = "white", command = self.clickHandler)
        self.btnToggle.place(x = 500, y = 150)
        
        # Light blulb ON and OFF handler
        self.labelBulb = tk.Label(parent, image = self.bulbOFF, bg = "white")
        self.labelBulb.place(x = 20, y = 20)


    def clickHandler(self):

        if self.currentState == "OFF":
            self.currentState = "ON"
            self.btnToggle.config(image = self.onPic)
            self.labelBulb.config(image = self.bulbON)

        else:
            self.currentState = "OFF"
            self.btnToggle.config(image = self.offPic)
            self.labelBulb.config(image = self.bulbOFF)