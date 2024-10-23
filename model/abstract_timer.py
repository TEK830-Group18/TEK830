from abc import ABC, abstractmethod
from datetime import datetime

class ATimer(ABC):
    """
    An abstract base class representing a timer.
    This class provides the basic interface for a timer, including methods to start, stop, reset, 
    get the current time, and set a new time. Subclasses must implement these methods.
    
    Methods:
        start() -> None:
        stop() -> None:
        reset() -> None:
            Resets the time to use the default time. This method is intended to reset any internal 
            timers or counters to their default state.
        get_time() -> datetime:
            Returns the current time as a datetime object.
        set_time(new_time: datetime) -> None:
    """

    def __init__(self) -> None:
        pass

    @abstractmethod
    def start(self) -> None:
        """
        Starts the timer with the default time if it is the first start or has been reset.
        Otherwise, resumes the stopped timer.
        """
        pass

    @abstractmethod
    def stop(self) -> None:
        """
        Stops the timer and keeps its current state and time.
        """
        pass

    @abstractmethod
    def reset(self) -> None:
        """
        Resets the time to use the default time.
        
        This method is intended to reset any internal timers or counters
        to their default state.
        """
        pass

    @abstractmethod
    def get_time(self) -> datetime:
        """
        Returns current time as a datetime object.

        Returns:
            datetime: The current time.
        """
        pass

    @abstractmethod
    def set_time(self, new_time: datetime) -> None:
        """
        Sets a new current time.
        Args:
            new_time (datetime): The new time to be set.
        """
        
        pass