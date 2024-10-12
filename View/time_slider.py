import customtkinter as ctk

from View.observable import Observable
from View.observer import Observer

class TimeSlider(ctk.CTkFrame, Observable):
    def __init__(self, parent):
        super().__init__(master=parent)
        
        self._obeservers: list = []
        
        self.updating: bool = False
        
        self._seconds:int = 0
        self._minute:int = 0
        self._hour:int = 0
        self.formatted_time = self.format_time(self._hour, self._minute, self._seconds)
        self.configure(fg_color="#0057AD")
        
        # init slider
        self._slider = ctk.CTkSlider(parent,
                                     from_=0,
                                     to=1440,
                                     orientation='horizontal',
                                     width=600,
                                     number_of_steps=1440,
                                     height=25,
                                     button_color="gray",
                                     button_hover_color="dark gray",
                                     progress_color="light gray"
                                     )
        self._slider.configure(command=self._update_values)
        self._slider.set(0)
        self._slider.grid(row=4, column=1, columnspan=2)        
    
    def _update_values(self, a):
        """_summary_
        Updates hours and minutes based on slider value, as well as notifying observers
        """
        self.updating = True
        self._hour = self.get_hours()
        self._minute = self.get_minutes()
        self.formatted_time = self.format_time(self._hour, self._minute, 0)
        self.notify_observers()
        self.updating = False
        
    def format_time(self, hour, minute, second) -> str:
        """Formats hours, minutes and seconds as HH:MM:SS.

        Args:
            hour (int): 
            minute (int): 
            second (int): 

        Returns:
            str: time formatted as "HH:MM:SS"
        """
        return str(hour).zfill(2) + ":" + str(minute).zfill(2) + ":" + str(second).zfill(2)
    
    def get_slider_value(self) -> int:
        return self._slider.get().as_integer_ratio()[0]
    
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