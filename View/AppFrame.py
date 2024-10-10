import tkinter as tk

class AppFrame(tk.Tk):
    WIDTH = 1280
    HEIGHT = 720
    IKEA_BLUE = "#0057AD"
    IKEA_YELLOW = "#FBDA0C"
   
    def __init__(self):
        super().__init__()
        # Need the image to be kept as instance variable, otherwise garbage collection removes it.
        self._harmapa_image = tk.PhotoImage(file="Images\HÄRMAPA.png")
        self.title('HÄRMAPA')
        self.configure(bg = AppFrame.IKEA_BLUE)
        
        # for centering screen
        self._screen_width = self.winfo_screenwidth()
        self._screen_height = self.winfo_screenheight()
        
        # for centering screen
        self._x = int((self._screen_width/2) - (AppFrame.WIDTH/2))
        self._y = int((self._screen_height/2) - (AppFrame.HEIGHT/2))
        
        self.geometry(f'{AppFrame.WIDTH}x{AppFrame.HEIGHT}+{self._x}+{self._y}')
        
        # for centering widgets
        self.columnconfigure(0, weight=1)
        self.columnconfigure(1, weight=1)
        self.columnconfigure(2, weight=1)
        self.columnconfigure(3, weight=1)
        
        self._title_lbl = tk.Label(image=self._harmapa_image, bg=AppFrame.IKEA_BLUE)
        self._title_lbl.place(x=0,y=0)