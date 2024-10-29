import json
from typing import List
from model.events.lamp_event import LampEvent
from model.algorithm.abstract_mimicking_algorithm import MimickingAlgorithm, Schedule

class Model():
    def __init__(self, data: str, scheduler: MimickingAlgorithm) -> None:
        self.user_data = self.read_data(data)
        self.schedule: Schedule = self.update_schedule(self.user_data, scheduler)

    def mainloop(self):
        pass
        #self.user_data = self.update_data()
        # self.schedule = self.update_schedule(self.user_data,)

    def read_data(self, path:str):
        with open(path, mode='r') as f:
            json_data = json.load(f)

            events : List[LampEvent]= []
            json_events = json_data['lamp_usage']
            for e in json_events:
                event = LampEvent.from_json(e)
                events.append(event)
        return events

    def update_schedule(self, user_data: List[LampEvent], scheduler: MimickingAlgorithm) -> Schedule:
        schedule = scheduler.createSchedule(user_data)
        return schedule