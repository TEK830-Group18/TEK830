from model.abstract_timer import ATimer
from datetime import datetime, timedelta
import time

class Timer(ATimer):
    """
    An implementation of a Timer class that uses the system time to keep track of time.
    """
    reset_timer: bool = True
    stopped: bool = False
    start_time: datetime
    elapsed_time: timedelta
    current_seconds: int = 0
    previous_seconds: int = 0

    def __init__(self) -> None:
        pass

    def start(self) -> None:
        """
        Starts the timer with the current system time, or resumes the running timer. If the timer is set to be reset, it initializes the start time to the current time.
        """
        if not self.reset_timer and not self.stopped:
            return

        if self.reset_timer:
            self.start_time = datetime.now()
            self.elapsed_time = timedelta(0)
            self.reset_timer = False
        
        curr_time = int(time.time())
        self.current_seconds = curr_time
        self.previous_seconds = curr_time
        self.stopped = False

    def stop(self) -> None:
        """
        Stops the timer if it is currently running and saves the current state.
        """
        if self.stopped:
            return
        
        self.__update_time()
        self.stopped = True

    def reset(self) -> None:
        """
        Resets the timer by setting the reset flag to True and restarting the timer.
        """
        self.reset_timer = True
        self.start()

    def get_time(self) -> datetime:
        """
        Get the current time.
        Returns:
            datetime: The current time. If the timer is stopped, it returns the start time plus the elapsed time.
                      If the timer is running, it updates the elapsed time and returns the start time plus the elapsed time.
        """
        if self.stopped:
            return self.start_time + self.elapsed_time
        
        self.__update_time()
        return self.start_time + self.elapsed_time

    def set_time(self, new_time: datetime) -> None:
        """
        Sets the start time of the timer to the specified new_time and resets the elapsed time.

        Args:
            new_time (datetime): The new start time for the timer.
        """
        self.start_time = new_time
        self.elapsed_time = timedelta(0)
        curr_time = int(time.time())
        self.current_seconds = curr_time
        self.previous_seconds = curr_time

    def __update_time(self):
        self.previous_seconds = self.current_seconds
        self.current_seconds = int(time.time())
        self.elapsed_time += timedelta(seconds= self.current_seconds - self.previous_seconds)
