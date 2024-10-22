import customtkinter as ctk

from View.colors import Colors
from model.abstract_model import Model
from model.observer import Observer
from View.time_slider import TimeSlider

class ClockWidget(ctk.CTkFrame):
    def __init__(self, parent, model: Model):
        super().__init__(master=parent)

        self.model = model
        
        self._timer_on: bool = False 
        
        self._time = 0 
        
        # Set current time as starting value on the controller, formatted 
        self._displayed_time = self._format_time(0,0,0)
        
        self._hours = 0
        self._minutes = 0
        self._seconds = 0

        # Configure row and column
        self.grid(row=2, column=1, columnspan=2)
        
        # Create and pack the label
        self._time_label = ctk.CTkLabel(self, text=f"{self._displayed_time}", font=("Helvetica", 30), text_color="white")
        self._time_label.grid(row=0, column=0, padx=10)
        self._time_label.configure(fg_color=Colors.IKEA_BLUE.value)
        
        self.configure(fg_color=Colors.IKEA_BLUE.value)
        self.start_timer_updates()
    
    def _get_hours_from_int(self, time:int):
        return (time // 60) % 24
    
    def _get_minutes_from_int(self, time:int):
        return (time % 60)
    
    def _get_seconds_from_value(self, time:int):
        seconds = time - int(time)
        return seconds
    
    # Get time
    def get_time_as_minutes(self):
        return self.model.get_time().hour * 60 + self.model.get_time().minute
    
    def _format_time(self, hour, minute, second) -> str:
        """Formats hours, minutes and seconds as HH:MM:SS.

        Args:
            hour (int): 
            minute (int): 
            second (int): 

        Returns:
            str: time formatted as "HH:MM:SS"
        """
        return str(hour).zfill(2) + ":" + str(minute).zfill(2) + ":" + str(second).zfill(2)
    
    def start_timer_updates(self):
        if not self._timer_on:
            self._timer_on = True
            self.update_time()
    
    def update_time(self):
        self._time = self.get_time_as_minutes()
        self._hours = self.model.get_time().hour
        self._minutes = self.model.get_time().minute
        self._seconds = self.model.get_time().second
        self._displayed_time = self._format_time(self._hours, self._minutes, self._seconds)
        self._time_label.configure(text = self._displayed_time)
        self.after(1000, self.update_time)
