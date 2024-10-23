import json
from typing import List
import View.AptLayout as AptView
from View.time_slider import TimeSlider
from model.abstract_model import Model
from model.abstract_timer import ATimer
from model.algorithm.abstract_mimicking_algorithm import MimickingAlgorithm
from model.events.lamp_event import LampEvent
from model.schedule import Schedule
from datetime import datetime, time
import time as t
from model.events.lamp_action import LampAction

class DemoModel(Model):
    def __init__(self, scheduler : MimickingAlgorithm, timer: ATimer):
        self.timer = timer
        self.scheduler = scheduler
        self.schedule = self.get_user_schedule()
        self.active_lamps_list = self.create_active_lamp_list()
        self.currently_active_lamps = []
        self.last_checked_minutes = None
        self.current_hours = 0
        self.current_minutes = 0
        self.current_time = datetime.now().replace(hour=0,minute=0,second=0)
        self.observers = []
        self.prev_time = datetime.now().replace(hour=0,minute=0,second=0)

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
        self.timer.start()
        self.timer.set_time(datetime.now().replace(hour=0,minute=0,second=0))

    def stop(self):
        self.timer.stop()

    def get_time(self):
        return self.timer.get_time()
        
    def set_time(self, time):
        time_int = time.hour * 60 + time.minute
        prev_active_lamps = self.currently_active_lamps
        self.timer.set_time(time)
        self.currently_active_lamps = self.active_lamps_list[time_int]
        
        if prev_active_lamps != self.currently_active_lamps:
            # if statement to see if user jumped forwards or backwards in time
            if self.prev_time <= time:
                lamps_to_update = list(set(self.currently_active_lamps) - set(prev_active_lamps))
                for lamp in lamps_to_update:
                    # if lamp from the difference is in the active lamps list, turn it on and vice verca
                    if lamp in self.currently_active_lamps:
                        self.publish_lamp_event(time,lamp,LampAction.ON)
                    else:
                        self.publish_lamp_event(time,lamp,LampAction.OFF)
            else:
                lamps_to_update = list(set(prev_active_lamps) - set(self.currently_active_lamps))
                for lamp in lamps_to_update:
                    if lamp not in self.currently_active_lamps:
                        self.publish_lamp_event(time,lamp,LampAction.OFF)
                    else:
                        self.publish_lamp_event(time,lamp,LampAction.ON)
        self.prev_time = time
        
    def publish_lamp_event(self, time : datetime, lamp_name : str, action : LampAction):
        event = LampEvent(time,lamp_name,action)
        print(f"Lamp {lamp_name} is {action.value}")
        self.publish(event)

    def publish(self, event):
        for o in self.observers:
            o.notify(event)

    def add_observer(self, observer):
        self.observers.append(observer)

    def remove_observer(self, observer):
        self.observers.remove(observer)

    def notify_observers(self):
        raise NotImplementedError

    def mainloop(self):
        self.start()
        # self.current_time = self.get_time()
        # lamps_to_update = []
        # while True:
        #     if self.current_time.minute > self.prev_time.minute and self.currently_active_lamps != self.active_lamps_list[self.current_time.minute]:
        #         if self.self.currently_active_lamps > self.active_lamps_list[self.current_time.minute]:
        #             lamps_to_update = list(set(self.currently_active_lamps) - set(self.active_lamps_list[self.current_time.minute]))

    def get_schedule(self):
        raise NotImplementedError

    def get_user_schedule(self):
        #TODO how to change schedule
        user_data = "tools\mock_user_data.json"
        user_events = self.read_data(user_data)
        user_schedule = Schedule.createSchedule(user_events)     
        return user_schedule
    
    def create_active_lamp_list(self) -> List[List[str]]:
        events = self.schedule.events[:]
        
        active_lamps = [[] for _ in range(1440)]
        
        checked_lamps = []
        
        for e in events:
            lamp_name = e.lamp
            for e2 in events:
                event_timestamp = e2.timestamp.hour * 60 + e2.timestamp.minute
                if e2.lamp == lamp_name and not lamp_name not in checked_lamps :
                    for i in range(event_timestamp,1440):
                        if e2.action.value == "on" and lamp_name not in active_lamps[i]:
                            active_lamps[i].append(lamp_name)
            checked_lamps.append(e.lamp)
                
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
