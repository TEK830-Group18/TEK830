import tkinter as tk

class Slider(tk.Frame):
    def __init__(self, parent):
        super().__init__(master=parent)
        self._seconds:int = 0
        self._minute:int = 0
        self._hour:int = 0
        self.formatted_time = self.format_time(self._hour, self._minute, self._seconds)
        # self.formatted_time = str(self._hour).zfill(2) + ":" + str(self._minute).zfill(2) + ":" + str(self._seconds).zfill(2)
        
        # init slider
        self._slider = tk.Scale(parent, from_=0, to=1440, orient='horizontal', length=200)
        self._slider.config(command=self.update_slider)
        self._slider.pack()
        
        self._time_label = tk.Label(text=self.formatted_time)
        self._time_label.pack()
        
    def update_slider(self, a):
        slider_val = self._slider.get()
        self._hour = (slider_val // 60) % 24
        self._minute = slider_val % 60
        self.formatted_time = self.format_time(self._hour, self._minute, 0)
        self._time_label.config(text=self.formatted_time)
        
    def format_time(self, hour, minute, second) -> str:
        return str(hour).zfill(2) + ":" + str(minute).zfill(2) + ":" + str(second).zfill(2)