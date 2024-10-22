import json
from typing import List
import View.AptLayout as AptView
from View.time_slider import TimeSlider
from model.abstract_model import Model
from model.abstract_timer import Timer
from model.algorithm.abstract_mimicking_algorithm import MimickingAlgorithm
from model.events.lamp_event import LampEvent
from model.schedule import Schedule
from datetime import datetime, time
from model.events.lamp_action import LampAction

class DemoModel(Model):
    def __init__(self, scheduler : MimickingAlgorithm, timer: Timer):
        self.timer = timer
        self.scheduler = scheduler
        self.schedule = self.get_user_schedule()
        self.active_lamps_list = self.create_active_lamp_list()
        self.currectly_active_lamps = []
        self.last_checked_minutes = None
        self.current_hours = 0
        self.current_minutes = 0
        self.observers = []

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

    def start(self):
        self.timer.set_time(datetime.now().replace(hour=0,minute=0,second=0))
        self.timer.start()

    def stop(self):
        self.timer.stop()

    def get_time(self):
        self.timer.get_time()
        
    def set_time(self, time):
        time_int = time.timestamp.hour * 60 + time.timestamp.minute
        prev_active_lamps = self.currectly_active_lamps
        self.timer.set_time(time)
        self.currectly_active_lamps = self.active_lamps_list[time_int]
        if prev_active_lamps != self.currectly_active_lamps:
            lamps_to_update = list(set(self.currectly_active_lamps) - set(prev_active_lamps))
            for lamp in lamps_to_update:
                event = LampEvent(time,lamp,"ON")
                self.publish(event)

    def add_observer(self, observer):
        self.observers.append(observer)

    def remove_observer(self, observer):
        self.observers.remove(observer)

    def notify_observers(self):
        raise NotImplementedError

    def publish(self, event):
        # when events published, notify observers
        for o in self.observers:
            o.notify(event)

    def mainloop(self):
        self.start()
        # get time and compare with schedule, publish events when neccessary.

    def get_schedule(self):
        raise NotImplementedError

    def get_user_schedule(self):
        user_data = "tools\mock_user_data.json"
        user_events = self.read_data(user_data)
        user_schedule = self.scheduler.createSchedule(user_events)     
        return user_schedule
    
    def create_active_lamp_list(self) -> List[List[str]]:
        events = self.schedule.events[:]
        
        active_lamps = [[] for _ in range(1440)]
        
        for e in events:
            lamp_name = e.lamp
            for e2 in events:
                event_timestamp = e2.timestamp.hour * 60 + e2.timestamp.minute
                if e2.lamp == lamp_name:
                    for i in range(event_timestamp,1440):
                        if e2.action == "ON":
                            active_lamps[i].append(lamp_name)
                events.remove(e2)
                
        return active_lamps
        
                
        
                        
    
    def read_data(self, path:str):
        with open(path, mode='r') as f:
            json_data = json.load(f)

            events : List[LampEvent]= []
            json_events = json_data['lamp_usage']
            for e in json_events:
                event = LampEvent.from_json(e)
                events.append(event)
        return events
    
    # Nah bruh
    def notify(self):
        self.current_hours = int(self.timeSlider.get_hours())
        self.current_minutes = int(self.timeSlider.get_minutes())
        self.current_time = time(self.current_hours, self.current_minutes)

        if self.last_checked_minutes != self.current_minutes:
            self.current_hours = self.current_hours
            self.current_minutes = self.current_minutes
            self.check_events()
            self.last_checked_minutes = self.current_minutes