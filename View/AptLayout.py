import tkinter as tk
from PIL import Image, ImageTk, ImageEnhance
from model.observer import Observer
from View.time_slider import TimeSlider
from model.schedule import Schedule
from datetime import time
from model.events.lamp_action import LampAction
import os


class AptLayout(Observer):
    def __init__(self, parent, controller : TimeSlider, schedule : Schedule):
        super().__init__()
        self._controller = controller
        self.schedule = schedule

        self.processed_events = set()

        # Darkness intensity
        self.DARKNESSINTENSITY = 0.5
        self.BRIGHTNESSINTENSITY = 1.0
        
        # Image directory (cross-platforms path)
        image_dir = os.path.join("Images")

        # Apartment layout image
        self.original_image = Image.open(os.path.join(image_dir, "AptLayout.png"))

        # Resizing the layout image
        aspect_ratio = self.original_image.width / self.original_image.height
        new_height = 380
        new_width = int(aspect_ratio * new_height)
        self.original_image = self.original_image.resize((new_width, new_height))

        self.modified_image = self.original_image.copy()

        # Coordinate for rooms in the layout
        self.room_coordinates = {
            "bedroom" : (128, 29, 192, 153),
            "livingroom" : (90, 158, 192, 309),
            "kitchen" : (26, 158, 90, 309),
            "bathroom" : (26, 29, 90, 153),
            "hall" : (95, 29, 127, 153)
        }
        
        #Intial state of all rums (Dark)
        self.room_state = {
            "bedroom" : False,
            "livingroom" : False,
            "kitchen" : False,
            "bathroom" : False,
            "hall" : False
        }

        self.display_layout(parent)
        
    # Method that make room dark
    def darken_rooms(self, coordinate):
        room_image = self.aptLayoutPic.crop(coordinate)
        room_dark = ImageEnhance.Brightness(room_image).enhance(self.darknessIntensity)
        self.aptLayoutPic.paste(room_dark, coordinate)

    # Method to adjust the brightness of a room
    def adjust_room_brightness(self, coordinate, brightness):
        room_image = self.original_image.crop(coordinate)
        room_adjusted = ImageEnhance.Brightness(room_image).enhance(brightness)
        self.modified_image.paste(room_adjusted, coordinate)

    # Method to apply brightness to all rooms
    def apply_all_brightness(self, room_name):
        if room_name in self.room_coordinates:
            coordinate = self.room_coordinates[room_name]
            brightness = self.BRIGHTNESSINTENSITY if self.room_state[room_name] else self.DARKNESSINTENSITY
            self.adjust_room_brightness(coordinate, brightness)


    # Method to make all the room dark initially
    def update_initial_brightness(self):
        self.modified_image = self.original_image.copy()  
        for room in self.room_state:  
            self.apply_all_brightness(room)
        self.update_display()

    # Method to toggle between darkness and light
    def toggle_rooms_state(self, room_name, action):
        if room_name in self.room_coordinates:
            if action == LampAction.ON:
                if not self.room_state[room_name]:
                    self.room_state[room_name] = True
                    print(f"Turning on {room_name.capitalize()}")
            elif action == LampAction.OFF:
                if self.room_state[room_name]:
                    self.room_state[room_name] = False
                    print(f"Turning off {room_name.capitalize()}")

            self.modified_image = self.original_image.copy()
            self.apply_all_brightness(room_name)

            for room in self.room_state:
                self.apply_all_brightness(room)

            self.update_display()
        else:
            print(f"Room {room_name} not found.")

    # Method to check the events
    def check_events(self):
        current_time = time(self.current_hours, self.current_minutes)

        for event in self.schedule.events:
            event_time = event.timestamp.time()

            if self.time_within_tolerance(current_time, event_time):
                print(f"Toggling {event.lamp} at {self.current_hours:02}:{self.current_minutes:02} with action {event.action}")
                self.toggle_rooms_state(event.lamp, event.action)
                self.processed_events.add(event_time)
    
    # Method to check if the current time is within the tolerance
    def time_within_tolerance(self, current_time : time, event_time : time, tolerance_minutes = 1):

        current_total_minutes = current_time.hour * 60 + current_time.minute
        event_total_minutes = event_time.hour * 60 + event_time.minute

        time_diff = abs(current_total_minutes - event_total_minutes)

        if time_diff > 720:
            time_diff = 1440 - time_diff
        
        return time_diff <= tolerance_minutes
    
    # Method to update the observer
    def notify(self):
        self.current_hours = int(self._controller.get_hours())
        self.current_minutes = int(self._controller.get_minutes())

        print(f"Update time in AptLayout: {self.current_hours:02}:{self.current_minutes:02}")
        self.check_events()
        
    # Method to update display
    def update_display(self):
        self.aptLayout = ImageTk.PhotoImage(self.modified_image)
        self.aptLayoutLabel.configure(image = self.aptLayout)
        self.aptLayoutLabel.image_names = self.aptLayout

        # Method to put the picture on the main frame
    def display_layout(self, parent):
        self.aptLayout = ImageTk.PhotoImage(self.modified_image)
        self.aptLayoutLabel = tk.Label(parent, image = self.aptLayout)
        self.aptLayoutLabel.grid(row=1,column=1,sticky="E", padx=20, pady=50)