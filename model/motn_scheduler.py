from model.scheduler import Scheduler
from model.schedule import Schedule
from model.events.lamp_event import LampEvent
from model.events.lamp_action import LampAction
from typing import List, Dict
from matplotlib import pyplot as plt
from datetime import datetime, time

# This scheduler determines the state of a lamp at each minute by checking if, in the collected data, the lamp was on more often than off at this time of day.
class MoreThanNotScheduler(Scheduler):
    def __init__(self) -> None:
        pass

    def createSchedule(self, user_actions: List[LampEvent]) -> Schedule:
        minutes = self.create_state_list(user_actions)

        print(minutes)

        events = self.create_event_list(minutes)
        
        return Schedule(events)

    def create_state_list(self, user_actions):
        minutes: List[Dict[str, int]] = [{} for _ in range(1440)]
        active: List[str] = []
        for i, minute in enumerate(minutes):
            for action in user_actions:
                if action.timestamp.hour * 60 + action.timestamp.minute == i:
                    if action.action == LampAction.ON:
                        active.append(action.lamp)
                    else:
                        active.remove(action.lamp)
            for lamp in active:
                minute[lamp] = minute.get(lamp, 0) + 1
        return minutes

    def create_event_list(self, minutes):
        count_threshold = self.calculate_count_threshold(minutes)
        active = []
        events: List[LampEvent] = []
        for i, minute in enumerate(minutes):
            for lamp, count in minute.items():
                if count > count_threshold and lamp not in active:
                    event = self.create_lamp_event(i, lamp, LampAction.ON)
                    events.append(event)
                    active.append(lamp)

                elif (count <= count_threshold and lamp in active):
                    event = self.create_lamp_event(i, lamp, LampAction.OFF)
                    events.append(event)
                    active.remove(lamp)
            
            for lamp in active:
                if lamp not in minute.keys():
                    event = self.create_lamp_event(i, lamp, LampAction.OFF)
                    events.append(event)
                    active.remove(lamp)
        return events

    def calculate_count_threshold(self, minutes):
        counts = []
        for minute in minutes:
            for lamp, count in minute.items():
                counts.append(count)
        count_threshold = max(counts) // 2
        return count_threshold

    def create_lamp_event(self, i, lamp, state):
        return LampEvent(
                        timestamp=datetime.combine(datetime.today(), time(i // 60, i % 60)),
                        lamp=lamp,
                        action=state
                    )
                    