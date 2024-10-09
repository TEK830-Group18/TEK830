import tkinter as tk

from View.observer import Observer
from View.time_slider import TimeSlider

class ClockWidget(tk.Frame, Observer):
    def __init__(self, parent, controller : TimeSlider):
        super().__init__(master=parent)
        
        self._controller = controller
        
        self._timer_on: bool = False  
        
        # Set current time as starting value on the controller, formatted 
        self._current_time = controller.get_formatted_time()
        
        self._hours = 0
        self._minutes = 0
        self._seconds = 0

        # Configure row and column
        self.rowconfigure(0, weight=1)
        self.columnconfigure(0, weight=1)

        # Create and pack the label
        self._time_label = tk.Label(self, text=f"{self._current_time}", font=("Helvetica", 40), fg="white")
        self._time_label.grid(row=0, column=0, padx=10, pady=20)  # Using grid to place the label
        self._time_label.configure(bg="#0057AD")
        
        self.configure(bg="#0057AD")

        self.pack(pady=20)
            
    def _update_time(self):
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
        
            self._current_time = self._controller.format_time(self._hours, self._minutes, self._seconds)
            self._time_label.config(text=self._current_time)
            self._seconds += 1
            tk.after_id = self.after(1000,self._update_time)
    
    def _get_hours_from_int(self, time:int):
        return (time // 60) % 24
    
    def _get_minutes_from_int(self, time:int):
        return (time % 60)
           
        
    def start_timer(self):
        slider_val = self._controller.get_slider_value()
        self._hours = self._get_hours_from_int(slider_val)
        self._minutes = self._get_minutes_from_int(slider_val)
        self._seconds = 0
        self._timer_on = True
        self._update_time()
        
    def stop_timer(self):
        self._current_time = self._controller.format_time(self._hours, self._minutes, self._seconds)
        self._timer_on = False
        self._time_label.config(text=self._current_time)
        
    def notified_update(self):
        self.after_cancel(tk.after_id)
        self._timer_on = False
        slider_val = self._controller.get_slider_value()
        
        self._hours = self._get_hours_from_int(slider_val)
        self._minutes = self._get_minutes_from_int(slider_val)
        self._seconds = 0
        
        self._current_time = self._controller.format_time(self._hours, self._minutes, self._seconds)
        self._time_label.config(text=self._current_time)
        self.start_timer()
