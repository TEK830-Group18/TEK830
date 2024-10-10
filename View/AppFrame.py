import tkinter as tk

class AppFrame(tk.Tk):
    WIDTH = 1280
    HEIGHT = 720
    IKEA_BLUE = "#0057AD"
    IKEA_YELLOW = "#FBDA0C"
   
    def __init__(self):
        super().__init__()
        # Need the image to be kept as instance variable, otherwise garbage collection removes it.
        self.harmapa_image = tk.PhotoImage(file="Images\HÄRMAPA.png")
        self.title('HÄRMAPA')
        self.geometry(f'{AppFrame.WIDTH}x{AppFrame.HEIGHT}')
        self.configure(bg = AppFrame.IKEA_BLUE)
        self.columnconfigure(0, weight=1)
        self.columnconfigure(1, weight=1)
        self.columnconfigure(2, weight=1)
        self.columnconfigure(3, weight=1)
        
        self._title_lbl = tk.Label(image=self.harmapa_image, bg=AppFrame.IKEA_BLUE)
        self._title_lbl.place(x=0,y=0)