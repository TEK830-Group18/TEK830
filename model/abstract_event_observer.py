from model.observer import Observer
from model.events.abstract_event import Event
from model.events.lamp_event import LampEvent
from abc import ABC, abstractmethod

class EventObserver(ABC):
    """
    Abstract class for observing events.
    """
    def __init__(self) -> None:
        pass

    @abstractmethod
    def notify(self, event: LampEvent) -> None:
        pass