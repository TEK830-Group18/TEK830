from abc import ABC, abstractmethod

from model.observer import Observer

class Observable(ABC):
    @abstractmethod
    def add_observer(self, observer: Observer) -> None:
        pass
    
    @abstractmethod
    def remove_observer(self, observer: Observer) -> None:
        pass
    
    @abstractmethod
    def notify_observers(self) -> None:
        pass