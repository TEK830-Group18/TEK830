
import tkinter as tk

from View.observer import Observer


class ClockHandler(Observer):
    
    def __init__(self) -> None:
        self._timer_on = False
        
        self._hours = 0
        self._minutes = 0
        self._seconds = 0
    
    def format_time(self, hour, minute, second) -> str:
        return str(hour).zfill(2) + ":" + str(minute).zfill(2) + ":" + str(second).zfill(2)
    
    def get_hours(self):
        return self._hours
    
    def get_minutes(self):
        return self._minutes
    
    def get_seconds(self):
        return self._seconds
    
    def update_time(self):
        if self._timer_on == True:
            if(self._seconds >= 60):
                self._seconds = 0
                self._minutes += 1                
            if(self._minutes >= 60):
                self._seconds = 0
                self._minutes = 0
                self._hours += 1
            if(self._hours >= 24):
                self._seconds = 0
                self._minutes = 0
                self._hours = 0
            self._seconds += 1
            tk.after_id = self.after(1000,self.update_time)