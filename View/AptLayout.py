import tkinter as tk
from PIL import Image, ImageTk, ImageEnhance
from model.abstract_event_observer import EventObserver
import model.demo_model as demo_model
import os

from model.events.lamp_action import LampAction

class AptLayout(EventObserver):
    def __init__(self, parent, model : demo_model):
        self.model = model
        
        # Image directory and new height
        IMAGE_DIR = os.path.join("Images")
        IMAGE_NAME = "AptLayout.png"
        NEW_HEIGHT = 380

        self.room_states = {
            "bedroom" : False,
            "livingroom" : False,
            "kitchen" : False,
            "bathroom" : False,
            "hall" : False
        }

        self.DARKNESSINTENSITY = 0.5
        self.BRIGHTNESSINTENSITY = 1.0

        # Coordinate for rooms in the layout
        self.room_coordinates = {
            "bedroom" : (128, 29, 192, 153),
            "livingroom" : (90, 158, 192, 309),
            "kitchen" : (26, 158, 90, 309),
            "bathroom" : (26, 29, 90, 153),
            "hall" : (95, 29, 127, 153)
        }
        # Apartment layout image
        self.original_image = Image.open(os.path.join(IMAGE_DIR, IMAGE_NAME))

        # Resizing the layout image
        aspect_ratio = self.original_image.width / self.original_image.height
        new_width = int(aspect_ratio * NEW_HEIGHT)
        self.original_image = self.original_image.resize((new_width, NEW_HEIGHT))
        self.modified_image = self.original_image.copy()

        self.display_layout(parent)
        self.update_initial_brightness()
 
    # Method to make all the room dark initially
    def update_initial_brightness(self):
        self.modified_image = self.original_image.copy()  
        for room in self.room_states:  
            self.apply_all_brightness(room)
        self.update_display()
    
    # Method to apply darkness or brightness to the room
    def darken_rooms(self, room_name):
        if room_name in self.room_coordinates:
            coordinate = self.room_coordinates[room_name]
            room_image = self.original_image.crop(coordinate)
            room_dark = ImageEnhance.Brightness(room_image).enhance(self.DARKNESSINTENSITY)
            self.modified_image.paste(room_dark, coordinate)

    # Method to apply brightness to the room
    def apply_all_brightness(self, room_name):
        if room_name in self.room_coordinates:
            coordinate = self.room_coordinates[room_name]
            brightness = (
                self.BRIGHTNESSINTENSITY if self.room_states[room_name]
                else self.DARKNESSINTENSITY
            )
            self.adjust_room_brightness(coordinate, brightness)

    # Method to adjust room brightness
    def adjust_room_brightness(self, coordinate, brightness):
        room_image = self.original_image.crop(coordinate)
        room_adjusted = ImageEnhance.Brightness(room_image).enhance(brightness)
        self.modified_image.paste(room_adjusted, coordinate)

    # Method to toggle room states
    def toggle_rooms_state(self, room_name, action : str):
        if room_name in self.room_coordinates:
            current_state = self.room_states[room_name]

        if action == LampAction.ON.value and not current_state:
            self.room_states[room_name] = True

        elif action == LampAction.OFF.value and current_state:
            self.room_states[room_name] = False
    
        self.update_layout()

    # Method to update the layout
    def update_layout(self):
        self.modified_image = self.original_image.copy()
        for room in self.room_states:
            self.apply_all_brightness(room)
        self.update_display()

    # Method to update display
    def update_display(self):
        self.aptLayout = ImageTk.PhotoImage(self.modified_image)
        self.aptLayoutLabel.configure(image = self.aptLayout)
        self.aptLayoutLabel.image_names = self.aptLayout

    # Method to update the display
    def display_layout(self, parent):
        self.aptLayout = ImageTk.PhotoImage(self.modified_image)
        self.aptLayoutLabel = tk.Label(parent, image = self.aptLayout)
        self.aptLayoutLabel.grid(row=1,column=1,sticky="E", padx=20, pady=50)

    # Method to update the observer
    def notify(self, event):
        self.toggle_rooms_state(event.lamp, event.action.value)
        self.update_display()