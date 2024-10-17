from abc import ABC, abstractmethod
from typing import List
from model.events.lamp_event import LampEvent
from model.schedule import Schedule

class MimickingAlgorithm(ABC):
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
