from abc import ABC, abstractmethod

class Observer(ABC):
    @abstractmethod
    def notified_update(self):
        pass