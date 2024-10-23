from datetime import datetime
import customtkinter as ctk
from View.colors import Colors
from model.abstract_model import Model

class TimeSlider(ctk.CTkFrame):
    def __init__(self, parent, model : Model):
        super().__init__(master=parent)
                
        self.model = model        
        
        self.updating: bool = False
        
        self._seconds:int = self.model.get_time().second
        self._minute:int = self.model.get_time().minute
        self._hour:int = self.model.get_time().hour
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
        self._start_value = self.model.get_time().hour*60 + self.model.get_time().minute
        self._slider.set(self._start_value)
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
        return (self.get_slider_value() // 60) % 24
    
    def get_minutes(self):
        return self.get_slider_value() % 60
            
    def set_time(self):
        time = datetime.now().replace(hour=self.get_hours(),minute=self.get_minutes(),second=0)
        self.model.set_time(time)
    
    def get_time(self) -> datetime:
        return self.model.get_time()
    
    def update_slider_value(self):
        time = self.get_time().hour * 60 + self.get_time().minute
        self._slider.set(time)