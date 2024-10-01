import tkinter as tk

class TimeSlider(tk.Frame):
    def __init__(self, parent):
        super().__init__(master=parent)
        
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
        slider_val = self._slider.get()
        self._hour = (slider_val // 60) % 24
        self._minute = slider_val % 60
        self.formatted_time = self.format_time(self._hour, self._minute, 0)
        self._time_label.config(text=self.formatted_time)
        # TODO UPDATE OBSERVERS
        #......................
        
    def _format_time(self, hour, minute, second) -> str:
        return str(hour).zfill(2) + ":" + str(minute).zfill(2) + ":" + str(second).zfill(2)
    
    def get_slider_value(self) -> int:
        return self._slider.get()