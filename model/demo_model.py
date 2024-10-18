
from datetime import datetime
import json
from typing import List
from model.abstract_model import Model
from model.events.lamp_event import LampEvent
from model.schedule import Schedule


class DemoModel(Model):
    def __init__(self):
        super().__init__()
        self._observers = []
        self._user_data_path = "tools/mock_user_data.json"
        self._user_schedule = self.get_user_schedule()
    
    def mainloop(self) -> None:
        pass

    def get_schedule(self) -> Schedule:
        pass
    
    def get_user_schedule(self) -> Schedule:
        user_data_lst = self._read_data(self.user_data_path)
        user_schedule = Schedule().createSchedule(user_data_lst)
        return user_schedule

    def get_time(self) -> datetime:
        pass

    def set_time(self, time: datetime) -> None:
        pass

    def start(self) -> None:
        pass

    def stop(self) -> None:
        pass

    def add_observer(self, observer) -> None:
        pass

    def remove_observer(self, observer) -> None:
        pass

    def notify_observers(self) -> None:
        pass
    
    def _read_data(self, path:str):
        with open(path, mode='r') as f:
            json_data = json.load(f)

            events : List[LampEvent]= []
            json_events = json_data['lamp_usage']
            for e in json_events:
                event = LampEvent.from_json(e)
                events.append(event)
        return events