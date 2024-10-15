from abc import ABC, abstractmethod
from abstract_event import Event
from model.observable import Observable
from abstract_timer import Timer
from abstract_event_observer import EventObserver
from datetime import datetime

class EventPublisher(Observable, Timer, ABC):
    """
    Abstract class for publishing events.
    """
    def __init__(self) -> None:
        pass

    @abstractmethod
    def publish(self, event: Event) -> None:
        pass

    @abstractmethod
    def add_observer(self, observer: EventObserver) -> None:
        pass

    @abstractmethod
    def remove_observer(self, observer: EventObserver) -> None:
        pass
    
    @abstractmethod
    def notify_observers(self) -> None:
        pass

    @abstractmethod
    def start(self) -> None:
        pass

    @abstractmethod
    def stop(self) -> None:
        pass

    @abstractmethod
    def get_time(self) -> datetime:
        pass

    @abstractmethod
    def set_time(self, time: datetime) -> None:
        pass