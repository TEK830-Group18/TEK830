from abc import ABC, abstractmethod
from model.events.lamp_event import LampEvent
from abstract_light_service import AbstractLightService

class AbstractTimerService(ABC):
    def __init__(self) -> None:
        pass

    @abstractmethod
    def addLightService(self, lightService: AbstractLightService) -> None:
        pass

    @abstractmethod
    def publishEvent(self, event: LampEvent) -> None:
        pass
