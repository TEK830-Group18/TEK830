import tkinter as tk

class AppFrame(tk.Tk):
    IKEA_BLUE = "#0057AD"
    IKEA_YELLOW = "#FBDA0C"
   
    def __init__(self):
        super().__init__()
        # Need the image to be kept as instance variable, otherwise garbage collection removes it.
        self._harmapa_image = tk.PhotoImage(file="Images\HÄRMAPA.png")
        self.title('HÄRMAPA')
        self.configure(bg = AppFrame.IKEA_BLUE)
        
        self._screen_width = self.winfo_screenwidth()
        self._screen_height = self.winfo_screenheight()
        
        self.geometry(f'{self._screen_width}x{self._screen_height}')
        
        # for centering widgets
        self.columnconfigure(0, weight=1)
        self.columnconfigure(1, weight=1)
        self.columnconfigure(2, weight=1)
        self.columnconfigure(3, weight=1)
        
        self._title_lbl = tk.Label(image=self._harmapa_image, bg=AppFrame.IKEA_BLUE)
        self._title_lbl.place(x=0,y=0)