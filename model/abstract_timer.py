from abc import ABC, abstractmethod
from datetime import datetime

class Timer(ABC):

    def __init__(self) -> None:
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