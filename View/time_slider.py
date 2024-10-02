import tkinter as tk

from View.observable import Observable
from View.observer import Observer

class TimeSlider(tk.Frame, Observable):
    def __init__(self, parent):
        super().__init__(master=parent)
        
        self._obeservers: list = []
        
        self.updating: bool = False
        
        self._seconds:int = 0
        self._minute:int = 0
        self._hour:int = 0
        self.formatted_time = self._format_time(self._hour, self._minute, self._seconds)
        
        # init slider
        self._slider = tk.Scale(parent, from_=0, to=1440, orient='horizontal', length=500)
        self._slider.config(command=self._update_values)
        self._slider.pack()
        
        # Create and add label to show time
        self._time_label = tk.Label(text=self.formatted_time)
        self._time_label.pack()
    
    def _update_values(self, a):
        self.updating = True
        self._hour = self.get_hours()
        self._minute = self.get_minutes()
        self.formatted_time = self._format_time(self._hour, self._minute, 0)
        self._time_label.config(text=self.formatted_time)
        self.notify_observers()
        self.updating = False
        
    def _format_time(self, hour, minute, second) -> str:
        return str(hour).zfill(2) + ":" + str(minute).zfill(2) + ":" + str(second).zfill(2)
    
    def get_slider_value(self) -> int:
        return self._slider.get()
    
    def get_formatted_time(self) -> str:
        return self.formatted_time
    
    def is_updating(self) -> bool:
        return self.updating
    
    def get_hours(self):
        return (self._slider.get() // 60) % 24
    
    def get_minutes(self):
        return self._slider.get() % 60
    
    def add_observer(self, observer: Observer):
        self._obeservers.append(observer)
        
    
    def remove_observer(self, observer: Observer) -> None:
        self._obeservers.remove(observer)
    
    def notify_observers(self) -> None:
        for ob in self._obeservers:
            ob.notified_update()