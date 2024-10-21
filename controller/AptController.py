import model.AptModel as AptModel
import View.time_slider as TimeSlider
import View.time_slider as TimeSlider
from datetime import time

class AptController:
    def __init__(self, model : AptModel, timeSlider : TimeSlider):
        self.model = model
        self.timeSlider = timeSlider
        self.last_checked_minutes = None
    
    def notify(self):
        self.current_hours = int(self.timeSlider.get_hours())
        self.current_minutes = int(self.timeSlider.get_minutes())
        self.current_time = time(self.current_hours, self.current_minutes)

        if self.last_checked_minutes != self.current_minutes:
            self.model.current_hours = self.current_hours
            self.model.current_minutes = self.current_minutes
            self.model.check_events()
            self.last_checked_minutes = self.current_minutes
            self.timeSlider.notify_observers()