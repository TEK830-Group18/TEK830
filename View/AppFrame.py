import customtkinter as ctk
from PIL import Image

class AppFrame(ctk.CTk):
    IKEA_BLUE = "#0057AD"
    IKEA_YELLOW = "#FBDA0C"
   
    def __init__(self):
        super().__init__()
        # Need the image to be kept as instance variable, otherwise garbage collection removes it.
        self._image = Image.open("Images\HÄRMAPA.png")
        image_width, image_height = self._image.size
        self._harmapa_image = ctk.CTkImage(self._image, size=(image_width-20, image_height-10))
        self.title('HÄRMAPA')
        self.configure(fg_color = AppFrame.IKEA_BLUE)
        
        self.window_height = 720
        self.window_width = 1280
        
        # For centering screen
        self.screen_width = self.winfo_screenwidth()
        self.screen_height = self.winfo_screenheight()

        # Calculate the center position
        self.x = (self.screen_width // 2) - (self.window_width // 2)
        self.y = (self.screen_height // 2) - (self.window_height // 2)

        # Set the geometry to center the window
        self.geometry(f"{self.window_width}x{self.window_height}+{self.x}+{self.y}")
        
        # for centering widgets
        self.columnconfigure(0, weight=1)
        self.columnconfigure(1, weight=1)
        self.columnconfigure(2, weight=1)
        self.columnconfigure(3, weight=1)
        
        self.rowconfigure(0, weight=1)
        # self.rowconfigure(1, weight=1)
        # self.rowconfigure(2, weight=1)
        # self.rowconfigure(3, weight=1)
        # self.rowconfigure(4, weight=1)
        # self.rowconfigure(5, weight=1)
        self.rowconfigure(6, weight=1)
        
        self._title_lbl = ctk.CTkLabel(self, image=self._harmapa_image, fg_color=AppFrame.IKEA_BLUE, text="")
        self._title_lbl.configure(width=image_width-20, height=image_height-10)
        self._title_lbl.place(x=20,y=10)