import tkinter as tk

class AppFrame(tk.Tk):
    def __init__(self):
        super().__init__()
        self.title('HÄRMAPA')
        self.geometry('1000x400')
        self.configure(bg = "white")
