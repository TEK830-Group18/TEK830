import json
from typing import List
import View.AptLayout as AptView
from View.time_slider import TimeSlider
from model.abstract_model import Model
from model.abstract_timer import ATimer
from model.algorithm.abstract_mimicking_algorithm import MimickingAlgorithm
from model.events.lamp_event import LampEvent
from model.schedule import Schedule
from datetime import datetime
import time as t
from model.events.lamp_action import LampAction

class DemoModel(Model):
    def __init__(self, scheduler : MimickingAlgorithm, timer: ATimer, start_time : datetime):
        self.timer = timer
        self.scheduler = scheduler
        self.user_schedule = self.get_user_schedule()
        self.algortihm_schedule = self.get_schedule()
        
        self.use_using_schedule = True
        self.current_schedule = self.user_schedule
        
        self.start_time = start_time
        self.current_hours = self.start_time.hour
        self.current_minutes = self.start_time.minute
        self.current_time = self.start_time
        self.prev_time = self.start_time
        self.observers = []

        self.current_time_in_minutes = self.current_time.hour * 60 + self.current_time.minute
            
        self.current_active_lamps_list = self.create_active_lamp_list()
        self.currently_active_lamps = self.current_active_lamps_list[self.current_time_in_minutes]
        self.prev_current_active_lamps_list = self.current_active_lamps_list

        # to turn on lamps that should be turned on, if given a start time that means that lights should be on
        for lamp in self.currently_active_lamps:
            self.publish_lamp_event(self.current_time,lamp,LampAction.ON)

    def start(self):
        self.timer.start()
        self.timer.set_time(self.start_time)

    def stop(self):
        self.timer.stop()

    def get_time(self):
        return self.timer.get_time()
        
    def set_time(self, time : datetime):
        time_int = self._get_minutes_from_datetime(time)
        prev_active_lamps = self.currently_active_lamps
        self.timer.set_time(time)
        self.currently_active_lamps = self.current_active_lamps_list[time_int]
        
        if len(self.currently_active_lamps) == 0:
            for lamp in prev_active_lamps:
                self.publish_lamp_event(time,lamp,LampAction.OFF)
        else: 
            if prev_active_lamps != self.currently_active_lamps:
                lamps_to_update = list(set(self.currently_active_lamps).symmetric_difference(set(prev_active_lamps)))
                for lamp in lamps_to_update:
                    # if lamp from the difference is in the active lamps list, turn it on and vice verca
                    if lamp in prev_active_lamps:
                        self.publish_lamp_event(time,lamp,LampAction.OFF)
                    else:
                        self.publish_lamp_event(time,lamp,LampAction.ON)
        self.prev_time = time
        
    def publish_lamp_event(self, time : datetime, lamp_name : str, action : LampAction):
        event = LampEvent(time,lamp_name,action)
        self.publish(event)

    def publish(self, event):
        for o in self.observers:
            o.notify(event)

    def add_observer(self, observer):
        self.observers.append(observer)
        for lamp in self.currently_active_lamps:
            self.publish(LampEvent(self.current_time,lamp,LampAction.ON))

    def remove_observer(self, observer):
        self.observers.remove(observer)

    def mainloop(self):
        self.start()
        while True:
            t.sleep(1)
            self.current_time = self.get_time()
            current_time_in_minutes = self._get_minutes_from_datetime(self.current_time)
            self.currently_active_lamps = self.current_active_lamps_list[current_time_in_minutes]
            
            prev_time_in_minutes = self._get_minutes_from_datetime(self.prev_time)
            prev_active_lamps = self.current_active_lamps_list[prev_time_in_minutes]
            
            lamps_to_update = []
            if self.current_time.minute > self.prev_time.minute and prev_active_lamps != self.currently_active_lamps:
                
                lamps_to_update = list(set(prev_active_lamps).symmetric_difference(set(self.current_active_lamps_list[current_time_in_minutes])))
                print(F"{lamps_to_update} are to be updated")
                
                if len(lamps_to_update) == 0:
                    for lamp in prev_active_lamps:
                        self.publish_lamp_event(self.current_time,lamp,LampAction.OFF)
                        
                for lamp in lamps_to_update:
                    # If lamp was part of active lamps then it should turn off, else on
                    if lamp in prev_active_lamps:
                        self.publish_lamp_event(self.current_time,lamp,LampAction.OFF)
                    else:
                        self.publish_lamp_event(self.current_time,lamp,LampAction.ON)
                self.prev_time = self.current_time

    def _get_minutes_from_datetime(self, time : datetime):
        return time.hour * 60 + time.minute

    def get_schedule(self):
        user_data = "tools\mock_user_data.json"
        user_events = self.read_data(user_data)
        return self.scheduler.createSchedule(user_events)
    
    def get_current_active_lights(self):
        return self.currently_active_lamps

    def get_user_schedule(self):
        user_data = "tools\mock_user_data.json"
        user_events = self.read_data(user_data)
        user_schedule = Schedule.createSchedule(user_events)     
        return user_schedule
    
    def create_active_lamp_list(self) -> List[List[str]]:
        events = self.current_schedule.events[:]
        
        active_lamps = [[] for _ in range(1440)]
        
        checked_lamps = []
        
        for e in events:
            lamp_name = e.lamp
            for e2 in events:
                event_timestamp = e2.timestamp.hour * 60 + e2.timestamp.minute
                if e2.lamp == lamp_name and not lamp_name not in checked_lamps:
                    for i in range(event_timestamp,1440):
                        if e2.action.value == "on" and lamp_name not in active_lamps[i]:
                            active_lamps[i].append(lamp_name)
                        if e2.action.value == "off" and lamp_name in active_lamps[i]:
                            active_lamps[i].remove(lamp_name)
            checked_lamps.append(e.lamp)
                
        return active_lamps
    
    def get_current_schedule(self) -> Schedule:
        return self.current_schedule
    
    def change_current_schedule(self):
        current_time_in_minutes = self._get_minutes_from_datetime(self.get_time())

        if not self.use_using_schedule:
            print("use user schedule")
            self.current_schedule = self.user_schedule
            self.publish_events_after_schedule_switch(current_time_in_minutes, self.prev_current_active_lamps_list)
            self.use_using_schedule = True
        else:
            print("use algorithm schedule")
            self.current_schedule = self.algortihm_schedule
            self.publish_events_after_schedule_switch(current_time_in_minutes, self.prev_current_active_lamps_list)
            self.use_using_schedule = False
        self.prev_current_active_lamps_list = self.current_active_lamps_list


    def publish_events_after_schedule_switch(self, current_time_in_minutes, prev_current_active_lamps_list):
        new_current_active_lamps_list = self.create_active_lamp_list()
        print(len(new_current_active_lamps_list[current_time_in_minutes]) == 0)
        print(prev_current_active_lamps_list[current_time_in_minutes])
        
        if len(new_current_active_lamps_list[current_time_in_minutes]) == 0:
            for lamp in prev_current_active_lamps_list[current_time_in_minutes]:
                self.publish_lamp_event(self.get_time(),lamp,LampAction.OFF)
            
        if prev_current_active_lamps_list[current_time_in_minutes] != new_current_active_lamps_list[current_time_in_minutes]:
            lamps_to_update = list(set(prev_current_active_lamps_list[current_time_in_minutes]).symmetric_difference(set(new_current_active_lamps_list[current_time_in_minutes])))
            for lamp in lamps_to_update:
                if lamp in prev_current_active_lamps_list[current_time_in_minutes]:
                    self.publish_lamp_event(self.get_time(),lamp,LampAction.OFF)
                else:
                    self.publish_lamp_event(self.get_time(),lamp,LampAction.ON)
        self.current_active_lamps_list = new_current_active_lamps_list

                    
    def read_data(self, path:str):
        with open(path, mode='r') as f:
            json_data = json.load(f)

            events : List[LampEvent]= []
            json_events = json_data['lamp_usage']
            for e in json_events:
                event = LampEvent.from_json(e)
                events.append(event)
        return events
