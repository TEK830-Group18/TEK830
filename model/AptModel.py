import View.demoModel as AptView
from View.time_slider import TimeSlider
from model.schedule import Schedule
from datetime import time
from model.events.lamp_action import LampAction

class AptModel:
    def __init__(self, schedule : Schedule, time_slider : TimeSlider):
        self.schedule = schedule
        self.timeSlider = time_slider
        self.last_checked_minutes = None
        self.current_hours = 0
        self.current_minutes = 0

        self.room_states = {
            "bedroom" : False,
            "livingroom" : False,
            "kitchen" : False,
            "bathroom" : False,
            "hall" : False
        }

        self.processed_events = set()

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


    # Toggle room states
    def toggle_rooms_state(self, room_name, action):
        if room_name in self.room_coordinates:
            current_state = self.room_states[room_name]

            if action == LampAction.ON and not current_state:
                self.room_states[room_name] = True
                print(f"Turning on {room_name.capitalize()}")

            elif action == LampAction.OFF and current_state:
                self.room_states[room_name] = False
                print(f"Turning off {room_name.capitalize()}")
    

    # Method to check the events
    def check_events(self):
        current_time = time(self.current_hours, self.current_minutes)

        for event in self.schedule.events:
            event_time = event.timestamp.time()
            
            if self.time_within_tolerance(current_time, event_time):
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
    
    def notify(self):
        self.current_hours = int(self.timeSlider.get_hours())
        self.current_minutes = int(self.timeSlider.get_minutes())
        self.current_time = time(self.current_hours, self.current_minutes)

        if self.last_checked_minutes != self.current_minutes:
            self.current_hours = self.current_hours
            self.current_minutes = self.current_minutes
            self.check_events()
            self.last_checked_minutes = self.current_minutes
            self.timeSlider.notify_observers()
