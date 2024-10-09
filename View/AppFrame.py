import tkinter as tk

class AppFrame(tk.Tk):
    def __init__(self):
        super().__init__()
        self.title('HÄRMAPA')
        self.geometry('1280x720')
        self.configure(bg = "#0057AD")
        
