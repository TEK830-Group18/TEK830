from datetime import datetime
import customtkinter as ctk

from View.colors import Colors
from model.abstract_model import Model
from model.observable import Observable
from model.observer import Observer

class TimeSlider(ctk.CTkFrame):
    def __init__(self, parent, model : Model):
        super().__init__(master=parent)
                
        self.model = model        
        
        self.updating: bool = False
        
        self._seconds:int = 0
        self._minute:int = 0
        self._hour:int = 0
        self.formatted_time = self.format_time(self._hour, self._minute, self._seconds)
        self.configure(fg_color=Colors.IKEA_BLUE.value)
        
        # init slider
        self._slider = ctk.CTkSlider(parent,
                                     from_=0,
                                     to=1440,
                                     orientation='horizontal',
                                     width=600,
                                     number_of_steps=1440,
                                     height=20,
                                     button_color="gray",
                                     button_hover_color="dark gray",
                                     progress_color="light gray"
                                     )
        self._slider.configure(command=self._update_time_in_model)
        self._slider.set(0)
        self._slider.grid(row=4, column=1, columnspan=2)        
    
    def _update_time_in_model(self, a):
        self.set_time()
    
    
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
            
    def set_time(self):
        #TODO convert int to datetime
        time = datetime()
        self.model.set_time(time)
    
    def get_time(self) -> datetime:
        return self.model.get_time()
    
    def update_slider_value(self):
        time = self.get_time().hour * 60 + self.get_time().minute
        self._slider.set(time)