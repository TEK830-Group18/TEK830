
import tkinter as tk

from model.observable import Observable
from model.observer import Observer

class ClockHandler(tk.Tk, Observable):
    
    def __init__(self) -> None:
        self._timer_on = False
        
        self._obeservers = []
        
        self._hours = 0
        self._minutes = 0
        self._seconds = 0
        self.formatted_time = self.format_time(self._hour, self._minute, self._second)
    
    def format_time(self, hour, minute, second) -> str:
        return str(hour).zfill(2) + ":" + str(minute).zfill(2) + ":" + str(second).zfill(2)
    
    def get_formatted_time(self) -> str:
        return self.formatted_time
    
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
            self.notify_observers()
            tk.after_id = self.after(1000,self.update_time)
            
    def start_timer(self, hours, minutes, seconds):
        self._hours = hours
        self._minutes = seconds
        self._seconds = 0
        self._timer_on = True
        self.update_time()
        
    def stop_timer(self):
        self._timer_on = False
        self.after_cancel(tk.after_id)
        
    def add_observer(self, observer: Observer):
        self._obeservers.append(observer)
        
    def remove_observer(self, observer: Observer) -> None:
        self._obeservers.remove(observer)
    
    def notify_observers(self) -> None:
        for ob in self._obeservers:
            ob.notified_update()