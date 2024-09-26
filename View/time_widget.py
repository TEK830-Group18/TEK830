import tkinter as tk
import time

class TimeWidget(tk.Frame):
    _time_label: tk.Label
    def __init__(self, parent):
        super().__init__(master=parent)
        _current_time = time.strftime('%H:%M:%S')
        
        # Configure row and column
        self.rowconfigure(0, weight=1)
        self.columnconfigure(0, weight=1)
        
        # Create and pack the label
        self._time_label = tk.Label(self, text=f"{_current_time}", font=("Helvetica", 18))
        self._time_label.grid(row=0, column=0, padx=10, pady=20)  # Using grid to place the label
        
        self.pack(pady=20)

    def update_time(self):
        current_time = time.strftime('%H:%M:%S')
        self._time_label.config(text=current_time)
        self.after(1000,self.update_time)
        
        
        