from typing import List
from dataclasses import dataclass
from model.events.lamp_event import LampEvent

@dataclass
class Schedule:
    events: List[LampEvent]

    @staticmethod
    def createSchedule(events: List[LampEvent]) -> 'Schedule':
        events.sort()
        return Schedule(events=events)


