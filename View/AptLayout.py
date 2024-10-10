import tkinter as tk
from PIL import Image, ImageTk, ImageEnhance
from View.observer import Observer
from View.time_slider import TimeSlider
from model.scheduler import Schedule
from datetime import datetime, time
import os


class AptLayout(Observer):
    def __init__(self, parent, controller : TimeSlider, schedule : Schedule):
        super().__init__()
        self._controller = controller
        self.schedule = schedule

        # Darkness intensity
        self.DARKNESSINTENSITY = 0.4
        
        # Image directory (cross-platforms path)
        image_dir = os.path.join("Images")

        # Apartment layout image
        self.original_image = Image.open(os.path.join(image_dir, "AptLayout.png"))

        # Resizing the layout image
        aspect_ratio = self.original_image.width / self.original_image.height
        new_height = 380
        new_width = int(aspect_ratio * new_height)
        self.aptLayoutPic = self.original_image.resize((new_width, new_height))

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
            room: False for room in self.room_coordinates
        }

        # Darken all rooms
        for room, coordinate in self.room_coordinates.items():
            self.darken_rooms(coordinate)

        self.display_layout(parent)

    # Method that make room dark
    def darken_rooms(self, coordinate):
        room_image = self.aptLayoutPic.crop(coordinate)
        room_dark = ImageEnhance.Brightness(room_image).enhance(self.DARKNESSINTENSITY)
        self.aptLayoutPic.paste(room_dark, coordinate)

    # Method to toggle between darkness and light
    def toggle_rooms_state(self, room_name, action):
        if room_name in self.room_coordinates:
            coordinate = self.room_coordinates[room_name]

            if action == "on":
                if not self.room_state[room_name]:
                    self.DARKNESSINTENSITY = 1.0
                    self.darken_rooms(coordinate)
                    self.room_state[room_name] = True
                elif action == "off":
                    if self.room_state[room_name]:
                        self.DARKNESSINTENSITY = 0.4
                        self.darken_rooms(coordinate)
                        self.room_state[room_name] = False

                self.update_display()
        else:
            print(f"Room {room_name} not found.")
    
    # Method to check if the current time is within the tolerance
    def time_within_tolerance(self, current_time : datetime, event_time : datetime, tolerance_seconds = 59):
        today = datetime.today()
        current_datetime = datetime.combine(today, current_time)
        event_datetime = datetime.combine(today, event_time)
        return abs((current_datetime - event_datetime).total_seconds()) <= tolerance_seconds

    # Method to update the observer
    def notified_update(self):
        self.current_hours = self._controller.get_hours()
        self.current_minutes = self._controller.get_minutes()
        self.current_seconds = 0

        current_time = time(self.current_hours, self.current_minutes, self.current_seconds)
        print(f"Update time in AptLayout: {self.current_hours:02}:{self.current_minutes:02}:{self.current_seconds:02}")

        for event in self.schedule.events:
            event_time = event.timestamp.time()
            print(f"Event time: {event_time}, Lamp: {event.lamp}, Action: {event.action}")

            if self.time_within_tolerance(current_time, event_time):
                self.toggle_rooms_state(event.lamp, event.action)
                print(f"Toggling {event.lamp} at {current_time} with action {event.action}")

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