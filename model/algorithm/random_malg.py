from model.algorithm.abstract_mimicking_algorithm import MimickingAlgorithm
from typing import List, Dict
from model.events.lamp_event import LampEvent
from model.schedule import Schedule
from datetime import datetime, time, timedelta
import random

class Scheduler(ABC):
    """
    Abstract base class for creating schedules.
    Methods:
        createSchedule(user_actions: List[LampEvent]) -> Schedule:
            Abstract method for creating a schedule based on user actions.
    """
    def __init__(self) -> None:
        pass

    @abstractmethod
    def createSchedule(self, user_actions: List[LampEvent]) -> Schedule:
        pass


class RandomScheduler(Scheduler):
    # TODO: Write a better version of this. Much is based on Github Copilot.
    periods_in_day: int

    def __init__(self) -> None:
        super().__init__()

    def createSchedule(self, user_actions: List[LampEvent]) -> Schedule:
        grouped_events = self.group_events_by_period(user_actions)
        average_times = self.calculate_average_times(grouped_events)
        random_schedule = self.create_random_schedule(grouped_events, average_times)
        return random_schedule

    @staticmethod
    def group_events_by_period(events: List[LampEvent]) -> Dict[str, List[LampEvent]]:
        periods = {
            "morning": (time(6, 0), time(12, 0)),
            "afternoon": (time(12, 0), time(18, 0)),
            "evening": (time(18, 0), time(23, 59, 59)),
            "night": (time(0, 0), time(6, 0))
        }

        grouped_events = {period: [] for period in periods}

        for event in events:
            event_time = event.timestamp.time()
            for period, (start, end) in periods.items():
                if start <= event_time < end:
                    grouped_events[period].append(event)
                    break

        return grouped_events

    @staticmethod
    def calculate_average_times(grouped_events: Dict[str, List[LampEvent]]) -> Dict[str, time]:
        average_times = {}

        for period, events in grouped_events.items():
            if events:
                total_seconds = sum(event.timestamp.hour * 3600 + event.timestamp.minute * 60 + event.timestamp.second for event in events)
                average_seconds = total_seconds // len(events)
                average_time = (datetime.min + timedelta(seconds=average_seconds)).time()
                average_times[period] = average_time

        return average_times

    @staticmethod
    def create_random_schedule(grouped_events: Dict[str, List[LampEvent]], average_times: Dict[str, time]) -> Schedule:
        random_events = []
        lamp_states = {}

        for period, events in grouped_events.items():
            if events:
                for event in events:
                    lamp = event.lamp
                    if lamp not in lamp_states:
                        lamp_states[lamp] = None

                    if lamp_states[lamp] is None or lamp_states[lamp] != event.action:
                        random_time = RandomMAlg.random_time_near_average(average_times[period])
                        random_event = LampEvent(
                            timestamp=datetime.combine(datetime.today(), random_time),
                            lamp=lamp,
                            action=event.action
                        )
                        random_events.append(random_event)
                        lamp_states[lamp] = event.action

        random_events.sort(key=lambda event: event.timestamp)
        return Schedule(events=random_events)

    @staticmethod
    def random_time_near_average(average_time: time, offset_minutes: int = 30) -> time:
        average_seconds = average_time.hour * 3600 + average_time.minute * 60 + average_time.second
        offset_seconds = offset_minutes * 60
        random_seconds = random.randint(average_seconds - offset_seconds, average_seconds + offset_seconds)
        random_time = (datetime.min + timedelta(seconds=random_seconds)).time()
        return random_time
    