import json
from typing import List
from model.events.lamp_event import LampEvent

class Model():
    def __init__(self, data) -> None:
        self.user_data = self.read_data(data)
        self.schedule = self.update_schedule(self.user_data)

    def mainloop(self):
        #self.user_data = self.update_data()
        self.schedule = self.update_schedule(self.user_data)

    def read_data(self, path:str):
        with open(path, mode='r') as f:
            json_data = json.load(f)

            events : List[LampEvent]= []
            for e in json_data:
                event = LampEvent.from_json(e)
                events.append(event)
        return events

    def update_schedule(self, data):
        pass