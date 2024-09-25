import tkinter as tk



class Lamp:
    def __init__(self, parent):


        # Bulbs
        self.bulbOFF = tk.PhotoImage(file = "TEK830/Images/OFF.png")
        self.bulbON = tk.PhotoImage(file = "TEK830/Images/ON.png")

        # Swithces
        self.offPic = tk.PhotoImage(file = "TEK830/Images/SWITCHOFF.png")
        self.btnOFF = tk.Button(parent, image = self.offPic, bd = 0, bg = "white")
        self.btnOFF.pack(padx=50, pady= 50)

        self.onPic = tk.PhotoImage(file = "TEK830/Images/SWITCHON.png")
        self.btnON = tk.Button(parent, image = self.onPic, bd = 0, bg = "white")
        self.btnON.pack(padx=50, pady= 50)



