import tkinter as tk
import time

class TimeWidget(tk.Frame):
    def __init__(self, parent, current_time):
        super().__init__(master=parent)
        self._current_time = current_time

        # Configure row and column
        self.rowconfigure(0, weight=1)
        self.columnconfigure(0, weight=1)

        # Create and pack the label
        self._time_label = tk.Label(self, text=f"{self._current_time}", font=("Helvetica", 18))
        self._time_label.grid(row=0, column=0, padx=10, pady=20)  # Using grid to place the label

        self.pack(pady=20)

    def set_time(self, new_time : time):
        self._current_time = new_time


    
    def update_time(self):
        """ 
            Updates time after one second based on actual real time, should be changed to update time based on slider in the future.
        """
        # TODO maybe make set current time in some other way in the future
        self._current_time = time.strftime('%H:%M:%S')
        self._time_label.config(text=self._current_time)
        self.after(1000,self.update_time)


