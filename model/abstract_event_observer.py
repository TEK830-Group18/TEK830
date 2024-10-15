from model.observer import Observer
from abstract_event import Event

class EventObserver(Observer):
    """
    Abstract class for observing events.
    """
    def __init__(self) -> None:
        pass

    def notify(self, event: Event) -> None:
        pass