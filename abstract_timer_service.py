from abc import ABC, abstractmethod
from datetime import datetime
from model.events.lamp_event import LampEvent
from abstract_light_service import AbstractLightService

class AbstractTimerService(ABC):
    def __init__(self) -> None:
        pass

    @abstractmethod
    def set_time(self, time: datetime) -> None:
        pass

    @abstractmethod
    def add_light_service(self, lightService: AbstractLightService) -> None:
        pass

    @abstractmethod
    def publish_event(self, event: LampEvent) -> None:
        pass
