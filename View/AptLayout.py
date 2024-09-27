import tkinter as tk
from PIL import Image, ImageTk, ImageEnhance
import os


class AptLayout:
    def __init__(self, parent):

        # Darkness intensity
        self.darknessIntensity = 0.4
        
        # Image directory (cross-platforms path)
        image_dir = os.path.join("Images")

        # Apartment layout image
        self.aptLayoutPic = Image.open(os.path.join(image_dir, "AptLayout.png"))

        # Resizing the layout image
        aspect_ratio = self.aptLayoutPic.width / self.aptLayoutPic.height
        old_width, old_height = self.aptLayoutPic.size
        new_height = 380
        new_width = int(aspect_ratio * new_height)
        self.aptLayoutPic = self.aptLayoutPic.resize((new_width, new_height))

        # Scaling factors 
        self.scale_width = new_width / old_width
        self.scale_height = new_height / old_height

        # Coordinate for rooms in the layout
        self.room_coordinations = {
            "bedroom" : (128, 29, 192, 153),
            "livingroom" : (90, 158, 192, 309),
            "kitchen" : (26, 158, 90, 309),
            "bathroom" : (26, 29, 90, 153),
            "hall" : (95, 29, 127, 153)
        }
        
        # Intial state of all rums (Dark)
        self.room_state = {
            room: True for room in self.room_coordinations
        }

        for room, coordinate in self.room_coordinations.items():
            self.darken_rooms(coordinate)
        self.display_layout(parent)

    # Method that make room dark
    def darken_rooms(self, coordinate):
        room_image = self.aptLayoutPic.crop(coordinate)
        room_dark = ImageEnhance.Brightness(room_image).enhance(self.darknessIntensity)
        self.aptLayoutPic.paste(room_dark, coordinate)

    # Method that turn on the light
    def brighten_rooms(self, coordinate):
        old_image = Image.open(os.path.join("Images", "AptLayout.png"))
        old_room_image = old_image.crop(coordinate)
        self.aptLayoutPic.paste(old_room_image, coordinate)

    # Method to toggle between darkness and light
    def toggle_rooms(self, room_name):
        if room_name in self.room_coordinations:
            coordinate = self.room_coordinations[room_name]

            if self.room_state[room_name]:
                self.brighten_rooms(coordinate)
            else:
                self.darken_rooms(coordinate)

            # Toggle between states
            self.room_state[room_name] = not self.room_state[room_name]

            # Update the display image
            self.update_display()

        else:
            print(f"Room {room_name} not found.")
    
    # Method to update display
    def update_display(self):
        self.aptLayout = ImageTk.PhotoImage(self.aptLayoutPic)
        self.aptLayoutLabel.configure(image = self.aptLayout)
        self.aptLayoutLabel.image_names = self.aptLayout

    # Method to put the picture on the main frame
    def display_layout(self, parent):
        self.aptLayout = ImageTk.PhotoImage(self.aptLayoutPic)
        self.aptLayoutLabel = tk.Label(parent, image = self.aptLayout)
        self.aptLayoutLabel.pack()
        self.aptLayoutLabel.place(x = 20, y = 10)