from abc import ABC, abstractmethod
from model.abstract_timer import ATimer
from model.abstract_event_publisher import EventPublisher
from model.observable import Observable
from model.schedule import Schedule
from datetime import datetime

class Model(EventPublisher, ABC):
    """
    Abstract class for the model.
    """
    def __init__(self) -> None:
        pass

    @abstractmethod
    def mainloop(self) -> None:
        pass

    @abstractmethod
    def get_schedule(self) -> Schedule:
        pass
    
    @abstractmethod
    def get_user_schedule(self) -> Schedule:
        pass

    @abstractmethod
    def get_time(self) -> datetime:
        pass

    @abstractmethod
    def set_time(self, time: datetime) -> None:
        pass

    @abstractmethod
    def start(self) -> None:
        pass

    @abstractmethod
    def stop(self) -> None:
        pass

    @abstractmethod
    def add_observer(self, observer) -> None:
        pass

    @abstractmethod
    def remove_observer(self, observer) -> None:
        pass

    @abstractmethod
    def notify_observers(self) -> None:
        pass