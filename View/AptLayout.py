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
        self.darknessIntensity = 0.4
        
        # Image directory (cross-platforms path)
        image_dir = os.path.join("Images")

        # Apartment layout image
        self.aptLayoutPic = Image.open(os.path.join(image_dir, "AptLayout.png"))

        # Resizing the layout image
        aspect_ratio = self.aptLayoutPic.width / self.aptLayoutPic.height
        new_height = 380
        new_width = int(aspect_ratio * new_height)
        self.aptLayoutPic = self.aptLayoutPic.resize((new_width, new_height))

        # Coordinate for rooms in the layout
        self.room_coordinations = {
            "bedroom" : (128, 29, 192, 153),
            "livingroom" : (90, 158, 192, 309),
            "kitchen" : (26, 158, 90, 309),
            "bathroom" : (26, 29, 90, 153),
            "hall" : (95, 29, 127, 153)
        }
        
        
        # Intial state of all rums (Dark)
        # self.room_state = {
        #     room: False for room in self.room_coordinations
        # }

        # Initial state of rooms
        initial_state = {
            "bedroom" : False,
            "livingroom" : False,
            "kitchen" : False,
            "bathroom" : False,
            "hall" : False
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
                room_name = event.lamp
                action = event.action
                print(f"Toggling {room_name}: {action} at {current_time}")

                if action == "on" and not self.room_state[room_name]:
                    print(f"Turning ON {room_name} at {current_time}")
                    self.toggle_rooms(room_name)
                    
                elif action == "off" and self.room_state[room_name]:
                    print(f"Turning OFF {room_name} at {current_time}")
                    self.toggle_rooms(room_name)



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