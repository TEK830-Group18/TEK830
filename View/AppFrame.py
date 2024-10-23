import customtkinter as ctk
from PIL import Image
import os

from View.colors import Colors

class AppFrame(ctk.CTk):
   
    def __init__(self):
        super().__init__()
        # Need the image to be kept as instance variable, otherwise garbage collection removes it.
        image_dir = os.path.join("Images")
        self._image = Image.open(os.path.join(image_dir, "HÄRMAPA.png"))
        image_width, image_height = self._image.size
        self._harmapa_image = ctk.CTkImage(self._image, size=(image_width-20, image_height-10))
        self.title('HÄRMAPA')
        self.configure(fg_color = Colors.IKEA_BLUE.value)
        
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
        
        # for centering
        self.rowconfigure(0, weight=1)
        self.rowconfigure(6, weight=1)
        
        self._title_lbl = ctk.CTkLabel(self, image=self._harmapa_image, fg_color=Colors.IKEA_BLUE.value, text="")
        self._title_lbl.configure(width=image_width-20, height=image_height-10)
        self._title_lbl.place(x=20,y=10)