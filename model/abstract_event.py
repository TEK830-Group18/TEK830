from abc import ABC, abstractmethod

class Event(ABC):
    """
    Abstract class for events.
    Attributes:
        time: The time the event occurs.
    """
    def __init__(self, time: int, action: str, target: str) -> None:
        pass

    @abstractmethod
    def get_time(self) -> int:
        pass

    @abstractmethod
    def get_action(self) -> str:
        pass

    @abstractmethod
    def get_target(self) -> str:
        pass